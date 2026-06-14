# Data & Cloud Services (in-experience Luau)

Persistent + cross-server data on Roblox. All cloud services are **server-only** (`Script`, never `LocalScript`). Every call is a network call that can fail → **always `pcall`**. This file covers the engine Luau APIs, not external Open Cloud REST (separate).

| Service | Persistence | Scope | Access | Analog |
|---|---|---|---|---|
| **DataStoreService** | Permanent | Cross-server | R/W | NoSQL DB |
| **MemoryStoreService** | ≤45 days (TTL) | Cross-server | R/W | In-memory cache |
| **MessagingService** | Ephemeral (pub/sub) | Cross-server | send/recv | Message bus |
| Luau in-memory | Session | Single server | R/W | Server RAM |

Decision: persists across sessions → DataStore. Frequent/temporary cross-server → MemoryStore. Notify other servers → MessagingService. Single-server only → plain Luau tables.

---

## DataStoreService

```lua
local DataStoreService = game:GetService("DataStoreService")
local store = DataStoreService:GetDataStore("PlayerData")        -- standard
local ordered = DataStoreService:GetOrderedDataStore("Leaders")  -- ordered (numbers only)
-- optional scope: GetDataStore(name, scope) — prepended to all keys; default "global"
```

A DataStore is a dictionary: unique string **key** → value. Keys consistent across all servers/places in the experience.

### Core methods (all yield, all wrap in pcall)

| Method | Purpose | Budget cost |
|---|---|---|
| `:GetAsync(key[, getOptions])` | Read; returns `value, keyInfo` | Read |
| `:SetAsync(key, val[, userIds, setOptions])` | Overwrite; returns version string | Write |
| `:UpdateAsync(key, transformFn)` | Atomic read-modify-write | **Read + Write** |
| `:IncrementAsync(key, delta)` | Atomic int increment | Write (read+write internally) |
| `:RemoveAsync(key)` | Delete; returns removed value | Remove |

```lua
local ok, err = pcall(function() store:SetAsync("User_1234", 50) end)
if not ok then warn(err) end

local ok, value = pcall(function() return store:GetAsync("User_1234") end)
```

### ✓ Prefer UpdateAsync over SetAsync (atomicity)

`SetAsync` blindly overwrites → if two servers set the same key, last write wins and **data is lost** (race/overwrite). `UpdateAsync` reads the latest value from the last writer, runs your transform, then writes — atomic. Use it for any key multiple servers may touch (player currency, shared counters).

```lua
local ok, newVal = pcall(function()
    return store:UpdateAsync("User_1234", function(old, keyInfo)
        old = old or { coins = 0 }
        old.coins += 10
        return old        -- return nil to ABORT the write (no change)
    end)
end)
```

- ✗ Transform callback **cannot yield** — no `task.wait`, no nested async calls inside it.
- `nil` return cancels the write.
- `IncrementAsync` is sugar over `UpdateAsync` for a single integer.
- `SetAsync` counts only Write; `UpdateAsync` counts **both Read and Write** budgets.

### OrderedDataStore (leaderboards)

Only stores **integers**. Supports `:GetSortedAsync(ascending, pageSize[, minValue, maxValue])` → `Pages`. No versioning/metadata (`keyInfo` always nil). PageSize 1–100.

```lua
local ok, pages = pcall(function() return ordered:GetSortedAsync(false, 100) end) -- descending top 100
if ok then
    for _, entry in pages:GetCurrentPage() do
        print(entry.key, entry.value)
    end
    -- pages.IsFinished ; pages:AdvanceToNextPageAsync()
end
```
Use ordered DS for **all-time persistent** rankings; use MemoryStore sorted maps for daily/ephemeral leaderboards.

