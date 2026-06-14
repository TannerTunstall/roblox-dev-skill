# Roblox Monetization, Marketplace & Publishing — Dense Reference

Expert reference for in-experience monetization (Luau), publishing/production, analytics, moderation/policy code requirements, and localization.

---

## 1. Robux Economy — Product Types (pick the right one)

| Product | Repeatable? | API to grant | Grant mechanism | Use for |
|---|---|---|---|---|
| **Developer Product** | ✓ buy many times | `PromptProductPurchase` → **`ProcessReceipt`** | consumable, server callback | currency, ammo, potions, refills, gacha pulls |
| **Game Pass** | ✗ one-time, permanent | `PromptGamePassPurchase` + `UserOwnsGamePassAsync` | ownership check on join | VIP area, permanent power-up, single avatar item |
| **Subscription** | recurring monthly | `PromptSubscriptionPurchase` + `GetUserSubscriptionStatusAsync` | status check (revocable) | recurring benefits, battle-pass-style |
| **Avatar asset** | ✗ (owned) | `PromptPurchase` + `PlayerOwnsAssetAsync` | ownership check | catalog/UGC items, bundles |
| **Premium** | membership | `PromptPremiumPurchase` + `Player.MembershipType` | engagement payouts | Premium-only perks |

- DevProducts are the **only** type granting through a server callback (`ProcessReceipt`); everything else is an ownership/status check on join. ✓
- Minimum price: DevProduct/Pass 1 Robux; Subscription 49 Robux. Payout hold ≈5 days (passes/products), 30 days (local-currency subs).
- ⚠ Cross-experience DevProduct **and** Game Pass sales disabled **2026-05-30** → migrate to Robux Transfers.

---

## 2. MarketplaceService — Core API

```lua
local MarketplaceService = game:GetService("MarketplaceService")
```

### Prompts (client or server; show purchase UI)
| Method | Signature |
|---|---|
| `PromptProductPurchase` | `(player, productId, equipIfPurchased?, currencyType?)` — DevProduct |
| `PromptGamePassPurchase` | `(player, gamePassId)` |
| `PromptPurchase` | `(player, assetId, equipIfPurchased?, currencyType?)` — avatar asset |
| `PromptSubscriptionPurchase` | `(player, subscriptionId)` — subId is string `"EXP-…"` |
| `PromptPremiumPurchase` | `(player)` |

### Finished events (UI closed — NOT proof of purchase)
| Event | Args |
|---|---|
| `PromptProductPurchaseFinished` | `(userId, productId, isPurchased)` — ⚠ **never** use to grant DevProducts; use `ProcessReceipt` |
| `PromptGamePassPurchaseFinished` | `(player, gamePassId, wasPurchased)` |
| `PromptPurchaseFinished` | `(player, assetId, isPurchased)` |
| `PromptSubscriptionPurchaseFinished` | `(player, subscriptionId, didTryPurchasing)` |

### Info / ownership (Async = yields, wrap in `pcall`)
- `GetProductInfo(id, infoType) → table` — fields: `Name`, `Description`, `PriceInRobux`, `IsForSale`, `Created`, `IsPublicDomain`, `Creator`, etc. `infoType` is `Enum.InfoType`: `Asset` | `Product` | `GamePass` | `Subscription` | `Bundle`.
- `GetDeveloperProductsAsync() → Pages` — all DevProducts for the game.
- `UserOwnsGamePassAsync(userId, gamePassId) → bool` — cached; refreshes on `PromptGamePassPurchaseFinished`.
- `PlayerOwnsAssetAsync(player, assetId) → bool` — avatar assets only, not DevProducts.
- Subscriptions (server-only checks): `GetUserSubscriptionStatusAsync(player, subId) → {IsSubscribed, …}`, `GetSubscriptionProductInfoAsync(subId)`, `GetUserSubscriptionPaymentHistoryAsync(player)`.
- Product intelligence: `RankProductsAsync(identifiers)` (strict rate limit — call once at join), `RecommendTopProductsAsync({Enum.InfoType…})` (≤50; empty if no sale in 28 days).

---

## 3. ProcessReceipt — THE Developer Product Grant Callback ★

`MarketplaceService.ProcessReceipt = function(receiptInfo) → Enum.ProductPurchaseDecision`

