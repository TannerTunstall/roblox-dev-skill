# Avatar, Animation, Audio & VFX Reference

Dense reference for Roblox characters, animation, avatars, audio, and visual effects. Exact API names; ✓ = recommended, ✗ = avoid.

---

## CHARACTERS & HUMANOID

### Model structure
- Character = `Model` + `Humanoid` + part assembly. Required parts named `HumanoidRootPart` (assembly root, invisible, drives physics) and `Head` (anchors name/health display).
- **R6**: 6 parts, joints via `Motor6D`. Legacy, blocky. Body color via `Torso`/`LeftArm` etc.
- **R15**: 15 `MeshPart`s, standardized joint hierarchy, supports scaling, layered clothing (`WrapLayer`/`WrapTarget`), `FaceControls`, attachments at standard points. ✓ Default for new work.
- `Humanoid` child `Animator` plays all animations. R15 adds higher-fidelity rigs (15 base + up to 37 extra joints) via `HumanoidRigDescription`/`DigitsRigDescription`.

### Key Humanoid properties
| Property | Notes |
|---|---|
| `Health` / `MaxHealth` | Health bar = ratio; green→yellow→red |
| `WalkSpeed` | studs/sec, default 16 |
| `JumpPower` | used when `UseJumpPower=true` (default jump impulse) |
| `JumpHeight` | studs; used when `UseJumpPower=false`. R15 default style |
| `UseJumpPower` | toggles JumpPower vs JumpHeight |
| `AutoRotate` | face movement direction |
| `RootPart` | the HumanoidRootPart |
| `FloorMaterial` | `Enum.Material`; `.Air` when airborne |
| `MoveDirection`, `WalkToPoint`, `WalkToPart` | read movement target |
| `PlatformStand`, `Sit`, `Jump` | state flags |
| `DisplayName` | name over head (defaults to account display name) |
| `HumanoidDescription` | applied appearance description |

### Movement methods
```lua
humanoid:MoveTo(position, optionalPart)  -- walk to world point; gives up after ~8s if unreachable
humanoid:Move(directionVector3, relativeToCamera)  -- continuous; Vector3.zero stops
humanoid.MoveToFinished:Connect(function(reached) end)  -- reached: bool
humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
humanoid:TakeDamage(amount)  -- subtracts unless ForceField present (✓ respects ForceField; Health -= does not)
```

### HumanoidStateType (Enum.HumanoidStateType)
| State | Meaning |
|---|---|
| `Running` | moving on ground |
| `RunningNoPhysics` | running, physics off |
| `Climbing` | on ladder/truss |
| `Swimming` / `StrafingNoPhysics` | in water |
| `Jumping` | initial jump |
| `Freefall` | airborne falling |
| `Landed` | just hit ground |
| `Seated` | in a Seat |
| `PlatformStanding` | on PlatformStand |
| `Ragdoll` | ragdoll |
| `GettingUp` | recovering |
| `FallingDown` | fell over |
| `Flying` | flying |
| `Dead` | health = 0 |
| `Physics` | full physics control |
| `None` | no state |

- `humanoid:SetStateEnabled(Enum.HumanoidStateType.X, false)` disables a state (e.g. disable `Jumping`).
- `humanoid.StateChanged:Connect(function(old, new) end)`, `humanoid:GetState()`.

### Health / death events
```lua
humanoid.Died:Connect(function() end)          -- fires when Health reaches 0
humanoid.HealthChanged:Connect(function(h) end)
-- Touch detection is on parts, not Humanoid:
part.Touched:Connect(function(hit)
    local hum = hit.Parent:FindFirstChildWhichIsA("Humanoid")
    if hum then hum:TakeDamage(25) end
end)
```
- Default respawn: `Players.CharacterAutoLoads=true` reloads ~5s after Died.

