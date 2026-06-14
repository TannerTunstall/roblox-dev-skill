# Roblox UI & UX Reference

Dense reference for building great Roblox UI with good cross-platform UX. All UI logic runs **client-side** (LocalScript / `RunContext.Client`). Most elements inherit `GuiObject`.

## GUI Object Model

### Containers
| Container | Where | Purpose |
|---|---|---|
| `ScreenGui` | `StarterGui` → cloned to each player's `PlayerGui` | 2D overlay on player screen |
| `SurfaceGui` | on a `BasePart` (parent or `Adornee`) | UI on a part face in 3D world |
| `BillboardGui` | on `BasePart`/`Attachment` (parent or `Adornee`) | UI in 3D that always faces camera |

`StarterGui` → clones to `PlayerGui` on spawn. `ScreenGui.Enabled=false` → contents don't render, process input, or update. Multiple ScreenGuis layer by `DisplayOrder` (higher = front). Access at runtime: `Players.LocalPlayer.PlayerGui:WaitForChild("X")`.

- `ScreenGui.ResetOnSpawn` (default `true`) → re-clones on respawn. Set `false` AND make it a **direct** child of StarterGui to persist (indirect/folder-nested always resets).
- `SurfaceGui`: `Face`, `Adornee` (overrides parent assoc, settable at runtime), `AlwaysOnTop` (renders over 3D, ignores light), `Brightness` (0–1000), `LightInfluence` (0–1), `MaxDistance` (default 1000, 0=infinite), `ZOffset` (layer order). Best practice: size children with **scale**. Interactive elements (buttons) need `SurfaceGui` in `PlayerGui` (via StarterGui) AND part `CanQuery=true`.
- `BillboardGui`: `Size` scale components = stud size in 3D (e.g. `UDim2.fromScale(10,2)`). `StudsOffset` (Vector3-style XYZ shift). `AlwaysOnTop`, `Brightness`, `LightInfluence`, `MaxDistance` (0/inf=infinite). Use `TextScaled` on labels so text scales with distance. Interactive elements need it in `PlayerGui`.

### Core GuiObjects
| Object | Notes |
|---|---|
| `Frame` | Container. `BackgroundColor3`, `BackgroundTransparency` (1=invisible container), `ClipsDescendants` |
| `TextLabel` / `ImageLabel` | Display text / image (non-interactive) |
| `TextButton` / `ImageButton` | Interactive (`GuiButton` subclass) |
| `TextBox` | Text input |
| `ScrollingFrame` | Frame with scrollable canvas + scroll bars |
| `CanvasGroup` | Frame-like; renders children as one group → `GroupTransparency`, `GroupColor3` (tween whole group) |
| `ViewportFrame` | Renders 3D content into 2D UI |
| `VideoFrame` | Plays video |

## Position & Size (UDim2)

`Position` and `Size` are `UDim2` = `{X.Scale, X.Offset}, {Y.Scale, Y.Offset}`.
- **Scale** = fraction (0–1) of **parent** size. **Offset** = pixels. Final = Scale% + Offset px (additive).
- ✓ Prefer **Scale** for responsive UI (adapts to all screen sizes/aspect ratios). ✗ Pure Offset breaks across devices.
- Constructors: `UDim2.new(sx,ox,sy,oy)`, `UDim2.fromScale(sx,sy)`, `UDim2.fromOffset(ox,oy)`.
- Studio infers: entering `0.5`→`{0.5,0},{0.5,0}` (scale); `20`→`{0,20},{0,20}` (offset).

### AnchorPoint
`Vector2` (0–1) origin within the object that `Position`/`Size` reference. Default `(0,0)`=top-left. `(0.5,0.5)`=center → object centers on its Position and scales outward from middle. ✓ Use `(0.5,0.5)` + scale Position for centered, tween-friendly elements.

### ZIndex / layering
- `GuiObject.ZIndex` (integer, +/-) → render order; higher renders on top.
- `ScreenGui.ZIndexBehavior` (default `Sibling`): children always render above parents; `ZIndex` orders among the same layer. `Global` mode orders purely by ZIndex across the tree (legacy).
- `Visible` (bool), `Active` (sinks input + enables gamepad selection).

### AbsolutePosition / AbsoluteSize
Read-only `Vector2` of actual rendered pixel position/size (after scale/offset/layout/constraints resolved). Use to position relative to other elements or to measure. Listen via `GetPropertyChangedSignal("AbsoluteSize")` / `:GetPropertyChangedSignal("AbsolutePosition")`.