**Why it's special:** It's the *only* reliable signal a DevProduct was actually paid for. Roblox **re-invokes it across rejoins and server restarts** until you return `PurchaseGranted`. If you don't persist the grant, you will **double-grant** (return Granted twice on rejoin) or **lose the purchase** (crash before granting + return Granted = player paid, got nothing).

### Rules
- ✓ Assign the callback **once**, in a single server `Script` in `ServerScriptService`.
- ✓ Must be **idempotent**: record `PurchaseId` in a DataStore so repeat invocations are no-ops.
- ✓ **Grant THEN record** — but record durably in the same pass; only return `PurchaseGranted` after the DataStore write of the `PurchaseId` succeeds.
- ✓ Return `Enum.ProductPurchaseDecision.NotProcessedYet` on ANY failure (player gone, DataStore error, unknown product) → Roblox retries on next join.
- ✗ Never trust `PromptProductPurchaseFinished` to grant.

### `receiptInfo` fields
`PurchaseId` (string, unique per txn — the idempotency key) · `PlayerId` (number) · `ProductId` (number) · `CurrencySpent` (number, actual Robux paid, accurate even under price-optimization) · `CurrencyType` (`Enum.CurrencyType.Robux`) · `PlaceIdWherePurchased` · `ProductPurchaseChannel` (`InExperience`/`ExperienceDetailsPage`/…).

### `Enum.ProductPurchaseDecision`
`PurchaseGranted` (resolve receipt, stop retries) · `NotProcessedYet` (leave open, retry later).

### Correct idempotent skeleton
```lua
local MarketplaceService = game:GetService("MarketplaceService")
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local purchaseHistory = DataStoreService:GetDataStore("PurchaseHistory")

-- Map productId -> grant function. Return true on success, false/error on failure.
local productGrants = {
    [123123] = function(player) -- 100 gold
        local gold = player:FindFirstChild("leaderstats") and player.leaderstats:FindFirstChild("Gold")
        if not gold then return false end
        gold.Value += 100
        return true
    end,
}

local function processReceipt(receiptInfo)
    local key = string.format("%d_%s", receiptInfo.PlayerId, receiptInfo.PurchaseId)

    -- 1. Idempotency: was this exact PurchaseId already granted?
    local alreadyGranted
    local ok = pcall(function()
        alreadyGranted = purchaseHistory:GetAsync(key)
    end)
    if not ok then
        return Enum.ProductPurchaseDecision.NotProcessedYet -- DataStore down; retry later
    end
    if alreadyGranted then
        return Enum.ProductPurchaseDecision.PurchaseGranted   -- safe no-op on rejoin
    end

    -- 2. Player must be in-server to receive the grant
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then
        return Enum.ProductPurchaseDecision.NotProcessedYet   -- they left; retry on next join
    end

    -- 3. Grant
    local grant = productGrants[receiptInfo.ProductId]
    local granted = grant ~= nil and select(2, pcall(grant, player)) == true
    if not granted then
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    -- 4. Durably record BEFORE returning Granted (UpdateAsync = atomic, retry-safe)
    local recorded = pcall(function()
        purchaseHistory:UpdateAsync(key, function() return true end)
    end)
    if not recorded then
        -- Grant happened but record failed; do NOT confirm — Roblox retries,
        -- idempotency in your grant fn or this skeleton must tolerate the redo.
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    return Enum.ProductPurchaseDecision.PurchaseGranted
end

MarketplaceService.ProcessReceipt = processReceipt
```

> Note: Roblox does **not** store per-user DevProduct/Pass purchase history — persisting it is your responsibility (DataStore). External (off-game) DevProduct sales also resolve through `ProcessReceipt` when the buyer next joins.

---

## 4. Game Passes — grant pattern

Passes are permanent; **re-check ownership every join** and on purchase-finished.

```lua
local PASS_ID = 0000000
-- On join:
Players.PlayerAdded:Connect(function(player)
    local ok, owns = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, PASS_ID)
    end)
    if ok and owns then grantPerk(player) end
end)
-- On purchase (server):
MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, passId, bought)
    if bought and passId == PASS_ID then grantPerk(player) end
end)
```
Prompt only if not owned: check `UserOwnsGamePassAsync` client-side before `PromptGamePassPurchase`.

---

## 5. Subscriptions