### Name / health display
- `Humanoid.DisplayDistanceType` (`Enum.HumanoidDisplayDistanceType`): `.Viewer` (uses viewer's distances), `.Subject` (humanoid controls own visibility), `.None` (never show).
- `Humanoid.NameDisplayDistance`, `Humanoid.HealthDisplayDistance` (studs).
- `Humanoid.HealthDisplayType` (`Enum.HumanoidHealthDisplayType`): `.AlwaysOn`, `.DisplayWhenDamaged`, `.AlwaysOff`.
- `Humanoid.NameOcclusion` (`Enum.NameOcclusion`): `.NoOcclusion`, `.OccludeAll`, `.EnemyOcclusion` (only different `Team`). No occlusion if occluder `Transparency>0.99` or behind a Humanoid-containing model. Team names render in `Team.TeamColor`.
- Filtered custom name: client → server `TextService:FilterStringAsync(text, player.UserId)` → `:GetNonChatStringForBroadcastAsync()` → assign `humanoid.DisplayName`.

### Character scaling (R15 only)
- Via `HumanoidDescription` scale props: `HeightScale`, `WidthScale`, `HeadScale`, `BodyTypeScale`, `ProportionScale` (no effect on R6).
- Or via `NumberValue` children of Humanoid: `BodyHeightScale`, `BodyWidthScale`, `BodyDepthScale`, `HeadScale`, `BodyProportionScale`, `BodyTypeScale` (set `.Value`).

---

## HUMANOIDDESCRIPTION (appearance)

Drives appearance for player AND NPC humanoids. ✗ Don't mix direct asset edits with HumanoidDescription (undefined behavior).

```lua
local desc = humanoid:GetAppliedDescription()  -- ✓ always read current before re-applying
desc.Torso = 86500008
desc.FaceAccessory = desc.FaceAccessory .. ",2535420239"  -- asset IDs comma-separated strings
humanoid:ApplyDescription(desc)                 -- apply to any Humanoid (yields)
-- or spawn with it:
player:LoadCharacterWithHumanoidDescription(desc)
```

- Asset-ID props (number or comma-string): `Face`, `Head`, `Torso`, `RightArm`, `LeftArm`, `RightLeg`, `LeftLeg`, `HatAccessory`, `HairAccessory`, `FaceAccessory`, `NeckAccessory`, `ShouldersAccessory`, `FrontAccessory`, `BackAccessory`, `WaistAccessory`, `GraphicTShirt`, `Shirt`, `Pants`, `ClimbAnimation`, `RunAnimation`, `JumpAnimation`, `IdleAnimation`, etc.
- Colors: `HeadColor`, `TorsoColor`, `LeftArmColor`, ... (`Color3`).
- Bulk accessories (layered support): `desc:SetAccessories({{Order=1, AssetId=id, AccessoryType=Enum.AccessoryType.Sweater}, ...}, includeRigidAccessories)`.
- `desc:GetAccessories(includeRigid)`, `desc:SetEmotes(t)`, `desc:SetEquippedEmotes({names})`, `desc:GetEmotes()`.

### Fetch descriptions
```lua
local Players = game:GetService("Players")
local desc = Players:GetHumanoidDescriptionFromUserId(userId)        -- yields
local desc2 = Players:GetHumanoidDescriptionFromOutfitId(outfitId)   -- yields
local model = Players:CreateHumanoidModelFromDescription(desc, Enum.HumanoidRigType.R15)  -- preview NPC
```
- Apply-to-all pattern: `Players.CharacterAutoLoads=false`, then in `Players.PlayerAdded` call `LoadCharacterWithHumanoidDescription`.

### Emotes
```lua
GuiService:SetEmotesMenuOpen(true)              -- GetEmotesMenuOpen() reads state
local desc = humanoid.HumanoidDescription
desc:SetEmotes({ Wave = {3576686446} })
desc:SetEquippedEmotes({"Wave"})               -- max 8, clockwise from wheel top
local played = humanoid:PlayEmote("Shrug")     -- → bool; must exist in description
StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.EmotesMenu, false)  -- hide wheel (not /e chat)
```

---

## ANIMATION

### Core workflow (Humanoid rigs)
```lua
local animator = character:WaitForChild("Humanoid"):WaitForChild("Animator")
local anim = Instance.new("Animation")
anim.AnimationId = "rbxassetid://2515090838"
local track = animator:LoadAnimation(anim)   -- → AnimationTrack
track.Priority = Enum.AnimationPriority.Action
track.Looped = true
track:Play(fadeTime, weight, speed)          -- all args optional
```
- ✓ Use `Animator:LoadAnimation`, NOT deprecated `Humanoid:LoadAnimation`.

### Non-Humanoid rigs
```lua
local controller = Instance.new("AnimationController")
controller.Parent = rig
local animator = Instance.new("Animator")
animator.Parent = controller
animator:LoadAnimation(anim):Play()
```

### AnimationTrack API
| Member | Notes |
|---|---|
| `:Play(fadeTime, weight, speed)` | start; fade blends in |
| `:Stop(fadeTime)` | `:Stop(0)` = instant |
| `:AdjustSpeed(speed)` | 1=normal, 0=pause, negative=reverse |
| `:AdjustWeight(weight, fadeTime)` | blend amount vs other tracks |
| `:GetMarkerReachedSignal(name)` | fires with marker Parameter string; connect BEFORE Play |
| `:GetTimeOfKeyframe(name)` | |
| `.Priority` | `Enum.AnimationPriority` |
| `.Looped`, `.IsPlaying`, `.Length` | |
| `.TimePosition`, `.Speed`, `.WeightCurrent`, `.WeightTarget` | |
| `.KeyframeReached` | fires for named keyframes |
| `.DidLoop`, `.Ended`, `.Stopped` | events |

- `animator:GetPlayingAnimationTracks()` → array; loop + `:Stop(0)` to clear (e.g. before swapping defaults).

### Markers
```lua
track:GetMarkerReachedSignal("FootStep"):Connect(function(param)
    -- param = marker's Parameter string (parse comma-separated yourself)
end)
```
- Distinct from keyframes; a keyframe named `End` (case-sensitive) must mark the final frame when replacing default animations.

### Priority / blending (`Enum.AnimationPriority`)
Highest → lowest: `Action4` > `Action3` > `Action2` > `Action` > `Movement` > `Idle` > `Core`. Higher overrides lower when simultaneously playing; equal priority blends by weight.
- Looping anims do NOT interpolate last→first keyframe; duplicate first keyframe as last for smooth loops.

### Replacing default animations (Animate script)
Default characters have an `Animate` LocalScript with nested instances per state; override `.AnimationId`. ✓ Server-side via `CharacterAppearanceLoaded`:
```lua
Players.PlayerAdded:Connect(function(p)
    p.CharacterAppearanceLoaded:Connect(function(char)
        local animator = char:WaitForChild("Humanoid"):WaitForChild("Animator")
        for _, t in animator:GetPlayingAnimationTracks() do t:Stop(0) end
        local a = char:WaitForChild("Animate")
        a.run.RunAnim.AnimationId = "rbxassetid://656118852"
    end)
end)
```
Paths: `run.RunAnim`, `walk.WalkAnim`, `jump.JumpAnim`, `idle.Animation1`/`idle.Animation2`, `fall.FallAnim`, `swim.Swim`, `swimidle.SwimIdle`, `climb.ClimbAnim`. Idle variant selection biased by `Animation1.Weight.Value` (IntValue child).

### Replication tradeoffs
- ✓ Animation played on a client `Animator` for the **local player's character** replicates automatically to all clients & server (network ownership).
- Server-owned models (NPCs): play server-side so all clients see it.
- ✗ Playing on client for a non-owned model won't replicate. Pick the side that owns the rig.
- Anim data saved to `ServerStorage` does NOT reach clients; move `KeyframeSequence`/`CurveAnimation` to `ReplicatedStorage` if a client needs it.

### IKControl (procedural inverse kinematics)
Parent to `Humanoid`/`AnimationController`. Required props:
- `Type` (`Enum.IKControlType`: `Position`, `Transform`), `EndEffector` (BasePart/Bone that reaches), `Target` (object with world position), `ChainRoot` (top of affected joint chain).
- Optional: `Weight` (blend), `Pole` (chain orientation). Honor real `Constraint`s (HingeConstraint elbow, BallSocketConstraint wrist) if attachments match the joint's `Motor6D.C0`/`C1`.

### Ownership / upload quirks
- ✗ Animations only play if you own them; **group-owned experiences require publishing the animation under the group** as Creator, else won't play.
- Export/Publish gives the `AnimationId` asset used in scripts.

---

## AVATAR (dev essentials)

### Accessories
- `Accessory` instance contains a `Handle` (BasePart) with an `Attachment` whose **name matches** a character attachment point (e.g. `HatAttachment`, `HairAttachment`, `FaceFrontAttachment`, `WaistCenterAttachment`).
- `humanoid:AddAccessory(accessory)` welds it to the matching attachment automatically (R15+Humanoid). Manual case (no Humanoid/non-R15): create `Weld` with `Part0`=accessory handle, `Part1`=target part.
- `humanoid:GetAccessories()`, `humanoid:RemoveAccessories()`.

### Layered clothing
- `WrapTarget` (on body MeshParts, holds cage via `CageMeshId`) + `WrapLayer` (clothing side). Clothing deforms to the body cage. Models lacking cages can't equip layered items. Non-R15 uses matching UVs.

### AvatarEditorService (catalog / inventory)
```lua
local AES = game:GetService("AvatarEditorService")
AES:PromptAllowInventoryReadAccess()                  -- prompt; then GetInventory works
AES.PromptAllowInventoryReadAccessCompleted:Connect(function(result) end)  -- Enum.AvatarPromptResult
local details = AES:GetItemDetails(assetId, Enum.AvatarItemType.Asset)     -- yields
local batch = AES:GetBatchItemDetails({ids}, Enum.AvatarItemType.Asset)
local results = AES:SearchCatalog(catalogSearchParams)  -- → CatalogPages
local rules = AES:GetAvatarRules()                       -- scale/asset limits
local conformed = AES:ConformToAvatarRules(humanoidDescription)
AES:PromptSaveAvatar(humanoidDescription, rigType)
AES:PromptCreateOutfit(humanoidDescription, rigType)
```

### AvatarCreationService (in-experience custom bodies)
- `AvatarCreationService:PromptCreateAvatarAsync(tokenId, player, humanoidDescription)` → `Enum.PromptCreateAvatarResult`, bundleId, outfitId. Requires an Avatar Creation Token (bought with Robux).
- Build body: `HumanoidDescription` with 6 child `BodyPartDescription` (`.Instance`=Folder of MeshParts, `.BodyPart`=`Enum.BodyPart`). Each of 15 MeshParts needs `EditableImage` + `WrapDeformer`(+`EditableMesh` cage). HumanoidDescription must have NO pre-existing asset IDs for those parts.
- Runtime mesh/texture: `AssetService:CreateEditableMeshAsync(content, {FixedSize=true})`, `:CreateEditableImageAsync`, `:CreateMeshPartAsync(content)`; `MeshPart:ApplyMesh(newMeshPart)`; `Content.fromUri(id)` / `Content.fromObject(editable)`.
- `EditableImage`: `:DrawImage(pos, img, Enum.ImageCombineType)`, `:DrawRectangle`, `:DrawImageProjected`. `meshPart.TextureContent = Content.fromObject(editableImage)`.
- `WrapDeformer:SetCageMeshContent(Content.fromObject(editableMesh))` deforms while preserving skinning+FACS.
- Photo-to-avatar (alpha): `RequestAvatarGenerationSessionAsync`, `PromptSelectAvatarGenerationImageAsync`, `GenerateAvatar2DPreviewAsync`/`LoadAvatar2DPreviewAsync`, `GenerateAvatarAsync`/`LoadGeneratedAvatarAsync` → HumanoidDescription. Then `Players:CreateHumanoidModelFromDescription` to display.
- Attribution on join: `Player:GetJoinData().GameJoinContext` → `JoinSource`(`Enum.JoinSource.CreatedItemAttribution`), `ItemType`, `AssetId`, `OutfitId`, `AssetType`.

### R6→R15 adapter
- `Workspace.AvatarUnificationMode = Enabled` (only when Avatar Type = R6). Injects invisible adapter `MeshPart`s named like R6 parts welded to R15; forwards R6 property changes.
- Quirks: `GetChildren()` returns BOTH proxy + R15 parts; use `WaitForChild` before indexing; Head is a MeshPart (`SpecialMesh.MeshId` fails); no Head collision — check `CollisionHead`; breaks rig-type-conditional code & custom avatar editors.

---

## AUDIO

Two systems. New audio API (graph + Wires) ✓ for new spatial/effects work; classic `Sound` still ubiquitous & simpler.

### NEW Audio API (graph of producers → modifiers → consumers via `Wire`)
- **Producers**: `AudioPlayer`, `AudioTextToSpeech`, `AudioDeviceInput` (mic), `AudioListener`.
- **Consumers**: `AudioEmitter` (3D speaker), `AudioDeviceOutput`, `AudioAnalyzer`, `AudioSpeechToText`.
- **Connector**: `Wire` with `.SourceInstance` (producer) + `.TargetInstance` (consumer); chain wires for effects.

```lua
local AudioPlayer = Instance.new("AudioPlayer")
AudioPlayer.AssetId = "rbxassetid://9120386436"   -- note: AssetId / Looping (not SoundId/Looped)
local out = Instance.new("AudioDeviceOutput")
local wire = Instance.new("Wire")
wire.SourceInstance = AudioPlayer
wire.TargetInstance = out
-- parent all under SoundService for 2D playback
AudioPlayer:Play()
```
- `AudioPlayer`: `AssetId`, `Volume`, `Looping`, `IsPlaying`, `TimePosition`, `:Play()`, `:Stop()`.
- **3D audio** (6 objects): AudioPlayer→Wire→`AudioEmitter` (parent emitter+player to the 3D object), and `AudioListener`→Wire→`AudioDeviceOutput`. Emitter parent position = sound origin; `AudioEmitter.DistanceAttenuation` = falloff curve.
- `AudioListener` placement via `SoundService.ListenerLocation` (`Default`/`None`/`Character`/`Camera`); Character/Camera auto-create an `AudioDeviceOutput`.
- `AudioDeviceInput.Player = LocalPlayer` selects whose mic. Requires `VoiceChatService.UseAudioApi = Enabled`.
- `AudioTextToSpeech`: `.Text` (≤300 chars), `.VoiceId`, `.Volume`.
- Effects (insert mid-graph, order matters): `AudioEqualizer`, `AudioCompressor`, `AudioReverb`, `AudioEcho`, `AudioChorus`, `AudioFlanger`, `AudioDistortion`, `AudioPitchShifter`, `AudioTremolo`, `AudioFader`, `AudioLimiter`, `AudioAnalyzer`. One effect can serve multiple producers.

### CLASSIC Sound API
```lua
local sound = Instance.new("Sound")
sound.SoundId = "rbxassetid://9120386436"
sound.Looped = true
sound.Volume = 1                                  -- 0–10, multiplicative; rarely > 2
sound.Parent = workspace                          -- placement decides positioning ↓
if not sound.IsLoaded then sound.Loaded:Wait() end  -- ✓ loads async — guard before precise timing
sound:Play()
```
| Property | Notes |
|---|---|
| `SoundId`, `Volume`, `PlaybackSpeed` | speed 2.0 = 2×+octave up; 0.5 = half+octave down |
| `Looped`, `Playing` | set `Playing=true` to autoplay |
| `IsLoaded`, `IsPlaying`, `TimePosition`, `TimeLength` | TimePosition seek/gate |
| `PlayOnRemove` | plays when sound is destroyed/removed |
| `SoundGroup` | assign to group (by reference, NOT parenting) |
| `RollOffMode` (`Inverse`/`Linear`/`InverseTapered`/`LinearSquare`), `RollOffMinDistance`, `RollOffMaxDistance`, `EmitterSize` | 3D falloff |

- Methods: `:Play()`, `:Stop()`, `:Pause()`, `:Resume()`. Events: `Loaded`, `Played`, `Paused`, `Resumed`, `Stopped`, `Ended`.

**Positional behavior = Parent location:**
| Parent | Emission |
|---|---|
| Child of block/sphere/cylinder `BasePart` | Volumetric surface (needs `SoundService.VolumetricAudio=Enabled`) |
| Child of `Attachment`/`MeshPart`/`WedgePart` | Point source 3D |
| In `SoundService` / `Workspace` (not part) | 2D background, same everywhere |

- `SoundService:PlayLocalSound(sound)` plays immediately on client; `SoundService.AmbientReverb` global reverb.
- `SoundGroup`: `.Volume` 0–10 multiplier over assigned sounds (relative volumes preserved); nest groups for a mix tree. Assign sounds via `Sound.SoundGroup`, not parenting.
- Legacy `SoundEffect` children of a Sound/SoundGroup: `EqualizerSoundEffect`, `CompressorSoundEffect`, `ReverbSoundEffect`, `ChorusSoundEffect`, `DistortionSoundEffect`, `EchoSoundEffect`, `FlangeSoundEffect`, `PitchShiftSoundEffect`, `TremoloSoundEffect`. Ducking: `CompressorSoundEffect` with `SideChain`, `Threshold`, `Attack`, `Release`, `Ratio`.
- Quirk: Toolbox inserts a legacy `Sound`, not `AudioPlayer` — right-click → Copy Asset ID for new API.

---

## VFX / VISUAL EFFECTS

### ParticleEmitter (parent to BasePart or Attachment)
```lua
local pe = Instance.new("ParticleEmitter")
pe.Rate = 50                                    -- particles/sec (max 400 desktop / 100 mobile)
pe.Lifetime = NumberRange.new(1, 2)             -- seconds (max 20)
pe.Speed = NumberRange.new(2, 15)               -- along EmissionDirection; change ≠ live particles
pe.SpreadAngle = Vector2.new(45, 0)
pe.Acceleration = Vector3.new(0, -10, 0)        -- gravity
pe.Color = ColorSequence.new(Color3.new(1,0,0), Color3.new(1,1,0))
pe.Transparency = NumberSequence.new({
    NumberSequenceKeypoint.new(0, 1), NumberSequenceKeypoint.new(0.2, 0), NumberSequenceKeypoint.new(1, 1) })
pe.Size = NumberSequence.new(0, 5)
pe.Parent = part
pe:Emit(20)                                     -- one-shot burst; :Clear() removes live particles
```
- Props: `Texture`, `LightEmission` (1=additive glow), `LightInfluence`, `Brightness`, `Rotation`, `RotSpeed`, `Drag`, `VelocityInheritance`, `EmissionDirection` (`Enum.NormalId`), `Enabled` (false stops new spawns only), `Orientation` (`Enum.ParticleOrientation`: `FacingCamera`/`FacingCameraWorldUp`/`VelocityParallel`/`VelocityPerpendicular`), `ZOffset`, `Squash`, `LockedToPart`, `TimeScale`, `Shape`/`ShapeStyle`/`ShapeInOut`.
- Flipbooks: `FlipbookLayout`, `FlipbookFramerate` (≤30), `FlipbookMode` (Loop/OneShot/PingPong/Random).
- Perf: Size → fill-rate; Rate/overlap → overdraw. Keep both modest. ✗ Don't spawn huge high-Rate emitters everywhere.

### Effect objects table
| Object | Parent | Key props |
|---|---|---|
| `ParticleEmitter` | BasePart/Attachment | Rate, Lifetime, Speed, Size, Color, Transparency, :Emit/:Clear |
| `Beam` | model (uses Attachments) | `Attachment0/1`, `Width0/1`, `CurveSize0/1`, `Color`, `Texture`, `TextureSpeed`, `TextureMode`, `Segments`, `FaceCamera`, `LightEmission` |
| `Trail` | part (uses Attachments) | `Attachment0/1`, `Lifetime`, `Color`, `Texture`, `WidthScale`, `MinLength`, `FaceCamera`, `Enabled`, `:Clear()` |
| `PointLight` | Attachment/BasePart | `Color`, `Brightness`, `Range`, `Shadows`, `Enabled` |
| `SpotLight` | Attachment/BasePart | + `Face` (`Enum.NormalId`), `Angle` (≤180) |
| `SurfaceLight` | BasePart | + `Face`, `Angle` (emits from whole face) |
| `Highlight` | Workspace (set `Adornee`) | `FillColor`, `FillTransparency`, `OutlineColor`, `OutlineTransparency`, `DepthMode`, `Enabled` |

```lua
local beam = Instance.new("Beam")
beam.Attachment0, beam.Attachment1 = a0, a1     -- BOTH required or won't render
beam.Width0, beam.Width1 = 0.5, 3
beam.CurveSize0, beam.CurveSize1 = 2, -2        -- cubic Bézier control offsets
beam.FaceCamera = true
beam.TextureMode = Enum.TextureMode.Wrap        -- Wrap/Static/Stretch
beam.Parent = model

local hl = Instance.new("Highlight")
hl.Adornee = model
hl.DepthMode = Enum.HighlightDepthMode.AlwaysOnTop  -- or Occluded
hl.FillTransparency, hl.OutlineColor = 0.5, Color3.new(1,1,0)
hl.Parent = workspace                           -- max 255 client-side; toggle Enabled (no perf cost)
```

### Lighting post-processing (parent to `Lighting`)
| Effect | Props |
|---|---|
| `BloomEffect` | `Intensity`, `Size`, `Threshold` |
| `BlurEffect` | `Size` |
| `ColorCorrectionEffect` | `Brightness`, `Contrast`, `Saturation`, `TintColor` |
| `SunRaysEffect` | `Intensity`, `Spread` |
| `DepthOfFieldEffect` | `FarIntensity`, `FocusDistance`, `InFocusRadius`, `NearIntensity` |

### NumberSequence / ColorSequence
```lua
NumberSequence.new(v)                    -- constant
NumberSequence.new(start, finish)        -- linear
NumberSequence.new({ NumberSequenceKeypoint.new(time, value, envelope) })  -- time 0→1
ColorSequence.new(c0, c1)                -- or {ColorSequenceKeypoint.new(t, Color3)...}
```
- Used for ParticleEmitter Color/Size/Transparency, Beam/Trail Color/Transparency, Trail WidthScale.

### Tweening effects
```lua
local TweenService = game:GetService("TweenService")
TweenService:Create(pointLight, TweenInfo.new(1), {Brightness = 0}):Play()
TweenService:Create(blur, TweenInfo.new(0.5), {Size = 24}):Play()
```
- ✓ Tween scalar props (`Light.Brightness`, `Highlight.FillTransparency`, `BlurEffect.Size`, scalar `Transparency`).
- ✗ `NumberSequence`/`ColorSequence` props are NOT tweenable — animate keypoints manually or swap whole sequences.

---

## QUIRKS CHEAT SHEET
- Animations must be **owned/published** by you (or the group for group games) or they won't play.
- ✓ `Animator:LoadAnimation` (not `Humanoid:LoadAnimation`, deprecated).
- Local player's character animations replicate automatically; play NPC anims on the server.
- R6 vs R15: scaling, layered clothing, FaceControls = R15 only; R6 uses 6 parts.
- `Humanoid:TakeDamage` respects ForceField; `Health -= n` does not.
- Sounds & audio assets load **async** — guard with `IsLoaded`/`Loaded:Wait()` before precise-timed playback.
- New audio API uses `AssetId`/`Looping`; classic uses `SoundId`/`Looped`.
- Sound positioning is decided by **parent**, not a property.
- Particles: GPU fill-rate (Size) + overdraw (Rate) are the perf killers; flipbooks auto-disable on low-memory clients.
- Highlight: max 255 client-side, rebuild cost on add/remove — toggle `Enabled` instead.
- Pathfinding: `PathfindingService:CreatePath(params)` → `path:ComputeAsync(start, finish)` (pcall + check `path.Status==Enum.PathStatus.Success`) → `path:GetWaypoints()`; loop with `humanoid:MoveTo(wp.Position)` and jump on `wp.Action==Enum.PathWaypointAction.Jump`; handle `path.Blocked`.