## Layout Structures (one per parent, controls siblings)

Inserting a layout **overrides/influences** sibling `Position`/`Size` (and `Rotation` for UIListLayout). Constraints (`UISizeConstraint`, `UIAspectRatioConstraint`) override the layout.

### UIListLayout
Rows/columns; auto-reflows on add/remove.
- `FillDirection`: `Horizontal` | `Vertical`
- `SortOrder`: `LayoutOrder` (by `GuiObject.LayoutOrder` int, ascending) | `Name`
- `HorizontalAlignment`: `Left`|`Center`|`Right`; `VerticalAlignment`: `Top`|`Center`|`Bottom` (aligns list bounds in container)
- `Padding` (`UDim`) — space **between** items (not around bounds; use `UIPadding` for that)
- `Wraps` (bool) — wrap to next line when overflow
- `HorizontalFlex`/`VerticalFlex` → `Enum.UIFlexAlignment`: `None`,`Fill`,`SpaceAround`,`SpaceBetween`,`SpaceEvenly` — distribute extra space
- `ItemLineAlignment` → `Enum.ItemLineAlignment`: `Start`,`Center`,`End`,`Stretch` (cross-axis alignment within a line; `Stretch` fills line)
- ✗ Reverse order: negate LayoutOrder (`0,1,2`→`0,-1,-2`)

### UIFlexItem (flexbox, child of a flexing item)
Insert as child of a GuiObject under a UIListLayout. `FlexMode` → `Enum.UIFlexMode`: `None`,`Grow`,`Shrink`,`Fill`,`Custom`. Use for e.g. fixed labels + a middle bar that `Fill`s remaining space. ⚠ Slight perf cost on resize/dynamic add — prefer grid when strict 2D alignment needed.

### UIGridLayout
Uniform cells. `CellSize` (UDim2), `CellPadding` (UDim2), `FillDirection`, `FillDirectionMaxCells` (int), `SortOrder`, alignments. ⚠ Child `UISizeConstraint.MinSize` > CellSize → item spans multiple cells.

### UITableLayout
HTML-table style: siblings = rows, their children = columns. `FillDirection` (default `Vertical`), `FillEmptySpaceColumns`/`FillEmptySpaceRows` (bool; if off, sibling `Size` sets cell dims), `Padding`, `SortOrder`. Overflow cells align top-left.

### UIPageLayout
Each sibling = a page. `:Next()`, `:Previous()`, `:JumpToIndex(i)` (0-based), `:JumpTo(guiObject)`. Props: `Circular`, `Animated`, `TweenTime`, `EasingStyle`, `EasingDirection`, `GamepadInputEnabled`, `ScrollWheelInputEnabled`, `TouchInputEnabled`, `Padding`, `FillDirection`. Use for tabs, tutorials, carousels.

## Size Modifiers & Constraints (child of target GuiObject)

| Object | Key props | Notes |
|---|---|---|
| `UIAspectRatioConstraint` | `AspectRatio` (W:H, default 1), `AspectType` (`FitWithinMaxSize`/`ScaleWithParentSize`), `DominantAxis` (`Width`/`Height`) | ✓ Keep images/tiles square or fixed ratio across screens. Overrides layout |
| `UISizeConstraint` | `MinSize`, `MaxSize` (Vector2 px) | Clamp pixel size; overrides layout |
| `UITextSizeConstraint` | `MinTextSize`, `MaxTextSize` (int) | ✓ Pair w/ `TextScaled` to keep text legible. ✗ Don't set min < 9 |
| `UIScale` | `Scale` (number) | Multiplies size of object **and all children** (incl. modifiers). ✓ Tween for hover-grow |

### AutomaticSize (a `GuiObject` property, not a modifier)
`Enum.AutomaticSize`: `None`(default),`X`,`Y`,`XY` — resizes object to fit descendants. When on, `Size` acts as **minimum**. Respects `AnchorPoint`. ✓ With `TextWrapped`+`Y` → multi-line text grows. ScrollingFrame uses `AutomaticCanvasSize` (same enum) instead. ✗ Don't combine with `TextScaled` (opposite goals).

## Appearance Modifiers (child of target)

