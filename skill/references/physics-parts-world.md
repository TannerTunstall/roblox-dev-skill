# Physics, Parts & World — Reference

Roblox 3D world: parts, CFrame math, assemblies/constraints, physics simulation, collisions, spatial queries, terrain, environment. Server-authoritative unless network ownership is delegated.

## Parts & Geometry

`Part` (Block/Sphere/Cylinder/Wedge/CornerWedge via `Shape`), `MeshPart` (imported), `TrussPart` (climbable), `WedgePart`, `CornerWedgePart`, `PartOperation` (solid-modeling unions/negates). All descend from `BasePart`. `Model` is a *container*, NOT a BasePart — it has no `Touched`, `CFrame` (use `:GetPivot()`/`:PivotTo()`, `:GetBoundingBox()`), or physics of its own.

### Key BasePart properties

| Property | Meaning |
|---|---|
| `Anchored` | `true` → immune to physics/gravity/collisions; never simulated. Server always owns anchored parts. |
| `CanCollide` | Physical collision on/off. `false` = passes through everything. Independent of touch events. |
| `CanTouch` | Gates `Touched`/`TouchEnded`. `false` = neither fires. Set `false` for perf when collisions not needed. |
| `CanQuery` | `false` = exempt from raycasts & spatial queries (still renders/collides). |
| `Massless` | `true` → contributes no mass to assembly; lower priority for root part. |
| `CFrame` | Position **and** rotation (3D coordinate frame). Authoritative transform. |
| `Position` | Vector3 shortcut to CFrame translation; setting it preserves rotation. |
| `Size` | Vector3 dimensions in studs. |
| `CollisionGroup` | String name of collision group (default `"Default"`). |
| `CustomPhysicalProperties` | `PhysicalProperties` overriding material defaults. |
| `Material` | `Enum.Material` — affects density/physics AND appearance. |
| `RootPriority` | Higher = more likely to be assembly root part. |

`CollisionFidelity` / `RenderFidelity` apply to `MeshPart`/`TriangleMeshPart` — see below.

✓ Set `CFrame` to move+rotate atomically; ✗ don't set `Position` then `Orientation` separately for moving objects (two-step, can desync welds).

```lua
local p = Instance.new("Part")
p.Size = Vector3.new(4, 1, 2)
p.Anchored = true
p.CFrame = CFrame.new(0, 10, 0) * CFrame.Angles(0, math.rad(45), 0)
p.Parent = workspace
```

### MeshPart fidelity

`RenderFidelity` (`Enum.RenderFidelity`): `Automatic` (default; Highest <250 studs, Medium 250–500, Lowest ≥500), `Precise` (always highest), `Performance` (always reduced).

`CollisionFidelity` (`Enum.CollisionFidelity`), lowest→highest cost: `Box` (bounding box), `Hull` (convex hull), `Default` (approximate, supports concavity), `PreciseConvexDecomposition` (most precise, expensive, never 1:1). Applies to `MeshPart` & `PartOperation`. Visualize via Studio Visualization Options → Collision fidelity.