- subId is a string like `"EXP-11111111"`. Status check **must run on server** (`GetUserSubscriptionStatusAsync(player, subId)` → `{IsSubscribed=bool, …}`).
- Subscriptions are **revocable** — if you persisted benefits to a DataStore, you must *revoke* when `IsSubscribed` becomes false.
- Listen `Players.UserSubscriptionStatusChanged:Connect(function(player, subId) … end)` to re-check on change (fires even if purchased from Store tab mid-session).
- Robux subs: 70%/mo, regional pricing forced on. Local-currency subs ($2.99–$14.99 tiers): 70% month 1, 100% after; require ID/phone-verified account; not in some regions/platforms — ⚠ only offer where supported or the buyer sees-but-can't-buy.
- Client prompts via `PromptSubscriptionPurchase`; expose status to client via a `RemoteFunction` whose `OnServerInvoke` calls `GetUserSubscriptionStatusAsync`.
- Real-time analytics via Cloud Webhooks: events `purchased`, `renewed`, `cancelled`, `refunded`.

---

## 6. Premium & Engagement Payouts

```lua
if player.MembershipType == Enum.MembershipType.Premium then … end
```
- `Enum.MembershipType`: `None` | `Premium`.
- `Players.PlayerMembershipChanged:Connect(function(player) … end)` — re-check after in-experience upgrade.
- `MarketplaceService:PromptPremiumPurchase(player)` — opens upgrade modal (instant Premium + stipend in-experience).
- Engagement-based payouts **deprecated 2025-07-24 → replaced by Creator Rewards** (earn Robux from share of Premium engagement). Don't paywall non-Premium; no gameplay advantage.

---

## 7. Mandatory Policy that Affects Code

### Text filtering — REQUIRED for ALL user-generated text shown to others
Failing to filter player text = policy violation / moderation. Applies to names, signs, custom messages, anything authored by a user and displayed to another.