- `UICorner`: `CornerRadius` (UDim) — Scale rounds to % of shortest edge (≥0.5=pill); Offset=px. (Beta: per-corner `TopLeftRadius` etc.)
- `UIStroke`: `Thickness`, `Color`, `Transparency` (independent of parent), `ApplyStrokeMode` (`Contextual`=text outline on text objects / `Border`), `LineJoinMode` (`Round`/`Bevel`/`Miter`), `StrokeSizingMode` (`FixedSize`/`ScaledSize`). Add child `UIGradient` for gradient stroke. ⚠ Don't tween `Thickness` on **text** (perf/flicker).
- `UIGradient`: `Color` (`ColorSequence`), `Transparency` (`NumberSequence`), `Offset` (Vector2 %), `Rotation` (deg), `Enabled`.
- `UIPadding`: `PaddingTop/Bottom/Left/Right` (UDim, neg allowed) — pads parent's **contents**. ✓ Use for padding around list bounds.

## Responsive / Adaptive Design (phone/tablet/console/PC)

✓ **Build with Scale** for Position/Size; use Offset only for things that must stay fixed pixels (e.g. 1px borders, fixed icon sizes paired with AspectRatio).
✓ `UIAspectRatioConstraint` to lock element shape across aspect ratios.
✓ `UITextSizeConstraint` + `TextScaled` for legible-but-bounded text.
✓ Test across emulated devices (phone/tablet/console) and orientations.

### Screen insets / safe areas
`ScreenGui.ScreenInsets` → `Enum.ScreenInsets`:
| Value | Behavior |
|---|---|
| `CoreUISafeInsets` (default) | Keeps children clear of top-bar buttons + device cutouts. ✓ For interactive UI |
| `DeviceSafeInsets` | Avoids device notches/cutouts only (not top bar) |
| `TopbarSafeInsets` | Keeps content between top bar and right safe edge; ScreenGui flexes horizontally |
| `None` | Full screen, may be hidden by notches. Only for non-interactive backgrounds |

- `GuiService:GetGuiInset()` → returns the topbar inset (Vector2 top-left, Vector2 bottom-right) so you can offset manually.
- `ScreenGui.IgnoreGuiInset` (bool) — if `true`, content starts at absolute screen top (under the topbar inset). ✗ Avoid overlapping interactive UI with the topbar.
- `PlayerGui.ScreenOrientation` / `StarterGui.ScreenOrientation` → `Enum.ScreenOrientation`: `LandscapeSensor`(default), `Sensor`(landscape+portrait), `LandscapeLeft`, `LandscapeRight`, `Portrait`. Detect via `PlayerGui:GetPropertyChangedSignal("ScreenOrientation")` + `CurrentScreenOrientation`.

### Mobile UX zones
✗ Don't place important info/buttons in **bottom-left/bottom-right reserved zones** (default thumbstick + jump button live there).
✓ Keep frequently-used buttons in **thumb-reachable zones** near the bottom corners. Tablets have larger screens — a button 40% from top is reachable on phone but not tablet. Position custom buttons **relative to the jump button** (find via `PlayerGui:FindFirstChild("JumpButton", true)`).
✓ Use **context-based UI** (proximity prompts) instead of always-on buttons; screen space is scarce on mobile.

### Default UI control
`StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.X, false)` — X: `PlayerList`,`Health`,`Backpack`,`Chat`,`EmotesMenu`,`SelfView`,`Captures`,`AvatarSwitcher`. Hide touch controls: `GuiService.TouchControlsEnabled = false`.

## Text, Fonts, Rich Text

`TextLabel`/`TextButton`/`TextBox` text props:
- `Text`, `TextColor3`, `TextTransparency`, `TextSize` (px), `TextXAlignment` (`Left`/`Center`/`Right`), `TextYAlignment` (`Top`/`Center`/`Bottom`), `LineHeight`, `MaxVisibleGraphemes` (typewriter), `TextDirection`.
- `TextScaled` (bool) — fills rect, **overrides TextSize**; pair with `UITextSizeConstraint`. Forces wrapping.
- `TextWrapped` (bool) — wrap to multiple lines.
- `TextTruncate` → `Enum.TextTruncate`: `None`,`AtEnd` (ellipsis).
- `FontFace` (`Font` datatype, modern; replaces deprecated `Font` enum). `Font.new(assetId, weight, style)`, `Font.fromEnum(Enum.Font.X)`, `Font.fromName(name, weight, style)`. `.Weight`=`Enum.FontWeight` (Regular=400, Bold=700, Thin…Heavy); `.Style`=`Enum.FontStyle` (`Normal`/`Italic`).
- Read-only: `TextBounds` (Vector2), `TextFits` (bool).

