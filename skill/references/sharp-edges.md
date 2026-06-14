# Sharp Edges — Roblox/Luau gotchas that bite everyone

Cross-cutting traps. Domain-specific quirks live in each domain's reference; this is the "why is it broken" quick-scan. Read before debugging anything weird.

## Replication & client/server
- ✗ The client and server have **separate DataModels**. An instance/value the server sets may not exist or match on the client yet, and vice-versa. Client changes to most things **don't replicate to the server**.
- ✗ **Never trust the client.** Anything in a `LocalScript`, `StarterGui`, `ReplicatedStorage`, or replicated to the client can be read/edited by an exploiter. Validate every remote arg server-side. (`networking-and-security.md`)
- ✗ Code/secrets in `ReplicatedStorage` or client scripts are **visible to exploiters**. Server-only logic/data → `ServerScriptService` / `ServerStorage`.
- `:WaitForChild()` on the client for anything the server creates/replicates — don't assume order. But `WaitForChild` with no timeout **hangs forever** if the thing never comes; pass a timeout and handle nil.
- With **StreamingEnabled**, parts can be absent client-side at any time; guard with `WaitForChild`/existence checks and keep authoritative logic on the server.

## Events & memory leaks
- ✗ **Undisconnected connections leak.** Every `:Connect` you don't `:Disconnect` keeps its closure (and captured instances) alive. Track and disconnect, or use `:Once`, or parent connections to the object's lifetime. The #1 Roblox memory leak.
- ✗ Holding references to destroyed/unparented instances keeps them in memory (shows up in `GetUnparentedInstancesAsync`). Null out refs; `:Destroy()` also disconnects the instance's own events.
- `Instance:Destroy()` is permanent (locks parent to nil). Use `:Remove()`/reparent if you need it back (rare).
- `.Changed` on a **value object** fires with the new value; on a general instance it fires with the **property name** — different signatures. Prefer `GetPropertyChangedSignal(prop)`.

## Timing & scheduling
- ✗ Use `task.wait()` not `wait()`, `task.spawn`/`task.defer` not `spawn`/`delay`, `task.delay` not `delay`. The legacy globals are throttled, less precise, and swallow errors.
- `task.wait(t)` waits **at least** `t` and returns actual elapsed — never assume exact timing or exact frame counts.
- ✗ `wait()`/`task.wait()` inside a tight `while true` with no yield floor can still starve; long synchronous loops freeze the whole script's thread.
- Connections fire on the scheduler; errors in one connection don't stop others, but **a yield inside a `Changed`/event handler** can reorder things subtly.

## Luau language
- ✗ Tables are **1-indexed**. `#t` is only valid for **gap-free** arrays; a `nil` hole makes `#` return any boundary. Don't `t[i] = nil` mid-array — use `table.remove`.
- ✗ Inserting `nil` into a table "ends" the array part. `table.insert(t, nil)` is a no-op/error pattern.
- `==` on tables/instances is **identity**, not deep equality.
- Integer vs float: `1` and `1.0` compare equal but `tostring`/serialization may differ; DataStore JSON has number precision limits.
- `and`/`or` short-circuit: `a and b or c` fails if `b` is falsy — classic ternary bug. Use `if-then-else` expr.
- Floating-point **CFrame drift** accumulates over many compositions; re-orthonormalize or rebuild from known values for long-lived transforms.

## Physics
- ✗ `Touched` is **unreliable**: misses fast/small parts, fires repeatedly (needs debounce), and only for parts with `CanTouch`. For deterministic detection use `Workspace:GetPartBoundsInBox`/`GetPartsInPart` with `OverlapParams`, or region/raycast checks.
- **Network ownership** decides who simulates a part. Default auto-assignment can hand a part to a client (lag/exploit surface). `:SetNetworkOwner(nil)` to force server, or a player for responsiveness — choose deliberately. (`physics-parts-world.md`)
- `Anchored` parts don't simulate physics and ignore forces/welds for movement.
- Legacy `BodyMovers` (BodyVelocity/BodyPosition) are deprecated → use mover constraints (`LinearVelocity`, `AlignPosition`, `VectorForce`, etc.).

## Data persistence
- ✗ Always `pcall` DataStore calls — the network **will** fail sometimes. No pcall = unhandled error = lost save.
- ✗ Use `UpdateAsync` (read-modify-write atomic) over `GetAsync`+`SetAsync` to avoid races/overwrites across servers.
- ✗ Without **session locking**, two servers (or a fast rejoin) can clobber/duplicate data. Implement a lock. (`data-and-cloud-services.md`)
- Save on `PlayerRemoving` **and** `game:BindToClose()` (server shutdown) — the former doesn't fire on a crash/shutdown.
- DataStores store **plain tables/JSON only** — no Instances, no functions, no mixed-type keys; ~4MB value limit, UTF-8 keys.
- Studio can't touch DataStores until you enable **Game Settings → Security → Studio Access to API Services**.

## UI
- ✗ Use **Scale** (UDim2 scale) for responsive layout, not raw Offset — Offset-only UI breaks across screen sizes. (`ui-ux.md`)
- `AbsolutePosition`/`AbsoluteSize` are only meaningful at runtime with a populated `PlayerGui`; they're 0/stale in edit mode.
- The top-bar **GuiInset** overlaps the top of the screen — account for `GuiService:GetGuiInset()` or set `IgnoreGuiInset`.
- Build/test in **portrait** too — most UI is made landscape-first and breaks rotated. Console needs `Selectable`/`GamepadSelection`.
- `Activated` (works across mouse/touch/gamepad) is usually better than `MouseButton1Click`.

## Monetization
- ✗ `ProcessReceipt` **must be idempotent** and persist a record before granting — it can re-fire across server restarts; non-idempotent = double-grants or lost purchases. Return the correct `Enum.ProductPurchaseDecision` (`PurchaseGranted` / `NotProcessedYet`). (`monetization-publishing.md`)
- ✗ You **must filter** all user-generated text shown to other players (`TextService:FilterStringAsync` / TextChatService) — it's policy, not optional.
- Real purchases can't be tested in Studio; use Game Passes/products in a published place.

## Studio
- ✗ Changes made **during a playtest** are discarded when you stop (unless you explicitly copy them out). Edit-mode and run-mode DataModels differ.
- Command Bar / plugin Luau runs in the **edit** DataModel — no `PlayerGui`, no live characters.
- `ChangeHistoryService` — wrap plugin edits in recordings or you break undo.

## API hygiene
- Prefer documented, non-deprecated APIs. Check `https://create.roblox.com/docs/reference/engine/deprecated.md` for the modern replacement before using anything old (BodyMovers, `wait`, `LoadAnimation` on Humanoid → on Animator, `Clothing`→layered, etc.).
- Confirm exact API names against `api/engine-api-index.txt` / `llms.txt` — don't invent members.