### Metadata & UserIds (standard DS only)
- `SetAsync(key, val, {userId1,...}, setOptions)` — userIds tag for IP/copyright tracking; `DataStoreSetOptions:SetMetadata({...})` for custom tags.
- `Get/Increment/RemoveAsync` return `keyInfo` (2nd value): `.Version`, `.CreatedTime`, `.UpdatedTime` (ms since epoch), `:GetUserIds()`, `:GetMetadata()`.
- ✗ When using metadata, you must re-supply it on every write or you lose it.
- Metadata limits: key ≤50 chars, value ≤250 chars, total ≤300 chars across all pairs.

---

## Serialization (what you can store)

Stored as **JSON** internally. Supported Luau types: nil, boolean, number, string, table (containing only supported types), buffer.

- ✗ **No Instances**, no functions, no `Vector3`/`CFrame`/`Color3`/`Enum` directly — serialize them to tables/primitives first.
- ✗ No `inf`, `-inf`, `nan` (not JSON-valid; become inaccessible via Open Cloud).
- Mixed/numeric table keys: numeric keys become strings if table length is 0. Use string keys to be safe.
- Unsupported types either error or silently store as `nil`. Debug with `HttpService:JSONEncode(value)` to preview exactly what gets stored / measure size.

### Size & naming limits

| Component | Limit |
|---|---|
| DataStore name | 50 chars |
| Key name | 50 chars |
| Scope | 50 chars |
| **Value (serialized)** | **4 MB (4,194,304 bytes) per key** |

- Key naming: use prefixes to organize, e.g. `User_1234/profiles/mage`, then `ListKeysAsync` with prefix `User_1234/profiles`.
- ✓ Store all of a player's data under **one key** (one table) so it stays consistent and versions atomically. Fewer data stores + single object per user = best practice.

---

## Limits, budgets & throttling

### Request budgets (server-level, default)
Each server has a per-request-type budget (refills over time, plus one-time startup burst). Check before bursts:

```lua
local Enum = Enum.DataStoreRequestType
local budget = DataStoreService:GetRequestBudgetForRequestType(Enum.SetIncrementAsync)
```
`DataStoreRequestType` values: `GetAsync`, `SetIncrementAsync`, `UpdateAsync`, `GetSortedAsync`, `SetIncrementSortedAsync`, `OnUpdate` (deprecated), `ListAsync`, `RemoveAsync`. Configure server limits with `:SetRateLimitForRequestType()`.

**Default server limits (standard DS):** Read `60 + numPlayers×40`/min · Write `60 + numPlayers×40`/min · List `5 + numPlayers×2`/min · Remove `60 + numPlayers×40`/min.
**Ordered DS:** Read `60+np×40` · Write `30+np×5` · List `5+np×2` · Remove `30+np×5` per minute.

**Experience-level limits** (scale with concurrent users, shared across servers): Standard Read `250+CCU×40`, Write `250+CCU×20`, List `10+CCU×2`, Remove `100+CCU×40` per minute.

### Per-key throughput limits (across all servers)
| Op | Limit |
|---|---|
| Read | 25 MB / min per key |
| Write | 4 MB / min per key |
Rounded up to next KB per request. Exceeding → `DatastoreThrottled` (data store) or `KeyThrottled` (single key).

### Throttle queues
4 queues (Set, Ordered Set, Get, Ordered Get), **30 requests each**. When full, requests are dropped with errors **301–306**. A queued call keeps yielding until processed.

### Key error codes
- `101` key empty · `102` key >50 chars · `103/104` unstorable value type · `105` value >4MB.
- `301-306` throttle queue full (dropped) · `403` Studio API access not enabled · `502` rejected (retry) · `501/503/504/505` parse/corruption (retry later).
- `*ExperienceThrottled` / `*GameServerThrottled` (StandardRead/Write/List/Remove, OrderedRead/...) → rate-limited, back off.

⚠ A failed **write** means the server didn't get a success response — it does **not** guarantee the backend write didn't happen. State may be unknown until you verify with an uncached read.

---

## Error handling & retry with backoff