### Rich Text (set `RichText = true` first, else tags render literally)
Tags: `<b>`,`<i>`,`<u>`,`<s>`,`<br/>`, `<uc>/<uppercase>`, `<sc>/<smallcaps>`, `<font color="#hex|rgb(r,g,b)" size="px" face="Name" family="rbxasset://..." weight="700|heavy" transparency="0.5">`, `<stroke color="" thickness="" transparency="" joins="round|bevel|miter" sizing="fixed|scaled">`, `<mark color="" transparency="">`, `<!-- comment -->`.
Escapes: `&lt;` `&gt;` `&quot;` `&apos;` `&amp;`. ⚠ Localization strips tags (re-apply manually). ⚠ Char-by-char animation breaks tags (strip before grapheme reveal).

### Images (ImageLabel/ImageButton)
`Image` (asset id), `ImageColor3` (tint), `ImageTransparency`. `ScaleType` → `Enum.ScaleType`: `Stretch`(default),`Slice`(9-slice),`Tile`(+`TileSize`),`Fit`,`Crop`. `ResampleMode` → `Enum.ResamplerMode`: `Default`(bilinear)/`Pixelated`(crisp/pixel-art). Sprite sheets: `ImageRectOffset`/`ImageRectSize` (Vector2). Set `BackgroundTransparency=1` to show image only.
**9-slice**: `ScaleType=Slice` + `SliceCenter` (`Rect.new(left,top,right,bottom)` in source px) + `SliceScale` (default 1) → borders don't distort when resized.

## ScrollingFrame
- `CanvasSize` (UDim2) — scrollable area; bar appears when canvas exceeds frame on an axis.
- `AutomaticCanvasSize` (`Enum.AutomaticSize`) — auto-grow canvas to fit children (✓ pair with UIListLayout/UIGridLayout).
- `CanvasPosition` (Vector2 px) — scroll offset (read/set).
- `ScrollBarThickness` (px), `ScrollingEnabled` (bool), `ScrollingDirection` (`X`/`Y`/`XY`), `ScrollBarImageColor3`/`Transparency`, `TopImage`/`MidImage`/`BottomImage`.
- `VerticalScrollBarInset`/`HorizontalScrollBarInset` → `Enum.ScrollBarInset`: `None`(bar overlaps content),`Always`/`ScrollBar`(content inset by thickness). `VerticalScrollBarPosition`: `Left`/`Right`.
- `ElasticBehavior` → `WhenScrollable`(default)/`Always`/`Never` (touch drag-past + spring-back).

## TextBox (input)
`Text`, `PlaceholderText`, `PlaceholderColor3`, `ClearTextOnFocus` (default true), `MultiLine`, `TextEditable`, `CursorPosition`, `SelectionStart`.
Events/methods: `FocusLost(enterPressed: bool, inputObject)` (✓ primary submit hook), `Focused`, `ReturnPressedFromOnScreenKeyboard`, `:CaptureFocus()` (opens mobile keyboard), `:ReleaseFocus(submitted?)`, `:IsFocused()`. React live: `GetPropertyChangedSignal("Text")`.

```lua
textBox.FocusLost:Connect(function(enterPressed)
    if enterPressed then submit(textBox.Text) end
end)
```

## Text Filtering (REQUIRED for user text shown to others)
✗ Never display raw user text to other players — Roblox **removes experiences lacking filtering**.
- **Server-side only**: `TextService:FilterStringAsync(text, fromUserId)` → `TextFilterResult`.
- Then `result:GetNonChatStringForBroadcastAsync()` (all users) or `:GetNonChatStringForUserAsync(userId)` (one user).
- ⚠ Wrap in `pcall` (yields/errors). ⚠ Filter **after** submit, not per-keystroke. Client `FocusLost`→`RemoteEvent:FireServer`→server filters. Also filter stored text (pet/place names) on retrieval.

## ViewportFrame (3D in UI)
Assign `CurrentCamera` (new `Instance.new("Camera")` parented inside it). Parent 3D objects directly inside, or under a child `WorldModel` (needed for Humanoid/animation/physics). Objects are NOT in real Workspace. Move the **camera** to update view. Lighting: `Ambient`, `LightColor`, `LightDirection`, `ImageColor3`, `ImageTransparency`. Reflections: add `Sky` child; parts need `Reflectance`/Glass/Foil or MeshPart `SurfaceAppearance.MetalnessMap`.