`SurfaceAppearance` (child, up to 4 PBR maps, needs UVs, doesn't affect geometry/physics). `MaterialVariant` (custom material w/ physical props). If both present, SurfaceAppearance textures win but MaterialVariant physical props still apply. MeshParts can't be authored in Studio — import via Blender/Maya.

## CFrame & Vector3 Math

A `CFrame` = position + 3×3 rotation. Multiplication composes transforms; `*` order matters (non-commutative).

### Constructors
- `CFrame.new(x,y,z)` / `CFrame.new(Vector3)` — position, identity rotation.
- `CFrame.new(pos, lookAtPos)` — position + front face toward target.
- `CFrame.lookAt(origin, target [, up])` — front (-Z) faces target. **Preferred** for facing.
- `CFrame.fromEulerAnglesXYZ(rx,ry,rz)` / `CFrame.Angles(rx,ry,rz)` — radians (use `math.rad()` for degrees). XYZ order.
- `CFrame.fromAxisAngle(axis, angle)`, `CFrame.fromMatrix(pos, vX, vY, vZ)`.

### Methods
| Method | Returns |
|---|---|
| `cf:ToWorldSpace(cf2)` | `cf * cf2` — offset/rotate relative to cf's own frame |
| `cf:ToObjectSpace(cf2)` | cf2 expressed in cf's local frame (`cf:Inverse() * cf2`) |
| `cf:PointToWorldSpace(v3)` | local point → world position |
| `cf:PointToObjectSpace(v3)` | world point → cf-local position |
| `cf:VectorToWorldSpace(v3)` | rotate a direction into world (ignores translation) |
| `cf:VectorToObjectSpace(v3)` | rotate world direction into local |
| `cf:Inverse()` | inverse transform |
| `cf:Lerp(cf2, alpha)` | interpolate (alpha 0–1) |
| `cf:GetComponents()` | x,y,z, R00..R22 (12 numbers) |
| `cf.Position`, `.LookVector` (-Z), `.RightVector` (+X), `.UpVector` (+Y), `.Rotation`, `.XVector/YVector/ZVector` | properties |

```lua
-- offset 2 studs along ANOTHER part's local Y (respecting its rotation):
redBlock.CFrame = blueCube.CFrame:ToWorldSpace(CFrame.new(0, 2, 0))
-- world point on a part's surface:
local worldPt = part.CFrame:PointToWorldSpace(Vector3.new(0, part.Size.Y/2, 0))
```

**Vector3**: `.new(x,y,z)`, `.zero`, `.one`, `.xAxis/yAxis/zAxis`; `:Dot`, `:Cross`, `:Lerp`, `:Unit`, `.Magnitude`, `:FixedVelocity` n/a. Arithmetic with `+ - *` (scalar or component). `CFrame.new(v3) + v3` offsets in world space.

⚠ **Float drift**: repeatedly multiplying CFrames (e.g. `cf = cf * delta` every frame) accumulates floating-point error and the rotation matrix denormalizes. Re-derive from a clean source or use `:Orthonormalize()`/lerp toward a known target instead of compounding.

## Assemblies, Welds & Constraints

An **assembly** = one+ parts rigidly joined (`WeldConstraint`, `Motor6D`, `RigidConstraint`); treated as one rigid body. Joints are only active in `Workspace`/`WorldModel` — non-functional elsewhere (e.g. ReplicatedStorage).

Assembly-wide props (read same on any member part): `AssemblyLinearVelocity`, `AssemblyAngularVelocity`, `AssemblyCenterOfMass` (read-only), `AssemblyMass` (∞ if any part anchored), `AssemblyRootPart`.

**Root part** priority: Anchored part > non-Massless > higher `RootPriority` > larger size/name-multiplier. The root doesn't move under Motor6D transforms; used for replication/ownership.

⚠ Anchoring: anchor *one* part → it becomes root, others implicitly anchored. Anchor *two+* parts in an assembly → assembly **splits** and the weld between them deactivates. To anchor a whole assembly, anchor only the root (anchoring all parts is *less* performant — more assemblies).

Apply forces/impulses to whole assembly: `:ApplyImpulse(v3)`, `:ApplyImpulseAtPosition(v3, pos)`, `:ApplyAngularImpulse(v3)`. Setting `AssemblyLinearVelocity` directly works but can look unrealistic — prefer constraints/impulses.

### Rigid joints — WeldConstraint vs Motor6D vs legacy

| Joint | Use |
|---|---|
| `WeldConstraint` | Fixed offset between two **BaseParts** (`Part0`/`Part1`), even if not touching. No attachments. Most common static weld. |
| `RigidConstraint` | Fixed offset between two **Attachments** or **Bones** (`Attachment0`/`Attachment1`). |
| `Motor6D` | Animatable rigid joint (`Part0`/`Part1`, `C0`/`C1`, `Transform`). Drives character/skeletal animation; root part stays put while `Transform` updates. |
| legacy `Weld`/`ManualWeld`/`Snap` | Deprecated `JointInstance` welds; prefer `WeldConstraint`/`RigidConstraint`. |

⚠ **WeldConstraint repositioning quirk**: setting a welded part's `Position` moves only that part and **recalculates** the weld offset (others stay). Setting its `CFrame` moves it **and** all welded parts, preserving offsets. Use `CFrame` to move a welded assembly as a unit.

### Mover constraints (force/torque — replace deprecated BodyMovers)

Connect 1–2 `Attachment`s (or `Bone`s). Build via Constraint picker or Explorer (`Attachment0`/`Attachment1`).

| Constraint | Effect | Replaces |
|---|---|---|
| `AlignPosition` | Force to move Attachment0 → Attachment1 (or to `Position` in `OneAttachment` mode) | `BodyPosition` |
| `AlignOrientation` | Torque to align orientation; `PrimaryAxisLookAt` mode points axis at Attachment1 | `BodyGyro` |
| `LinearVelocity` | Maintain constant velocity (`Line`/`Plane`/`Vector` via `VelocityConstraintMode`) | `BodyVelocity` |
| `AngularVelocity` | Maintain constant angular velocity; `RelativeTo` frame | `BodyAngularVelocity` |
| `VectorForce` | Constant linear force; `RelativeTo` (`World`/`Attachment0`/`Attachment1`) | `BodyForce`/`BodyThrust` |
| `Torque` | Constant torque about center of mass | — |
| `LineForce` | Force along line between two attachments (needs both) | `RocketPropulsion`(+AlignOrientation) |
| `AnimationConstraint` | Constrains attachments by an offset CFrame transform | — |

`AlignPosition` details: `RigidityEnabled` (true = max force ASAP; false uses `MaxForce`/`MaxVelocity`/`Responsiveness`). `Mode` = `TwoAttachment`(default)/`OneAttachment`. `ReactionForceEnabled` applies equal-opposite force to both. `ApplyAtCenterOfMass` avoids unwanted torque. `ForceLimitMode` `Magnitude`/`PerAxis`, `ForceRelativeTo`.

```lua
local ap = Instance.new("AlignPosition")
ap.Mode = Enum.PositionAlignmentMode.OneAttachment
ap.Attachment0 = part:FindFirstChildOfClass("Attachment")
ap.Position = Vector3.new(0, 20, 0)
ap.MaxForce = 100000; ap.Responsiveness = 50
ap.Parent = part
```

### Mechanical constraints (conceptual connections)

All need 1–2 `Attachment`s except `WeldConstraint` & `NoCollisionConstraint` (use `Part0`/`Part1`).

| Constraint | Behavior |
|---|---|
| `BallSocketConstraint` | Same position, free 3-axis rotation; optional tilt/twist limits |
| `HingeConstraint` | Rotate about one axis (X axes aligned). Powered: `Motor`/`Servo` |
| `PrismaticConstraint` | Slide one axis, no rotation; sliding doors/elevators |
| `CylindricalConstraint` | Slide + rotate; independent linear & angular actuators |
| `SpringConstraint` | Spring+damper force; optional min/max length, `Stiffness`/`Damping` |
| `TorsionSpringConstraint` | Torque to bring two axes together |
| `UniversalConstraint` | Keeps two axes perpendicular (drive shafts) |
| `RopeConstraint` | Max separation = `Length`; optional winch (`WinchEnabled`) |
| `RodConstraint` | Fixed separation; optional tilt limits |
| `PlaneConstraint` | Move attachments onto a plane |
| `WeldConstraint` | Rigid (see above) |
| `RigidConstraint` | Rigid between attachments/bones |
| `NoCollisionConstraint` | Disable collision between two specific parts only (still collide with world) |

**HingeConstraint power**: `ActuatorType` = `None`/`Motor`/`Servo`. Motor → drives toward `AngularVelocity` (`MotorMaxTorque`, `MotorMaxAcceleration`). Servo → drives toward `TargetAngle` (`AngularSpeed`, `ServoMaxTorque`). `LimitsEnabled` → `LowerAngle`/`UpperAngle`/`Restitution`. Both attachments' `Axis` (yellow arrow) must point the same way.

⚠ Attachment **orientation matters** for hinge/cylindrical/universal rotation axes.

## Physics Simulation

### Network ownership — CRITICAL
Distributed physics: each unanchored `BasePart`/assembly is owned by server **or** one client. Owner simulates it; ownership reduces latency (responsive) but moves trust to client.

- Default: server owns. Server **always** owns anchored parts (cannot change).
- Engine auto-assigns nearby unanchored parts to the closest player's client.
- `part:SetNetworkOwner(player)` (server-only) — force ownership. `SetNetworkOwner(nil)` = server.
- `part:SetNetworkOwnershipAuto()` — revert to automatic.
- `part:GetNetworkOwner()` → Player or nil. `part:GetNetworkOwnershipAuto()` → bool. `part:CanSetNetworkOwnership()`.
- Setting ownership on one assembly in a mechanism (no anchored parts) sets it for **every** assembly in that mechanism.

```lua
-- give vehicle to its driver for responsiveness:
vehicleSeat.Changed:Connect(function(prop)
  if prop == "Occupant" then
    local hum = vehicleSeat.Occupant
    local plr = hum and Players:GetPlayerFromCharacter(hum.Parent)
    if plr then vehicleSeat:SetNetworkOwner(plr)
    else vehicleSeat:SetNetworkOwnershipAuto() end
  end
end)
```

⚠ **Pitfalls**:
- Wrong owner = jitter/lag. In a vehicle, the *first* player to sit (e.g. passenger) gains ownership of the whole assembly — explicitly reassign to driver.
- Assign loose parts resting on a vehicle to the same client as the vehicle.
- `SetNetworkOwner(nil)` for security-critical objects, but conservatively — server sim feels jittery to clients.
- **Exploit surface**: the engine cannot verify client-owned physics. A client can teleport owned parts, clip through walls, fly. `Touched` events are tied to ownership — a client can **fake** `Touched` on parts it owns (sword hitting across map). Always validate client-driven hits server-side.
- Visualize via Studio → Network owners (green = you sim+own, red = buffer zone, white/grey = server/other owns, black = unowned/no physics).

### Mass, density & physical properties
`Mass = Density × volume`. `PhysicalProperties.new(...)` overloads:
- `(material)` — defaults for that `Enum.Material`.
- `(density, friction, elasticity)`
- `(density, friction, elasticity, frictionWeight, elasticityWeight)`
- `(..., acousticAbsorption)`

Limits (clamped): Density 0.0001–100, Friction 0.0–2.0, Elasticity 0.0–1.0, FrictionWeight 0.0–100, ElasticityWeight 0.0–100. Water density = 1 RMU/stud³ → density <1 floats, >1 sinks. Concrete 2.403, Plastic 0.7, Wood 0.35, Metal 7.85, Ice (friction 0.02 = slippery), Rubber (elasticity 0.95, friction 1.5 = bouncy/grippy).

Pairwise friction/elasticity = weighted avg: `(aVal*aWeight + bVal*bWeight)/(aWeight+bWeight)`. Resolution priority: part `CustomPhysicalProperties` > MaterialVariant props > material override > base material defaults.

```lua
part.CustomPhysicalProperties = PhysicalProperties.new(2.5, 0.4, 0.1, 1, 1)
```

### Units
1 stud = 28 cm; 1 second = 1 second; 1 RMU = 21.952 kg. Gravity (`Workspace.Gravity`): Classic 196.2, Realistic 35, Action 75 studs/s². 1 m/s = 3.57 studs/s. Engine never converts internally — keep units consistent (e.g. for VR).

### Sleep system
Assemblies sleep (skip simulation) when not moving/accelerating. States: **awake**, **sleeping**, **sleep-checking** (non-moving but neighbor of awake). Thresholds: linear vel 0.33, rotational vel 0.42, linear/rot accel 0.24 studs/s(²); neighbor wake at higher values; wake accel 16.9.

⚠ Slow-moving parts may sleep unexpectedly. Wake an assembly by: collision with assembly >1 stud/s; changing any physics prop (`Anchored`, `CanCollide`, `CustomPhysicalProperties`, `Massless`, velocity, etc.); applying nonzero impulse; changing `Workspace.Gravity/GlobalWind/AirDensity`; adding/changing a constraint; `Motor.CurrentAngle` change; seated `VehicleSeat`; within `Explosion.BlastRadius`. Actuated joints (powered hinge/prismatic/cylindrical, AlignPosition/Orientation with rigidity off, AngularVelocity, winch rope) use stricter thresholds to allow slow controlled motion. Visualize: Awake parts (red=awake, orange=sleep-checking).

## Collisions

### Touch events — UNRELIABLE
`part.Touched:Connect(fn)` and `part.TouchEnded:Connect(fn)` pass `otherPart`. Fire **only** from physical simulation movement — **NOT** from setting `Position`/`CFrame` to intersect. Gated by `CanTouch`; fire regardless of `CanCollide`.

⚠ Quirks: fire many times in rapid succession as objects settle; `TouchEnded` only when *entire* bounds exit; tied to network ownership (spoofable). Use a debounce:

```lua
local function onTouched(other)
  if part:GetAttribute("Touched") then return end
  part:SetAttribute("Touched", true)
  -- ... handle ...
  task.wait(1)
  part:SetAttribute("Touched", false)
end
part.Touched:Connect(onTouched)
```

`Model` has no Touched — loop its `BasePart` children and connect each (ignore `otherPart:IsDescendantOf(model)` self-hits). For reliable presence checks prefer `GetPartsInPart` over `GetTouchingParts`/Touched.

### Collision groups (`PhysicsService`)
Server-side, single script (registration order matters — race conditions if split).

```lua
local PS = game:GetService("PhysicsService")
PS:RegisterCollisionGroup("Characters")
PS:CollisionGroupSetCollidable("Characters", "Characters", false) -- no self-collision
part.CollisionGroup = "Characters"  -- assign by string name
```
Other APIs: `:UnregisterCollisionGroup(name)`, `:GetCollisionGroups()`, `:IsCollisionGroupRegistered(name)`, `:CollisionGroupsAreCollidable(a,b)`, `:GetRegisteredCollisionGroups()`. Parts in non-colliding groups pass through even with `CanCollide=true`. A part belongs to exactly one group. `Terrain` (a BasePart) can be assigned a group. `"StudioSelectable"` group controls 3D-viewport click selection (use as RaycastParams.CollisionGroup in plugins).

Part-to-part exception without groups: `NoCollisionConstraint`.

## Raycasting & Spatial Queries

All on `WorldRoot` (Workspace inherits). Direction vector encodes length; max ray length 15,000 studs.

```lua
local rp = RaycastParams.new()
rp.FilterDescendantsInstances = {char}
rp.FilterType = Enum.RaycastFilterType.Exclude  -- or Include
rp.IgnoreWater = true
rp.CollisionGroup = "Default"
rp.RespectCanCollide = false   -- true → use CanCollide instead of CanQuery
local result = workspace:Raycast(origin, direction, rp)
if result then
  print(result.Instance, result.Position, result.Distance, result.Material, result.Normal)
end
```

`RaycastResult`: `.Instance`, `.Position`, `.Distance`, `.Material`, `.Normal`. Returns `nil` on miss.

### Shapecasts → `RaycastResult?` (use RaycastParams)
| Method | Limits / notes |
|---|---|
| `Workspace:Blockcast(cframe, size, direction, params)` | block ≤512 studs, travel ≤1024 |
| `Workspace:Spherecast(position, radius, direction, params)` | radius ≤256, travel ≤1024 |
| `Workspace:Shapecast(part, direction, params)` | casts an arbitrary part's shape |

⚠ Shapecasts do **not** detect parts already intersecting the shape at the start.

### Overlap queries → `{BasePart}` (use OverlapParams)
| Method | Accuracy |
|---|---|
| `Workspace:GetPartsInPart(part, op)` | exact geometry (best `GetTouchingParts` replacement) |
| `Workspace:GetPartBoundsInBox(cframe, size, op)` | bounding boxes (faster, looser); cframe = center |
| `Workspace:GetPartBoundsInRadius(position, radius, op)` | bounding boxes vs sphere |
| `BasePart:GetTouchingParts()` | legacy, no params; only CanCollide parts unless part has a `.Touched` connection |

`OverlapParams.new()` (no args; set fields): `FilterDescendantsInstances`, `FilterType` (or newer `ExcludeInstances`/`IncludeInstances` — exclusions win; `nil` include = all, `{}` = none), `MaxParts` (0 = unlimited), `CollisionGroup`, `RespectCanCollide` (use CanCollide instead of CanQuery), `BruteForceAllSlow` (ignore part props, checks all — perf hit, not for live), `Tolerance` (0–0.05 studs).

⚠ With `StreamingEnabled`, distant parts may not be streamed to a client → raycast/query misses. Streaming "imposter" terrain/models are visual only, not query targets. Set `CanQuery=false` to exempt a part.

## Terrain

`Workspace.Terrain` (a `BasePart`). Voxels are 4×4×4 studs with a material. Editor: generate, sculpt, paint, sea level, import heightmap/colormap (1px = 4 studs, ≤4096²).

Scripting fill: `Terrain:FillBlock(cframe, size, material)`, `:FillBall(center, radius, material)`, `:FillCylinder(cframe, height, radius, material)`, `:FillWedge(cframe, size, material)`, `:FillRegion(region3, resolution, material)`. Read/write voxels: `Terrain:ReadVoxels(region3, resolution)` → (materials, occupancies) arrays; `Terrain:WriteVoxels(region3, resolution, materials, occupancies)`. Other: `:ReplaceMaterial`, `:Clear`, `:CountCells`, `:FillTerrain`.

```lua
workspace.Terrain:FillBlock(CFrame.new(0,0,0), Vector3.new(64,8,64), Enum.Material.Grass)
```

Water: `WaterColor`, `WaterReflectance`, `WaterTransparency`, `WaterWaveSize`, `WaterWaveSpeed`. Grass anim: `Decoration` (on), `GrassLength` (0.1–1), driven by global wind. Custom colors: `MaterialColors`. Terrain materials: Asphalt, Basalt, Brick, Cobblestone, Concrete, CrackedLava, Glacier, Grass, Ground, Ice, LeafyGrass, Limestone, Mud, Pavement, Rock, Salt, Sand, Sandstone, Slate, Snow, WoodPlanks, Water, Air. Raycasts can `IgnoreWater`.

## Environment

### Lighting (service)
- Time: `ClockTime` (0–24 hrs) ⇄ `TimeOfDay` (string "HH:MM:SS") — linked. Neither tracks real time. `GeographicLatitude` moves sun/moon without changing time.
- Color: `Ambient`, `OutdoorAmbient`, `ColorShift_Top`, `ColorShift_Bottom`.
- Intensity: `Brightness`, `ExposureCompensation` (±).
- Shadows: `GlobalShadows` (bool), `ShadowSoftness` (0–1, Realistic style only).
- Env reflection: `EnvironmentDiffuseScale`, `EnvironmentSpecularScale` (→1 = realistic metal/smooth reflections).
- `LightingStyle` (`Enum.LightingStyle`): `Realistic` (advanced) / `Soft` (flat). `PrioritizeLightingQuality` (bool).

### Atmosphere (parented to Lighting)
`Density` (air particles, obstructs distant view), `Offset` (light transmission to sky bg; balance vs Density), `Color`, `Decay` (hue away from sun; needs Haze+Glare), `Glare` (around sun; needs Haze>0), `Haze` (haziness above horizon).

### Clouds (parented to Terrain — only render there)
`Cover` (0–1 sparse→full), `Density` (transparency/storminess), `Color`. Direction/speed from global wind.

### Sky / Skybox (parented to Lighting)
Faces: `SkyboxBk/Dn/Ft/Lf/Rt/Up` (seamless cube). Celestial: `SunTextureId`, `SunAngularSize` (0 hides), `MoonTextureId`, `MoonAngularSize` (0 hides), `StarCount`, `CelestialBodiesShown` (bool). `SkyboxOrientation` (Vector3 deg, Y→X→Z; only skybox surfaces rotate). Sun/moon rise/set by `ClockTime`/`TimeOfDay`.

### Global wind
`Workspace.GlobalWind` (Vector3 = direction+strength). Affects terrain grass & dynamic clouds. Particles follow when `ParticleEmitter.WindAffectsDrag` + `Drag>0`; `Fire`/`Smoke` follow by default.

### Post-processing (under Lighting = all players, under Camera = one)
`BloomEffect`, `BlurEffect`, `ColorCorrectionEffect` (`Brightness`/`Contrast`/`Saturation`/`TintColor`), `DepthOfFieldEffect`, `SunRaysEffect` (tracks sun via ClockTime), `ColorGradingEffect` (`TonemapperPreset`: `Default`/`Retro`). Some effects need a higher Studio Editor Quality Level to preview.

## Streaming (physics-relevant)
`Workspace.StreamingEnabled` (non-scriptable, Studio-only). On clients, distant `BasePart`s may not be present → raycasts/queries/physics may miss them. Client-side physics simulation **only runs in streamed-in regions** (even for locally created/Persistent instances) — add a `Player.ReplicationFocus` / `:AddReplicationFocus()` near far objects to keep them simulating. Assemblies stream **in** as complete units (with constraints/attachments) and don't stream **out** until all their parts are eligible. Streamed-out instances are reparented to `nil` (not Destroyed); local-only property changes can be lost on re-stream. Per-model: `Model.ModelStreamingMode` (`Nonatomic`/`Atomic`/`Persistent`/`PersistentPerPlayer`); `Workspace.ModelStreamingBehavior` (`Legacy`/`Improved`).
