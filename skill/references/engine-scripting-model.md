# Roblox Engine Scripting Model

Dense reference for the DataModel, service tree, instance lifecycle, script types/RunContext, client-server replication, events, the frame loop, Parallel Luau, and modules. Luau is gradually-typed Lua 5.1 + extensions. Tables are 1-indexed.

## The DataModel (`game`)

`game` (class `DataModel`) is the root of the hierarchy describing a place: 3D world, environment, and scripts. The server runs a "runtime" copy of the "edit" data model; each client also receives a copy. The server is the authority; it replicates state to clients.

```lua
local Players = game:GetService("Players")          -- ✓ always fetch services this way
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")      -- `workspace` global also works
```

- ✓ Convention: one `local X = game:GetService("X")` per script, variable named after the service. Same convention in ModuleScripts.
- `game:GetService(name)` creates the service if absent; safe to call repeatedly (returns the singleton).
- `game:FindService(name)`, `game:GetChildren()` (top-level services), `game:GetDescendants()`.
- `game.Loaded` event / `game:IsLoaded()` — client finished loading the full data model.
- `game:BindToClose(fn)` — server runs `fn` before shutdown (e.g. flush DataStores); a resumption point.

### Key container services & where code goes

| Service | Replicates to client? | Put here |
|---|---|---|
| `Workspace` | yes (renders the 3D world) | parts, terrain, models; `Camera`, `Terrain` pre-exist |
| `Lighting` | yes | `Atmosphere`, `Sky`, lighting settings |
| `ReplicatedStorage` | yes (both sides see it) | shared `ModuleScript`s, `RemoteEvent`/`RemoteFunction`, client `Script`s (RunContext=Client), assets to clone |
| `ReplicatedFirst` | yes, FIRST (once) | minimal loading-screen `LocalScript`/client `Script` + its assets |
| `ServerScriptService` | ✗ never | server `Script`s, server-only `ModuleScript`s |
| `ServerStorage` | ✗ never | server-only assets (maps, templates) to clone at runtime |
| `StarterPlayer.StarterPlayerScripts` | copied → `Player.PlayerScripts` | general client `LocalScript`s |
| `StarterPlayer.StarterCharacterScripts` | copied → `Player.Character` on spawn | per-character `LocalScript`s |
| `StarterGui` | copied → `Player.PlayerGui` (cleared on respawn) | UI + client GUI scripts |
| `StarterPack` | copied → `Player.Backpack` | `Tool`s, optional `LocalScript`s |
| `Players` | — | server creates one `Player` per client; `Players.LocalPlayer` on client only |

- `Starter*` containers are **templates**: their contents are *copied* into the player at runtime. The original stays in place. A `Script` (RunContext≠Legacy) placed in a Starter container runs in BOTH the original and the copy — undesirable; use `LocalScript`s there instead.
- ✓ `ServerStorage` scripts don't run, but `ServerScriptService` scripts can `require` ModuleScripts inside it.
- Organize with `Folder` (no behavior) and `Model` (geometric part groups).

## Instance basics

Everything inherits from `Instance`. Common members:

```lua
local p = Instance.new("Part")        -- create
p.Name = "Crate"
p.Parent = Workspace                  -- ✓ set Parent LAST (after configuring props) to avoid replicating intermediate states
p:Clone()                             -- deep copy (only Archivable descendants)
p:Destroy()                           -- remove + disconnect connections; do not reuse after
p:GetFullName()                       -- "Workspace.Crate"
```

### Hierarchy navigation

```lua
script.Parent                              -- the script's parent instance
inst:GetChildren()                         -- array of direct children
inst:GetDescendants()                      -- array of all descendants
inst:FindFirstChild("Name")                -- child or nil (does NOT yield)
inst:FindFirstChild("Name", true)          -- recursive
inst:FindFirstChildOfClass("RemoteEvent")  -- by class
inst:FindFirstChildWhichIsA("BasePart")    -- includes subclasses
inst:WaitForChild("Name")                  -- YIELDS until child exists (or timeout arg)
```

- ✗ `inst.SomeChild` (dot indexing for children) errors if the child isn't present yet — fragile under replication/streaming.
- ✓ Use `WaitForChild` in client scripts for anything that replicates from the server; use `FindFirstChild` when absence is valid.
- `inst.ChildAdded`, `inst.ChildRemoved`, `inst.DescendantAdded`, `inst.AncestryChanged`, `inst.Destroying` events.

### Attributes vs Value objects

Attributes = custom typed properties stored directly on any instance (replicate server→client). Prefer them over `IntValue`/`StringValue` for simple per-instance data; they can't hold tables/functions (use ModuleScripts for those).