```lua
local function retry(fn, attempts)
    attempts = attempts or 4
    for i = 1, attempts do
        local ok, result = pcall(fn)
        if ok then return true, result end
        if i < attempts then
            task.wait(2 ^ (i - 1))   -- exponential backoff: 1, 2, 4, ...
        end
    end
    return false
end
```
✓ Retry on throttle/internal errors with exponential backoff. After a failed write, verify with an **uncached read** before refunding/retrying (see caching).

---

## Caching & eventual consistency

- `GetAsync` caches values **locally for 4 seconds** per DataStore instance. Repeated gets return the cached value (free — no budget/throughput cost).
- Different DataStore instances (different scope, or `AllScopes`) have **separate caches** → can be inconsistent.
- Version/list methods never cache. DataStores are **eventually consistent** — a read right after a write may return stale data.

```lua
-- Bypass cache for verification reads after a write
local opts = Instance.new("DataStoreGetOptions")
opts.UseCache = false
local ok, fresh = pcall(function() return store:GetAsync(key, opts) end)
```
✗ Uncached gets always count against throughput/server budgets — use sparingly.

---

## Versioning & listing

- `SetAsync`/`UpdateAsync`/`IncrementAsync` create a versioned backup on the **first write of each UTC hour**. Subsequent writes in the same hour overwrite. Backups expire 30 days after being superseded; latest never expires.
- `:ListVersionsAsync(key, sortDir, minDate, maxDate, pageSize)` → `DataStoreVersionPages`.
- `:GetVersionAsync(key, version)` → value at that version.
- `:GetVersionAtTimeAsync(key, unixTimestampMillis)`. · `:RemoveVersionAsync(key, version)`.

```lua
-- Roll back to value at/before a timestamp
local maxDate = DateTime.fromUniversalTime(2025, 1, 9, 1, 42)
local ok, pages = pcall(function()
    return store:ListVersionsAsync(KEY, Enum.SortDirection.Descending, nil, maxDate.UnixTimestampMillis)
end)
if ok then
    local items = pages:GetCurrentPage()
    if #items > 0 then
        local _, value, info = pcall(function() return store:GetVersionAsync(KEY, items[1].Version) end)
        store:SetAsync(KEY, value)   -- restore
    end
end
```

**Listing:**
- `DataStoreService:ListDataStoresAsync([prefix, pageSize])` — all data stores.
- `DataStore:ListKeysAsync([prefix, pageSize, cursor, excludeDeleted])` — keys, filter by prefix. Returns `DataStoreListingPages`; items have `.KeyName`.
- `DataStoreOptions.AllScopes = true` (with scope `""`) lists keys across all scopes; new keys must be written as `scope/keyname`.

---

## Player data lifecycle

Load on `PlayerAdded`, save on `PlayerRemoving` **and** `BindToClose` (shutdown). Naive Set on remove risks data loss/duplication if the same player is being saved from another server — use **session locking**.

### ✗ #1 mistake: no pcall + no session lock
Without session locking, a player teleporting/rejoining fast can have two servers load+save the same key, overwriting each other (item duplication / lost progress). Without pcall, a transient network failure crashes the save and loses data.

### ✓ CORRECT session-locked save/load skeleton

