# Roblox Performance Optimization

Expert reference. Budgets are device-dependent targets, not hard limits.

## Mindset: measure first

- **Never optimize blind.** Profile, find the actual bottleneck, fix it, re-measure. The "obvious" cause is often wrong.
- **Frame budget = 16.67 ms @ 60 FPS** (the default cap; Windows users can raise to 240 FPS). 33.33 ms=30, 8.33 ms=120, 4.17 ms=240.
- **Consistency > raw FPS.** 59 frames at 10 ms + 1 frame at 410 ms still reads as a jarring stutter even though it "averages" 60 FPS. Hunt spikes.
- **Four separate budgets** — don't conflate:
  | Budget | Where | Cap / target |
  |---|---|---|
  | Client compute (FPS) | client CPU+GPU | 16.67 ms/frame |
  | Server compute (heartbeat) | server CPU | capped 60 Hz; keep `Steps Per Sec` ≈60 |
  | Memory | client & server, separate | server: keep <50% of `6.25 GiB + (100 MiB × max_players)`; client OOM-crashes on low-end/mobile |
  | Network (replication) | client↔server | watch data ping vs network ping |
  | Load time | join→playable | stopwatch; target "jump-in" feel |
- Server has **no frame rate** (doesn't render); server heartbeat is the analog. Low heartbeat raises latency for *all* clients.
- **Profile on a low-end/mobile baseline device.** Powerful PCs + an FPS cap hide problems (4 ms vs 16 ms both look like 60 FPS). On a phone struggling at 30 FPS, a 4× frame is unmissable. Pick a baseline device, test on it throughout dev.
- Server memory **only grows** as players connect; it does **not** shrink when they leave (until the server shuts down/recycles).
- Studio testing skews memory & FPS (runs server+client locally); read real numbers from the **client**.

## Profiling & diagnostic tools

| Tool | Shortcut | Env | Use for |
|---|---|---|---|
| Developer Console | `F9` (server: `Ctrl/⌘+F9`) | Studio + Live | logs, Memory, Server Stats/Jobs, ScriptProfiler, LuauHeap, launch MicroProfiler |
| MicroProfiler | `Ctrl+Alt+F6` (`⌘⌥F6`); pause `Ctrl/⌘+P` | Studio + Live | per-frame task timeline; find spikes & their cause |
| Performance Stats bar | `Ctrl+Alt+F7` (`⌘⌥F7`) | In-game | mem, CPU, GPU, net sent/recv, ping |
| Performance Summary overlay | `Ctrl+Shift+F5` (`⌘⇧F5`) / `Shift+F5` | both | FPS summary |
| Render Stats (Timing/Scene) | `Shift+F2` | both | draw calls, triangles |
| Debug Stats (graphics/physics/net) | `Shift+Ctrl+F1..F5` | both | detailed overlays |
| Network debug stats | `Shift+F3` | client | per-client data ping |
| Scene Analysis | Window ▸ Performance Summary ▸ Scene Analysis (Beta Features) | Studio play/test | instance/triangle/memory composition (see below) |
| Network Simulation | `Alt/⌥+S` | Studio | simulate latency/jitter/loss |
| Performance Dashboard | — | Creator Dashboard / Live | aggregate FPS, heartbeat, mem, crash rate over time |

### MicroProfiler

- **Frame graph** (top): bar height = ms. Hover for CPU/GPU. **Timeline** (below): width = task duration; stacked labels = parent→child (fix worst *child*, not parent).
- Bar colors: **orange** = Jobs Wall > Render Wall (scripts/physics/animation bottleneck); **blue** = Render Wall > Jobs Wall (rendering bottleneck — density/movement/lighting); **red** = render-bound *and* GPU Wait >2.5 ms (complexity/textures/effects). No "good" color; only matters if you're missing frame goals.
- `Ctrl/⌘+F` jumps to the worst occurrence of a tagged task across the dump. Right-click label → zoom to its duration. Groups/Threads menus filter.
- **Custom tags:** wrap code in `debug.profilebegin("Label")` / `debug.profileend()` → shows on timeline. Many engine API calls have built-in tags.
- **Threads:** *Main* (RBX Main, CPU render prep, input, Humanoids, anim, sound, script resumes), *Worker* (RBX Worker — net, physics, pathfinding), *Render* (GPU; prepare→perform→present).
- **Dumps:** "Save to file" (web/mobile) or **Dump** menu → `microprofile-<date>-<time>.html` in logs dir (`%LOCALAPPDATA%\Roblox\logs`, macOS `~/Library/Logs/Roblox`). Dump = only the captured frames (except counters mode). Max **60 frames** for server capture; ≤4 s delay.
- **Server profiling:** desktop client, join place you can edit → `Ctrl/⌘+F9` → MicroProfiler dropdown → **Server** tab → set frames/delay → **Begin server recording**.
- **Mobile** (best place to profile): Settings → MicroProfiler **On**, browse to `<device-ip>:1338` from a machine on same network. `:1338/90` for more frames; Re-capture for fresh.
- **Modes:** frame, detailed, **timers** (list w/ call counts), **counters** (instance count + bytes; cumulative since start), groups/threads (web only), hidden (desktop only).
- **Web-only:** X-Ray (memory heat coloring; `C`=total alloc size); **flame graphs** (Export CPU/memory — great for cheap-but-frequent tasks); drag a 2nd dump in → **diff flame graph** (regression/improvement). Don't combine dumps across *different places*.
- **Network capture** (dumps only, not live): Network menu → High/Low/Off. View via X-Ray/Network: recv (top) / sent (bottom) rows; physics=blue, data=green, assets=red. Use Log Scale for spikes. Right-click → Network events (per-packet size/direction/type, asset IDs at High verbosity).

### Developer Console — memory & script perf

- **Memory tab** (Client/Server): `CoreMemory` (engine, not yours) vs `PlaceMemory` (yours — most actionable). Key `PlaceMemory` labels: `GraphicsMeshParts`, `GraphicsTexture`, `Sounds`, `PhysicsParts`, `PhysicsCollision`, `Instances`, `Animation`. Also `UntrackedMemory`, `PlaceScriptMemory` (per-script), `CoreScriptMemory`.
- **Leak signals:** `LuaHeap` high/growing • `InstanceCount` consistently growing • `PlaceScriptMemory` per-script growth.
- **Luau Heap** tool: snapshot heap; compare snapshots over time. Views: Graph (alloc tree, root=`registry`; <2 KB collapsed to `…`), Object Tags (function/table/thread), Memory Categories (`debug.setmemorycategory`), Object Classes (VM only), **Unique References** & **Unparented Instances** (instances reachable only by scripts → leak hunting; shows pinning paths).
- **Script Profiler** (Dev Console): records CPU time per function call. Freq 1 KHz (default) or 10 KHz (precise, costlier). Client/Server. Callgraph (by frame task) or Functions view. Ignores sleeping/waiting threads. Exports JSON (durations in µs).
- **Server Jobs** tab: expand **Heartbeat** → **Steps Per Sec** = server heartbeat. **Server Stats**: avg ping. **Print Join Size Breakdown** (Studio Settings ▸ Network) → top-20 instances by join size.

### Scene Analysis (Studio play mode, runtime DataModel — client *and* server)

Squarified treemap + list; right-click → jump to Explorer / select all users. Modes & matching `SceneAnalysisService` API (also via Studio MCP):
| Mode | API | Returns |
|---|---|---|
| Script memory | `GetScriptMemoryAsync` | per-script Luau VM heap bytes |
| Unparented instances | `GetUnparentedInstancesAsync` | instances held by Luau but out of DataModel, grouped by host script |
| Instance composition | `GetInstanceCompositionAsync` | instance counts by category & class |
| Triangle composition | `GetTriangleCompositionAsync` | tris + draw calls by pass (Shadows/Opaque/Transparent/Terrain/Grass/Particles/Sky/UI) |
| Animation memory | `GetAnimationMemoryAsync` | loaded clip mem, dedup by clip |
| Audio memory | `GetAudioMemoryAsync` | loaded audio mem, dedup by asset ID |

Triangle stats reflect the dev machine, **not** the player's phone. Unparented refs are normal unless unexpected.

```lua
-- Quick load-time baseline (LocalScript in ReplicatedFirst)
local t0 = os.clock()
game.Loaded:Connect(function()
    print(("Loaded in %.4fs, %d instances"):format(os.clock()-t0, #workspace:GetDescendants()))
end)
```

## Rendering (client-only)

### Draw calls

A draw call = one batch of GPU draw instructions; high overhead. **Fewer draw calls = faster frame.** Targets: aim well under ~1,000 draw calls and ~1,000,000 tris on a midrange baseline; high-end caps higher.

- **Instancing:** engine collapses identical meshes into one draw call when same `MeshContent` **and** identical `SurfaceAppearance` (or, absent SurfaceAppearance, identical `TextureContent`); or identical material when neither texture exists.
  - ✓ Upload each mesh/texture **once**, duplicate in Studio (Packages help). Reuse asset IDs.
  - ✗ Importing a whole map at once → duplicate copies get unique IDs → no instancing + duplicated memory. Importer does **no** dedup.
- Find missed instancing (same name, different MeshId = candidate dupes):

```lua
for _, d in workspace:GetDescendants() do
    if d:IsA("MeshPart") then print(d.Name .. ", " .. d.MeshId) end
end -- enable Stack Lines; repeated lines = good reuse, unique lines = possible dupes
```

- **Decals, textures, particles don't batch** — they add draw calls. Watch `ParticleEmitter` property changes (dramatic cost).
- **Excessive object density:** FPS drops when looking at one cluttered area → density too high.

### Triangles, LOD, fidelity

- Triangle count matters less than draw calls but still affects frame time. Avoid `RenderFidelity = Precise` on many meshes.
- `MeshPart.RenderFidelity` → `Automatic` or `Performance` lets meshes fall back to simpler versions.
- **Model LOD (streaming):** `Model.LevelOfDetail`:
  - `SLIM` (beta, Win/macOS) — auto-generated lightweight composite mesh, camera-distance quality tiers. Static meshes + platform avatars only (no skinned/runtime-modified/animated). First load generates assets in cloud (delay). Group spatially-related parts in a Model; SLIM ignores folders. Keep model <64 cubic studs (or use Atomic) so it streams in whole.
  - `StreamingMesh` — low-res imposter; best ≥1024 studs away; no textures; no physics/raycast/collision; set descendant models to `Disabled`.
  - `Disabled`/`Automatic` — not present outside radius.
- **Avatar LOD:** `Workspace.EnableSLIMAvatars` + streaming → lightweight animated avatar reps for crowds. R6, NPCs, custom-proportion avatars, and post-`CharacterAppearanceLoaded` changes are **excluded**.
- **Culling:** frustum + occlusion culling are automatic. For indoor maps, consider manual room/portal culling.

### Lighting & shadows

- Shadows are expensive. Engine auto-degrades shadow quality as graphics level drops, **disabling shadows below quality level 4**. Reduce shadow cost to keep them enabled longer.
- ✓ `BasePart.CastShadow=false` on small/distant parts (may cause artifacts) • disable shadows on moving objects • `Light.Shadows=false` where unneeded • limit light range/angle • fewer lights • per-room lights indoors.
- MicroProfiler tags: `computeLightingPerform`, `LightGridCPU` (voxel light grid), `ShadowMapSystem`, `Prepare`/`Perform`, `UpdateView` (prep+particles), `RenderView` (render+post).

### Transparency overdraw

- Overlapping partial-transparency objects re-render the same pixels multiple times → costly. ✓ Use only Transparency `0` or `1`; avoid layered transparencies.

### FastCluster pitfalls

- Skinned MeshParts in a Model **without** a Humanoid use spatial FastClusters; moving them forces cluster rebuilds. Workaround: embed a Humanoid in the Model (forces single unified cluster, no rebuild on move) — only for parts that *do* move (adds memory). Always re-profile.
- Too many parts in a Model → more frequent full rebuilds. `updateInvalidatedFastClusters` >4 ms in MicroProfiler signals avatar/cluster churn.

## Streaming (`Workspace.StreamingEnabled`)

Highest-impact memory lever; on by default for new places. Improves join time, memory, FPS, server bandwidth. Distance-based → larger worlds benefit most. **All streaming props are non-scriptable — set on Workspace in Studio.** Streaming applies **only** to `Workspace` descendants (not ReplicatedStorage/ReplicatedFirst).

### How it works

- **Stream in:** on join, Workspace replicates *except* BaseParts, their descendants, and Models set to Atomic/Persistent/PersistentPerPlayer (and Nonatomic models when `ModelStreamingBehavior=Improved`). Rest streams in by proximity.
- **Stream out:** client removes far BasePart regions per `StreamOutBehavior`, furthest-first; never inside `StreamingMinRadius`. Streamed-out instance is **parented to `nil`** (not destroyed) so Luau state reconnects on stream-in — `ChildRemoved`/`DescendantRemoving` fire on the **parent**. Local-only (unreplicated) property changes are **lost** on out→in. Client-created/cloned instances are exempt from stream-out unless parented under a server instance.
- **Assemblies** stream in as complete units (with Constraints/Attachments); anchored = only parts in radius. Don't stream out until all their parts are eligible. Avoid huge moving assemblies (sync spikes).

### Properties

| Prop | Effect |
|---|---|
| `StreamingMinRadius` | always-loaded high-priority radius; **never** streams out. Must load before gameplay. Raising costs memory+bandwidth. |
| `StreamingTargetRadius` | max stream-in distance & max full-detail view distance. **Must be > MinRadius** (gap = buffer vs network pauses). Smaller = less server load. |
| `StreamOutBehavior` | `LowMemory` (default; out only beyond min radius under mem pressure) / `Opportunistic` (aggressively GC beyond target radius even w/o pressure — best for low-end/large content) |
| `StreamingIntegrityMode` | pause client when player outside loaded area. `PauseOutsideLoadedArea` recommended (prevents falling through unloaded terrain). |
| `ModelStreamingBehavior` | `Legacy` (default) vs `Improved` for Nonatomic models |

### ModelStreamingMode (per-Model, `Model.ModelStreamingMode`)

- **Nonatomic** (default): Legacy → container+non-BasePart descendants replicate on join, parts stream later. Improved → model streams in only when ≥1 BasePart eligible; streams out when last BasePart leaves. Part-less "container" models replicate near join, exempt from stream-out unless under a BasePart.
- **Atomic:** all initial descendants stream **together** when any descendant BasePart is eligible; streams out together when all parts eligible. Client scripts: `WaitForChild` the **model**, then descendants are guaranteed present (no per-descendant WaitForChild). ⚠ Atomicity is **initial replication only** — instances added *later* stream normally. Don't put far-apart parts in one atomic model (whole spatial extent treated as one unit).
- **Persistent:** sent whole after join, **never** streams out. Wait for `Workspace.PersistentLoaded` before access. **Rare use only** — overuse hurts perf/memory; not a way to bypass streaming.
- **PersistentPerPlayer:** Persistent for players added via `Model:AddPersistentPlayer()`, Atomic for others; revert with `RemovePersistentPlayer()`.

### Replication focus & proactive streaming

- Default focus = character `PrimaryPart`. Override via `Player.ReplicationFocus`; add/remove extra foci via `Player:AddReplicationFocus()`/`RemoveReplicationFocus()`. ⚠ Each focus multiplies server streaming load (9 moving foci ≈ 10 players); too many client foci → OOM risk. Client physics simulates **only** in streamed areas (even for Persistent/local instances) — add a focus to keep distant things simulating.
- `Player:RequestStreamAroundAsync(pos)` (server) — pre-fetch before teleport to cut pop-in. **Not a guarantee** content arrives (bandwidth/memory dependent).

### Streaming bugs & patterns

- **Never assume an instance under Workspace exists on the client.** Validate / use `WaitForChild`. ~10 ms delay between server create and client replication — a RemoteEvent/RemoteFunction can arrive **before** the part it references exists.
- Detect stream in/out with CollectionService tags:

```lua
local CS = game:GetService("CollectionService")
for _, x in CS:GetTagged("Thing") do track(x) end
CS:GetInstanceAddedSignal("Thing"):Connect(track)
CS:GetInstanceRemovedSignal("Thing"):Connect(untrack)
```

- ✗ Local clone/reparent ReplicatedStorage→Workspace → client-only copy, eligible to stream out, no server updates (desync). Flatten nested models; a Persistent inside an Atomic forces the whole Atomic persistent.
- Custom pause screen: `GuiService:SetGameplayPausedNotificationEnabled(false)` + watch `Player.GameplayPaused`. Debug overlay: `Shift+Ctrl+F3` then `Shift+1` to the Streaming panel.

## Memory & leaks

- **Leaks hit servers hardest** (up for days vs short client sessions).
- **Undisconnected connections:** engine never GCs an active connection, its callback, or values it captures. Connections auto-disconnect only when the **instance is destroyed** — and Player objects/characters are **not** auto-destroyed when a user leaves, so `CharacterAdded` etc. leak. Fix: `Connection:Disconnect()`, destroy the instance, or destroy the script.
- **Player/character cleanup:** enable `Workspace.PlayerCharacterDestroyBehavior`, or manually:

```lua
Players.PlayerAdded:Connect(function(p)
    p.CharacterRemoving:Connect(function(c) task.defer(c.Destroy, c) end)
end)
Players.PlayerRemoving:Connect(function(p) task.defer(p.Destroy, p) end)
```

- **Growing tables:** `playerInfo[player] = {}` on join but never cleared → grows forever + iteration gets slower. Clear on `PlayerRemoving`.
- **Animations** are a top production leak source (scripts keep clips alive after model destroyed). Use Scene Analysis Animation/Unparented + LuauHeap Unparented Instances.
- Held Instance refs that aren't in the DataModel → LuauHeap **Unique References** / **Unparented Instances** shows the pinning path.

## Script performance

- Luau runs synchronously on the main thread until it yields. Expensive sync work directly costs frame time.
- ✗ **High-frequency RunService events** (`PreRender`, `PreAnimation`/`PreSimulation`, `PostSimulation`, `Heartbeat`) doing heavy work every frame. Reserve per-frame code for things that truly need it (camera). MicroProfiler scopes: `RunService.PreRender/PreSimulation/PostSimulation/Heartbeat`.
- ✗ Expensive table ops (serialize/deserialize/deep-clone, recursive iteration over large tables).
- ✗ `:WaitForChild` in loops; deep `GetDescendants`/traversal each frame.
- ✓ **Break long work across frames** with `task.wait()` (e.g. 5 ms/frame → done in 20 frames, FPS held). 100 ms once/frame = 10 FPS.
- ✓ **Localize/cache:** call a method once, store the value, reuse. Cache service & instance refs in upvalues.
- ✓ **Debounce / throttle** high-frequency triggers and input.
- ✓ `task` library; `Disconnect()` unneeded connections.
- ✓ **Parallel Luau / Actors** (`Actor`, parallel) for heavy CPU work that doesn't touch the DataModel ([multithreading]).
- ✓ **Native code generation** (`--!native`) — compiles server scripts to machine code (CPU-bound, no DataModel-heavy).
- ✓ Spatial partitioning / "only process nearby" to bound per-frame work.
- ✓ `table.create(n)` to pre-size; avoid per-frame table/closure allocations (use X-Ray to spot allocation hotspots).
- Verify a suspect with `debug.profilebegin`/`profileend` then read the MicroProfiler label.

## Physics

- Adaptive timestepping (default 60/120/240 Hz by complexity) is cheaper than fixed 240 Hz mode (4× steps/frame). ✓ Anchor everything that doesn't need simulation (static NPCs).
- ✓ Minimize constraints/joints per assembly; reduce self-collision (no-collision constraints on ragdoll limbs).
- ✗ `CanCollide`/`CanTouch`/`CanQuery=false` on non-interactive parts.
- **CollisionFidelity** memory+CPU ranking: `Box` (cheapest) < `Hull` < `Default`/`Precise` (most expensive; precise is also slowest to compute). Box-collide small anchored parts; build custom box-part colliders for big complex meshes. Filter Explorer by `CollisionFidelity=PreciseConvexDecomposition` to find offenders. High `PhysicsParts` mem = reduce fidelity. Scopes: `physicsStepped`, `worldStep`.

## Humanoids

`Humanoid` is powerful but costly. Scopes: `stepHumanoid`, `stepAnimation`, `updateInvalidatedFastClusters`.

- ✗ All `HumanoidStateType`s enabled on NPCs → use `Humanoid:SetStateEnabled()` to disable unused (e.g. Climbing).
- ✗ Frequent instantiate/modify/respawn of Humanoid/skinned models (worst with layered clothing) — pool & reactivate NPCs instead of destroy/recreate; only spawn NPCs near players, cull when far.
- ✗ Server-side NPC animations replicate per-NPC → play on the **client** (create `Animator` locally; play only for nearby NPCs).
- ✓ Static NPCs: use `AnimationController` (no Humanoid). Moving NPCs: custom movement controller + AnimationController.
- ✓ Don't change avatar hierarchy after instantiation. Procedural anim: update `Motor6D.Transform`, not `JointInstance.C0/C1`. Attach extra BaseParts **outside** the avatar Model. Avoid runtime size/scale changes (rebuild FastCluster).

## Networking & replication

- ✗ Excessive remote traffic: replicating every frame, un-throttled input replication, sending more than needed (whole inventory vs the one purchased item). ✓ Send on **change**, at low frequency.
- ✗ Creating/destroying large instance trees (maps) at runtime is network-heavy → **chunk** and load over multiple frames.
- ✗ Leftover Animation Editor metadata in rigs replicates on every clone → strip it before publishing.
- ✗ **Server-side `TweenService`** → replicates tweened property every frame + jitters with latency. ✓ Tween on the **client**.
- ✓ Don't replicate purely-visual things (explosions, spell VFX, viewmodels) — server only needs the location/outcome; clients render locally.
- ✗ Don't dump everything in `ReplicatedStorage` (client loads it all) — use `ServerStorage` for client-irrelevant data.
- Scopes: `ProcessPackets` (incoming events/property changes), `Allocate Bandwidth and Run Senders` (outgoing, server). If **data ping ≫ network ping** → replication queue backlog; inspect with MicroProfiler network capture.

## Assets

- **Textures:** GPU memory ∝ pixel count, **not** disk size. 1024² = 4× the memory of 512². Pre-upload compression / alpha removal cuts disk size but **not** GPU memory (images transcoded to fixed format). Most images ≤512²; minor ones ≤256². Use **trim sheets** / sprite sheets (`ImageRectOffset`/`ImageRectSize`); tint one texture via `SurfaceAppearance.Color` instead of many colored copies.
- **Meshes:** upload once, reuse (Packages); import map assets individually (Importer does no dedup). Group by size to find duplicate mesh IDs.
- **Audio:** surprising memory hog — load only what a section needs, not all at once. Deleting all instances referencing a track unloads it.
- **Duplicate assets** (same content, different IDs) waste memory + block instancing — the #1 avoidable mistake.

## Load times — preloading

- `ContentProvider:PreloadAsync(list)` downloads assets in background to avoid pop-in. ✗ Don't over-preload (loading whole `Workspace` → huge load times). ✗ Don't poll `ContentProvider.RequestQueueSize` (unreliable + slow).
- ✓ Preload only: loading-screen images, key menu icons/backgrounds, spawn-area assets. Provide a **Skip Loading** button for large sets.

## Triage: "if X is slow, check Y"

| Symptom | Check / likely cause |
|---|---|
| Low client FPS, MicroProfiler **blue** bars | rendering: object density, draw calls, lighting/shadows, overdraw |
| Low client FPS, **orange** bars | scripts / physics / animations on worker threads |
| Low FPS, **red** bars, GPU Wait >2.5 ms | object complexity, texture size, VFX |
| FPS drops only in one map area | local object density / draw calls too high; missed instancing |
| Consistent (non-spiky) low FPS | something runs **every frame** (per-frame RunService work) |
| Periodic stutter spikes | spiky frames in graph → physics, GC, big remote/instance-tree events, respawns |
| Low server heartbeat (`Steps Per Sec`<60) | server scripts, physics, replication; profile server MicroProfiler |
| High ping; data ping ≫ network ping | replication queue backlog — too much/too-frequent remote traffic |
| Client OOM / crash on mobile | enable streaming, `Opportunistic` stream-out, reduce textures/audio, model/avatar LOD |
| Server memory growing over time | leak: undisconnected connections, uncleaned Player/char, growing tables, held refs (LuauHeap) |
| `InstanceCount`/`LuaHeap` climbing | instance ref leak / table leak → LuauHeap Unparented + Scene Analysis |
| High draw calls (Render Stats) | dup meshes/textures break instancing; decals/particles; density |
| High `GraphicsTexture` | oversized textures; reduce pixel count; trim sheets |
| High `PhysicsParts`/`PhysicsCollision` | reduce CollisionFidelity; anchor; disable CanCollide |
| `updateInvalidatedFastClusters` >4 ms | avatar/model instantiation churn; runtime scale/property changes; moving skinned parts |
| Long load time | over-preloading; large join size (Print Join Size Breakdown); enable streaming |
| Texture pop-in but slow load | preloading too much — preload only essentials |
| Instance missing on client right after remote | ~10 ms stream delay — `WaitForChild`/validate before access |