```lua
inst:SetAttribute("Harvestable", true)         -- create or modify; nil deletes it
local v = inst:GetAttribute("Harvestable")
local all = inst:GetAttributes()               -- dictionary
inst:GetAttributeChangedSignal("Health"):Connect(function() ... end)
inst.AttributeChanged:Connect(function(name) ... end)  -- any attribute
```

### CollectionService tags

Tags group related instances; replicate server→client. Better than walking the tree for "all enemies".

```lua
local CollectionService = game:GetService("CollectionService")
CollectionService:AddTag(inst, "Enemy")
CollectionService:HasTag(inst, "Enemy")
CollectionService:RemoveTag(inst, "Enemy")
for _, e in CollectionService:GetTagged("Enemy") do ... end
CollectionService:GetInstanceAddedSignal("Enemy"):Connect(function(inst) ... end)
CollectionService:GetInstanceRemovedSignal("Enemy"):Connect(function(inst) ... end)
```

## Script types & RunContext

Three classes (all `LuaSourceContainer`):

- `Script` — runs on server or client depending on location + `RunContext`.
- `LocalScript` — runs only on the client. No RunContext.
- `ModuleScript` — reusable; never runs on its own. `require()` it.

`Script.RunContext` (modern, location-independent) values:

| RunContext | Where it runs | Notes |
|---|---|---|
| `Legacy` (default) | server, only if in a server container (`Workspace`, `ServerScriptService`, etc.) | legacy container-based rule |
| `Server` | server; can also run in `ReplicatedStorage` (but don't — it replicates) | ✓ for server logic |
| `Client` | client; runs in `ReplicatedStorage`, `ReplicatedFirst`, `StarterCharacterScripts`, `StarterPlayerScripts` | runs in Starter containers AND their copy — avoid Starter locations for Client `Script`s |

### Recommended placement

- ✓ Server code: `Script` (RunContext=`Server`) in `ServerScriptService`, alongside server-only ModuleScripts.
- ✓ Client code: `Script` (RunContext=`Client`) in `ReplicatedStorage`, alongside client-only ModuleScripts. (Debugger points to the stable `ReplicatedStorage` location instead of the ephemeral `PlayerScripts` copy.)
- ✓ Shared code: `ModuleScript`s in `ReplicatedStorage`.
- ✓ Minimal client loading script: `ReplicatedFirst` (RunContext=`Client`).
- ✓ In `Starter*` containers, use `LocalScript`s (not Client `Script`s).
- ✓ Common architecture: keep nearly all logic in `ModuleScript`s; `require` them from exactly one server `Script` and one client `Script`.
- ✓ For scripts inside Models/Packages, set `RunContext` explicitly to remove ambiguity.
- Script Sync disk naming: `name.luau`=ModuleScript, `name.server.luau`=Server, `name.client.luau`=Client, `name.local.luau`=LocalScript, `name.legacy.luau`=Legacy.

## Client–server boundary & replication

Roblox is multiplayer by default; server is authoritative ("FilteringEnabled" mindset is now mandatory). Replication keeps the data model, physics, and chat in sync.

- Server `Script` changes to replicated containers (`Workspace`, `ReplicatedStorage`, `Lighting`) propagate to clients automatically.
- Client changes to its local data model do **not** replicate back to the server (except via Remotes and engine-managed physics for owned assemblies). The server can overwrite client changes.
- `ServerStorage`/`ServerScriptService` are never sent to clients. Storing large maps there until needed reduces initial client traffic.
- Physics: assemblies have a *network owner* (a client or the server) that simulates them; usually automatic, can be set for responsiveness.
- ✗ Never trust the client. Validate every client→server request on the server (does the player actually own that item? is the move legal?).
- Latency is ~100–300 ms for most players; Studio defaults to none — set Network Simulation in Studio Settings to test.

### What does NOT cross the boundary correctly (Remote/Bindable args)
- Functions → arrive as `nil`. Metatables → stripped. Non-string table keys → coerced to strings.
- Tables are deep-copied (identities differ on the other side); ✗ don't pass mixed numeric+string-keyed tables or `nil` values.
- Instances only visible to the sender (e.g. a `ServerStorage` descendant sent to a client, or a client-created part sent to server) → arrive as `nil`.

## Event-driven model

Most engine behavior is reactive. The core pattern: get services → require modules → define functions → connect them to events.

```lua
local Players = game:GetService("Players")
local function onPlayerAdded(player)            -- event passes args
	player.CharacterAdded:Connect(function(char) ... end)
end
Players.PlayerAdded:Connect(onPlayerAdded)      -- :Connect returns an RBXScriptConnection
```

### Connect / Once / Wait / Disconnect

```lua
local conn = part.Touched:Connect(function(hit) ... end)
conn:Disconnect()                  -- stop listening
part.Touched:Once(fn)              -- ✓ auto-disconnects after first fire (vs manual connect+disconnect)
local hit = part.Touched:Wait()    -- YIELDS, returns the event's args
```

- ✓ Disconnect connections you no longer need to avoid leaks (especially per-player/per-character ones).
- All non-deferred connections on an instance auto-disconnect when it's `:Destroy()`ed (and when a `Player`/`Character` is removed).
- Each connected handler runs on its own thread; one erroring handler doesn't stop others. Multiple handlers fire in unpredictable order.

### Property / attribute change detection

```lua
inst.Changed:Connect(function(prop) ... end)                 -- fires on any property (for non-BaseParts)
inst:GetPropertyChangedSignal("Health"):Connect(function() ... end)  -- one property, no args
inst:GetAttributeChangedSignal("Score"):Connect(function() ... end)
inst.AttributeChanged:Connect(function(attrName) ... end)
```

### Deferred events (`Workspace.SignalBehavior`)

Recommended mode `Deferred`: handlers are queued and resumed at the next *resumption point* rather than firing immediately (better perf/correctness). Template places default to Deferred; `Default` is currently Immediate but will become Deferred.

- Re-entrancy depth limit is 10 (prevents infinite event cascades).
- Resumption points (in rough order): input processing → `PreRender` → legacy `wait/spawn/delay` → `PreAnimation` → `PreSimulation` → `PostSimulation` → `task.wait/spawn/delay` → `Heartbeat` → `BindToClose`.
- ✗ Patterns that assume immediate firing break:
  ```lua
  local ok = false
  event:Connect(function() ok = true end)
  trigger()        -- handler hasn't run yet under Deferred
  return ok        -- ✗ always false; yield first or restructure
  ```
- Under Deferred, `Destroy()`/property changes happen immediately; the handler runs *after*, seeing the already-changed state. `Destroy()` runs pending handlers; `Disconnect()` drops pending ones.

## Frame / update lifecycle — `RunService`

Use `RunService` for per-frame logic and context checks. Per frame, events fire in this order:

| Event | Side | Use |
|---|---|---|
| `RunService.PreRender` | client only | camera/UI updates just before rendering (formerly `RenderStepped`) |
| `RunService.PreAnimation` | both | before animations evaluate |
| `RunService.PreSimulation` | both | before physics step (formerly `Stepped`); passes `(deltaTime)` |
| `RunService.PostSimulation` | both | after physics step (formerly `Heartbeat` semantics); passes `(deltaTime)` |
| `RunService.Heartbeat` | both | end of frame, after physics; passes `(deltaTime)` |

```lua
local RunService = game:GetService("RunService")
RunService.Heartbeat:Connect(function(dt)
	position += velocity * dt           -- ✓ scale by deltaTime for frame-rate independence
end)
```

- Context checks: `RunService:IsServer()`, `:IsClient()`, `:IsStudio()`, `:IsRunning()`.
- `RunService:BindToRenderStep(name, priority, fn)` — client-only; run `fn` each render frame at a chosen `Enum.RenderPriority`; pair with `RunService:UnbindFromRenderStep(name)`. ✓ Preferred for camera/character logic that must run before render.
- `task.wait()` (no arg) ≡ waiting for one `Heartbeat`.

## task scheduling (use over legacy globals)

```lua
task.spawn(fn, ...)        -- resume immediately on a new thread (replaces spawn)
task.defer(fn, ...)        -- resume at end of current resumption point (replaces spawn, no throttle)
task.delay(n, fn, ...)     -- resume after n seconds (next Heartbeat); n=0 → next step
local dt = task.wait(n)    -- yield n seconds, returns actual elapsed; no arg → next Heartbeat
```

- ✗ Avoid legacy `wait()`, `spawn()`, `delay()` — throttled and less optimized. ✓ Use `task.*`.

## Parallel Luau (Actors)

Run code across multiple threads for CPU-heavy work (NPC logic, raycast validation, procedural gen).

- Place scripts under `Actor` instances (`Class.Actor`); each Actor is an isolation unit. Scripts in the *same* Actor run serially w.r.t. each other — use **many** Actors for real parallelism. Don't nest Actors; a script is owned by its closest ancestor Actor. `script:GetActor()`.
- Switch phases with yieldable `task.desynchronize()` (→ parallel) and `task.synchronize()` (→ serial). Or `signal:ConnectParallel(fn)` to run a handler in parallel directly.

```lua
RunService.Heartbeat:ConnectParallel(function()
	-- parallel: heavy read-only computation here
	task.synchronize()
	-- serial: now safe to mutate the data model
end)
```

- Thread safety levels (per API member; default = **Unsafe**): Unsafe (no parallel access), Read Parallel (read only), Local Safe (within same Actor), Safe (read+write). Check tags in the API reference.
- ✗ In a desynchronized phase you generally **cannot write to the data model**, and **cannot `require()`** — require modules earlier in a serial context.
- ✗ `Terrain:WriteVoxels`, instance mutation, etc. must run in the serial phase (`task.synchronize()` first).
- Cross-thread comms: `Actor:SendMessage(topic, ...)` + `Actor:BindToMessage(topic, fn)` / `Actor:BindToMessageParallel(topic, fn)`; `SharedTable` (atomic shared state, no copy on send); or read/write data-model properties/attributes (with sync restrictions).

## Modules & shared code

```lua
-- ModuleScript (e.g. in ReplicatedStorage), returns one value (table/function/etc., not nil):
local PickupManager = {}
function PickupManager.getBonus(rarity) ... end
return PickupManager
```

```lua
-- Consumer (server or client):
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PickupManager = require(ReplicatedStorage:WaitForChild("PickupManager"))
PickupManager.getBonus("legendary")
```

- A module's body runs **once per side**; `require` returns the *same cached reference* thereafter (mutations persist). Server and client each get their own independent instance/copy.
- ✗ Don't `require` modules circularly → "Requested module was required recursively".
- ✓ Use ModuleScripts (not value objects/attributes) to share tables, functions, and config across many objects.
- ✓ Encapsulate networking/error-prone services in a module (e.g. one RemoteEvent wrapper with an `id` arg) to keep the rest of the codebase clean.

## Bindable vs Remote events

**Bindable** = same side of the boundary. **Remote** = across the boundary.

### BindableEvent / BindableFunction (one side only)
```lua
bindable.Event:Connect(function(...) end)    -- listener
bindable:Fire(...)                           -- async, doesn't yield
local r = bindableFunc:Invoke(...)           -- yields until OnInvoke returns
bindableFunc.OnInvoke = function(...) return v end  -- only the LAST assignment is used
```
Often a ModuleScript is a cleaner alternative for same-side coordination.

### RemoteEvent (one-way, no return) — place in `ReplicatedStorage`
```lua
-- Client → Server
remote:FireServer(...)                                      -- client
remote.OnServerEvent:Connect(function(player, ...) end)     -- server; player is ALWAYS first arg
-- Server → one Client
remote:FireClient(player, ...)                              -- server
remote.OnClientEvent:Connect(function(...) end)             -- client (no player arg; use Players.LocalPlayer)
-- Server → all Clients
remote:FireAllClients(...)                                  -- server
```
- `UnreliableRemoteEvent` — same API, drops ordering/reliability for perf; use for continuous, non-critical data.
- Clients can't talk directly to each other: relay client→server→`FireClient`/`FireAllClients`.

### RemoteFunction (two-way, yields)
```lua
local result = remoteFunc:InvokeServer(...)                 -- client yields for return
remoteFunc.OnServerInvoke = function(player, ...) return v end  -- server; last definition wins
```
- ✗ Avoid `InvokeClient` server→client→server: a client error/disconnect errors or yields the server forever. Use a `RemoteEvent` instead for things like GUI updates.

## Replication order & streaming awareness

The engine does **not** guarantee the order in which objects/changes replicate to clients → `WaitForChild` is essential.

Predictable client startup sequence:
1. `ReplicatedFirst` contents load; its client scripts run first.
   - ✓ Those scripts can read `ReplicatedFirst` without `WaitForChild`.
   - ✗ They can't safely read other services yet (using `WaitForChild` there defeats `ReplicatedFirst`'s purpose).
