# Roblox Engine API Cheat-Sheet (generated)

Engine classes: 886 · enums: 588 · generated from API-Dump.json.

> This lists concrete member signatures for the **highest-traffic** APIs only. For any other API, use the indexes in `api/engine-api-index.txt` (one-liners for every class/enum/datatype) and WebFetch `https://create.roblox.com/docs/reference/engine/classes/<Name>.md`.

Signature legend: `.prop: Type` · `:method(args) -> Ret` · `.Event: Event(args)`. Deprecated & non-scriptable members are omitted.


## All Services (319)

`game:GetService("Name")` for any of these:

AccountService, AchievementService, ActivityHistoryEventService, AdService, AnalyticsService, 
AnimationClipProvider, AnimationFromVideoCreatorService, AnimationFromVideoCreatorStudioService, 
AnnotationsService, AppAgeSignalsService, AppLifecycleObserverService, AppRatingPromptService, 
AppStorageService, AppUpdateService, AssetCounterService, AssetDeliveryProxy, AssetImportService, 
AssetManagerService, AssetQualityService, AssetService, AudioFocusService, AvatarChatService, 
AvatarCreationService, AvatarEditorService, AvatarImportService, AvatarSettings, BadgeService, 
BrowserService, BugReporterService, BulkImportService, CSGDictionaryService, 
CacheableContentProvider, CalloutService, CaptureService, ChangeHistoryService, 
ChangeHistoryStreamingService, Chat, CloudCRUDService, CloudExecutionService, ClusterPacketCache, 
CollaboratorsService, CollectionService, CommerceService, ConfigService, ConfigureServerService, 
ConnectivityService, ContentProvider, ContextActionService, ControllerService, CookiesService, 
CoreGui, CoreGuiConfiguration, CorePackages, CoreScriptDebuggingManagerHelper, 
CoreScriptSyncService, CreationDBService, CreatorStoreService, CrossDMScriptChangeListener, 
DataModelPatchService, DataStoreService, Debris, DebugSettings, DebuggablePluginWatcher, 
DebuggerConnectionManager, DebuggerManager, DebuggerUIService, DeferredAssetManagerService, 
DesignFoundationsService, DeviceIdService, DraftsService, DraggerService, EditableService, 
EncodingService, EventIngestService, ExampleV2Service, ExperienceAuthService, 
ExperienceNotificationService, ExperienceService, ExperienceStateCaptureService, 
ExperienceStateRecordingService, ExplorerServiceVisibilityService, FaceAnimatorService, 
FacialAgeEstimationService, FacialAnimationRecordingService, FacialAnimationStreamingServiceV2, 
FeatureRestrictionManager, FileManagerService, FileSyncReplicationService, FlagStandService, 
FlyweightService, FriendService, GamePassService, GameSettings, GamepadService, GenerationService, 
GenericChallengeService, Geometry, GeometryService, GongService, GroupService, GuiService, 
GuidRegistryService, HSRDataContentProvider, HapticService, HarmonyService, HeapProfilerService, 
HeatmapQueryService, HeatmapService, HeightmapImporterService, Hopper, HttpRbxApiService, 
HttpService, ILegacyStudioBridge, IXPService, ImageScreenCaptureService, IncrementalPatchBuilder, 
InsertService, InstanceExtensionsService, InstanceFileSyncService, InternalMessagingService, 
InternalMessagingServiceVerifier, JointsService, KeyboardService, KeyframeSequenceProvider, 
LSPFileSyncService, LanguageService, LegacyStudioBridge, Lighting, LinkingService, 
LiveScriptingService, LiveSyncService, LocalStorageService, LocalizationService, LodDataService, 
LogReporterService, LogService, LoginService, LuaSettings, LuaWebService, 
LuauScriptAnalyzerService, MLModelDeliveryService, MLService, MarketplaceService, 
MatchmakingService, MaterialGenerationService, MaterialService, MemStorageService, 
MemoryStoreService, MeshContentProvider, MessageBusService, MessagingService, 
MetaBreakpointManager, MicroProfilerService, ModerationService, MouseService, NetworkClient, 
NetworkServer, NetworkSettings, NonReplicatedCSGDictionaryService, NotificationService, 
OmniRecommendationsService, OpenCloudService, PackageService, PackageUIService, Packages, 
PartyEmulatorService, PatchBundlerFileWatch, PathfindingService, PerformanceControlService, 
PermissionsService, PhysicsService, PhysicsSettings, PlaceAssetIdsService, PlaceStatsService, 
PlacesService, PlatformCloudStorageService, PlatformFriendsService, PlatformLibraries, 
PlayerDataService, PlayerEmulatorService, PlayerHydrationService, PlayerViewService, Players, 
PluginConnectionService, PluginDebugService, PluginGuiService, PluginManagementService, 
PluginPolicyService, PointsService, PolicyService, Preloaded, ProceduralBehaviorSchedulerService, 
ProcessInstancePhysicsService, ProximityPromptService, PublishService, RbxAnalyticsService, 
RecommendationService, ReflectionService, RemoteCommandService, RemoteCursorService, 
RemoteDebuggerServer, RenderSettings, ReplicatedFirst, ReplicatedStorage, 
RibbonNotificationService, RobloxPluginGuiService, RobloxReplicatedStorage, RobloxServerStorage, 
RolloutValidationService, RomarkRbxAnalyticsService, RomarkService, RtMessagingService, RunService, 
RuntimeContentService, RuntimeScriptService, SafetyService, SceneAnalysisService, 
ScriptChangeService, ScriptCloneWatcher, ScriptCloneWatcherHelper, ScriptCommitService, 
ScriptContext, ScriptDebuggerService, ScriptEditorService, ScriptProfilerService, 
ScriptRegistrationService, ScriptService, Selection, SelectionHighlightManager, 
SerializationService, ServerScriptService, ServerStorage, ServiceVisibilityService, 
SessionCheckService, SessionService, SharedTableRegistry, SlimAnimationReplicationService, 
SlimContentProvider, SlimDebugSettings, SlimReplicationService, SlimService, 
SmoothVoxelsUpgraderService, SnippetService, SocialService, SolidModelContentProvider, 
SoundService, SoundShimService, SpawnerService, StartPageService, StarterGui, StarterPack, 
StarterPlayer, StartupMessageService, Stats, StopWatchReporter, Studio, StudioAssetService, 
StudioCameraService, StudioCaptureService, StudioData, StudioDeviceEmulatorService, 
StudioDeviceSimulatorService, StudioPublishService, StudioScriptDebugEventListener, 
StudioSdkService, StudioService, StudioTestService, StudioUserService, StudioWidgetsService, 
StylingService, SystemThemeService, TaskScheduler, TeamCreateData, TeamCreatePublishService, 
TeamCreateService, Teams, TelemetryService, TeleportService, TemporaryCageMeshProvider, 
TemporaryScriptService, TestService, TextBoxService, TextChatService, TextService, 
TextureGenerationService, ThirdPartyUserService, TimerService, ToastNotificationService, 
TouchInputService, TraceRouteService, TracerService, TutorialService, TweenService, 
UGCAvatarService, UGCValidationService, UIDragDetectorService, UniqueIdLookupService, 
UnvalidatedAssetService, UserGameSettings, UserInputService, UserService, UserStorageService, 
VRService, VRStatusService, VersionControlService, VideoCaptureService, VideoScreenCaptureService, 
VideoService, VirtualInputManager, VirtualUser, VisibilityCheckDispatcher, Visit, 
VisualizationModeService, VoiceChatInternal, VoiceChatService, WebSocketService, WebViewService, 
Workspace, WrapDeformMeshProvider

## Curated class members


### Workspace  ‹WorldRoot›
```
  .AirDensity: float
  .AirTurbulenceIntensity: float
  .AllowThirdPartySales: bool
  .ClientAnimatorThrottling: ClientAnimatorThrottlingMode
  .CurrentCamera: Camera
  .DistributedGameTime: double
  .FallHeightEnabled: bool
  .FallenPartsDestroyHeight: float
  .GlobalWind: Vector3
  .Gravity: float
  .InsertPoint: Vector3
  .Retargeting: AnimatorRetargetingMode
  .StreamingEnabled: bool
  .Terrain: Terrain
  :GetNumAwakeParts() -> int
  :GetPhysicsThrottling() -> int
  :GetRealPhysicsFPS() -> double
  :GetServerTimeNow() -> double
  :JoinToOutsiders(objects: Instances, jointType: JointCreationMode) -> null
  :PGSIsEnabled() -> bool
  :UnjoinFromOutsiders(objects: Instances) -> null
  .PersistentLoaded: Event(player: Player)
```

### Players  ‹Instance›
```
  .BubbleChat: bool
  .CharacterAutoLoads: bool
  .ClassicChat: bool
  .LocalPlayer: Player
  .MaxPlayers: int
  .PreferredPlayers: int
  .RespawnTime: float
  :BanAsync(config: Dictionary) -> null
  :CreateHumanoidModelFromDescriptionAsync(description: HumanoidDescription, rigType: HumanoidRigType, assetTypeVerification: AssetTypeVerification) -> Model
  :CreateHumanoidModelFromUserIdAsync(userId: User) -> Model
  :GetBanHistoryAsync(userId: User) -> BanHistoryPages
  :GetCharacterAppearanceInfoAsync(userId: User) -> Dictionary
  :GetFriendsAsync(userId: User) -> FriendPages
  :GetHumanoidDescriptionFromOutfitIdAsync(outfitId: int64) -> HumanoidDescription
  :GetHumanoidDescriptionFromUserIdAsync(userId: User) -> HumanoidDescription
  :GetNameFromUserIdAsync(userId: User) -> string
  :GetPlayerByUserId(userId: User) -> Player
  :GetPlayerFromCharacter(character: Model) -> Player
  :GetPlayers() -> Instances
  :GetUserIdFromNameAsync(userName: string) -> int64
  :GetUserThumbnailAsync(userId: User, thumbnailType: ThumbnailType, thumbnailSize: ThumbnailSize) -> Tuple
  :UnbanAsync(config: Dictionary) -> null
  .PlayerAdded: Event(player: Player)
  .PlayerMembershipChanged: Event(player: Player)
  .PlayerRemoving: Event(player: Player, reason: PlayerExitReason)
  .UserSubscriptionStatusChanged: Event(user: Player, subscriptionId: string)
```