## Tweening UI (TweenService)
```lua
local TweenService = game:GetService("TweenService")
local info = TweenInfo.new(time, easingStyle, easingDirection, repeatCount, reverses, delayTime)
local tween = TweenService:Create(obj, info, {Position = UDim2.fromScale(0.5,0.5), Rotation = 45})
tween:Play()  -- also :Pause(), :Cancel()
tween.Completed:Connect(function() ... end)  -- chain sequences
```
`TweenInfo.new(time, easingStyle=Quad, easingDirection=Out, repeatCount=0, reverses=false, delayTime=0)`. repeatCount<0 = infinite.
- `EasingStyle`: `Linear`,`Sine`,`Quad`,`Cubic`,`Quart`,`Quint`,`Exponential`,`Circular`,`Back`(overshoot),`Bounce`,`Elastic`.
- `EasingDirection`: `In`,`Out`,`InOut`.
- Tween targets: `Position`/`Size` (use scale UDim2 + `AnchorPoint(0.5,0.5)`), `Rotation`, transparency (`BackgroundTransparency`/`TextTransparency`/`ImageTransparency`, or `CanvasGroup.GroupTransparency` for whole-object fade), colors, `UIScale.Scale`, `UIStroke` props.

## Input Handling for UI

### Buttons (GuiButton: TextButton/ImageButton)
- ✓ **`Activated(inputObject, clickCount)`** — input-agnostic; fires on click, tap, AND gamepad confirm (ButtonA). Use for cross-platform.
- ✗ `MouseButton1Click`/`Down`/`Up`, `MouseButton2*` — mouse-only, no gamepad/touch.
- Hover (mouse-only): `MouseEnter`, `MouseLeave`, `MouseMoved`.
- `AutoButtonColor` (default true) — auto darken on hover/press; disable for custom states.
- `Modal` (bool) — frees the locked mouse while button visible (for in-gameplay menus).
- ImageButton state swap (no code): `HoverImage`, `PressedImage`.

### UserInputService (UIS, client)
- `InputBegan`/`InputChanged`/`InputEnded` fire `(inputObject, gameProcessedEvent)`.
- ⚠ **CRITICAL**: `if gameProcessedEvent then return end` — `true` means a GuiObject/engine already consumed it; prevents UI clicks double-firing world actions.
- `InputObject`: `.UserInputType`, `.KeyCode`(+`.Name`), `.Position`(Vector3 px; thumbstick -1..1), `.Delta`, `.UserInputState`.
- Device caps: `TouchEnabled` (⚠ true on touch laptops — NOT a mobile check), `KeyboardEnabled`, `MouseEnabled`, `GamepadEnabled`.
- ✓ **`PreferredInput`** → `Enum.PreferredInput`: `Touch`,`KeyboardAndMouse`,`Gamepad` — best for layout decisions. Listen via `GetPropertyChangedSignal("PreferredInput")`.
- ⚠ `GetLastInputType()`/`LastInputTypeChanged` thrash/flicker — prefer PreferredInput.
- Cursor: `MouseIcon`, `MouseIconEnabled`, `MouseBehavior` (`Default`/`LockCenter`/`LockCurrentPosition`).

### Gamepad / console GUI navigation (GuiService)
- ✓ `GuiService.SelectedObject` = a GuiObject → starts controller focus (set `nil` to disable). `GuiService:Select(container)` selects first selectable descendant.
- `GuiObject.Selectable` (bool) — can receive selection. `NextSelectionUp/Down/Left/Right` → explicit nav targets (else auto by spatial layout). `SelectionImageObject` → custom highlight. `SelectionOrder`. Events: `SelectionGained`/`SelectionLost`.
- Default: ButtonA activates selected button (fires `Activated`), ButtonB = back. Thumbstick1 + DPad move.
- Sources `Enum.UserInputType.Gamepad1`–`Gamepad8`. Buttons: `ButtonA`(confirm),`ButtonB`(cancel),`ButtonX`,`ButtonY`,`ButtonL1/R1/L2/R2/L3/R3`,`DPadUp/Down/Left/Right`,`ButtonStart`,`ButtonSelect`,`Thumbstick1`/`Thumbstick2`.