```lua
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local store = DataStoreService:GetDataStore("PlayerData_v1")
local DEFAULT = { coins = 0, level = 1 }
local sessions = {}                 -- userId -> loaded data (in-memory authoritative copy)
local SERVER_ID = game.JobId .. "/" .. tostring(os.time())
local LOCK_TIMEOUT = 60             -- seconds before a stale lock is force-stealable

local function retry(fn)
    for i = 1, 4 do
        local ok, res = pcall(fn)
        if ok then return true, res end
        task.wait(2 ^ (i - 1))
    end
    return false
end

-- Acquire lock + load data atomically via UpdateAsync
local function loadPlayer(player)
    local key = "user_" .. player.UserId
    local ok, data = retry(function()
        return store:UpdateAsync(key, function(old)
            old = old or { data = DEFAULT }
            local lock = old.lock
            if lock and lock.owner ~= SERVER_ID and (os.time() - lock.time) < LOCK_TIMEOUT then
                return nil          -- locked by a live server → abort, retry later
            end
            old.lock = { owner = SERVER_ID, time = os.time() }
            return old
        end)
    end)
    if ok and data then
        sessions[player.UserId] = data.data
    else
        player:Kick("Could not load your data. Please rejoin.")
    end
end

-- Save + release lock
local function savePlayer(player, release)
    local key = "user_" .. player.UserId
    local payload = sessions[player.UserId]
    if not payload then return end
    retry(function()
        return store:UpdateAsync(key, function(old)
            old = old or {}
            if old.lock and old.lock.owner ~= SERVER_ID then
                return nil          -- we lost the lock; don't clobber
            end
            old.data = payload
            old.lock = (not release) and { owner = SERVER_ID, time = os.time() } or nil
            return old
        end)
    end)
end

Players.PlayerAdded:Connect(loadPlayer)
Players.PlayerRemoving:Connect(function(player)
    savePlayer(player, true)        -- save + release lock
    sessions[player.UserId] = nil
end)

-- Autosave every 60s (refreshes lock + persists progress)
task.spawn(function()
    while true do
        task.wait(60)
        for _, player in Players:GetPlayers() do
            savePlayer(player, false)
        end
    end
end)

-- Save everyone on server shutdown — engine waits for this to finish (~30s cap)
game:BindToClose(function()
    if RunService:IsStudio() then return end
    for _, player in Players:GetPlayers() do
        task.spawn(function() savePlayer(player, true) end)
    end
    task.wait(5)                    -- give async saves time to flush
end)
```

### ProfileStore / ProfileService
For production, prefer the open-source **ProfileStore** (successor to **ProfileService**) library — it implements robust session locking, autosave, lock stealing, and reconciliation for you. Strongly recommended over hand-rolling the above for real games.

---

## MemoryStoreService

Fast, low-latency, **cross-server** in-memory storage. Ephemeral (TTL up to 45 days). Server-only. Use for matchmaking queues, match state, live/seasonal leaderboards, shared inventories, auctions, DS caches. **Studio is isolated from production memory.**

```lua
local MemoryStoreService = game:GetService("MemoryStoreService")
```

Three structures: **SortedMap** (ordered KV), **HashMap** (unordered KV, auto-partitioned, >1000 keys), **Queue** (FIFO/priority). Choose: need order → SortedMap; scan + >1000 keys → HashMap; ordered processing → Queue; <1000 keys → SortedMap.

### Quotas (experience-level, not per-server)
| Quota | Value |
|---|---|
| Memory | `64 KB + 1.2 KB × users` (8-day taper down) |
| Request units | `1000 + 120 × CCU` per minute |
| Items per structure | 1,000,000 |
| Size per structure | 100 MB |
| Value size (map item) | 32 KB |
| Key / sortKey size | 128 chars |
| Max TTL | 3,888,000 s (45 days) |

Over memory quota → writes that grow memory fail; deletes/non-growing writes still succeed. Most calls = 1 request unit; `GetRangeAsync`/`ReadAsync` cost per item returned; `HashMap:UpdateAsync` ≥2 units; `ListItemsAsync` = partitions scanned + items returned. `Queue:ReadAsync` adds 1 unit per 2s of wait.

### SortedMap
```lua
local map = MemoryStoreService:GetSortedMap("Leaderboard")
map:SetAsync(key, value, expirationSeconds, sortKey)   -- sortKey optional (number or string)
map:GetAsync(key)
map:GetRangeAsync(Enum.SortDirection.Ascending, count, lowerBound, upperBound) -- bounds = {key=, sortKey=}
map:UpdateAsync(key, function(value, sortKey) return newValue, newSortKey end, expiration)
map:RemoveAsync(key)
map:GetSizeAsync()
```
Sort order: numeric sortKeys < string sortKeys < no sortKey; ties broken by key. `UpdateAsync` auto-retries on contention (until success, callback returns nil, or max retries → conflict).