### Player  ‹Instance›
```
  .AccountAge: int
  .AutoJumpEnabled: bool
  .CameraMaxZoomDistance: float
  .CameraMinZoomDistance: float
  .CameraMode: CameraMode
  .CanLoadCharacterAppearance: bool
  .Character: Model
  .CharacterAppearanceId: int64
  .DevCameraOcclusionMode: DevCameraOcclusionMode
  .DevComputerCameraMode: DevComputerCameraMovementMode
  .DevComputerMovementMode: DevComputerMovementMode
  .DevEnableMouseLock: bool
  .DevTouchCameraMode: DevTouchCameraMovementMode
  .DevTouchMovementMode: DevTouchMovementMode
  .DisplayName: string
  .FollowUserId: int64
  .GameplayPaused: bool
  .HasRobloxSubscription: bool
  .HasVerifiedBadge: bool
  .HealthDisplayDistance: float
  .LocaleId: string
  .MembershipType: MembershipType
  .NameDisplayDistance: float
  .Neutral: bool
  .PartyId: string
  .ReplicationFocus: Instance
  .RespawnLocation: SpawnLocation
  .Team: Team
  .TeamColor: BrickColor
  .User: User
  .UserId: int64
  :AddReplicationFocus(part: BasePart) -> null
  :ClearCachedAvatarAppearance() -> null
  :ClearCharacterAppearance() -> null
  :DistanceFromCharacter(point: Vector3) -> float
  :GetData() -> PlayerData
  :GetFriendsOnlineAsync(maxFriends: int) -> Array
  :GetFriendsWhoPlayedAsync() -> Array
  :GetJoinData() -> Dictionary
  :GetMouse() -> Mouse
  :GetNetworkPing() -> float
  :HasAppearanceLoaded() -> bool
  :IsFriendsWithAsync(userId: User) -> bool
  :IsInGroupAsync(groupId: int64) -> bool
  :IsVerified() -> bool
  :Kick(message: string) -> null
  :LoadCharacterAsync() -> null
  :LoadCharacterWithHumanoidDescriptionAsync(humanoidDescription: HumanoidDescription, assetTypeVerification: AssetTypeVerification) -> null
  :Move(walkDirection: Vector3, relativeToCamera: bool) -> null
  :RemoveReplicationFocus(part: BasePart) -> null
  :RequestStreamAroundAsync(position: Vector3, timeOut: double) -> null
  .CharacterAdded: Event(character: Model)
  .CharacterAppearanceLoaded: Event(character: Model)
  .CharacterRemoving: Event(character: Model)
  .Chatted: Event(message: string, recipient: Player)
  .Idled: Event(time: double)
  .OnTeleport: Event(teleportState: TeleportState, placeId: int64, spawnName: string)
```

### ReplicatedStorage  ‹Instance›
_(inherits all members from superclass)_

### ServerStorage  ‹Instance›
_(inherits all members from superclass)_

### ServerScriptService  ‹Instance›
_(inherits all members from superclass)_

### StarterGui  ‹BasePlayerGui›
```
  .ScreenOrientation: ScreenOrientation
  .ShowDevelopmentGui: bool
  :GetCore(parameterName: string) -> Variant
  :GetCoreGuiEnabled(coreGuiType: CoreGuiType) -> bool
  :SetCore(parameterName: string, value: Variant) -> null
  :SetCoreGuiEnabled(coreGuiType: CoreGuiType, enabled: bool) -> null
```

### StarterPack  ‹Instance›
_(inherits all members from superclass)_

### StarterPlayer  ‹Instance›
```
  .AllowCustomAnimations: bool
  .AutoJumpEnabled: bool
  .CameraMaxZoomDistance: float
  .CameraMinZoomDistance: float
  .CameraMode: CameraMode
  .CharacterBreakJointsOnDeath: bool
  .CharacterJumpHeight: float
  .CharacterJumpPower: float
  .CharacterMaxSlopeAngle: float
  .CharacterUseJumpPower: bool
  .CharacterWalkSpeed: float
  .ClassicDeath: bool
  .DevCameraOcclusionMode: DevCameraOcclusionMode
  .DevComputerCameraMovementMode: DevComputerCameraMovementMode
  .DevComputerMovementMode: DevComputerMovementMode
  .DevTouchCameraMovementMode: DevTouchCameraMovementMode
  .DevTouchMovementMode: DevTouchMovementMode
  .EnableMouseLockOption: bool
  .HealthDisplayDistance: float
  .LoadCharacterAppearance: bool
  .LuaCharacterController: CharacterControlMode
  .NameDisplayDistance: float
  .UserEmotesEnabled: bool
```

### Lighting  ‹Instance›
```
  .Ambient: Color3
  .Brightness: float
  .ClockTime: float
  .ColorShift_Bottom: Color3
  .ColorShift_Top: Color3
  .EnvironmentDiffuseScale: float
  .EnvironmentSpecularScale: float
  .ExposureCompensation: float
  .FogColor: Color3
  .FogEnd: float
  .FogStart: float
  .GeographicLatitude: float
  .GlobalShadows: bool
  .LightingStyle: LightingStyle
  .OutdoorAmbient: Color3
  .PrioritizeLightingQuality: bool
  .ShadowSoftness: float
  .TimeOfDay: string
  :GetMinutesAfterMidnight() -> double
  :GetMoonDirection() -> Vector3
  :GetMoonPhase() -> float
  :GetSunDirection() -> Vector3
  :SetMinutesAfterMidnight(minutes: double) -> null
  .LightingChanged: Event(skyChanged: bool)
```

### SoundService  ‹Instance›
```
  .AcousticSimulationEnabled: bool
  .AmbientReverb: ReverbType
  .CharacterSoundsUseNewApi: RolloutState
  .DistanceFactor: float
  .DopplerScale: float
  .RespectFilteringEnabled: bool
  .RolloffScale: float
  :GetListener() -> Tuple
  :GetMixerTime() -> double
  :PlayLocalSound(sound: Instance) -> null
  :SetInputDevice(nameOrInstance: Variant, guidOrPin: string) -> null
  :SetListener(listenerType: ListenerType, listener: Tuple) -> null
```

### RunService  ‹Instance›
```
  .FrameNumber: int64
  :BindToRenderStep(name: string, priority: int, function: Function) -> null
  :BindToSimulation(function: Function, frequency: StepFrequency, priority: int) -> RBXScriptConnection
  :GetPredictionStatus(context: Instance) -> PredictionStatus
  :IsClient() -> bool
  :IsResimulating() -> bool
  :IsRunMode() -> bool
  :IsRunning() -> bool
  :IsServer() -> bool
  :IsStudio() -> bool
  :SetPredictionMode(context: Instance, mode: PredictionMode) -> null
  :UnbindFromRenderStep(name: string) -> null
  .Heartbeat: Event(deltaTime: double)
  .Misprediction: Event(time: double, instances: Array, stats: Dictionary)
  .PostSimulation: Event(deltaTimeSim: double)
  .PreAnimation: Event(deltaTimeSim: double)
  .PreRender: Event(deltaTimeRender: double)
  .PreSimulation: Event(deltaTimeSim: double)
  .RenderStepped: Event(deltaTime: double)
  .Rollback: Event(time: double)
  .Stepped: Event(time: double, deltaTime: double)
```

### UserInputService  ‹Instance›
```
  .AccelerometerEnabled: bool
  .GamepadEnabled: bool
  .GyroscopeEnabled: bool
  .KeyboardEnabled: bool
  .MouseBehavior: MouseBehavior
  .MouseDeltaSensitivity: float
  .MouseEnabled: bool
  .MouseIcon: ContentId
  .MouseIconContent: Content
  .MouseIconEnabled: bool
  .OnScreenKeyboardPosition: Vector2
  .OnScreenKeyboardSize: Vector2
  .OnScreenKeyboardVisible: bool
  .PreferredInput: PreferredInput
  .TouchEnabled: bool
  .VREnabled: bool
  :CreateVirtualInput() -> Object
  :GamepadSupports(gamepadNum: UserInputType, gamepadKeyCode: KeyCode) -> bool
  :GetConnectedGamepads() -> Array
  :GetDeviceAcceleration() -> InputObject
  :GetDeviceGravity() -> InputObject
  :GetDeviceRotation() -> Tuple
  :GetFocusedTextBox() -> TextBox
  :GetGamepadConnected(gamepadNum: UserInputType) -> bool
  :GetGamepadState(gamepadNum: UserInputType) -> Instances
  :GetImageForKeyCode(keyCode: KeyCode) -> ContentId
  :GetKeysPressed() -> Instances
  :GetLastInputType() -> UserInputType
  :GetMouseButtonsPressed() -> Instances
  :GetMouseDelta() -> Vector2
  :GetMouseLocation() -> Vector2
  :GetNavigationGamepads() -> Array
  :GetStringForKeyCode(keyCode: KeyCode) -> string
  :GetSupportedGamepadKeyCodes(gamepadNum: UserInputType) -> Array
  :IsGamepadButtonDown(gamepadNum: UserInputType, gamepadKeyCode: KeyCode) -> bool
  :IsKeyDown(keyCode: KeyCode) -> bool
  :IsMouseButtonPressed(mouseButton: UserInputType) -> bool
  :IsNavigationGamepad(gamepadEnum: UserInputType) -> bool
  :RecenterUserHeadCFrame() -> null
  :SetNavigationGamepad(gamepadEnum: UserInputType, enabled: bool) -> null
  .DeviceAccelerationChanged: Event(acceleration: InputObject)
  .DeviceGravityChanged: Event(gravity: InputObject)
  .DeviceRotationChanged: Event(rotation: InputObject, cframe: CFrame)
  .GamepadConnected: Event(gamepadNum: UserInputType)
  .GamepadDisconnected: Event(gamepadNum: UserInputType)
  .InputBegan: Event(input: InputObject, gameProcessedEvent: bool)
  .InputChanged: Event(input: InputObject, gameProcessedEvent: bool)
  .InputEnded: Event(input: InputObject, gameProcessedEvent: bool)
  .JumpRequest: Event()
  .LastInputTypeChanged: Event(lastInputType: UserInputType)
  .PointerAction: Event(wheel: float, pan: Vector2, pinch: float, gameProcessedEvent: bool)
  .TextBoxFocusReleased: Event(textboxReleased: TextBox)
  .TextBoxFocused: Event(textboxFocused: TextBox)
  .TouchDrag: Event(dragDirection: SwipeDirection, numberOfTouches: int, gameProcessedEvent: bool)
  .TouchEnded: Event(touch: InputObject, gameProcessedEvent: bool)
  .TouchLongPress: Event(touchPositions: Array, state: UserInputState, gameProcessedEvent: bool)
  .TouchMoved: Event(touch: InputObject, gameProcessedEvent: bool)
  .TouchPan: Event(touchPositions: Array, totalTranslation: Vector2, velocity: Vector2, state: UserInputState, gameProcessedEvent: bool)
  .TouchPinch: Event(touchPositions: Array, scale: float, velocity: float, state: UserInputState, gameProcessedEvent: bool)
  .TouchRotate: Event(touchPositions: Array, rotation: float, velocity: float, state: UserInputState, gameProcessedEvent: bool)
  .TouchStarted: Event(touch: InputObject, gameProcessedEvent: bool)
  .TouchSwipe: Event(swipeDirection: SwipeDirection, numberOfTouches: int, gameProcessedEvent: bool)
  .TouchTap: Event(touchPositions: Array, gameProcessedEvent: bool)
  .TouchTapInWorld: Event(position: Vector2, processedByUI: bool)
  .WindowFocusReleased: Event()
  .WindowFocused: Event()
```

