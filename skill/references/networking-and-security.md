# Roblox Multiplayer Networking & Exploit Security

Dense reference for an expert AI coding assistant. Source: Roblox Creator Docs (`scripting/events`, `scripting/security`, `projects/client-server`, `physics/network-ownership`, engine YAML).

**Golden rule: NEVER trust the client. The server is the only authority.** Every value from a client may be fabricated, malicious, or malformed.

---

## 1. Client-Server Model & Replication

Roblox experiences are multiplayer by default and run a client-server model. The **server is the ultimate authority** for state; it keeps clients in sync via **replication** (data model, physics, chat).

The server's role: receive input → **validate** action is possible/permissible → execute & update authoritative state → replicate results to clients. The client's role: render the world and send input.

### Replication facts (verbatim principles)
- Instances are **server-authoritative**: to replicate to everyone, an instance must be **created on the server**.
- Properties are server-authoritative: most must be **changed on the server** to be visible to all clients.
- An instance generally either replicates to **all** clients or none (exception: streaming).
- If an instance is ever a descendant of a **replication container**, expect much of its state to replicate to all clients.

### DataModel split: where things live & replicate

| Container | Visible to | Replicates to clients? | Use for |
|---|---|---|---|
| `Workspace` | server + clients | ✓ | 3D world, parts |
| `ReplicatedStorage` | server + clients | ✓ | Remotes, shared (non-sensitive) modules/assets |
| `ReplicatedFirst` | server + clients | ✓ | Loading screens, early client scripts |
| `StarterPlayer` / `StarterPlayerScripts` | clients | ✓ (LocalScripts) | Client-only scripts |
| `StarterGui` | clients | ✓ | Player UI |
| `ServerScriptService` | **server only** | ✗ | Server game logic, secrets |
| `ServerStorage` | **server only** | ✗ | Server data, configs, item databases, admin tools |

✓ Put logic/data in `ServerScriptService`/`ServerStorage` **from day one**.
✗ Never place sensitive logic or data in `ReplicatedStorage`, `Workspace`, or any replicated container.

**Decompilation:** Any `LocalScript`, `Script` with `RunContext.Client`, or `ModuleScript` replicated to a client **can be decompiled** — even if disabled, never required, or never run. Server-only Scripts/ModuleScripts in `ServerStorage`/`ServerScriptService` **never replicate** and cannot be decompiled. ✗ Do not mix server-only + client code in one shared ModuleScript — server logic (passwords, business rules) gets exposed.

✗ Avoid descriptive/predictable names for sensitive remotes, scripts, models — predictable hierarchies ease exploit development.

---

## 2. RemoteEvent — one-way, no yield

Asynchronous, one-way communication across the boundary. Does **not** yield. Place where both sides see it (usually `ReplicatedStorage`).

| Direction | Sender | Receiver |
|---|---|---|
| Client → Server | `RemoteEvent:FireServer(args)` | `RemoteEvent.OnServerEvent:Connect(function(player, args) end)` |
| Server → Client | `RemoteEvent:FireClient(player, args)` | `RemoteEvent.OnClientEvent:Connect(function(args) end)` |
| Server → All Clients | `RemoteEvent:FireAllClients(args)` | `RemoteEvent.OnClientEvent:Connect(function(args) end)` |

- **`OnServerEvent`'s first parameter is ALWAYS the firing `Player`** (injected by the engine, NOT spoofable). Additional args follow.
- `FireClient`'s first arg is the target `Player`. `OnClientEvent` does NOT receive a player param (use `Players.LocalPlayer`).
- Clients cannot talk directly to other clients — relay via server (`FireServer` → server validates → `FireClient`/`FireAllClients`).
- **Throttling:** client→server `FireServer` is rate-limited to **~500 requests/sec per client, shared across all RemoteEvents+UnreliableRemoteEvents of the same type**. Limit recurring remotes.

---

## 3. RemoteFunction — two-way, yields

Synchronous, two-way. Sender **yields** until recipient returns. `OnServerInvoke`/`OnClientInvoke` are **callbacks** (assigned, not `:Connect`ed). Only the **last** assigned callback runs.

