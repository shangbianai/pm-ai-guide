# React Three Fiber + drei 速查

> 数据来源：[pmndrs/drei](https://github.com/pmndrs/drei) 官方 README（2026-09 抓取）、R3F 官方文档。
> drei 使用独立的 `three-stdlib` 而非 `three/examples/jsm`。React Native 引入路径为 `@react-three/drei/native`（不含 Html/Loader）。

## 安装与版本

```bash
npm install three @react-three/fiber @react-three/drei
```

- R3F v8 ↔ React 18；v9 ↔ React 19（升级前查官方迁移指南）
- three / R3F / drei 三者版本需兼容对齐，升级时逐个确认

## R3F 核心 API（速记）

| API | 用途 |
|-----|------|
| `<Canvas>` | 渲染根组件，声明即挂载 WebGL 上下文 |
| `useFrame((state, delta) => {})` | 每帧回调，做动画/读取时钟 |
| `useThree()` | 取 camera / gl / scene / size 等状态 |
| `useLoader(Loader, url)` | 加载 GLTF/纹理等资源 |
| `<primitive object={...} />` | 挂载已有 three 对象 |
| 事件：`onClick` / `onPointerOver` 等 | 直接写在 mesh 上，raycaster 内建 |

## drei helper 全分类速查

### 相机 Cameras
PerspectiveCamera · OrthographicCamera · CubeCamera

### 控制 Controls
CameraControls · ScrollControls · PresentationControls · KeyboardControls · FaceControls · MotionPathControls

### 辅助 Gizmos
GizmoHelper · PivotControls · DragControls · TransformControls · Grid · Helper / useHelper

### 几何 Shapes
Plane · Box · Sphere · Circle · Cone · Cylinder · Tube · Torus · TorusKnot · Ring · Tetrahedron · Polyhedron · Icosahedron · Octahedron · Dodecahedron · Extrude · Lathe · Shape · RoundedBox · ScreenQuad · Line · QuadraticBezierLine · CubicBezierLine · CatmullRomLine · Facemesh

### 抽象 Abstractions
Image · Text · Text3D · Effects · PositionalAudio · Billboard · ScreenSpace · ScreenSizer · GradientTexture · Edges · Outlines · Trail · Sampler · ComputedAttribute · Clone · useAnimations · MarchingCubes · Decal · Svg · AsciiRenderer · Splat

### 材质 Shaders
MeshReflectorMaterial · MeshWobbleMaterial · MeshDistortMaterial · MeshRefractionMaterial · MeshTransmissionMaterial · MeshDiscardMaterial · PointMaterial · SoftShadows · shaderMaterial

### 修改器 Modifiers
CurveModifier

### 杂项 Misc
useContextBridge · Html · CycleRaycast · Select · SpriteAnimator · Stats · StatsGl · Wireframe · useDepthBuffer · useFBO · useCamera · useCubeCamera · useDetectGPU · useAspect · useCursor · useIntersect · useBoxProjectedEnv · useTrail · useSurfaceSampler · FaceLandmarker

### 加载 Loading
Loader · useProgress · useGLTF · useFBX · useTexture · useKTX2 · useCubeTexture · useVideoTexture · useFont · useSpriteLoader

### 性能 Performance
Instances · Merged · Points · Segments · Detailed · Preload · BakeShadows · meshBounds · AdaptiveDpr · AdaptiveEvents · Bvh · PerformanceMonitor

### 视口/门户 Portals
Hud · View · RenderTexture · RenderCubeTexture · Fisheye · Mask · MeshPortalMaterial

### 舞台 Staging（布景/光影/环境，做高质量 demo 场景的起点）
Center · Resize · BBAnchor · Bounds · CameraShake · Float · Stage · Backdrop · Shadow · Caustics · ContactShadows · RandomizedLight · AccumulativeShadows · SpotLight · SpotLightShadow · Environment · Lightformer · Sky · Stars · Sparkles · Cloud · useEnvironment · useMatcapTexture · useNormalTexture

## 高频组合模式

- **快速高质量场景**：`<Canvas>` + `<Stage>`（自动布光/居中/地面阴影）
- **文字 3D**：`Text`（troika）或 `Text3D`（需字体 JSON）
- **玻璃/液体质感**：`MeshTransmissionMaterial`（配 `Environment` 环境贴图）
- **反射地面**：`MeshReflectorMaterial`
- **滚动叙事**：`ScrollControls` + 页面 section
- **低多边形粒子**：`Points` + `PointMaterial`；大量重复体用 `Instances`
- **性能自适应**：`PerformanceMonitor` + `AdaptiveDpr`；复杂模型 `Detailed`（LOD）
- **HTML 叠加**：`Html`（把 DOM 定位到 3D 坐标，仅客户端）

## 官方资源

- R3F 文档：https://r3f.docs.pmnd.rs
- drei 文档：https://drei.docs.pmnd.rs
- three.js 文档：https://threejs.org/docs
- 生态姊妹库：`@react-three/postprocessing`（后处理）、`@react-three/rapier`（物理）、`@react-three/xr`