### ContextActionService  ‹Instance›
```
  :BindAction(actionName: string, functionToBind: Function, createTouchButton: bool, inputTypes: Tuple) -> null
  :BindActionAtPriority(actionName: string, functionToBind: Function, createTouchButton: bool, priorityLevel: int, inputTypes: Tuple) -> null
  :BindActivate(userInputTypeForActivation: UserInputType, keyCodesForActivation: Tuple) -> null
  :GetAllBoundActionInfo() -> Dictionary
  :GetBoundActionInfo(actionName: string) -> Dictionary
  :GetButton(actionName: string) -> Instance
  :GetCurrentLocalToolIcon() -> string
  :SetDescription(actionName: string, description: string) -> null
  :SetImage(actionName: string, image: string) -> null
  :SetPosition(actionName: string, position: UDim2) -> null
  :SetTitle(actionName: string, title: string) -> null
  :UnbindAction(actionName: string) -> null
  :UnbindActivate(userInputTypeForActivation: UserInputType, keyCodeForActivation: KeyCode) -> null
  :UnbindAllActions() -> null
  .LocalToolEquipped: Event(toolEquipped: Instance)
  .LocalToolUnequipped: Event(toolUnequipped: Instance)
```

### TweenService  ‹Instance›
```
  :Create(instance: Instance, tweenInfo: TweenInfo, propertyTable: Dictionary) -> Tween
  :GetValue(alpha: float, easingStyle: EasingStyle, easingDirection: EasingDirection) -> float
  :SmoothDamp(current: Variant, target: Variant, velocity: Variant, smoothTime: float, maxSpeed: float?, dt: float?) -> ()
```

### Debris  ‹Instance›
```
  :AddItem(item: Instance, lifetime: double) -> null
```

### CollectionService  ‹Instance›
```
  :AddTag(instance: Instance, tag: string) -> null
  :GetAllTags() -> Array
  :GetInstanceAddedSignal(tag: string) -> RBXScriptSignal
  :GetInstanceRemovedSignal(tag: string) -> RBXScriptSignal
  :GetTagged(tag: string) -> Instances
  :GetTags(instance: Instance) -> Array
  :HasTag(instance: Instance, tag: string) -> bool
  :RemoveTag(instance: Instance, tag: string) -> null
  .TagAdded: Event(tag: string)
  .TagRemoved: Event(tag: string)
```

### PhysicsService  ‹Instance›
```
  :CollisionGroupSetCollidable(name1: string, name2: string, collidable: bool) -> null
  :CollisionGroupsAreCollidable(name1: string, name2: string) -> bool
  :GetMaxCollisionGroups() -> int
  :GetRegisteredCollisionGroups() -> Array
  :IsCollisionGroupRegistered(name: string) -> bool
  :RegisterCollisionGroup(name: string) -> null
  :RenameCollisionGroup(from: string, to: string) -> null
  :UnregisterCollisionGroup(name: string) -> null
```

### TeleportService  ‹Instance›
```
  :GetArrivingTeleportGui() -> Instance
  :GetLocalPlayerTeleportData() -> Variant
  :GetPlayerPlaceInstanceAsync(userId: User) -> Tuple
  :GetTeleportSetting(setting: string) -> Variant
  :PromptExperienceDetailsAsync(player: Player, universeId: int64) -> PromptExperienceDetailsResult
  :ReserveServerAsync(placeId: int64) -> Tuple
  :SetTeleportGui(gui: Instance) -> null
  :SetTeleportSetting(setting: string, value: Variant) -> null
  :Teleport(placeId: int64, player: Instance, teleportData: Variant, customLoadingScreen: Instance) -> null
  :TeleportAsync(placeId: int64, players: Instances, teleportOptions: Instance) -> Instance
  :TeleportPartyAsync(placeId: int64, players: Instances, teleportData: Variant, customLoadingScreen: Instance) -> string
  :TeleportToPlaceInstance(placeId: int64, instanceId: string, player: Instance, spawnName: string, teleportData: Variant, customLoadingScreen: Instance) -> null
  :TeleportToPrivateServer(placeId: int64, reservedServerAccessCode: string, players: Instances, spawnName: string, teleportData: Variant, customLoadingScreen: Instance) -> null
  :TeleportToSpawnByName(placeId: int64, spawnName: string, player: Instance, teleportData: Variant, customLoadingScreen: Instance) -> null
  .LocalPlayerArrivedFromTeleport: Event(loadingGui: Instance, dataTable: Variant)
  .TeleportInitFailed: Event(player: Instance, teleportResult: TeleportResult, errorMessage: string, placeId: int64, teleportOptions: Instance)
```

### DataStoreService  ‹Instance›
```
  :GetDataStore(name: string, scope: string, options: Instance) -> DataStore
  :GetGlobalDataStore() -> DataStore
  :GetOrderedDataStore(name: string, scope: string) -> OrderedDataStore
  :GetRequestBudgetForRequestType(requestType: DataStoreRequestType) -> int
  :ListDataStoresAsync(prefix: string, pageSize: int, cursor: string) -> DataStoreListingPages
  :SetRateLimitForRequestType(requestType: DataStoreRequestType, baseLimit: int, perPlayerLimit: int) -> null
```

### MemoryStoreService  ‹Instance›
```
  :GetHashMap(name: string) -> MemoryStoreHashMap
  :GetQueue(name: string, invisibilityTimeout: int) -> MemoryStoreQueue
  :GetSortedMap(name: string) -> MemoryStoreSortedMap
```

### MessagingService  ‹Instance›
```
  :PublishAsync(topic: string, message: Variant) -> null
  :SubscribeAsync(topic: string, callback: Function) -> RBXScriptConnection
```

### HttpService  ‹Instance›
```
  .HttpEnabled: bool
  :CreateWebStreamClient(streamClientType: WebStreamClientType, requestOptions: Dictionary) -> WebStreamClient
  :GenerateGUID(wrapInCurlyBraces: bool) -> string
  :GetAsync(url: Variant, nocache: bool, headers: Variant) -> string
  :GetSecret(key: string) -> Secret
  :JSONDecode(input: string) -> Variant
  :JSONEncode(input: Variant) -> string
  :PostAsync(url: Variant, data: string, content_type: HttpContentType, compress: bool, headers: Variant) -> string
  :RequestAsync(requestOptions: Dictionary) -> Dictionary
  :UrlEncode(input: string) -> string
```

### MarketplaceService  ‹Instance›
```
  :BindReceiptHandler(transactionType: ReceiptType, handler: Function, filter: Array?) -> RBXScriptConnection
  :GetDeveloperProductsAsync() -> Instance
  :GetProductInfoAsync(assetId: int64, infoType: InfoType) -> Dictionary
  :GetRobloxSubscriptionDetailsAsync(user: Player) -> Dictionary
  :GetSubscriptionProductInfoAsync(subscriptionId: string) -> Dictionary
  :GetUserSubscriptionDetailsAsync(user: Player, subscriptionId: string) -> Dictionary
  :GetUserSubscriptionPaymentHistoryAsync(user: Player, subscriptionId: string) -> Array
  :GetUserSubscriptionStatusAsync(user: Player, subscriptionId: string) -> Dictionary
  :GetUsersPriceLevelsAsync(userIds: Array) -> Array
  :OpenShop(player: Player) -> null
  :PlayerOwnsAssetAsync(player: Instance, assetId: int64) -> bool
  :PlayerOwnsBundleAsync(player: Player, bundleId: int64) -> bool
  :PromptBulkPurchase(player: Player, lineItems: Array, options: Dictionary) -> null
  :PromptBundlePurchase(player: Instance, bundleId: int64) -> null
  :PromptCancelSubscription(user: Player, subscriptionId: string) -> null
  :PromptGamePassPurchase(player: Instance, gamePassId: int64) -> null
  :PromptProductPurchase(player: Instance, productId: int64, equipIfPurchased: bool, currencyType: CurrencyType) -> null
  :PromptPurchase(player: Instance, assetId: int64, equipIfPurchased: bool, currencyType: CurrencyType) -> null
  :PromptRobloxSubscriptionPurchase(user: Player) -> null
  :PromptRobuxTransferAsync(sender: Player, receiverUserId: int64, amount: int64) -> string
  :PromptSubscriptionPurchase(user: Player, subscriptionId: string) -> null
  :RankProductsAsync(productIdentifiers: Array) -> Array
  :RecommendTopProductsAsync(infoTypes: Array) -> Array
  :UserOwnsGamePassAsync(userId: User, gamePassId: int64) -> bool
  .PromptBulkPurchaseFinished: Event(player: Instance, status: MarketplaceBulkPurchasePromptStatus, results: Dictionary)
  .PromptBundlePurchaseFinished: Event(player: Instance, bundleId: int64, wasPurchased: bool)
  .PromptGamePassPurchaseFinished: Event(player: Instance, gamePassId: int64, wasPurchased: bool)
  .PromptPremiumPurchaseFinished: Event()
  .PromptProductPurchaseFinished: Event(userId: int64, productId: int64, isPurchased: bool)
  .PromptPurchaseFinished: Event(player: Instance, assetId: int64, isPurchased: bool)
  .PromptRobloxSubscriptionPurchaseFinished: Event(user: Player, didTryPurchasing: bool)
  .PromptSubscriptionPurchaseFinished: Event(user: Player, subscriptionId: string, didTryPurchasing: bool)
  .ProcessReceipt: Callback
```

### BadgeService  ‹Instance›
```
  :AwardBadgeAsync(userId: User, badgeId: int64) -> bool
  :CheckUserBadgesAsync(userId: User, badgeIds: Array) -> Array
  :GetBadgeInfoAsync(badgeId: int64) -> Dictionary
  :UserHasBadgeAsync(userId: User, badgeId: int64) -> bool
```

### GamePassService  ‹Instance›
_(inherits all members from superclass)_

### PathfindingService  ‹Instance›
```
  :CreatePath(agentParameters: Dictionary) -> Path
  :FindPathAsync(start: Vector3, finish: Vector3) -> Path
```

### Teams  ‹Instance›
```
  :GetTeams() -> Instances
```

### Chat  ‹Instance›
```
  .BubbleChatEnabled: bool
  .LoadDefaultChat: bool
  :CanUserChatAsync(userId: int64) -> bool
  :CanUsersChatAsync(userIdFrom: int64, userIdTo: int64) -> bool
  :Chat(partOrCharacter: Instance, message: string, color: ChatColor) -> null
  :FilterStringAsync(stringToFilter: string, playerFrom: Player, playerTo: Player) -> string
  :FilterStringForBroadcast(stringToFilter: string, playerFrom: Player) -> string
  :InvokeChatCallback(callbackType: ChatCallbackType, callbackArguments: Tuple) -> Tuple
  :RegisterChatCallback(callbackType: ChatCallbackType, callbackFunction: Function) -> null
  :SetBubbleChatSettings(settings: Variant) -> null
  .Chatted: Event(part: Instance, message: string, color: ChatColor)
```

### TextChatService  ‹Instance›
```
  .ChatTranslationEnabled: bool
  .ChatVersion: ChatVersion
  .CreateDefaultCommands: bool
  .CreateDefaultTextChannels: bool
  :CanUserChatAsync(userId: User) -> bool
  :CanUsersChatAsync(userIdFrom: User, userIdTo: User) -> bool
  :CanUsersDirectChatAsync(requesterUserId: User, userIds: Array) -> Array
  :DisplayBubble(partOrCharacter: Instance, message: string) -> null
  :GetChatGroupsAsync(players: Instances) -> Array
  .BubbleDisplayed: Event(partOrCharacter: Instance, textChatMessage: TextChatMessage)
  .MessageReceived: Event(textChatMessage: TextChatMessage)
  .SendingMessage: Event(textChatMessage: TextChatMessage)
  .OnBubbleAdded: Callback
  .OnChatWindowAdded: Callback
  .OnIncomingMessage: Callback
```

