# threeui 组件全量目录（Community 版）

> 数据来源：[MengTo/threeui](https://github.com/MengTo/threeui)（Design+Code 出品，Community 代码 MIT；全站含 Pro 共 378 个，本目录仅开源 Community 部分）
> 抓取日期：2026-09-08，主条目 **43 个**、变体 **61 个**（以 [threeui.com](https://threeui.com) 为准）。

## 安装方式（npm 包，v1.2.0）

```bash
npm install @designcodeio/threeui
```

```tsx
// 共享样式必须引入，否则组件渲染异常
import { AtTheHorizon } from "@designcodeio/threeui";
import "@designcodeio/threeui/style.css";

export function Hero() {
  return <AtTheHorizon />;
}
```

也可用官方 CLI 把组件源码直接拉进项目（需 OAuth 登录，可拉取的范围含 Community）：

```bash
npx @designcodeio/threeui-cli add <组件id>   # id 见下表，如 dot-matrix
```

npm 包导出组件（PascalCase 导出名）共 103 个：AmberHalftone, AnimatedTopDock, AudioWordmark, BallStudy, BellFieldBackground, BestsellersBookShowcase, BookshelfScene, BrandOrbs, CharacterCarousel, CharacterFilmstrip, CharacterWave, CircleButtons, ClothStudy, CloudField, CompleteShelfLandingPage, CondensationBackground, ConnectivityGraph, ConstellationField, CrtBackground, DataField, DefenseLines, DiagnosticsPanel, DimensionalField, DotBorderButton, DotMatrixBackground, EditorialIntroSection, ElementsBackground, ElementsCollection, EmberStorm, EmeraldHorizonBackground, EngravedCertificate, ExpanseField, FloatingDotsCta, FlowField, FluidFieldBackground, FluxVortex, Gallery, GalleryHeading, GatewayFlow, GenerateButton, GenerativeTree, GlassmorphismCta, GlobeCollection, GradientBeamCta, GradientCta, GradientPillButton, HalftoneFlow, IgnitionButton, InductionButton, InterfaceLines, JapaneseTowerLandscape, KageLandingPage, KoiStudies, LandscapeScene, LaserCollection, LaunchButton, LiquidFormBackground, LiquidMetalButton, LogicCoreField, LumenCta, MengToSketchbookLandingPage, MorphingGlyphCloud, NebulaBackground, NeonTypography, NewsletterFooterSection, OrbitalSphereBackground, OutlineTypeflow, ParticleDrift, ParticleNetwork, ParticleWordmark, PerformanceGauges, PlasmaButton, PortalFieldCollection, PredictiveArcCanvas, RectangleButtons, RibbonFieldBackground, RippleStudy, SemanticBloom, ShaderButtons, Sketchbook, SkeuomorphicToggle, SkeuomorphicToggleCollection, SlidingTextCta, SparkBadge, SpinningBorderButton, StreamConvergenceBackground, StructureFlowCollection, SylvaHero, SylvaLivingWorldScene, TactileButton, TempleNightScene, TextAnimationCollection, TextPathStudies, ThinkingButton, ThreeUIIntro, TopoField, TopologyField, TypographyVortexCanvas, UplinkLoader, VoidField, WarpFieldBackground, WireframeForms, WovenCloth。

## 目录条目（按分类）

### 完整落地页 Landing Pages（2）

| id | 名称 | 运行时 | 简介（官方英文） |
|------|------|------|------|
| `kage-landing-page` | Kage | Full HTML + DOM/CSS + Three.js | The complete authored Kage temple experience, preserved as an interactive full-page document with its original navigation, scroll scenes, and local Three.js world. |
| `meng-to-sketchbook-landing-page` | Sketchbook | Full HTML + DOM/CSS + JavaScript | A tactile personal portfolio built as a Singapore sketchbook, with nine illustrated plates, curled page turns, a draggable magnifying glass, zoom controls, a botanical paper atmosphere, and an editorial index. |

### Hero 场景 Hero（3）

| id | 名称 | 运行时 | 简介（官方英文） |
|------|------|------|------|
| `complete-shelf-landing-page` | Complete Shelf | Full HTML + DOM/CSS + Three.js r165 | The complete Working Volumes bookshelf page with all seven tools, its responsive editorial interface, and authored Three.js presentation. |
| `bestsellers-book-showcase` | Bestsellers Book Showcase | Full HTML + DOM/CSS + embedded media | The complete Field Manuals book showcase, preserved unchanged with its editorial layout, authored motion, interactions, and embedded media. |
| `sylva-hero` | Sylva | Full HTML + DOM/CSS + local Three.js | The complete Sylva Living Green page, preserved with its Three.js scene, local typography, card imagery, and embedded liquid-metal buttons. The moss-root world with pale flowers, ferns, drifting pollen, the landing butterfly, and native liquid-metal controls behind the full hero layout. |

### Three.js 场景 Three.js（8）

| id | 名称 | 运行时 | 简介（官方英文） |
|------|------|------|------|
| `sylva-living-world` | Sylva Living World | Three.js r149 | The original procedural moss-root world with pale flowers, ferns, drifting pollen, scan light, and a landing butterfly. |
| `temple-night` | Temple Night | Three.js r149 | Kage’s procedural Kyoto mountain temple after dark, with the exact authored architecture, rain, mist, leaves, pointer wisps, camera composition, and bloom pipeline. |
| `landscape` | Landscape | Three.js r149 | A tower-free procedural terrain whose light, sky, fog, stars, rain, lightning, snow, grass, and stones move through seven authored environment states. |
| `japanese-tower` | Country Towers | Three.js r149 + Canvas 2D | Six country-specific towers assembling above a procedural landscape: Japanese, Chinese, Vietnamese, Thai, Khmer, and Ottoman. |
| `bookshelf` | Bookshelf | Three.js r165 | The exact seven-volume Bookshelf collection with its authored room, carousel shelf, individual cover artwork, foil, pages, inspection, opening, and page-turn system. |
| `structure-flow` | Structure Flow | Three.js r128–r160 | Thirteen authored Three.js field studies collected as one family, spanning particle domes, horizons, orbital systems, matrices, topology, fluid fields, embers, and vortexes. |
| `warp-field` | Warp Field | Three.js r128 | Nexus’s focused hero warp: 400 emerald additive streaks and 40 luminous tiles streaming through an authored deep-space fog field. |
| `woven-cloth` | Woven Cloth | Three.js r160 | A Three.js woven-cloth simulation with Woven Cloth typography printed into its procedural textile so every letter deforms with the fabric, and three companion cloths woven around the same Verlet sheet. |

### 背景 Backgrounds（9）

| id | 名称 | 运行时 | 简介（官方英文） |
|------|------|------|------|
| `predictive-arc` | Predictive Arc | Canvas 2D + Raw WebGL + Three.js r128 | Eight animated arc, signal, ribbon, void, and halftone scenes collected in one Canvas 2D, raw-WebGL, and Three.js family. |
| `liquid-form` | Liquid Form | Raw WebGL | A centered silver ray-marched liquid form with authored studio reflections and pointer-responsive camera drift. |
| `crt` | CRT | Raw WebGL + Canvas 2D | One sharpened curved-glass CRT tube driving four screens: the Matrix-era boot terminal, a monochrome film leader, a noise-torn blue signal fault, and an 8-bit console title. |
| `energy-orb` | Globe | Raw WebGL + Canvas 2D | The original layered FBM energy sphere with translucent rim glow and depth-aware star field. |
| `spark-badge` | Spark Badge | Canvas 2D | A luminous credential badge held together by curl-noise embers, carved typography, rain occlusion, waterline sparks, and an adaptive particle field. |
| `elements` | Elements | Raw WebGL2 + Canvas 2D | Water, lightning, fire, condensation, and a painterly generative tree collected as one elemental family across WebGL2 and Canvas 2D. |
| `constellation-field` | Constellation Field | Canvas 2D + Raw WebGL | A family of particle networks, gateways, interface lines, defense traces, and topographic fields gathered into one configurable collection. |
| `portal-field` | Portal Field | Three.js r134 + Raw WebGL + Canvas 2D | Five ambient field backgrounds collected across Three.js, raw WebGL, and Canvas 2D renderers. |
| `matrix-field` | Laser | Raw WebGL | Four pointer-reactive laser scenes spanning a preserved matrix junction, atmospheric blade, vanishing array, and halftone relay. |

### 按钮 Buttons（4）

| id | 名称 | 运行时 | 简介（官方英文） |
|------|------|------|------|
| `star-portal` | Shader Buttons | Raw WebGL + Canvas 2D + CSS | Six authored shader and canvas button treatments collected into one interactive family. |
| `rectangle-buttons` | Rectangle Buttons | DOM + CSS | Twenty-two authored rectangle-button and animated CTA treatments collected into one family. |
| `circle-buttons` | Circle Buttons | DOM + CSS | Three compact circular icon controls using the exact Dark Glass, Launch, and Dot Border material systems. |
| `liquid-metal-button` | Liquid Metal Button | Raw WebGL 2 + DOM/CSS | A prismatic liquid-metal control in Sign up pill, Liquid Orb, and configurable Play Circle variants, with pointer-following bloom and press ripples. |

### 文字动画 Text Animation（5）

| id | 名称 | 运行时 | 简介（官方英文） |
|------|------|------|------|
| `typography-vortex` | Typography Vortex | Canvas 2D | Sable’s complete rotating typography vortex with crisp prerendered rings, drifting glyphs, pointer dissolution, particle dust, and click suction — with dark and light surfaces. |
| `semantic-bloom` | Semantic Bloom | Canvas 2D + DOM/CSS | A customizable Codex wordmark that draws a viscous particle organism toward its letters, illuminating the text as the network searches and reconnects. |
| `globe-study` | Text Path Studies | Canvas 2D | Six interactive Canvas 2D typography studies spanning a globe, flowing outlines, morphing glyphs, cloth physics, ripples, and a particle sphere. |
| `gallery-heading` | Gallery Heading | Canvas 2D | An oversized headline ringed by twelve 4:3 plates — one flat colour each, shaded by a procedural noise field rather than a gradient — that hold still until the pointer arrives, then orbit. Four galleries, each with its own field, typography, and direction. |
| `article-headings` | Article Headings | DOM/CSS + Canvas 2D | Three expressive text treatments collected in one family: a chromatic intro, a particle wordmark, and an audio-reactive identity lockup. |

### UI 元素 UI Elements（7）

| id | 名称 | 运行时 | 简介（官方英文） |
|------|------|------|------|
| `character-carousel` | Character Carousel | DOM + CSS | Two authored editorial character-card carousels collected as a light filmstrip and a dark responsive wave. |
| `gallery` | Gallery | Three.js r149 | The isolated Vantrix hero image ribbon: sixteen curved editorial panels orbiting a vertical cylindrical rail on a quiet paper grid. |
| `engraved-certificate` | Engraved Certificate | Canvas 2D + DOM/CSS | A responsive engraved certificate: plate field, dual guilloche rosettes, and a drifting harmonic pass that auto-cycles through four cam states. |
| `diagnostics-panel` | Diagnostics Panel | Canvas 2D | Three diagnostic illustration variants — layered planes, node cubes, and a flowing mesh — each isolated without page chrome or copy. |
| `skeuomorphic-toggle` | Skeuomorphic Toggle | DOM/CSS + Three.js + Raw WebGL | Four takes on one switch: the preserved tactile skeuomorphic export plus flat modern, Three.js glass, and shader-lit treatments, each matching light and dark appearances automatically. |
| `wireframe-forms` | Wireframe Forms | Canvas 2D | A family of rotating wireframe forms, with the cube, crossed cylinders, and nested sphere isolated as individual variants. |
| `brand-orbs` | Brand Orbs | Canvas 2D | Twenty-three animated brand marks rebuilt as small and medium dimensional dot orbs for AI status, product activity, and compact loading states. |

### 纯 CSS CSS（5）

| id | 名称 | 运行时 | 简介（官方英文） |
|------|------|------|------|
| `performance-gauges` | Performance Gauges | DOM + CSS | Four layered CSS instruments — tachometer, speedometer, turbo boost, and EV power — each isolated to one full-bleed dial with polar tick geometry, scale bands, and a self-testing needle sweep. |
| `uplink-loader` | Uplink Loader | DOM + CSS + JavaScript | A cinematic secure-uplink loader with stepped progress, illuminated telemetry ticks, neon readouts, technical corner markers, mirrored side rails, scanlines, and procedural grain. |
| `koi-studies` | Koi Studies | DOM + CSS 3D + Canvas 2D + WebGL | A tactile stack of three Japanese koi studies with CSS 3D depth, pointer tilt, drag and keyboard navigation, pixel-mask reveals, and animated halftone imagery. |
| `animated-top-dock` | Animated Top Dock | DOM + CSS + WebGL + Three.js r128 | Sable’s proximity-spring menu in four fits: the authored centred dock, a modern command bar, a fitted pixel-terminal strip, and a vertical refracting Three.js glass rail. |
| `sketchbook` | Sketchbook | DOM + CSS 3D | The exact Singapore paper sketchbook with nested-strip page curls, direct dragging, tilt, zoom, a movable magnifying glass, and its complete authored plate set. |

## 变体条目（61）

以下条目是上表某主条目的预设变体（`variantOf` 指向主条目 id），CLI/npm 用法相同：

| id | 变体属于 | 分类 |
|------|------|------|
| `stream-convergence` | `portal-field` | Backgrounds |
| `bell-field` | `portal-field` | Backgrounds |
| `flow-field` | `portal-field` | Backgrounds |
| `elemental-water` | `elements` | Backgrounds |
| `elemental-lightning` | `elements` | Backgrounds |
| `elemental-flame` | `elements` | Backgrounds |
| `condensation` | `elements` | Backgrounds |
| `generative-tree` | `elements` | Backgrounds |
| `ribbon-field` | `predictive-arc` | Backgrounds |
| `outline-typeflow` | `globe-study` | Text Animation |
| `morphing-glyph-cloud` | `globe-study` | Text Animation |
| `cloth-study` | `globe-study` | Text Animation |
| `ripple-study` | `globe-study` | Text Animation |
| `ball-study` | `globe-study` | Text Animation |
| `threeui-intro` | `article-headings` | Text Animation |
| `particle-wordmark` | `article-headings` | Text Animation |
| `audio-wordmark` | `article-headings` | Text Animation |
| `ignition-button` | `star-portal` | Buttons |
| `induction-button` | `star-portal` | Buttons |
| `plasma-button` | `star-portal` | Buttons |
| `tactile-button` | `star-portal` | Buttons |
| `thinking-button` | `star-portal` | Buttons |
| `sliding-text-cta` | `rectangle-buttons` | Buttons |
| `floating-dots-cta` | `rectangle-buttons` | Buttons |
| `launch-button` | `rectangle-buttons` | Buttons |
| `dot-border-button` | `rectangle-buttons` | Buttons |
| `gradient-cta` | `rectangle-buttons` | Buttons |
| `spinning-border-button` | `rectangle-buttons` | Buttons |
| `glassmorphism-cta` | `rectangle-buttons` | Buttons |
| `generate-button` | `rectangle-buttons` | Buttons |
| `gradient-pill-button` | `rectangle-buttons` | Buttons |
| `gradient-beam-cta` | `rectangle-buttons` | Buttons |
| `lumen-cta` | `rectangle-buttons` | Buttons |
| `editorial-intro` | `saas-dark` | Sections |
| `newsletter-footer` | `saas-dark` | Sections |
| `character-filmstrip` | `character-carousel` | UI Elements |
| `character-wave` | `character-carousel` | UI Elements |
| `cloud-field` | `portal-field` | Backgrounds |
| `void-field` | `predictive-arc` | Backgrounds |
| `emerald-horizon` | `structure-flow` | Three.js |
| `orbital-sphere` | `structure-flow` | Three.js |
| `dot-matrix` | `structure-flow` | Three.js |
| `expanse-field` | `structure-flow` | Three.js |
| `logic-core` | `structure-flow` | Three.js |
| `dimensional-field` | `structure-flow` | Three.js |
| `data-field` | `structure-flow` | Three.js |
| `topology-field` | `structure-flow` | Three.js |
| `halftone-flow` | `predictive-arc` | Backgrounds |
| `neon-sign` | `article-headings` | Text Animation |
| `nebula` | `structure-flow` | Three.js |
| `fluid-field` | `structure-flow` | Three.js |
| `ember-storm` | `structure-flow` | Three.js |
| `particle-drift` | `constellation-field` | Backgrounds |
| `particle-network` | `constellation-field` | Backgrounds |
| `flux-vortex` | `structure-flow` | Three.js |
| `amber-halftone` | `predictive-arc` | Backgrounds |
| `gateway-flow` | `constellation-field` | Backgrounds |
| `connectivity-graph` | `constellation-field` | Backgrounds |
| `interface-lines` | `constellation-field` | Backgrounds |
| `defense-lines` | `constellation-field` | Backgrounds |
| `topo-field` | `constellation-field` | Backgrounds |