| Direction | Caller | Callback |
|---|---|---|
| Client → Server → Client | `local r = RemoteFunction:InvokeServer(args)` | `RemoteFunction.OnServerInvoke = function(player, args) ... return result end` |
| Server → Client → Server | `RemoteFunction:InvokeClient(player, args)` | `RemoteFunction.OnClientInvoke = function(args) ... end` |

`OnServerInvoke` first param is the firing `Player`.

### ✗ InvokeClient (Server → Client) is DANGEROUS — verbatim risks
- If the client **throws an error, the server throws too**.
- If the client **disconnects** mid-invocation, `InvokeClient` **throws an error**.
- If the client **doesn't return a value, the server yields forever** (a malicious client never returns → permanent hang).
- Never trust the returned value either — it is fully client-controlled.

✓ For server→client one-way needs (e.g. updating a GUI), use a **RemoteEvent** (`FireClient`), not `InvokeClient`.

---

## 4. UnreliableRemoteEvent — high-frequency, lossy

Variant of RemoteEvent: asynchronous, **unordered, unreliable**, one-way, no yield. Same method/event names (`FireServer`/`FireClient`/`FireAllClients`, `OnServerEvent`/`OnClientEvent`).

- **No delivery guarantee** — lost events are NOT resent (packet loss / engine perf).
- **No ordering guarantee** — receive order may not match fire order.
- **Payload limit: events > 1000 bytes are DROPPED** (Studio logs the overage). Buffers/some types are compressed, so verifying size pre-fire is hard.
- Same ~500 req/sec client throttle (shared pool with RemoteEvent).
- `Remote event invocation discarded` logs when no listener exists.

✓ Use for **ephemeral / continuously-changing** data: position/replication streams, transient VFX, non-critical telemetry. Trades reliability+ordering for **lower latency & network traffic**.
✗ Don't use when ordering/reliability matters (state changes, currency, purchases) — use RemoteEvent.

---

## 5. BindableEvent / BindableFunction — same-side ONLY

Bind behaviors between scripts **on the same side** of the boundary (server↔server or client↔client). **Cannot cross the network boundary** — for that, use Remotes.

| Object | API | Yields? |
|---|---|---|
| `BindableEvent` | `:Fire(args)` → `.Event:Connect(function(args) end)` | No |
| `BindableFunction` | `:Invoke(args)` → `.OnInvoke = function(args) ... return v end` | Yes (until callback found) |

- BindableEvent connections run as separate threads; one erroring doesn't stop others; multiple connections fire in **unpredictable order**.
- BindableFunction: only one `OnInvoke` (last assigned wins); no `return` → returns `nil`; if callback never set, invoker **never resumes**.
- ModuleScripts are often a better alternative for sharing data between scripts.

---

## 6. Remote argument limitations (apply to all remotes & bindables)

Can pass: Roblox types (`Enum`, `Instance`, `Vector3`, `CFrame`, `Color3`, …) + Luau primitives (number/string/boolean) + tables.