- **Chat:** `TextChatService` filters automatically server-side before delivery; each recipient gets age/region-appropriate `TextChatMessage.Text`. Gate delivery with server-only `TextChannel.ShouldDeliverCallback(message, textSource) → truthy`.
- **Non-chat UGC text** (server-only, yields):
```lua
local TextService = game:GetService("TextService")
local ok, result = pcall(function()
    return TextService:FilterStringAsync(rawText, fromUserId) -- result: TextFilterResult
end)
if ok then
    local forBroadcast = result:GetNonChatStringForBroadcastAsync()      -- shown to everyone / persisted
    local forUser = result:GetNonChatStringForUserAsync(toUserId)         -- per-recipient
end
```
- `GetChatForUserAsync` is **deprecated** (returns empty) — use `TextChatService`.
- Filter on the **server**, never client. Re-filter when displaying (don't cache one filtered string for all recipients).

### PolicyService — compliance gating by region/age
```lua
local PolicyService = game:GetService("PolicyService")
local policy = PolicyService:GetPolicyInfoForPlayerAsync(player) -- yields, pcall it
```
Returned flags (act on these in code):
| Field | Meaning / required behavior |
|---|---|
| `ArePaidRandomItemsRestricted` (bool) | true → **must not** offer loot boxes/gacha to this player |
| `IsPaidItemTradingAllowed` (bool) | gate paid-item trading |
| `IsEligibleToPurchaseSubscription` | hide sub offers if false |
| `IsEligibleToPurchaseCommerceProduct` | gate USD commerce products |
| `IsContentSharingAllowed` | gate user upload/share of content |
| `AreAdsAllowed` | gate immersive/rewarded ads |
| `IsSubjectToChinaPolicies` | true → apply China compliance |
| `IsPaidItemTradingAllowed` / `AllowedExternalLinkReferences` (legacy, empty) | — |

⚠ **Studio cannot test real purchases** — Robux is charged for real even in test mode; test DevProduct external flow via Creator Hub *Test Mode* (low-cost items, visible only to you/group).

---

## 8. Publishing & Production

### Place vs Experience
- **Experience** = the game (one or more places). **Place** = a single scene/level (3D world + scripts). **Start place** = where players load in.
- File menu: **Publish to Roblox** (new experience) · **Publish to Roblox As…** (overwrite/add place to existing experience) · **Save to Roblox** (save current place version without changing live).
- An experience has **versions** (Version History per place: view/download/restore previous). Publishing overwrites the live start place.

### Experience Settings (File ▸ Experience Settings) — tabs
| Tab | Key code-relevant settings |
|---|---|
| **Permissions** | Playability: **Private** (default) / **Limited** (friends/testers) / **Public** |
| **Monetization** | Paid Access (Robux / local currency), Private Servers toggle |
| **Security** | **Allow HTTP Requests**, **Enable Studio Access to API Services** (DataStore in Studio), Third-Party Sales/Teleports, Mesh/Image APIs |
| **Localization** | Source language, Automatic Text Capture, Use Translated Content, Automatic Translation |
| **Places** | Per-place max players, Version History |
| **Basic Info** | Content maturity label, devices, icon |

### Maturity & Compliance (IXP questionnaire)
- Creator Dashboard ▸ Audience ▸ Maturity & Compliance. Produces a label: **Minimal / Mild / Moderate / Restricted (18+)**.
- Questionnaire covers Violence, Blood, Fear, Crude Humor, Gambling, Strong Language, Romantic Themes, Alcohol, Social Hangout, Free-form Creation, Sensitive Issues, **Paid Random Items**, **Paid Item Trading**, Media Sharing, AI Interaction.
- Two questionnaire answers map directly to runtime: **Paid Random Items** → must honor `ArePaidRandomItemsRestricted`; **Paid Item Trading** → must honor `IsPaidItemTradingAllowed`.
- Public/Limited requires a completed questionnaire + (for all-ages) ID/parent age verification + 2FA + fee.

### Access & Collaboration (roles)
- Permission levels: **Owner** (full) · **Edit** (edit + play) · **Play** (playtest only) · **No Access**.
- User-owned: Edit grantable only to Roblox **friends**; Play to anyone/group. Group-owned: configure via group **Roles** (all experiences) or per-experience override in *Manage Collaborators*. **Team Create** for simultaneous editing.

### Release strategy
- Iterate safely with **Experiments** (A/B tests for causal metric impact) + **Configs** (live-tune values without restarting servers). Cadence: small updates every 2–4 wks, big features every 2–3 mo.

---

## 9. AnalyticsService — Instrumentation

```lua
local AnalyticsService = game:GetService("AnalyticsService")
```
⚠ **Server-only, published experiences only** — events from client/Studio are dropped.

### Economy events
```lua
AnalyticsService:LogEconomyEvent(
    player,
    Enum.AnalyticsEconomyFlowType.Source,  -- or .Sink
    "Coins",                                -- currency name (≤5 currencies)
    amount,                                 -- always POSITIVE (sinks shown negative on dash)
    endingBalance,                          -- balance AFTER txn
    Enum.AnalyticsEconomyTransactionType.IAP.Name, -- .Name for string
    "ItemSKU"                               -- optional itemSKU
)
```
- `Enum.AnalyticsEconomyFlowType`: `Source` (earn) · `Sink` (spend).
- `Enum.AnalyticsEconomyTransactionType`: `IAP`, `TimedReward`, `Onboarding`, `Shop`, `Gameplay`, `ContextualPurchase` (or custom string). Unlocks Economy dashboard (sources/sinks, avg wallet).

### Funnel events
```lua
-- One-time (e.g. onboarding/FTUE) — no session id:
AnalyticsService:LogOnboardingFunnelStepEvent(player, stepNumber, stepName)
-- Recurring (e.g. shop) — needs funnelSessionId (GUID per session):
AnalyticsService:LogFunnelStepEvent(player, funnelName, funnelSessionId, stepNumber, stepName)
```
- Repeated steps counted once; skipped steps auto-complete earlier ones. Filters apply to **first step only**; cohorted by entry date. ≤10 funnels. **Validate step numbers server-side** to block exploiters.

### Custom events
```lua
AnalyticsService:LogCustomEvent(player, "MissionStarted")        -- counter (value=1)
AnalyticsService:LogCustomEvent(player, "MissionDuration", 120)  -- with value
```
- ≤100 custom events. Prefer **custom fields** over many event names (event-name cardinality is tight). Aggregations: count, unique users, sum/avg/min/max, avg per user.

### Key metrics (built-in dashboards) — why instrument
| Metric | Definition |
|---|---|
| **D1 / D7 / D30 retention** | % of a join-date cohort returning after 1/7/30 days. D1→core loop & FTUE; D7→progression; D30→endgame/social |
| **Avg session time** | total time ÷ sessions; tied to retention |
| **DAU / MAU**, stickiness | daily/monthly actives; DAU/MAU = stickiness |
| **Conversion rate (payer)** | % of DAU who purchased anything |
| **ARPPU** | avg revenue per *paying* user |
| **ARPDAU** | avg revenue per DAU (= conversion × ARPPU) |
- Cohort down-funnel: 7D playtime/user, 7D payer-conversion, 7D & 30D revenue/user. Instrument funnels at onboarding (biggest drop-off) and shop (improves conversion & ARPPU).

---

## 10. Localization

```lua
local LocalizationService = game:GetService("LocalizationService")
```
- `GetTranslatorForPlayerAsync(player) → Translator` (yields) · `GetTranslatorForLocaleAsync(localeId) → Translator` (e.g. `"es"`, `"pt"`).
- `Translator:Translate(object, sourceString) → string` · `Translator:FormatByKey(key, args) → string`.
- `player.LocaleId` / `Translator.LocaleId` — listen `GetPropertyChangedSignal("LocaleId")` for live language switches.
- **LocalizationTable** columns: `Context`, `Key`, `Source`, then per-locale codes. Supports image/sound asset-id localization.
- **AutoLocalize** (GuiObject property, default true): engine auto-translates static UI text from the localization table — no scripting needed. Disable per-object for dynamic/server-set text.
- **Automatic Text Capture (ATC)** (Experience Settings ▸ Localization): captures live UI strings (only `AutoLocalize=true` GuiObjects; excludes Roblox chat/leaderboards, platform Badge/Pass names, embedded-image text).
- **Automatic Translation** ("Use Translated Content"): machine-translates Name/Description + captured strings; never overrides manual entries.

---

## 11. Marketplace (Avatar Items) & Creator Programs — payout-relevant

- Upload fees: **2D** (t-shirt/shirt/pants) 10 Robux · **3D** (accessory/body/animation) 300 Robux. Non-refundable on rejection.
- Publishing advance (refundable from sales): 2D items ~10 Robux; 3D e.g. Hat 1500 (non-limited) / 13000 (paid limited).
- Revenue split: Roblox commission ~30%; in-experience purchases also pay the **experience owner** a commission (3D ~40%, classic 2D ~10%). 30-day escrow hold on commissions. Progressive revenue share (Marketplace 3D) scales 30%→up to 70%.
- **DevEx (Developer Exchange):** convert **Earned Robux** → USD. Min **30,000** Robux; standard rate ~$0.0035/Robux (18+ boosted rate for qualifying age-verified US sales). Requires 13+, verified email, tax form. Cash Out via Creator Hub ▸ Finances.
- **Creator Rewards** (replaces engagement payouts): Robux for Premium engagement share.

---

## 12. Quirks / Gotchas Checklist

- ✗ Granting DevProducts via `PromptProductPurchaseFinished` → double-grant or lost purchase. ✓ Only `ProcessReceipt`.
- ✗ `ProcessReceipt` without DataStore idempotency → re-grant on every rejoin/restart. ✓ Key on `PurchaseId`.
- ✗ Returning `PurchaseGranted` before durably recording → if you crash next time it re-grants. ✓ Record then confirm.
- ✗ Assigning `ProcessReceipt` in multiple scripts → only the last wins. ✓ Exactly one server script.
- ✗ Showing unfiltered user text → policy violation. ✓ `TextChatService` / `FilterStringAsync` server-side, per-recipient.
- ✗ Offering gacha without checking `ArePaidRandomItemsRestricted`. ✓ Gate via `PolicyService`.
- ✗ Subscription/ownership checks on client. ✓ Server-only.
- ✗ Expecting real purchases to work in Studio. ✓ Use Creator Hub Test Mode (real Robux still charged).
- ✗ Analytics from client/Studio silently dropped. ✓ Server + published only.
- ✗ Enabling DataStores forgotten → "Studio Access to API Services" off. ✓ Toggle in Security settings.
- ⚠ Cross-experience Pass/DevProduct sales end 2026-05-30 → Robux Transfers.