### ProximityPromptService  ‹Instance›
```
  .Enabled: bool
  .MaxIndicatorsVisible: int
  .MaxPromptsVisible: int
  .IndicatorHidden: Event(prompt: ProximityPrompt)
  .IndicatorShown: Event(prompt: ProximityPrompt)
  .PromptButtonHoldBegan: Event(prompt: ProximityPrompt, playerWhoTriggered: Player)
  .PromptButtonHoldEnded: Event(prompt: ProximityPrompt, playerWhoTriggered: Player)
  .PromptHidden: Event(prompt: ProximityPrompt)
  .PromptShown: Event(prompt: ProximityPrompt, inputType: ProximityPromptInputType)
  .PromptTriggerEnded: Event(prompt: ProximityPrompt, playerWhoTriggered: Player)
  .PromptTriggered: Event(prompt: ProximityPrompt, playerWhoTriggered: Player)
```

### ContentProvider  ‹Instance›
```
  .BaseUrl: string
  .RequestQueueSize: int
  :GetAssetFetchStatus(contentId: ContentId) -> AssetFetchStatus
  :GetAssetFetchStatusChangedSignal(contentId: ContentId) -> RBXScriptSignal
  :ListEncryptedAssets() -> Array
  :PreloadAsync(contentIdList: Array, callbackFunction: Function) -> null
  :RegisterDefaultEncryptionKey(encryptionKey: string) -> null
  :RegisterDefaultSessionKey(sessionKey: string) -> null
  :RegisterEncryptedAsset(assetId: ContentId, encryptionKey: string) -> null
  :RegisterSessionEncryptedAsset(contentId: ContentId, sessionKey: string) -> null
  :UnregisterDefaultEncryptionKey() -> null
  :UnregisterEncryptedAsset(assetId: ContentId) -> null
  .AssetFetchFailed: Event(assetId: ContentId)
```

### ReplicatedFirst  ‹Instance›
```
  :RemoveDefaultLoadingScreen() -> null
```

### GuiService  ‹Instance›
```
  .AutoSelectGuiEnabled: bool
  .CoreGuiNavigationEnabled: bool
  .GuiNavigationEnabled: bool
  .MenuIsOpen: bool
  .PreferredTextSize: PreferredTextSize
  .PreferredTransparency: float
  .ReducedMotionEnabled: bool
  .SelectedObject: GuiObject
  .TopbarInset: Rect
  .TouchControlsEnabled: bool
  .ViewportDisplaySize: DisplaySize
  :CloseInspectMenu() -> null
  :DismissNotification(notificationId: string) -> bool
  :GetEmotesMenuOpen() -> bool
  :GetGameplayPausedNotificationEnabled() -> bool
  :GetGuiInset() -> Tuple
  :GetInsetArea(screenInsets: ScreenInsets) -> Rect
  :GetInspectMenuEnabled() -> bool
  :InspectPlayerFromHumanoidDescription(humanoidDescription: Instance, name: string) -> null
  :InspectPlayerFromUserId(userId: User) -> null
  :IsTenFootInterface() -> bool
  :Select(selectionParent: Instance) -> null
  :SendNotification(notificationInfo: Dictionary) -> string
  :SetEmotesMenuOpen(isOpen: bool) -> null
  :SetGameplayPausedNotificationEnabled(enabled: bool) -> null
  :SetInspectMenuEnabled(enabled: bool) -> null
  .MenuClosed: Event()
  .MenuOpened: Event()
```

### StarterPlayerScripts  ‹Instance›
_(inherits all members from superclass)_

### StarterCharacterScripts  ‹StarterPlayerScripts›
_(inherits all members from superclass)_

### AnalyticsService  ‹Instance›
```
  :GetDurationLoggerTimestamp() -> int
  :GetPlayerSegmentsAsync(player: Player) -> Dictionary
  :LogCustomEvent(player: Player, eventName: string, value: double, customFields: Dictionary) -> null
  :LogEconomyEvent(player: Player, flowType: AnalyticsEconomyFlowType, currencyType: string, amount: float, endingBalance: float, transactionType: string, itemSku: string, customFields: Dictionary) -> null
  :LogFunnelStepEvent(player: Player, funnelName: string, funnelSessionId: string, step: int, stepName: string, customFields: Dictionary) -> null
  :LogOnboardingFunnelStepEvent(player: Player, step: int, stepName: string, customFields: Dictionary) -> null
  :LogProgressionCompleteEvent(player: Player, progressionPathName: string, level: int, levelName: string, customFields: Dictionary) -> null
  :LogProgressionEvent(player: Player, progressionPathName: string, status: AnalyticsProgressionType, level: int, levelName: string, customFields: Dictionary) -> null
  :LogProgressionFailEvent(player: Player, progressionPathName: string, level: int, levelName: string, customFields: Dictionary) -> null
  :LogProgressionStartEvent(player: Player, progressionPathName: string, level: int, levelName: string, customFields: Dictionary) -> null
```

### PolicyService  ‹Instance›
```
  :CanViewBrandProjectAsync(player: Player, brandProjectId: string) -> bool
  :GetPolicyInfoForPlayerAsync(player: Instance) -> Dictionary
```

### GroupService  ‹Instance›
```
  :GetAlliesAsync(groupId: int64) -> StandardPages
  :GetEnemiesAsync(groupId: int64) -> StandardPages
  :GetGroupInfoAsync(groupId: int64) -> Variant
  :GetGroupsAsync(userId: User) -> Array
  :GetRolesInGroupAsync(userId: User, groupId: int64) -> Variant
  :PromptJoinAsync(groupId: int64) -> GroupMembershipStatus
```

### AssetService  ‹Instance›
```
  :ComposeDecalAsync(decal: Decal, layers: Array) -> null
  :CreateAssetAsync(object: Object, assetType: AssetType, requestParameters: Dictionary) -> Tuple
  :CreateAssetVersionAsync(object: Object, assetType: AssetType, assetId: int64, requestParameters: Dictionary) -> Tuple
  :CreateDataModelContentAsync(content: Content, options: Dictionary?) -> Tuple
  :CreateEditableImage(editableImageOptions: Dictionary?) -> EditableImage
  :CreateEditableImageAsync(content: Content, editableImageOptions: Dictionary?) -> EditableImage
  :CreateEditableMesh(editableMeshOptions: Dictionary?) -> EditableMesh
  :CreateEditableMeshAsync(content: Content, editableMeshOptions: Dictionary?) -> EditableMesh
  :CreateMeshPartAsync(meshContent: Content, options: Dictionary) -> MeshPart
  :CreatePlaceAsync(placeName: string, templatePlaceID: int64, description: string) -> int64
  :CreatePlaceInPlayerInventoryAsync(player: Instance, placeName: string, templatePlaceID: int64, description: string) -> int64
  :CreateSurfaceAppearanceAsync(content: Dictionary) -> SurfaceAppearance
  :GetAssetIdsForPackageAsync(packageAssetId: int64) -> Array
  :GetAudioMetadataAsync(idList: Array) -> Array
  :GetBundleDetailsAsync(bundleId: int64) -> Dictionary
  :GetGamePlacesAsync() -> Instance
  :LoadAssetAsync(assetId: int64) -> Instance
  :PromptCreateAssetAsync(player: Player, instance: Instance, assetType: AssetType) -> Tuple
  :PromptImportAnimationClipFromVideoAsync(player: Player, progressCallback: Function) -> Tuple
  :SavePlaceAsync(requestParameters: Dictionary?) -> null
  :SearchAudioAsync(searchParameters: AudioSearchParams) -> AudioPages
```

### TextService  ‹Instance›
```
  :FilterAndTranslateStringAsync(stringToFilter: string, fromUserId: int64, targetLocales: Array, textContext: TextFilterContext) -> TextFilterTranslatedResult
  :FilterStringAsync(stringToFilter: string, fromUserId: int64, textContext: TextFilterContext) -> TextFilterResult
  :GetFamilyInfoAsync(assetId: ContentId) -> Dictionary
  :GetTextBoundsAsync(params: GetTextBoundsParams) -> Vector2
  :GetTextSize(string: string, fontSize: int, font: Font, frameSize: Vector2) -> Vector2
  :GetTextSizeOffsetAsync(fontSize: int, font: Font) -> float
```

### LocalizationService  ‹Instance›
```
  .RobloxLocaleId: string
  .SystemLocaleId: string
  :GetCorescriptLocalizations() -> Instances
  :GetCountryRegionForPlayerAsync(player: Instance) -> string
  :GetTableEntries(instance: Instance) -> Array
  :GetTranslatorForLocaleAsync(locale: string) -> Instance
  :GetTranslatorForPlayer(player: Instance) -> Instance
  :GetTranslatorForPlayerAsync(player: Instance) -> Instance
```

### HapticService  ‹Instance›
```
  :GetMotor(inputType: UserInputType, vibrationMotor: VibrationMotor) -> Tuple
  :IsMotorSupported(inputType: UserInputType, vibrationMotor: VibrationMotor) -> bool
  :IsVibrationSupported(inputType: UserInputType) -> bool
  :SetMotor(inputType: UserInputType, vibrationMotor: VibrationMotor, vibrationValues: Tuple) -> null
```

### VRService  ‹Instance›
```
  .AutomaticScaling: VRScaling
  .AvatarGestures: bool
  .ControllerModels: VRControllerModelMode
  .FadeOutViewOnCollision: bool
  .GuiInputUserCFrame: UserCFrame
  .LaserPointer: VRLaserPointerMode
  .ThirdPersonFollowCamEnabled: bool
  .VREnabled: bool
  :GetTouchpadMode(pad: VRTouchpad) -> VRTouchpadMode
  :GetUserCFrame(type: UserCFrame) -> CFrame
  :GetUserCFrameEnabled(type: UserCFrame) -> bool
  :RecenterUserHeadCFrame() -> null
  :RequestNavigation(cframe: CFrame, inputUserCFrame: UserCFrame) -> null
  :SetTouchpadMode(pad: VRTouchpad, mode: VRTouchpadMode) -> null
  .NavigationRequested: Event(cframe: CFrame, inputUserCFrame: UserCFrame)
  .TouchpadModeChanged: Event(pad: VRTouchpad, mode: VRTouchpadMode)
  .UserCFrameChanged: Event(type: UserCFrame, value: CFrame)
  .UserCFrameEnabled: Event(type: UserCFrame, enabled: bool)
```