### HashMap
```lua
local hm = MemoryStoreService:GetHashMap("Inventory")
hm:SetAsync(key, value, expirationSeconds)
hm:GetAsync(key)
hm:UpdateAsync(key, function(old) return new end, expiration)  -- ≥2 request units, auto-retries
hm:ListItemsAsync(pageSize)                                    -- paginated, returns Pages
hm:RemoveAsync(key)
```

### Queue
```lua
local queue = MemoryStoreService:GetQueue("MatchQueue", invisibilityTimeout) -- default 30s
queue:AddAsync(value, expirationSeconds, priority)   -- priority 0/nil = FIFO; higher = first
local ok, items, id = pcall(function() return queue:ReadAsync(count, allOrNothing, waitTimeout) end)
queue:RemoveAsync(id)                                -- MUST remove after processing
queue:GetSizeAsync(excludeInvisible)
```
**Invisibility timeout**: a read item is hidden from other servers for N seconds. If not `RemoveAsync`'d before timeout (error/crash), it becomes visible again → guarantees processing but `RemoveAsync` ASAP to avoid duplicates.

### MemoryStore best practices
✓ Smallest viable TTL; ✓ explicitly remove processed items (TTL is safety net); ✓ exponential backoff on `DataUpdateConflict`/`RequestThrottled`; ✓ shard hot keys/large structures by prefix. Status codes: `DataUpdateConflict`, `*RequestsOverLimit`, `*MemoryOverLimit`, `ItemValueSizeTooLarge` (>32KB), `InvalidClientAccess`.

---

## MessagingService (cross-server pub/sub)

Fire-and-forget messaging between servers of the same experience. Use for announcements, server browsers, live events, cross-server triggers. **Not durable** — offline servers miss messages.

```lua
local MessagingService = game:GetService("MessagingService")
local TOPIC = "GlobalAnnounce"

-- Subscribe (returns a connection to :Disconnect())
local ok, conn = pcall(function()
    return MessagingService:SubscribeAsync(TOPIC, function(message)
        print(message.Data)        -- .Data = payload, .Sent = epoch timestamp
    end)
end)

-- Publish
pcall(function()
    MessagingService:PublishAsync(TOPIC, { event = "BossSpawned", at = os.time() })
end)
```
- Payload (`Data`) may be a string/number/table; **serialized like JSON** (same type restrictions as DataStores).
- Latency: typically ~1 second delivery; **not** real-time/guaranteed.
- Both methods yield → wrap in `pcall`. Disconnect subscriptions on `player.AncestryChanged` / when done.

### Limits
| Limit | Value |
|---|---|
| Topic size | 80 chars |
| Message size | 1,024 chars (1 KiB) |
| Messages sent / server | `600 + 240 × players` per min |
| Messages received / topic | `40 + 80 × servers` per min |
| Messages received / experience | `400 + 200 × servers` per min |
| Subscriptions / server | `20 + 8 × players` |
| Subscribe requests / server | 240 per min |

Open Cloud `publishMessage` REST API shares these same limits.

---

## Matchmaking & Teleportation

### Matchmaking (Roblox-managed)
When a player joins, Roblox finds eligible servers (excludes full/private/reserved/shutting-down), **scores** each by weighted sum of **signal** values, and routes to the highest score. Signals derive from **attributes** (numeric or categorical). Default Roblox signals: location, age group, latency, language, device. **Custom attributes** (player or server, universe-level) feed **custom signals**; custom signals read player data you supply. Tune **signal weights** in the Creator Hub matchmaking config; preview on mock servers. Numeric signal = closeness of joining player's value to server average; categorical = how common the player's value is in the server. This is config-driven (Creator Hub), not a Luau API you call per-join.