### ContextActionService (CAS) — cross-platform actions + auto touch buttons
- `CAS:BindAction(name, handler, createTouchButton: bool, ...inputs)` — inputs = KeyCodes/UserInputTypes; createTouchButton auto-makes an on-screen button on touch devices.
- `BindActionAtPriority(name, handler, createTouchButton, priority, ...inputs)`, `UnbindAction(name)`.
- Handler: `(actionName, inputState: Enum.UserInputState, inputObject)` → return `Enum.ContextActionResult.Sink` (consume) or `.Pass`.
- Touch button styling (only if createTouchButton=true): `SetTitle`, `SetImage`, `SetPosition(UDim2)`, `GetButton(name)`→ImageButton.

### Touch gestures (UIS)
`TouchTap`,`TouchTapInWorld`,`TouchLongPress`,`TouchPan`,`TouchPinch`,`TouchRotate`,`TouchSwipe`,`TouchStarted/Moved/Ended` — all pass `gameProcessedEvent`; check it.

### Input Action System (newer, edit-time, preferred for cross-platform)
Instances in `ReplicatedStorage` (e.g. folder "Inputs"). `RunContext.Client`.
- `InputContext`: `.Enabled` (toggle group), `.Priority`, `.Sink` (consume bound inputs at priority, block lower contexts incl. PlayerScripts — for menus).
- `InputAction`: `.Type` → `Enum.InputActionType`: `Bool`,`Direction1D`,`Direction2D`(Vector2),`Direction3D`,`ViewportPosition`. Events: `Pressed`/`Released` (Bool only), `StateChanged` (all), `:GetState()`. ⚠ analog/continuous: StateChanged fires once → poll `GetState()` each frame via `RunService:BindToRenderStep`.
- `InputBinding` (child of action, one per device): `.KeyCode`, `.UIButton` (link a StarterGui GuiButton for touch), composite `.Up/.Down/.Left/.Right/.Forward/.Backward`, `.Scale` (~0.01 for MouseDelta/TouchDelta), `.PressedThreshold`/`.ReleasedThreshold` (analog triggers).

## UX Best Practices
- ✓ **Hit targets**: size buttons large enough for thumbs; don't rely on padding for tap area (pad the button itself). Respect thumb/reserved zones on mobile.
- ✓ **Feedback states**: hover (MouseEnter/HoverImage), press (PressedImage/AutoButtonColor), disabled (dim + `Active=false`/`Selectable=false`), selected (SelectionImageObject for gamepad). Tween scale/color for tactile feel.
- ✓ **Avoid GuiInset overlap**: use `CoreUISafeInsets`; don't put interactive UI under the topbar.
- ✓ **Accessibility**: legible text (`UITextSizeConstraint` min ≥9), sufficient contrast, gamepad navigability (Selectable + Next* wiring), respect `PreferredInput`.
- ✓ **Performance**: minimize instance count; use `CanvasGroup` to batch-render/fade groups; **off-screen culling** — set `Visible=false` or `Enabled=false` for hidden ScreenGuis (skips render/input/update); recycle list items in long ScrollingFrames instead of thousands of instances; avoid tweening UIStroke `Thickness` on text; flex/AutomaticSize have reflow cost on resize.

## Frameworks (devs commonly use)
- **React-lua / Roact** — declarative component UI (React port). State→UI diffing.
- **Fusion** — reactive state library (`Value`, `Computed`, `Spring`/`Tween` bindings, declarative `New`).
Both reduce imperative boilerplate for complex/stateful UI; native instances still underneath.

## Common Gotchas
- ⚠ `ClipsDescendants` does NOT work if the frame or any ancestor has nonzero `Rotation`.
- ⚠ Interactive SurfaceGui/BillboardGui buttons need the Gui in `PlayerGui` (via StarterGui) + part `CanQuery=true`.
- ⚠ `RichText` must be `true` or tags render as literal text; localization strips tags.
- ⚠ `TextScaled` overrides `TextSize`; don't combine with `AutomaticSize`.
- ⚠ Layout objects override sibling Position/Size — set LayoutOrder, not Position, to order.
- ⚠ Filter user text **server-side after submit**, in `pcall`; never per-keystroke or client-side.
- ⚠ Always early-return on `gameProcessedEvent` in UIS handlers.
- ⚠ `TouchEnabled` ≠ mobile; use `PreferredInput`.
- ⚠ ScreenGui `ResetOnSpawn` persists only as a direct StarterGui child with the flag off.