### Instance  ‹Object›
```
  .Archivable: bool
  .Capabilities: SecurityCapabilities
  .Name: string
  .Parent: Instance
  .Sandboxed: bool
  :AddTag(tag: string) -> null
  :ClearAllChildren() -> null
  :Clone() -> Instance
  :Destroy() -> null
  :FindFirstAncestor(name: string) -> Instance
  :FindFirstAncestorOfClass(className: string) -> Instance
  :FindFirstAncestorWhichIsA(className: string) -> Instance
  :FindFirstChild(name: string, recursive: bool) -> Instance
  :FindFirstChildOfClass(className: string) -> Instance
  :FindFirstChildWhichIsA(className: string, recursive: bool) -> Instance
  :FindFirstDescendant(name: string) -> Instance
  :GetActor() -> Actor
  :GetAttribute(attribute: string) -> Variant
  :GetAttributeChangedSignal(attribute: string) -> RBXScriptSignal
  :GetAttributes() -> Dictionary
  :GetChildren() -> Instances
  :GetDescendants() -> Instances
  :GetFullName() -> string
  :GetStyled(name: string, selector: string?) -> Variant
  :GetStyledPropertyChangedSignal(property: string) -> RBXScriptSignal
  :GetTags() -> Array
  :HasTag(tag: string) -> bool
  :IsAncestorOf(descendant: Instance) -> bool
  :IsDescendantOf(ancestor: Instance) -> bool
  :IsPropertyModified(property: string) -> bool
  :QueryDescendants(selector: string) -> Instances
  :RemoveTag(tag: string) -> null
  :ResetPropertyToDefault(property: string) -> null
  :SetAttribute(attribute: string, value: Variant) -> null
  :WaitForChild(childName: string, timeOut: double) -> Instance
  .AncestryChanged: Event(child: Instance, parent: Instance)
  .AttributeChanged: Event(attribute: string)
  .ChildAdded: Event(child: Instance)
  .ChildRemoved: Event(child: Instance)
  .DescendantAdded: Event(descendant: Instance)
  .DescendantRemoving: Event(descendant: Instance)
  .Destroying: Event()
  .StyledPropertiesChanged: Event()
```

### BasePart  ‹PVInstance›
```
  .Anchored: bool
  .AssemblyAngularVelocity: Vector3
  .AssemblyCenterOfMass: Vector3
  .AssemblyLinearVelocity: Vector3
  .AssemblyMass: float
  .AssemblyRootPart: BasePart
  .AudioCanCollide: bool
  .BackSurface: SurfaceType
  .BottomSurface: SurfaceType
  .BrickColor: BrickColor
  .CFrame: CFrame
  .CanCollide: bool
  .CanQuery: bool
  .CanTouch: bool
  .CastShadow: bool
  .CenterOfMass: Vector3
  .CollisionGroup: string
  .Color: Color3
  .CurrentPhysicalProperties: PhysicalProperties
  .CustomPhysicalProperties: PhysicalProperties
  .EnableFluidForces: bool
  .ExtentsCFrame: CFrame
  .ExtentsSize: Vector3
  .FrontSurface: SurfaceType
  .LeftSurface: SurfaceType
  .LocalTransparencyModifier: float
  .Locked: bool
  .Mass: float
  .Massless: bool
  .Material: Material
  .MaterialVariant: string
  .Orientation: Vector3
  .PivotOffset: CFrame
  .Position: Vector3
  .ReceiveAge: float
  .Reflectance: float
  .ResizeIncrement: int
  .ResizeableFaces: Faces
  .RightSurface: SurfaceType
  .RootPriority: int
  .Rotation: Vector3
  .Size: Vector3
  .TopSurface: SurfaceType
  .Transparency: float
  :AngularAccelerationToTorque(angAcceleration: Vector3, angVelocity: Vector3) -> Vector3
  :ApplyAngularImpulse(impulse: Vector3) -> null
  :ApplyImpulse(impulse: Vector3) -> null
  :ApplyImpulseAtPosition(impulse: Vector3, position: Vector3) -> null
  :CanCollideWith(part: BasePart) -> bool
  :CanSetNetworkOwnership() -> Tuple
  :GetClosestPointOnSurface(position: Vector3) -> Vector3
  :GetConnectedParts(recursive: bool) -> Instances
  :GetJoints() -> Instances
  :GetMass() -> float
  :GetNetworkOwner() -> Instance
  :GetNetworkOwnershipAuto() -> bool
  :GetNoCollisionConstraints() -> Instances
  :GetTouchingParts() -> Instances
  :GetVelocityAtPosition(position: Vector3) -> Vector3
  :IntersectAsync(parts: Instances, collisionfidelity: CollisionFidelity, renderFidelity: RenderFidelity) -> Instance
  :IsGrounded() -> bool
  :Resize(normalId: NormalId, deltaAmount: int) -> bool
  :SetNetworkOwner(playerInstance: Player) -> null
  :SetNetworkOwnershipAuto() -> null
  :SubtractAsync(parts: Instances, collisionfidelity: CollisionFidelity, renderFidelity: RenderFidelity) -> Instance
  :TorqueToAngularAcceleration(torque: Vector3, angVelocity: Vector3) -> Vector3
  :UnionAsync(parts: Instances, collisionfidelity: CollisionFidelity, renderFidelity: RenderFidelity) -> Instance
  .TouchEnded: Event(otherPart: BasePart)
  .Touched: Event(otherPart: BasePart)
```

### Part  ‹FormFactorPart›
```
  .Shape: PartType
```

### MeshPart  ‹TriangleMeshPart›
```
  .DoubleSided: bool
  .HasSkinnedMesh: bool
  .MeshContent: Content
  .MeshId: ContentId
  .RenderFidelity: RenderFidelity
  .TextureContent: Content
  .TextureID: ContentId
  :ApplyMesh(meshPart: Instance) -> null
```

### Model  ‹PVInstance›
```
  .ModelStreamingMode: ModelStreamingMode
  .PrimaryPart: BasePart
  .WorldPivot: CFrame
  :AddPersistentPlayer(playerInstance: Player) -> null
  :GetBoundingBox() -> ()
  :GetExtentsSize() -> Vector3
  :GetPersistentPlayers() -> Instances
  :GetScale() -> float
  :MoveTo(position: Vector3) -> null
  :RemovePersistentPlayer(playerInstance: Player) -> null
  :ScaleTo(newScaleFactor: float) -> null
  :TranslateBy(delta: Vector3) -> null
```

### Humanoid  ‹Instance›
```
  .AutoJumpEnabled: bool
  .AutoRotate: bool
  .AutomaticScalingEnabled: bool
  .BreakJointsOnDeath: bool
  .CameraOffset: Vector3
  .DisplayDistanceType: HumanoidDisplayDistanceType
  .DisplayName: string
  .EvaluateStateMachine: bool
  .FloorMaterial: Material
  .Health: float
  .HealthDisplayDistance: float
  .HealthDisplayType: HumanoidHealthDisplayType
  .HipHeight: float
  .Jump: bool
  .JumpHeight: float
  .JumpPower: float
  .MaxHealth: float
  .MaxSlopeAngle: float
  .MoveDirection: Vector3
  .NameDisplayDistance: float
  .NameOcclusion: NameOcclusion
  .PlatformStand: bool
  .RequiresNeck: bool
  .RigType: HumanoidRigType
  .RootPart: BasePart
  .SeatPart: BasePart
  .Sit: bool
  .TargetPoint: Vector3
  .UseJumpPower: bool
  .WalkSpeed: float
  .WalkToPart: BasePart
  .WalkToPoint: Vector3
  :AddAccessory(accessory: Instance) -> null
  :ApplyDescriptionAsync(humanoidDescription: HumanoidDescription, assetTypeVerification: AssetTypeVerification) -> null
  :ApplyDescriptionResetAsync(humanoidDescription: HumanoidDescription, assetTypeVerification: AssetTypeVerification) -> null
  :BuildRigFromAttachments() -> null
  :ChangeState(state: HumanoidStateType) -> null
  :EquipTool(tool: Instance) -> null
  :GetAccessories() -> Array
  :GetAppliedDescription() -> HumanoidDescription
  :GetBodyPartR15(part: Instance) -> BodyPartR15
  :GetLimb(part: Instance) -> Limb
  :GetMoveVelocity() -> Vector3
  :GetRelativeVelocityAtFloor() -> Vector3
  :GetState() -> HumanoidStateType
  :GetStateEnabled(state: HumanoidStateType) -> bool
  :Move(moveDirection: Vector3, relativeToCamera: bool) -> null
  :MoveTo(location: Vector3, part: Instance) -> null
  :PlayEmoteAsync(emoteName: string) -> bool
  :RemoveAccessories() -> null
  :ReplaceBodyPartR15(bodyPart: BodyPartR15, part: BasePart) -> bool
  :SetStateEnabled(state: HumanoidStateType, enabled: bool) -> null
  :TakeDamage(amount: float) -> null
  :UnequipTools() -> null
  .ApplyDescriptionFinished: Event(description: HumanoidDescription)
  .Climbing: Event(speed: float)
  .Died: Event()
  .FallingDown: Event(active: bool)
  .FreeFalling: Event(active: bool)
  .GettingUp: Event(active: bool)
  .HealthChanged: Event(health: float)
  .Jumping: Event(active: bool)
  .MoveToFinished: Event(reached: bool)
  .PlatformStanding: Event(active: bool)
  .Ragdoll: Event(active: bool)
  .Running: Event(speed: float)
  .Seated: Event(active: bool, currentSeatPart: BasePart)
  .StateChanged: Event(old: HumanoidStateType, new: HumanoidStateType)
  .StateEnabledChanged: Event(state: HumanoidStateType, isEnabled: bool)
  .Strafing: Event(active: bool)
  .Swimming: Event(speed: float)
  .Touched: Event(touchingPart: BasePart, humanoidPart: BasePart)
```

### HumanoidDescription  ‹Instance›
```
  .BackAccessory: string
  .BodyTypeScale: float
  .ClimbAnimation: int64
  .DepthScale: float
  .Face: int64
  .FaceAccessory: string
  .FallAnimation: int64
  .FrontAccessory: string
  .GraphicTShirt: int64
  .HairAccessory: string
  .HatAccessory: string
  .Head: int64
  .HeadColor: Color3
  .HeadScale: float
  .HeightScale: float
  .IdleAnimation: int64
  .JumpAnimation: int64
  .LeftArm: int64
  .LeftArmColor: Color3
  .LeftLeg: int64
  .LeftLegColor: Color3
  .MoodAnimation: int64
  .NeckAccessory: string
  .Pants: int64
  .ProportionScale: float
  .RightArm: int64
  .RightArmColor: Color3
  .RightLeg: int64
  .RightLegColor: Color3
  .RunAnimation: int64
  .Shirt: int64
  .ShouldersAccessory: string
  .StaticFacialAnimation: bool
  .SwimAnimation: int64
  .Torso: int64
  .TorsoColor: Color3
  .UseAvatarSettings: bool
  .WaistAccessory: string
  .WalkAnimation: int64
  .WidthScale: float
  :AddEmote(name: string, assetId: int64) -> null
  :GetAccessories(includeRigidAccessories: bool) -> Array
  :GetEmotes() -> Dictionary
  :GetEquippedEmotes() -> Array
  :RemoveEmote(name: string) -> null
  :SetAccessories(accessories: Array, includeRigidAccessories: bool) -> null
  :SetEmotes(emotes: Dictionary) -> null
  :SetEquippedEmotes(equippedEmotes: Array) -> null
  .EmotesChanged: Event(newEmotes: Dictionary)
  .EquippedEmotesChanged: Event(newEquippedEmotes: Array)
```