### TeleportService (move players between servers/places)
```lua
local TeleportService = game:GetService("TeleportService")

-- Reserved (private) server for matchmaking/parties:
local code, privateServerId = TeleportService:ReserveServer(placeId)  -- server-only

local options = Instance.new("TeleportOptions")
options.ReservedServerAccessCode = code      -- send a matched party to the reserved server
options:SetTeleportData({ matchId = "abc", team = "red" })  -- arbitrary serializable payload
TeleportService:TeleportAsync(placeId, { player1, player2 }, options)
```
- `ReserveServer(placeId)` → returns **access code** + reserved server id (server-only). Players teleported with that code land in the same isolated instance — ideal for custom matchmaking/lobbies.
- **Teleport data** (`SetTeleportData` / `TeleportOptions`): passed to the destination, read via `TeleportService:GetLocalPlayerTeleportData()` (client) or `Player:GetJoinData().TeleportData` (server).
- ✗ **Validate teleport data on arrival — it is client-influenceable in some flows.** Never trust it for currency/permissions; re-verify against DataStore/MemoryStore authoritative state. Treat it as a hint, not a source of truth.
- Wrap teleports in `pcall` and handle `TeleportService.TeleportInitFailed`; retry with backoff.

---

## Players service essentials

```lua
local Players = game:GetService("Players")

Players.PlayerAdded:Connect(function(player)
    player.UserId          -- stable numeric id; use for DataStore keys (NOT Name)
    player.Name            -- username (can change) — never key data by Name
    player.DisplayName
    player.User            -- Datatype.User (domain-scoped identity); player.User.Id
    player.CharacterAdded:Connect(function(char)
        local hum = char:WaitForChild("Humanoid")
    end)
end)
Players.PlayerRemoving:Connect(function(player) end)
```

- **UserId vs Name**: `UserId` is permanent and unique → always the data store key. `Name` changes; only for display.
- **Domain-scoped IDs**: new players get an experience-scoped `UserId` (different per experience); returning players keep their global id. Both are non-colliding integers, so `player.UserId` keys keep working. Engine APIs accept `Datatype.User` or numeric id interchangeably; `User.fromId(id)`, `user:ToString()`/`User.fromString()` for persisting full identity.
- **Character lifecycle**: `CharacterAdded` (spawn), `CharacterRemoving`/`Humanoid.Died` (despawn after `Players.RespawnTime`). `Players.CharacterAutoLoads = false` + `player:LoadCharacterAsync()` for manual spawn.
- **Thumbnails**: `Players:GetUserThumbnailAsync(userId, Enum.ThumbnailType.HeadShot, Enum.ThumbnailSize.Size420x420)` → image url (yields, pcall). Types: `AvatarThumbnail`, `AvatarBust`, `HeadShot`.
- **Lookup**: `GetPlayerByUserId(id)`, `GetPlayers()`, `GetNameFromUserIdAsync(id)`, `GetUserIdFromNameAsync(name)`. **Bans**: `Players:BanAsync({...})` or Creator Hub.

---

## Quirks & gotchas (high-signal)

- ✗ **#1 mistake**: no `pcall` and no session lock → lost saves on transient failures + duplication/overwrites across servers. Always do both.
- **Studio access**: DataStores are blocked in Studio until **Game Settings → Security → Enable Studio Access to API Services** is on. Error `403` otherwise. ⚠ Studio shares **live** DataStore data — use a separate test universe, not production. (MemoryStore is auto-isolated in Studio.)
- **Eventual consistency**: read right after a write may be stale (4s local cache + backend lag). Use `UseCache = false` for verification reads. **Failed write ≠ no write** — backend may have applied it; verify before refunding/retrying.
- **UpdateAsync callback can't yield** and `nil` aborts the write.
- **Key data by UserId**, never username. Store one table per user under one key for atomic, consistent versioning.
- **OrderedDataStore** = integers only, no versioning/metadata.
- **MemoryStore is not durable** — never put data that must survive 45 days there; mirror to DataStore.
- **MessagingService is best-effort**, ~1s latency, 1 KiB max — not for guaranteed/real-time delivery.
- **Teleport data is untrusted** — re-validate against authoritative storage on arrival.
- Snapshot DataStores (Open Cloud, once/day) before shipping data-logic changes to guard against corruption overwrites.