2. Rest of the game loads → `game.Loaded` fires / `IsLoaded()` true.
3. `PlayerScripts` (from `StarterPlayerScripts`) and client `Script`s in `ReplicatedStorage` run — can read `ReplicatedStorage` without `WaitForChild`.
4. `Character` spawns → `StarterCharacterScripts` copies run.

- Same-type changes (e.g. two attribute writes) generally arrive in order; cross-type ordering (a property change vs a `FireAllClients`) is **not** guaranteed — detect via events, don't assume.
- **Instance streaming** (`Workspace.StreamingEnabled`): the server initially sends only nearby `Workspace` content; parts stream in/out over time. Client scripts must `WaitForChild` (or handle nil) for `Workspace` objects — they may not exist yet or may be removed. Tune via per-model streaming controls. Server always has the full data model.

## Quick do/don't

- ✓ Server is the source of truth; validate all client input server-side.
- ✓ `game:GetService` for services; `WaitForChild` for replicated/streamed children.
- ✓ Set `Instance.Parent` last; `task.*` over legacy globals; `:Once`/`:Disconnect` to manage connections; scale motion by `deltaTime`.
- ✗ Don't put server logic or secrets in replicated containers (`ReplicatedStorage`/`Workspace`).
- ✗ Don't pass functions/metatables/mixed-key tables/server-only instances through Remotes/Bindables.
- ✗ Don't assume replication order, immediate event firing under Deferred, or that `Workspace` children exist on the client.
- ✗ Don't mutate the data model or `require` in a desynchronized parallel phase.