### Animator  ‹Instance›
```
  .EvaluationThrottled: bool
  .PreferLodEnabled: bool
  .RootMotion: CFrame
  .RootMotionWeight: float
  :ApplyJointVelocities(motors: Variant) -> null
  :GetPlayingAnimationTracks() -> Array
  :GetTrackByAnimationId(animationId: ContentId) -> AnimationTrack
  :LoadAnimation(animation: Animation) -> AnimationTrack
  :RegisterEvaluationParallelCallback(callback: Function) -> null
  .AnimationPlayed: Event(animationTrack: AnimationTrack)
```

### Animation  ‹Instance›
```
  .AnimationContent: Content
  .AnimationId: ContentId
```

### AnimationTrack  ‹Instance›
```
  .Animation: Animation
  .IsPlaying: bool
  .Length: float
  .Looped: bool
  .Priority: AnimationPriority
  .Speed: float
  .TimePosition: float
  .WeightCurrent: float
  .WeightTarget: float
  :AdjustSpeed(speed: float) -> null
  :AdjustWeight(weight: float, fadeTime: float) -> null
  :GetMarkerReachedSignal(name: string) -> RBXScriptSignal
  :GetParameter(key: string) -> Variant
  :GetParameterDefaults() -> Dictionary
  :GetTargetInstance(name: string) -> Instance
  :GetTargetNames() -> Array
  :GetTimeOfKeyframe(keyframeName: string) -> double
  :Play(fadeTime: float, weight: float, speed: float) -> null
  :SetParameter(key: string, value: Variant) -> null
  :SetTargetInstance(name: string, target: Instance) -> null
  :Stop(fadeTime: float) -> null
  .DidLoop: Event()
  .Ended: Event()
  .KeyframeReached: Event(keyframeName: string)
  .Stopped: Event()
```

### Tool  ‹BackpackItem›
```
  .CanBeDropped: bool
  .Enabled: bool
  .Grip: CFrame
  .GripForward: Vector3
  .GripPos: Vector3
  .GripRight: Vector3
  .GripUp: Vector3
  .ManualActivationOnly: bool
  .RequiresHandle: bool
  .ToolTip: string
  :Activate() -> null
  :Deactivate() -> null
  .Activated: Event()
  .Deactivated: Event()
  .Equipped: Event(mouse: Mouse)
  .Unequipped: Event()
```

### Accessory  ‹Accoutrement›
```
  .AccessoryType: AccessoryType
```

### Attachment  ‹Instance›
```
  .Axis: Vector3
  .CFrame: CFrame
  .Orientation: Vector3
  .Position: Vector3
  .SecondaryAxis: Vector3
  .Visible: bool
  .WorldAxis: Vector3
  .WorldCFrame: CFrame
  .WorldOrientation: Vector3
  .WorldPosition: Vector3
  .WorldSecondaryAxis: Vector3
  :GetConstraints() -> Instances
```

### Sound  ‹Instance›
```
  .AcousticSimulationEnabled: bool
  .AudioContent: Content
  .IsLoaded: bool
  .IsPaused: bool
  .IsPlaying: bool
  .LoopRegion: NumberRange
  .Looped: bool
  .PlayOnRemove: bool
  .PlaybackLoudness: double
  .PlaybackRegion: NumberRange
  .PlaybackRegionsEnabled: bool
  .PlaybackSpeed: float
  .Playing: bool
  .RollOffMaxDistance: float
  .RollOffMinDistance: float
  .RollOffMode: RollOffMode
  .SoundGroup: SoundGroup
  .SoundId: ContentId
  .TimeLength: double
  .TimePosition: double
  .Volume: float
  :Pause() -> null
  :Play() -> null
  :Resume() -> null
  :Stop() -> null
  .DidLoop: Event(soundId: string, numOfTimesLooped: int)
  .Ended: Event(soundId: string)
  .Loaded: Event(soundId: string)
  .Paused: Event(soundId: string)
  .Played: Event(soundId: string)
  .Resumed: Event(soundId: string)
  .Stopped: Event(soundId: string)
```

### ParticleEmitter  ‹Instance›
```
  .Acceleration: Vector3
  .Brightness: float
  .Color: ColorSequence
  .Drag: float
  .EmissionDirection: NormalId
  .Enabled: bool
  .FlipbookBlendFrames: bool
  .FlipbookFramerate: NumberRange
  .FlipbookIncompatible: string
  .FlipbookLayout: ParticleFlipbookLayout
  .FlipbookMode: ParticleFlipbookMode
  .FlipbookSizeX: int
  .FlipbookSizeY: int
  .FlipbookStartRandom: bool
  .Lifetime: NumberRange
  .LightEmission: float
  .LightInfluence: float
  .LocalTransparencyModifier: float
  .LockedToPart: bool
  .Orientation: ParticleOrientation
  .Rate: float
  .RotSpeed: NumberRange
  .Rotation: NumberRange
  .Shape: ParticleEmitterShape
  .ShapeInOut: ParticleEmitterShapeInOut
  .ShapePartial: float
  .ShapeStyle: ParticleEmitterShapeStyle
  .Size: NumberSequence
  .Speed: NumberRange
  .SpreadAngle: Vector2
  .Squash: NumberSequence
  .Texture: ContentId
  .TextureContent: Content
  .TimeScale: float
  .Transparency: NumberSequence
  .VelocityInheritance: float
  .WindAffectsDrag: bool
  .ZOffset: float
  :Clear() -> null
  :Emit(particleCount: int) -> null
```

### Beam  ‹Instance›
```
  .Attachment0: Attachment
  .Attachment1: Attachment
  .Brightness: float
  .Color: ColorSequence
  .CurveSize0: float
  .CurveSize1: float
  .Enabled: bool
  .FaceCamera: bool
  .LightEmission: float
  .LightInfluence: float
  .LocalTransparencyModifier: float
  .Segments: int
  .Texture: ContentId
  .TextureContent: Content
  .TextureLength: float
  .TextureMode: TextureMode
  .TextureSpeed: float
  .Transparency: NumberSequence
  .Width0: float
  .Width1: float
  .ZOffset: float
  :SetTextureOffset(offset: float) -> null
```

### Trail  ‹Instance›
```
  .Attachment0: Attachment
  .Attachment1: Attachment
  .Brightness: float
  .Color: ColorSequence
  .Enabled: bool
  .FaceCamera: bool
  .Lifetime: float
  .LightEmission: float
  .LightInfluence: float
  .LocalTransparencyModifier: float
  .MaxLength: float
  .MinLength: float
  .Texture: ContentId
  .TextureContent: Content
  .TextureLength: float
  .TextureMode: TextureMode
  .Transparency: NumberSequence
  .WidthScale: NumberSequence
  :Clear() -> null
```

### Light  ‹Instance›
```
  .Brightness: float
  .Color: Color3
  .Enabled: bool
  .Shadows: bool
```

### PointLight  ‹Light›
```
  .Range: float
```

### SpotLight  ‹Light›
```
  .Angle: float
  .Face: NormalId
  .Range: float
```

### SurfaceLight  ‹Light›
```
  .Angle: float
  .Face: NormalId
  .Range: float
```

### ProximityPrompt  ‹Instance›
```
  .ActionText: string
  .AutoLocalize: bool
  .ClickablePrompt: bool
  .Enabled: bool
  .Exclusivity: ProximityPromptExclusivity
  .GamepadKeyCode: KeyCode
  .HoldDuration: float
  .KeyboardKeyCode: KeyCode
  .MaxActivationDistance: float
  .MaxIndicatorDistance: float
  .ObjectText: string
  .RequiresLineOfSight: bool
  .RootLocalizationTable: LocalizationTable
  .Style: ProximityPromptStyle
  .UIOffset: Vector2
  :InputHoldBegin() -> null
  :InputHoldEnd() -> null
  .IndicatorHidden: Event()
  .IndicatorShown: Event()
  .PromptButtonHoldBegan: Event(playerWhoTriggered: Player)
  .PromptButtonHoldEnded: Event(playerWhoTriggered: Player)
  .PromptHidden: Event()
  .PromptShown: Event(inputType: ProximityPromptInputType)
  .TriggerEnded: Event(playerWhoTriggered: Player)
  .Triggered: Event(playerWhoTriggered: Player)
```

### ClickDetector  ‹Instance›
```
  .CursorIcon: ContentId
  .CursorIconContent: Content
  .MaxActivationDistance: float
  .MouseClick: Event(playerWhoClicked: Player)
  .MouseHoverEnter: Event(playerWhoHovered: Player)
  .MouseHoverLeave: Event(playerWhoHovered: Player)
  .RightMouseClick: Event(playerWhoClicked: Player)
```

### Camera  ‹PVInstance›
```
  .CFrame: CFrame
  .CameraSubject: Instance
  .CameraType: CameraType
  .DiagonalFieldOfView: float
  .FieldOfView: float
  .FieldOfViewMode: FieldOfViewMode
  .Focus: CFrame
  .HeadLocked: bool
  .HeadScale: float
  .MaxAxisFieldOfView: float
  .NearPlaneZ: float
  .VRTiltAndRollEnabled: bool
  .ViewportSize: Vector2
  :GetPartsObscuringTarget(castPoints: Array, ignoreList: Instances) -> Instances
  :GetRenderCFrame() -> CFrame
  :GetRoll() -> float
  :ScreenPointToRay(x: float, y: float, depth: float) -> Ray
  :SetRoll(rollAngle: float) -> null
  :ViewportPointToRay(x: float, y: float, depth: float) -> Ray
  :WorldToScreenPoint(worldPoint: Vector3) -> Tuple
  :WorldToViewportPoint(worldPoint: Vector3) -> Tuple
  :ZoomToExtents(boundingBoxCFrame: CFrame, boundingBoxSize: Vector3) -> null
  .InterpolationFinished: Event()
```

### Script  ‹BaseScript›
```
  .Source: ProtectedString
```

### LocalScript  ‹Script›
_(inherits all members from superclass)_

### ModuleScript  ‹LuaSourceContainer›
```
  .Source: ProtectedString
```

### BaseScript  ‹LuaSourceContainer›
```
  .Disabled: bool
  .Enabled: bool
  .RunContext: RunContext
```

### LuaSourceContainer  ‹Instance›
_(inherits all members from superclass)_

### RemoteEvent  ‹BaseRemoteEvent›
```
  :FireAllClients(arguments: Tuple) -> null
  :FireClient(player: Player, arguments: Tuple) -> null
  :FireServer(arguments: Tuple) -> null
  .OnClientEvent: Event(arguments: Tuple)
  .OnServerEvent: Event(player: Player, arguments: Tuple)
```

### RemoteFunction  ‹Instance›
```
  :InvokeClient(player: Player, arguments: Tuple) -> Tuple
  :InvokeServer(arguments: Tuple) -> Tuple
  .OnClientInvoke: Callback
  .OnServerInvoke: Callback
```

### BindableEvent  ‹Instance›
```
  :Fire(arguments: Tuple) -> null
  .Event: Event(arguments: Tuple)
```

### BindableFunction  ‹Instance›
```
  :Invoke(arguments: Tuple) -> Tuple
  .OnInvoke: Callback
```