| Limitation | Behavior |
|---|---|
| **Functions** | NOT replicated → arrive as `nil`. |
| **Metatables** | Lost in transit (metatable data dropped; only raw fields remain). |
| **Non-string table indices** (Instance/userdata/function keys) | Auto-converted to strings. |
| **Mixed numeric+string keys** | Can drop elements; pass a pure array OR pure dictionary. |
| **`nil` values/indices in tables** | Avoid — unsupported. |
| **Table identity** | Tables are **copied** — received/returned tables are NOT `==` to the original. |
| **Non-replicated instances** | An instance only the sender can see (e.g. a `ServerStorage` descendant, or a client-made part the server doesn't know) arrives as `nil`. |

⚠ Implication: a client can send a **table that mimics an Instance** (with `ClassName`, `Name`, etc.) to spoof object args → always `typeof(x) == "Instance"` AND check location/class (§7).

---

## 7. THE SECURITY MODEL — Never trust the client

A determined exploiter has **complete control** over local state and network traffic. Assume every client-sent value is manipulated. Exploiters can:

- Decompile any replicated LocalScript/ModuleScript (even if never run).
- Take **network ownership** of their character and unanchored parts.
- Trigger client-initiated events (`Touched`, `ProximityPrompt`, `ClickDetector`) **at any range/frequency**.
- Modify their position, physics, world interactions.
- **Fire/invoke any Remote at any frequency with arbitrary args** (except the injected first `Player` arg).
- Change anything in their local DataModel **without firing expected events** (e.g. set `Humanoid.WalkSpeed` locally; server can't read it).
- Arbitrarily alter behavior of any locally-running code.

**Therefore: all critical logic must be validated server-side or run exclusively on the server.** Mental model: treat every `FireServer()` like an HTTP request from an anonymous stranger.

### Threat-model every feature
- If a client could send any value for any param, what's the worst outcome?
- What if used 1,000+ times/sec? Max acceptable rate?
- Could an exploiter use it to ruin another player's experience?
- Minimum state/info I must expose for this to work?

---

## 8. Input validation & sanitization (validate EVERY remote arg)

Apply layered checks server-side before using any client data:

1. **Type & structure** — `typeof(x)` exact match. For instances: `typeof(x) == "Instance"` **and** `x:IsDescendantOf(expectedFolder)` (and check `ClassName`/location). Reject tables masquerading as instances. Cap string length (expensive ops scale with length).
2. **Value/range** — within logical bounds (qty > 0, valid IDs, real items). Guard money/items/UGC.
3. **NaN / Inf** — both are valid `number`s but bypass comparisons. `local isNaN = n ~= n`; `local isInf = math.abs(n) == math.huge`. NaN passes type checks and fails ALL `<`/`>` checks silently → poisons trades/economy.
4. **Context/permission** — is the player allowed? Close enough to shop? Has the key? Character alive? Owns the item?
5. **Existence** — target/object exists before operating.
6. **Rate limit** (§10) — server-side cooldown/bucket per player per action.

✓ Server **calculates** all outcomes (damage, price, reward). ✗ Client never sends an amount/result to apply directly.

### ✗ The NaN trap (verbatim-style)
```lua
-- VULNERABLE: NaN bypasses every check
if typeof(offeredGold) ~= "number" then return end        -- typeof(NaN) == "number" ✗ passes
if offeredGold < 0 or offeredGold > 1e6 then return end    -- NaN<0 false, NaN>1e6 false ✗ passes
if offeredGold > player.Gold.Value then return end          -- NaN > x false ✗ passes
-- fraudulent NaN trade created, poisons every downstream system
```
✓ Add explicitly: `if offeredGold ~= offeredGold then return end` and a positivity check `if not (offeredGold > 0) then return end` (which rejects NaN, since `NaN > 0` is false).

---

## 9. Common exploit vectors & defenses

| Vector | What the exploiter does | Defense |
|---|---|---|
| **Remote spam** | Fire a remote 100s–1000s/sec → effects/server overload | Server-side rate limit (§10); silently drop excess |
| **Bad/malformed args** | `nil`, NaN, Inf, huge strings, spoofed-Instance tables, negative qty | Full validation (§8); reject silently |
| **Client-changed replicated values** | Modify local `WalkSpeed`/UI/cooldowns; server can't read local changes | Keep authoritative state server-side; never read gameplay-critical values off the client |
| **RemoteFunction InvokeClient hang** | Never return / disconnect mid-invoke → server yields forever / errors | Don't `InvokeClient`; use `FireClient` (RemoteEvent) |
| **Exposed logic/data** | Decompile replicated scripts; read `ReplicatedStorage`/`Workspace` content; data-mine unreleased assets | Server-only code in `ServerScriptService`/`ServerStorage`; ship confidential content only when ready |
| **Network ownership abuse** | Teleport/fly/speed/fling via owned-part physics; spoof `Touched` (§11) | Server-side movement validation; anchor or `SetNetworkOwner(nil)` for critical parts; validate `Touched` |
| **Untrusted `require`/asset loading** | Remote args specify a module/asset ID or instance path for server to load/`require`/delete | ✗ Never `require`/load/delete arbitrary client-specified paths/IDs; check type, class, AND location |
| **Client→client relay** (`FireAllClients`) | Spam, invalid data, unauthorized broadcasts that error/disrupt all clients | Server = **gatekeeper not relay**: validate + rate-limit + permission-check before broadcasting |
| **Trade/data-store dupes** | Race conditions, leave mid-trade, invalid data fails save | Validate before commit; transaction-like all-or-nothing; revert on failure |
| **Marketplace spoofing** | Fake `PromptProductPurchaseFinished` client signal | Grant ONLY in server `ProcessReceipt`; handle already-granted receipts |
| **ProximityPrompt / ClickDetector / DragDetector** | Fire events at any range, ignoring `Enabled`/`MaxActivationDistance`/`HoldDuration` | Re-check enabled state + player state + distance + rate limit server-side; anchor parts |
| **Subplace teleport** | Client-teleport into restricted/unreleased subplaces (kick happens AFTER replication) | "Secure within universe only" access control; keep dev/test in separate private universes |
| **Third-party backdoors** | Toolbox models with hidden malicious scripts → server access, data theft | Sandbox models (`Sandboxed=true`, minimal `Capabilities`); inspect/avoid obfuscated scripts; restrict Network/DataStore/AssetRequire/LoadString caps |

### Client-triggered instance gotchas (verbatim)
- **ProximityPrompt:** exploiter fires events even if server `Enabled=false`; only `Triggered` has a server distance check — `PromptButtonHoldBegan`/`TriggerEnded` have **none**; server accepts holds even if `HoldDuration` is faked to 0.
- **ClickDetector:** **no server checks at all**; any event at any distance, even disabled/unparented.
- **DragDetector:** drag events respect `Enabled`+`PermissionPolicy`; all other props unchecked.
- ⚠ If these sit under unanchored parts, an exploiter takes network ownership and **moves the part to their character to bypass distance checks** — anchor or use the ownership API for critical actions.

---

## 10. Rate limiting / server-side cooldowns

Any client-triggerable server logic can be spammed (remotes, `Touched`, prompts, ClickDetectors). **Never rely solely on a client-side limit** — it's cosmetic. Limit anything that: hits rate-limited APIs (`DataStoreService`, `BadgeService`), is computationally expensive (cloning big models), or is exploitable when rapid (currency/teleport/invuln).

**Token bucket** (recommended): each user has a bucket of `capacity` tokens, refilling at `capacity/windowSeconds`/sec; spend one per action; allows bursts but caps average rate.

```lua
-- ServerScriptService module
local chatLimiter = TokenBucket.new(5, 10) -- burst 5, refill 0.5 tok/sec

ChatRemote.OnServerEvent:Connect(function(player, message)
    if not chatLimiter:allow(player.UserId) then return end -- too fast: drop
    -- ...other validation, then process
end)
Players.PlayerRemoving:Connect(function(p) chatLimiter.buckets[p.UserId] = nil end) -- avoid leak
```
✓ Clear per-player state on `PlayerRemoving`. ✓ Simple debounce: store `lastUsed[player]`; reject if `tick() - lastUsed < COOLDOWN`.

---

## 11. Network ownership & physics (the trust hole)

Roblox distributes physics: it auto-assigns **network ownership** of unanchored parts/assemblies to the nearest client for responsiveness. The owning client's physics simulation is replicated to server + others.

- Server owns all parts by default; **always owns anchored parts** (cannot change).
- `BasePart:SetNetworkOwner(player)` — assign to a player. `SetNetworkOwner(nil)` — server owns. `SetNetworkOwnershipAuto()` — revert to engine. `GetNetworkOwner()` — query.

### ⚠ Security (verbatim): Roblox cannot verify physics for client-owned parts
A client owning a part can: **teleport it, push it through walls, make it fly, set velocity/CFrame to Inf/NaN to fling other players' parts** (even parts they don't own). They can also **spoof or suppress `Touched`** — e.g. make a sword "hit" a player across the map, or never register a hit. ✓ Validate `Touched` events fired by clients.

✓ For gameplay-critical unanchored parts, manually set ownership / disable auto ownership. ⚠ Use `SetNetworkOwner(nil)` **conservatively** — it can cause jittery physics for clients.

### Movement validation
Clients control character movement/physics → speed/fly/teleport hacks. No universal solution (varies by game; must account for ~100–300ms latency). Approaches: distance-over-time vs theoretical max speed (project onto XZ plane for ground movement), leaky-bucket accumulators for bursts, exempt legitimate teleport mechanics. The future-proof fix is **server authority** (beta) — moves physics+movement validation entirely server-side.

---

## 12. Anti-cheat realities

You can **detect** but cannot fully **prevent** client tampering — it's fundamental to client-server architecture, not a Roblox limitation. **Design so a cheating client only hurts itself.**

- **The server decides.** Never ban on client-side detection — trivially bypassed.
- **Prevent harm first / quiet mitigation.** Rubber-band a speed-hacker to last valid position rather than instant-kick; clamp values; drop requests. Punish only to protect others.
- **Be proportional & reversible.** Assume false positives; prefer temp suspensions over permanent bans.
- **Design > detection.** Validation + rate limiting are primary; heuristics supplement.

**Heuristics** = flag technically-possible-but-improbable behavior (compare to theoretical max/baseline): Fastest Completion Time, Rate of Gain (currency/sec), Action Cadence (robotic timing = bot). Each is a **signal, not proof** → accumulate a **suspicion score**; act only past a high threshold from multiple varied signals.

**Honeypots:** decoy remotes no legitimate client ever fires → any traffic = high-confidence exploiter → log + kick. Variant: track intended direction (server→client remotes fired FROM a client = caught).

**Consequence ladder:** silent logging → quiet mitigation → temporary restrictions → visible enforcement (kick/suspend/`Players:BanAsync()`). Delay visible consequences to avoid teaching exploiters detection triggers. Use the Ban API for persistent offenders (prevents rejoin, tracks across universe).

---

## 13. Bandwidth & performance of remotes

- ✗ Don't fire remotes per-frame / per-`Heartbeat`. ✓ **Batch** updates into one remote with a table payload; throttle to e.g. 10–20 Hz.
- ~500 req/sec/client cap is **shared** across all RemoteEvents+UnreliableRemoteEvents — minimize remote count (also shrinks attack surface).
- ✓ Use **UnreliableRemoteEvent** for high-frequency, non-critical, latest-state-only data (positions, transient VFX). Keep payloads < 1000 bytes (else dropped).
- ✓ Use **RemoteEvent** for state changes, currency, purchases (reliable + ordered).
- Most players see 100–300ms latency; design with tolerance and avoid chatty round-trips.

---

## 14. ✓ Correct validated remote handler skeleton

```lua
-- Script in ServerScriptService
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local ServerStorage = game:GetService("ServerStorage")

local BuyItem = ReplicatedStorage:WaitForChild("BuyItem") :: RemoteFunction
local ItemData = ReplicatedStorage:WaitForChild("ItemData") -- shared, NON-sensitive
local TokenBucket = require(ServerStorage.TokenBucket)
local limiter = TokenBucket.new(5, 10) -- burst 5, ~0.5/sec sustained

local SHOP_RANGE = 30

local function buyItem(player: Player, item: any): (boolean, string?)
    -- 1. RATE LIMIT
    if not limiter:allow(player.UserId) then return false, "Too fast" end

    -- 2. TYPE / STRUCTURE (reject spoofed-Instance tables)
    if typeof(item) ~= "Instance" or not item:IsDescendantOf(ItemData) then
        return false, "Invalid item"
    end

    -- 3. EXISTENCE / CONTEXT: character alive
    local char = player.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    local hum = char and char:FindFirstChildOfClass("Humanoid")
    if not (hrp and hum and hum.Health > 0) then return false, "Not alive" end

    -- 4. PERMISSION / DISTANCE (server reads server-side position, not client's)
    local shop = workspace:FindFirstChild("ShopCounter")
    if not shop or (hrp.Position - shop.Position).Magnitude > SHOP_RANGE then
        return false, "Too far"
    end

    -- 5. VALUE: server owns price + balance; NaN/Inf rejected via (> 0)
    local price = item:GetAttribute("Price")
    if typeof(price) ~= "number" or not (price > 0) then return false, "Bad price" end
    local gold = player:GetAttribute("Gold") or 0
    if gold < price then return false, "Not enough gold" end

    -- 6. APPLY: server calculates outcome, updates authoritative state
    player:SetAttribute("Gold", gold - price)
    grantItem(player, item) -- server-side grant
    return true, nil
end

BuyItem.OnServerInvoke = buyItem -- callback (only last assignment wins)
```

**Pattern: validate → then apply.** Type → structure → existence → permission/distance → value (incl. NaN/Inf) → rate limit → server-computed apply. Reject silently or with a generic message; log suspicious activity with the `Player`; never echo internal state.