### UnreliableRemoteEvent  ‹BaseRemoteEvent›
```
  :FireAllClients(arguments: Tuple) -> null
  :FireClient(player: Player, arguments: Tuple) -> null
  :FireServer(arguments: Tuple) -> null
  .OnClientEvent: Event(arguments: Tuple)
  .OnServerEvent: Event(player: Player, arguments: Tuple)
```

### Actor  ‹Model›
```
  :BindToMessage(topic: string, function: Function) -> RBXScriptConnection
  :BindToMessageParallel(topic: string, function: Function) -> RBXScriptConnection
  :SendMessage(topic: string, message: Tuple) -> null
```

### ValueBase  ‹Instance›
_(inherits all members from superclass)_

### IntValue  ‹ValueBase›
```
  .Value: int64
  .Changed: Event(value: int64)
```

### StringValue  ‹ValueBase›
```
  .Value: string
  .Changed: Event(value: string)
```

### BoolValue  ‹ValueBase›
```
  .Value: bool
  .Changed: Event(value: bool)
```

### NumberValue  ‹ValueBase›
```
  .Value: double
  .Changed: Event(value: double)
```

### ObjectValue  ‹ValueBase›
```
  .Value: Instance
  .Changed: Event(value: Instance)
```

### CFrameValue  ‹ValueBase›
```
  .Value: CFrame
  .Changed: Event(value: CFrame)
```

### Vector3Value  ‹ValueBase›
```
  .Value: Vector3
  .Changed: Event(value: Vector3)
```

### Color3Value  ‹ValueBase›
```
  .Value: Color3
  .Changed: Event(value: Color3)
```

### GuiObject  ‹GuiBase2d›
```
  .Active: bool
  .AnchorPoint: Vector2
  .AutomaticSize: AutomaticSize
  .BackgroundColor3: Color3
  .BackgroundTransparency: float
  .BorderColor3: Color3
  .BorderMode: BorderMode
  .BorderSizePixel: int
  .ClipsDescendants: bool
  .GuiState: GuiState
  .InputSink: InputSink
  .Interactable: bool
  .LayoutOrder: int
  .NextSelectionDown: GuiObject
  .NextSelectionLeft: GuiObject
  .NextSelectionRight: GuiObject
  .NextSelectionUp: GuiObject
  .Position: UDim2
  .Rotation: float
  .Selectable: bool
  .SelectionImageObject: GuiObject
  .SelectionOrder: int
  .Size: UDim2
  .SizeConstraint: SizeConstraint
  .Transparency: float
  .Visible: bool
  .ZIndex: int
  :TweenPosition(endPosition: UDim2, easingDirection: EasingDirection, easingStyle: EasingStyle, time: float, override: bool, callback: Function) -> bool
  :TweenSize(endSize: UDim2, easingDirection: EasingDirection, easingStyle: EasingStyle, time: float, override: bool, callback: Function) -> bool
  :TweenSizeAndPosition(endSize: UDim2, endPosition: UDim2, easingDirection: EasingDirection, easingStyle: EasingStyle, time: float, override: bool, callback: Function) -> bool
  .InputBegan: Event(input: InputObject)
  .InputChanged: Event(input: InputObject)
  .InputEnded: Event(input: InputObject)
  .MouseEnter: Event(x: int, y: int)
  .MouseLeave: Event(x: int, y: int)
  .MouseMoved: Event(x: int, y: int)
  .MouseWheelBackward: Event(x: int, y: int)
  .MouseWheelForward: Event(x: int, y: int)
  .SelectionGained: Event()
  .SelectionLost: Event()
  .TouchLongPress: Event(touchPositions: Array, state: UserInputState)
  .TouchPan: Event(touchPositions: Array, totalTranslation: Vector2, velocity: Vector2, state: UserInputState)
  .TouchPinch: Event(touchPositions: Array, scale: float, velocity: float, state: UserInputState)
  .TouchRotate: Event(touchPositions: Array, rotation: float, velocity: float, state: UserInputState)
  .TouchSwipe: Event(swipeDirection: SwipeDirection, numberOfTouches: int)
  .TouchTap: Event(touchPositions: Array)
```

### GuiBase2d  ‹GuiBase›
```
  .AbsolutePosition: Vector2
  .AbsoluteRotation: float
  .AbsoluteSize: Vector2
  .AutoLocalize: bool
  .RootLocalizationTable: LocalizationTable
  .SelectionBehaviorDown: SelectionBehavior
  .SelectionBehaviorLeft: SelectionBehavior
  .SelectionBehaviorRight: SelectionBehavior
  .SelectionBehaviorUp: SelectionBehavior
  .SelectionGroup: bool
  .SelectionChanged: Event(amISelected: bool, previousSelection: GuiObject, newSelection: GuiObject)
```

### ScreenGui  ‹LayerCollector›
```
  .ClipToDeviceSafeArea: bool
  .DisplayOrder: int
  .IgnoreGuiInset: bool
  .SafeAreaCompatibility: SafeAreaCompatibility
  .ScreenInsets: ScreenInsets
```

### Frame  ‹GuiObject›
```
  .Style: FrameStyle
```

### TextLabel  ‹GuiLabel›
```
  .ContentText: string
  .Font: Font
  .FontFace: Font
  .LineHeight: float
  .LocalizedText: string
  .MaxVisibleGraphemes: int
  .OpenTypeFeatures: string
  .OpenTypeFeaturesError: string
  .RichText: bool
  .Text: string
  .TextBounds: Vector2
  .TextColor3: Color3
  .TextDirection: TextDirection
  .TextFits: bool
  .TextScaled: bool
  .TextSize: float
  .TextStrokeColor3: Color3
  .TextStrokeTransparency: float
  .TextTransparency: float
  .TextTruncate: TextTruncate
  .TextWrapped: bool
  .TextXAlignment: TextXAlignment
  .TextYAlignment: TextYAlignment
```

### TextButton  ‹GuiButton›
```
  .ContentText: string
  .Font: Font
  .FontFace: Font
  .LineHeight: float
  .LocalizedText: string
  .MaxVisibleGraphemes: int
  .OpenTypeFeatures: string
  .OpenTypeFeaturesError: string
  .RichText: bool
  .Text: string
  .TextBounds: Vector2
  .TextColor3: Color3
  .TextDirection: TextDirection
  .TextFits: bool
  .TextScaled: bool
  .TextSize: float
  .TextStrokeColor3: Color3
  .TextStrokeTransparency: float
  .TextTransparency: float
  .TextTruncate: TextTruncate
  .TextWrapped: bool
  .TextXAlignment: TextXAlignment
  .TextYAlignment: TextYAlignment
```

### TextBox  ‹GuiObject›
```
  .ClearTextOnFocus: bool
  .ContentText: string
  .CursorPosition: int
  .Font: Font
  .FontFace: Font
  .LineHeight: float
  .MaxVisibleGraphemes: int
  .MultiLine: bool
  .OpenTypeFeatures: string
  .OpenTypeFeaturesError: string
  .PlaceholderColor3: Color3
  .PlaceholderText: string
  .RichText: bool
  .SelectionStart: int
  .ShowNativeInput: bool
  .Text: string
  .TextBounds: Vector2
  .TextColor3: Color3
  .TextDirection: TextDirection
  .TextEditable: bool
  .TextFits: bool
  .TextScaled: bool
  .TextSize: float
  .TextStrokeColor3: Color3
  .TextStrokeTransparency: float
  .TextTransparency: float
  .TextTruncate: TextTruncate
  .TextWrapped: bool
  .TextXAlignment: TextXAlignment
  .TextYAlignment: TextYAlignment
  :CaptureFocus() -> null
  :IsFocused() -> bool
  :ReleaseFocus(submitted: bool) -> null
  .FocusLost: Event(enterPressed: bool, inputThatCausedFocusLoss: InputObject)
  .Focused: Event()
  .ReturnPressedFromOnScreenKeyboard: Event()
```

### ImageLabel  ‹GuiLabel›
```
  .Image: ContentId
  .ImageColor3: Color3
  .ImageContent: Content
  .ImageRectOffset: Vector2
  .ImageRectSize: Vector2
  .ImageTransparency: float
  .IsLoaded: bool
  .ResampleMode: ResamplerMode
  .ScaleType: ScaleType
  .SliceCenter: Rect
  .SliceScale: float
  .TileSize: UDim2
```

### ImageButton  ‹GuiButton›
```
  .HoverImage: ContentId
  .HoverImageContent: Content
  .Image: ContentId
  .ImageColor3: Color3
  .ImageContent: Content
  .ImageRectOffset: Vector2
  .ImageRectSize: Vector2
  .ImageTransparency: float
  .IsLoaded: bool
  .PressedImage: ContentId
  .PressedImageContent: Content
  .ResampleMode: ResamplerMode
  .ScaleType: ScaleType
  .SliceCenter: Rect
  .SliceScale: float
  .TileSize: UDim2
```

### ScrollingFrame  ‹GuiObject›
```
  .AbsoluteCanvasSize: Vector2
  .AbsoluteWindowSize: Vector2
  .AutomaticCanvasSize: AutomaticSize
  .BottomImage: ContentId
  .BottomImageContent: Content
  .CanvasPosition: Vector2
  .CanvasSize: UDim2
  .ElasticBehavior: ElasticBehavior
  .HorizontalScrollBarInset: ScrollBarInset
  .MidImage: ContentId
  .MidImageContent: Content
  .ScrollBarImageColor3: Color3
  .ScrollBarImageTransparency: float
  .ScrollBarThickness: int
  .ScrollingDirection: ScrollingDirection
  .ScrollingEnabled: bool
  .TopImage: ContentId
  .TopImageContent: Content
  .VerticalScrollBarInset: ScrollBarInset
  .VerticalScrollBarPosition: VerticalScrollBarPosition
  :GetScrollVelocity() -> Vector2
  :ResetScrollVelocity() -> null
```

### CanvasGroup  ‹GuiObject›
```
  .GroupColor3: Color3
  .GroupTransparency: float
```

### UICorner  ‹UIComponent›
```
  .BottomLeftRadius: UDim
  .BottomRightRadius: UDim
  .CornerRadius: UDim
  .TopLeftRadius: UDim
  .TopRightRadius: UDim
```

### UIPadding  ‹UIComponent›
```
  .PaddingBottom: UDim
  .PaddingLeft: UDim
  .PaddingRight: UDim
  .PaddingTop: UDim
```

### UIListLayout  ‹UIGridStyleLayout›
```
  .HorizontalFlex: UIFlexAlignment
  .ItemLineAlignment: ItemLineAlignment
  .Padding: UDim
  .VerticalFlex: UIFlexAlignment
  .Wraps: bool
```

### UIGridLayout  ‹UIGridStyleLayout›
```
  .AbsoluteCellCount: Vector2
  .AbsoluteCellSize: Vector2
  .CellPadding: UDim2
  .CellSize: UDim2
  .FillDirectionMaxCells: int
  .StartCorner: StartCorner
```

### UITableLayout  ‹UIGridStyleLayout›
```
  .FillEmptySpaceColumns: bool
  .FillEmptySpaceRows: bool
  .MajorAxis: TableMajorAxis
  .Padding: UDim2
```

### UIAspectRatioConstraint  ‹UIConstraint›
```
  .AspectRatio: float
  .AspectType: AspectType
  .DominantAxis: DominantAxis
```

### UISizeConstraint  ‹UIConstraint›
```
  .MaxSize: Vector2
  .MinSize: Vector2
```

### UIStroke  ‹UIComponent›
```
  .ApplyStrokeMode: ApplyStrokeMode
  .BorderOffset: UDim
  .BorderStrokePosition: BorderStrokePosition
  .Color: Color3
  .Enabled: bool
  .LineJoinMode: LineJoinMode
  .StrokeSizingMode: StrokeSizingMode
  .Thickness: float
  .Transparency: float
  .ZIndex: int
```

### UIGradient  ‹UIComponent›
```
  .Color: ColorSequence
  .Enabled: bool
  .Offset: Vector2
  .Rotation: float
  .Transparency: NumberSequence
```

### UIScale  ‹UIComponent›
```
  .Scale: float
```

### UIFlexItem  ‹UIComponent›
```
  .FlexMode: UIFlexMode
  .GrowRatio: float
  .ItemLineAlignment: ItemLineAlignment
  .ShrinkRatio: float
```

### UIPageLayout  ‹UIGridStyleLayout›
```
  .Animated: bool
  .Circular: bool
  .CurrentPage: GuiObject
  .EasingDirection: EasingDirection
  .EasingStyle: EasingStyle
  .GamepadInputEnabled: bool
  .Padding: UDim
  .ScrollWheelInputEnabled: bool
  .TouchInputEnabled: bool
  .TweenTime: float
  :JumpTo(page: Instance) -> null
  :JumpToIndex(index: int) -> null
  :Next() -> null
  :Previous() -> null
  .PageEnter: Event(page: Instance)
  .PageLeave: Event(page: Instance)
  .Stopped: Event(currentPage: Instance)
```

### BillboardGui  ‹LayerCollector›
```
  .Active: bool
  .Adornee: Instance
  .AlwaysOnTop: bool
  .Brightness: float
  .ClipsDescendants: bool
  .CurrentDistance: float
  .DistanceStep: float
  .ExtentsOffset: Vector3
  .ExtentsOffsetWorldSpace: Vector3
  .LightInfluence: float
  .MaxDistance: float
  .PlayerToHideFrom: Instance
  .Size: UDim2
  .SizeOffset: Vector2
  .StudsOffset: Vector3
  .StudsOffsetWorldSpace: Vector3
```

### SurfaceGui  ‹SurfaceGuiBase›
```
  .AlwaysOnTop: bool
  .Brightness: float
  .CanvasSize: Vector2
  .ClipsDescendants: bool
  .LightInfluence: float
  .MaxDistance: float
  .PixelsPerStud: float
  .SizingMode: SurfaceGuiSizingMode
  .ToolPunchThroughDistance: float
  .ZOffset: float
```

### ViewportFrame  ‹GuiObject›
```
  .Ambient: Color3
  .CurrentCamera: Camera
  .ImageColor3: Color3
  .ImageTransparency: float
  .LightColor: Color3
  .LightDirection: Vector3
```

### Constraint  ‹Instance›
```
  .Active: bool
  .Attachment0: Attachment
  .Attachment1: Attachment
  .Color: BrickColor
  .Enabled: bool
  .Visible: bool
```

### WeldConstraint  ‹Instance›
```
  .Active: bool
  .Enabled: bool
  .Part0: BasePart
  .Part1: BasePart
```

### Motor6D  ‹Motor›
```
  .Transform: CFrame
```

### AlignPosition  ‹Constraint›
```
  .ApplyAtCenterOfMass: bool
  .ForceLimitMode: ForceLimitMode
  .ForceRelativeTo: ActuatorRelativeTo
  .MaxAxesForce: Vector3
  .MaxForce: float
  .MaxVelocity: float
  .Mode: PositionAlignmentMode
  .Position: Vector3
  .ReactionForceEnabled: bool
  .Responsiveness: float
  .RigidityEnabled: bool
```

### AlignOrientation  ‹Constraint›
```
  .AlignType: AlignType
  .CFrame: CFrame
  .LookAtPosition: Vector3
  .MaxAngularVelocity: float
  .MaxTorque: float
  .Mode: OrientationAlignmentMode
  .PrimaryAxis: Vector3
  .PrimaryAxisOnly: bool
  .ReactionTorqueEnabled: bool
  .Responsiveness: float
  .RigidityEnabled: bool
  .SecondaryAxis: Vector3
```

### LinearVelocity  ‹Constraint›
```
  .ForceLimitMode: ForceLimitMode
  .ForceLimitsEnabled: bool
  .LineDirection: Vector3
  .LineVelocity: float
  .MaxAxesForce: Vector3
  .MaxForce: float
  .MaxPlanarAxesForce: Vector2
  .PlaneVelocity: Vector2
  .PrimaryTangentAxis: Vector3
  .ReactionForceEnabled: bool
  .RelativeTo: ActuatorRelativeTo
  .SecondaryTangentAxis: Vector3
  .VectorVelocity: Vector3
  .VelocityConstraintMode: VelocityConstraintMode
```

### AngularVelocity  ‹Constraint›
```
  .AngularVelocity: Vector3
  .MaxTorque: float
  .ReactionTorqueEnabled: bool
  .RelativeTo: ActuatorRelativeTo
```

### VectorForce  ‹Constraint›
```
  .ApplyAtCenterOfMass: bool
  .Force: Vector3
  .RelativeTo: ActuatorRelativeTo
```

### Attachment  ‹Instance›
```
  .Axis: Vector3
  .CFrame: CFrame
  .Orientation: Vector3
  .Position: Vector3
  .SecondaryAxis: Vector3
  .Visible: bool
  .WorldAxis: Vector3
  .WorldCFrame: CFrame
  .WorldOrientation: Vector3
  .WorldPosition: Vector3
  .WorldSecondaryAxis: Vector3
  :GetConstraints() -> Instances
```

### RodConstraint  ‹Constraint›
```
  .CurrentDistance: float
  .Length: float
  .LimitAngle0: float
  .LimitAngle1: float
  .LimitsEnabled: bool
  .Thickness: float
```

### RopeConstraint  ‹Constraint›
```
  .CurrentDistance: float
  .Length: float
  .Restitution: float
  .Thickness: float
  .WinchEnabled: bool
  .WinchForce: float
  .WinchResponsiveness: float
  .WinchSpeed: float
  .WinchTarget: float
```

### SpringConstraint  ‹Constraint›
```
  .Coils: float
  .CurrentLength: float
  .Damping: float
  .FreeLength: float
  .LimitsEnabled: bool
  .MaxForce: float
  .MaxLength: float
  .MinLength: float
  .Radius: float
  .Stiffness: float
  .Thickness: float
```

### HingeConstraint  ‹Constraint›
```
  .ActuatorType: ActuatorType
  .AngularResponsiveness: float
  .AngularSpeed: float
  .AngularVelocity: float
  .CurrentAngle: float
  .LimitsEnabled: bool
  .LowerAngle: float
  .MotorMaxAcceleration: float
  .MotorMaxTorque: float
  .Radius: float
  .Restitution: float
  .ServoMaxTorque: float
  .TargetAngle: float
  .UpperAngle: float
```

### PrismaticConstraint  ‹SlidingBallConstraint›
_(inherits all members from superclass)_

### BodyVelocity  ‹BodyMover›
```
  .MaxForce: Vector3
  .P: float
  .Velocity: Vector3
  :GetLastForce() -> Vector3
  :lastForce() -> Vector3
```

### BodyPosition  ‹BodyMover›
```
  .D: float
  .MaxForce: Vector3
  .P: float
  .Position: Vector3
  :GetLastForce() -> Vector3
  .ReachedTarget: Event()
```

### Terrain  ‹BasePart›
```
  .MaxExtents: Region3int16
  .WaterColor: Color3
  .WaterReflectance: float
  .WaterTransparency: float
  .WaterWaveSize: float
  .WaterWaveSpeed: float
  :CellCenterToWorld(x: int, y: int, z: int) -> Vector3
  :CellCornerToWorld(x: int, y: int, z: int) -> Vector3
  :Clear() -> null
  :ClearVoxelsAsync_beta(region: Region3, channelIds: Array) -> null
  :CopyRegion(region: Region3int16) -> TerrainRegion
  :CountCells() -> int
  :FillBall(center: Vector3, radius: float, material: Material) -> null
  :FillBlock(cframe: CFrame, size: Vector3, material: Material) -> null
  :FillCylinder(cframe: CFrame, height: float, radius: float, material: Material) -> null
  :FillRegion(region: Region3, resolution: float, material: Material) -> null
  :FillWedge(cframe: CFrame, size: Vector3, material: Material) -> null
  :GetMaterialColor(material: Material) -> Color3
  :GetMaterialSlot(slotIndex: int) -> Tuple
  :IterateVoxelsAsync_beta(region: Region3, resolution: int, channelIds: Array) -> TerrainIterateOperation
  :ModifyVoxelsAsync_beta(region: Region3, resolution: int, channelIds: Array) -> TerrainModifyOperation
  :PasteRegion(region: TerrainRegion, corner: Vector3int16, pasteEmptyCells: bool) -> null
  :ReadVoxelChannels(region: Region3, resolution: float, channelIds: Array) -> Dictionary
  :ReadVoxels(region: Region3, resolution: float) -> Tuple
  :ReadVoxelsAsync_beta(region: Region3, resolution: int, channelIds: Array) -> TerrainReadOperation
  :ReplaceMaterial(region: Region3, resolution: float, sourceMaterial: Material, targetMaterial: Material) -> null
  :ResetMaterialSlot(slotIndex: int) -> null
  :SetMaterialColor(material: Material, value: Color3) -> null
  :SetMaterialSlot(slotIndex: int, baseMaterial: Material, materialVariant: string, color: Color3) -> null
  :WorldToCell(position: Vector3) -> Vector3
  :WorldToCellPreferEmpty(position: Vector3) -> Vector3
  :WorldToCellPreferSolid(position: Vector3) -> Vector3
  :WriteVoxelChannels(region: Region3, resolution: float, channels: Dictionary) -> null
  :WriteVoxels(region: Region3, resolution: float, materials: Array, occupancy: Array) -> null
  :WriteVoxelsAsync_beta(region: Region3, resolution: int, channelIds: Array) -> TerrainWriteOperation
```

### Seat  ‹Part›
```
  .Disabled: bool
  .Occupant: Humanoid
  :Sit(humanoid: Instance) -> null
```

### VehicleSeat  ‹BasePart›
```
  .AreHingesDetected: int
  .Disabled: bool
  .HeadsUpDisplay: bool
  .MaxSpeed: float
  .Occupant: Humanoid
  .Steer: int
  .SteerFloat: float
  .Throttle: int
  .ThrottleFloat: float
  .Torque: float
  .TurnSpeed: float
  :Sit(humanoid: Instance) -> null
```

### SpawnLocation  ‹Part›
```
  .AllowTeamChangeOnTouch: bool
  .Duration: int
  .Enabled: bool
  .Neutral: bool
  .TeamColor: BrickColor
```

## Curated datatypes

_(datatype members not present in this dump; see `api/engine-api-index.txt` datatype section and WebFetch the .md pages)_
