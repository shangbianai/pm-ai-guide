# react-bits 组件全量目录

> 数据来源：[DavidHDev/react-bits](https://github.com/DavidHDev/react-bits)（46.9k⭐，MIT + Commons Clause，个人/商用免费，禁止转卖库本身）
> 抓取日期：2026-09-08，共 **171 个组件**（每周更新，以 [reactbits.dev](https://reactbits.dev) 为准）。

## 安装方式

每个组件 4 种变体：`JS-CSS` / `JS-TW`（Tailwind）/ `TS-CSS` / `TS-TW`，安装命令末尾追加变体后缀：

```bash
# shadcn CLI（项目需先 npx shadcn@latest init）
npx shadcn@latest add @react-bits/<组件名>-TS-TW

# jsrepo CLI（无需 shadcn，配置见 jsrepo.dev）
npx jsrepo add @react-bits/<组件名>-TS-TW
```

也可以直接在 reactbits.dev 组件页复制源码手动放入项目。组件名即 PascalCase 名（下表「组件」列）。

## 常见外部依赖（安装对应组件时按需 npm install）

| 依赖 | 用途 | 涉及组件数 |
|------|------|-----------|
| `ogl` | WebGL 背景类组件 | 47 |
| `gsap` | 时间线/物理动画 | 35 |
| `three` + `@react-three/fiber`/`@react-three/drei` | 3D 类组件 | ~30 |
| `motion`（新版 framer-motion） | 滚动/入场动画包装 | 20 |
| `@react-three/postprocessing`、`postprocessing` | 后处理特效 | 5 |
| 其他个别组件：`matter-js`（物理）、`@use-gesture/react`（手势）、`lenis`（平滑滚动）、`face-api.js` | 按需 | 各 1 |

下表「依赖」列为空（—）表示纯 CSS/React 实现，零外部依赖。

## 文本动画 Text Animations（32）

| 组件 | 依赖 | 简介（官方英文） |
|------|------|------|
| [ASCIIText](https://reactbits.dev/text-animations/ascii-text) | — | Renders text with an animated ASCII background for a retro feel. |
| [BlurText](https://reactbits.dev/text-animations/blur-text) | `motion` | Text starts blurred then crisply resolves for a soft-focus reveal effect. |
| [CircularText](https://reactbits.dev/text-animations/circular-text) | `motion` | Layouts characters around a circle with optional rotation animation. |
| [CountUp](https://reactbits.dev/text-animations/count-up) | `motion` | Animated number counter supporting formatting and decimals. |
| [CurvedLoop](https://reactbits.dev/text-animations/curved-loop) | — | Flowing looping text path along a customizable curve with drag interaction. |
| [DecryptedText](https://reactbits.dev/text-animations/decrypted-text) | `motion` | Hacker-style decryption cycling random glyphs until resolving to real text. |
| [DepthText](https://reactbits.dev/text-animations/depth-text) | — | Layered extruded type with parallax that shifts against the pointer. |
| [EchoText](https://reactbits.dev/text-animations/echo-text) | — | Ghosted copies trail behind the text and settle into a single word. |
| [FallingText](https://reactbits.dev/text-animations/falling-text) | `matter-js` | Characters fall with gravity + bounce creating a playful entrance. |
| [FoldText](https://reactbits.dev/text-animations/fold-text) | `gsap` | Lines unfold into place like creased paper opening flat. |
| [FuzzyText](https://reactbits.dev/text-animations/fuzzy-text) | — | Vibrating fuzzy text with controllable hover intensity. |
| [GlitchText](https://reactbits.dev/text-animations/glitch-text) | — | RGB split and distortion glitch effect with jitter effects. |
| [GradientText](https://reactbits.dev/text-animations/gradient-text) | `motion` | Animated gradient sweep across live text with speed and color control. |
| [MaskedHeading](https://reactbits.dev/text-animations/masked-heading) | `gsap` | A large headline with a drifting colour mesh or image showing through the glyphs, revealed word by word. |
| [ParticleText](https://reactbits.dev/text-animations/particle-text) | — | Text assembles from drifting particles that scatter and reform on demand. |
| [RotatingText](https://reactbits.dev/text-animations/rotating-text) | `motion` | Cycles through multiple phrases with 3D rotate / flip transitions. |
| [ScrambledText](https://reactbits.dev/text-animations/scrambled-text) | `gsap` | Detects cursor position and applies a distortion effect to text. |
| [ScrollFloat](https://reactbits.dev/text-animations/scroll-float) | `gsap` | Text gently floats / parallax shifts on scroll. |
| [ScrollReveal](https://reactbits.dev/text-animations/scroll-reveal) | `gsap` | Text gently unblurs and reveals on scroll. |
| [ScrollVelocity](https://reactbits.dev/text-animations/scroll-velocity) | `motion` | Text marquee animatio - speed and distortion scale with user's scroll velocity. |
| [ShinyText](https://reactbits.dev/text-animations/shiny-text) | `motion` | Metallic sheen sweeps across text producing a reflective highlight. |
| [Shuffle](https://reactbits.dev/text-animations/shuffle) | `@gsap/react`, `gsap` | Animated text reveal where characters shuffle before settling. |
| [SplitFlapText](https://reactbits.dev/text-animations/split-flap-text) | — | Mechanical split-flap departure board that clacks through to each new phrase. |
| [SplitText](https://reactbits.dev/text-animations/split-text) | `@gsap/react`, `gsap` | Splits text into characters / words for staggered entrance animation. |
| [StrokeText](https://reactbits.dev/text-animations/stroke-text) | `gsap` | Outlined letterforms draw themselves on, then flood with fill. |
| [TextCursor](https://reactbits.dev/text-animations/text-cursor) | `motion` | Make any text element follow your cursor, leaving a trail of copies behind it. |
| [TextLoop](https://reactbits.dev/text-animations/text-loop) | `gsap` | A seamless text marquee that flows along curved SVG paths. |
| [TextPressure](https://reactbits.dev/text-animations/text-pressure) | — | Characters scale / warp interactively based on pointer pressure zone. |
| [TextType](https://reactbits.dev/text-animations/text-type) | `gsap` | Typewriter effect with blinking cursor and adjustable typing cadence. |
| [TrueFocus](https://reactbits.dev/text-animations/true-focus) | `motion` | Applies dynamic blur / clarity based over a series of words in order. |
| [VariableProximity](https://reactbits.dev/text-animations/variable-proximity) | `motion` | Letter styling changes continuously with pointer distance mapping. |
| [WarpText](https://reactbits.dev/text-animations/warp-text) | `ogl` | WebGL warp that bends and refracts the text around the pointer. |

## 动画 Animations（38）

| 组件 | 依赖 | 简介（官方英文） |
|------|------|------|
| [AnimatedContent](https://reactbits.dev/animations/animated-content) | `gsap` | Wrapper that animates any children on scroll or mount with configurable direction, distance, duration, easing and disappear options. |
| [Antigravity](https://reactbits.dev/animations/antigravity) | `@react-three/fiber`, `three` | 3D antigravity particle field that repels from the cursor with smooth motion. |
| [BlobCursor](https://reactbits.dev/animations/blob-cursor) | `gsap` | Organic blob cursor that smoothly follows the pointer with inertia and elastic morphing. |
| [ClickSpark](https://reactbits.dev/animations/click-spark) | — | Creates particle spark bursts at click position. |
| [Crosshair](https://reactbits.dev/animations/crosshair) | `gsap` | Custom crosshair cursor with tracking, and link hover effects. |
| [Cubes](https://reactbits.dev/animations/cubes) | `gsap` | 3D rotating cube cluster. Supports auto-rotation or hover interaction. |
| [CursorGrid](https://reactbits.dev/animations/cursor-grid) | — | Canvas grid whose cells light up around the cursor with configurable radius, falloff and click pulses. |
| [ElasticMesh](https://reactbits.dev/animations/elastic-mesh) | `ogl` | Spring-mesh surface that stretches under the pointer and settles back with damped physics. |
| [ElectricBorder](https://reactbits.dev/animations/electric-border) | — | Jittery electric energy border with animated arcs, glow and adjustable intensity. |
| [FadeContent](https://reactbits.dev/animations/fade-content) | `gsap` | Simple directional fade / slide entrance / exit wrapper with threshold-based activation. |
| [GhostCursor](https://reactbits.dev/animations/ghost-cursor) | `three` | Semi-transparent ghost cursor that smoothly follows the real cursor with a trailing effect. |
| [GlareHover](https://reactbits.dev/animations/glare-hover) | — | Adds a realistic moving glare highlight on hover over any element. |
| [GlowCursor](https://reactbits.dev/animations/glow-cursor) | `ogl` | Shader-powered light trail that smoothly follows the pointer with customizable glow, color, taper and pulse. |
| [GradualBlur](https://reactbits.dev/animations/gradual-blur) | — | Progressively un-blurs content based on scroll or trigger creating a cinematic reveal. |
| [HalftoneReveal](https://reactbits.dev/animations/halftone-reveal) | `ogl` | Print-style halftone dot matrix that resolves into sharp content around the cursor. |
| [ImageTrail](https://reactbits.dev/animations/image-trail) | `gsap` | Cursor-based image trail with several built-in variants. |
| [LaserFlow](https://reactbits.dev/animations/laser-flow) | `three` | Dynamic laser light that flows onto a surface, customizable effect. |
| [LogoLoop](https://reactbits.dev/animations/logo-loop) | — | Continuously looping marquee of brand or tech logos with seamless repeat and hover pause. |
| [MagicRings](https://reactbits.dev/animations/magic-rings) | `three` | Interactive magic rings effect with customizable parameters. |
| [Magnet](https://reactbits.dev/animations/magnet) | — | Elements magnetically ease toward the cursor then settle back with spring physics. |
| [MagnetLines](https://reactbits.dev/animations/magnet-lines) | — | Animated field lines bend toward the cursor. |
| [MetaBalls](https://reactbits.dev/animations/meta-balls) | `ogl` | Liquid metaball blobs that merge and separate with smooth implicit surface animation. |
| [MetallicPaint](https://reactbits.dev/animations/metallic-paint) | — | Liquid metallic paint shader which can be applied to SVG elements. |
| [Noise](https://reactbits.dev/animations/noise) | — | Animated film grain / noise overlay adding subtle texture and motion. |
| [OrbitImages](https://reactbits.dev/animations/orbit-images) | `motion` | SVG Path customizable orbiting images effect |
| [PixelSwap](https://reactbits.dev/animations/pixel-swap) | — | Pixel fragments assemble into a full cover, swap arbitrary content, then dissolve away with reversible colors and triggers. |
| [PixelTrail](https://reactbits.dev/animations/pixel-trail) | `@react-three/drei`, `@react-three/fiber`, `three` | Pixelated cursor trail emitting fading squares with retro digital feel. |
| [PixelTransition](https://reactbits.dev/animations/pixel-transition) | `gsap` | Pixel dissolve transition for content reveal on hover. |
| [Ribbons](https://reactbits.dev/animations/ribbons) | `ogl` | Flowing responsive ribbons/cursor trail driven by physics and pointer motion. |
| [RippleDistortion](https://reactbits.dev/animations/ripple-distortion) | `ogl` | Pointer-driven water displacement that warps content and leaves a decaying wake. |
| [ScrollExpand](https://reactbits.dev/animations/scroll-expand) | — | A rounded media frame that grows to full bleed as it scrolls through the viewport. |
| [ShapeBlur](https://reactbits.dev/animations/shape-blur) | `three` | Morphing blurred geometric shape. The effect occurs on hover. |
| [SplashCursor](https://reactbits.dev/animations/splash-cursor) | — | Liquid splash burst at cursor with curling ripples and waves. |
| [StarBorder](https://reactbits.dev/animations/star-border) | — | Animated star / sparkle border orbiting content with twinkle pulses. |
| [StickerPeel](https://reactbits.dev/animations/sticker-peel) | `gsap` | Sticker corner lift + peel interaction using 3D transform and shadow depth. |
| [Strands](https://reactbits.dev/animations/strands) | `ogl` | Glowing ribbon-like strands that ripple and weave across a transparent canvas. |
| [SwarmCursor](https://reactbits.dev/animations/swarm-cursor) | `ogl` | Flocking particle swarm that chases the pointer, jostles for space and drifts apart at rest. |
| [TargetCursor](https://reactbits.dev/animations/target-cursor) | `gsap` | A cursor follow animation with 4 corners that lock onto targets. |

## UI 组件 Components（45）

| 组件 | 依赖 | 简介（官方英文） |
|------|------|------|
| [AccordionGallery](https://reactbits.dev/components/accordion-gallery) | `gsap` | Panels expand on hover or focus, revealing parallax imagery and captions. |
| [AnimatedList](https://reactbits.dev/components/animated-list) | `motion` | List items enter with staggered motion variants for polished reveals. |
| [BorderGlow](https://reactbits.dev/components/border-glow) | — | Glowing mesh-gradient border that follows cursor direction and intensifies near edges. |
| [BounceCards](https://reactbits.dev/components/bounce-cards) | `gsap` | Cards bounce that bounce in on mount. |
| [BubbleMenu](https://reactbits.dev/components/bubble-menu) | `gsap` | Floating circular expanding menu with staggered item reveal. |
| [CardNav](https://reactbits.dev/components/card-nav) | `gsap`, `react-icons` | Expandable navigation bar with card panels revealing nested links. |
| [CardSwap](https://reactbits.dev/components/card-swap) | `gsap` | Cards animate position swapping with smooth layout transitions. |
| [Carousel](https://reactbits.dev/components/carousel) | `motion`, `react-icons` | Responsive carousel with touch gestures, looping and transitions. |
| [ChromaGrid](https://reactbits.dev/components/chroma-grid) | `gsap` | A responsive grid of grayscale tiles. Hovering the grid reaveals their colors. |
| [CircularGallery](https://reactbits.dev/components/circular-gallery) | `ogl` | Circular orbit gallery rotating images. |
| [Counter](https://reactbits.dev/components/counter) | `motion` | Flexible animated counter supporting increments + easing. |
| [CurvedInput](https://reactbits.dev/components/curved-input) | — | Arc-bent input bar with text, caret and submit button all following the curve. |
| [DecayCard](https://reactbits.dev/components/decay-card) | `gsap` | Hover parallax effect that disintegrates the content of a card. |
| [DepthCarousel](https://reactbits.dev/components/depth-carousel) | `gsap` | Cards recede into depth on a 3D rail, with drag, keyboard and auto-advance. |
| [Dock](https://reactbits.dev/components/dock) | `motion` | macOS style magnifying dock with proximity scaling of icons. |
| [DomeGallery](https://reactbits.dev/components/dome-gallery) | `@use-gesture/react` | Immersive 3D dome gallery projecting images on a hemispheric surface. |
| [DriftWall](https://reactbits.dev/components/drift-wall) | — | An endless perspective wall of tiles drifting past, lifting on hover. |
| [ElasticSlider](https://reactbits.dev/components/elastic-slider) | `@chakra-ui/react`, `motion`, `react-icons` | Slider handle stretches elastically then snaps with spring physics. |
| [FlowingMenu](https://reactbits.dev/components/flowing-menu) | `gsap` | Liquid flowing active indicator glides between menu items. |
| [FluidGlass](https://reactbits.dev/components/fluid-glass) | `@react-three/drei`, `@react-three/fiber`, `maath`, `three` | Glassmorphism container with animated liquid distortion refraction. |
| [FlyingPosters](https://reactbits.dev/components/flying-posters) | `ogl` | 3D posters rotate on scroll infinitely. |
| [Folder](https://reactbits.dev/components/folder) | — | Interactive folder opens to reveal nested content smooth motion. |
| [GlassIcons](https://reactbits.dev/components/glass-icons) | — | Icon set styled with frosted glass blur. |
| [GlassSurface](https://reactbits.dev/components/glass-surface) | — | Advanced Apple-style glass surface with real-time distortion + lighting. |
| [GooeyNav](https://reactbits.dev/components/gooey-nav) | — | Navigation indicator morphs with gooey blob transitions between items. |
| [InfiniteMenu](https://reactbits.dev/components/infinite-menu) | `gl-matrix` | Horizontally looping menu effect that scrolls endlessly with seamless wrap. |
| [InfiniteSpiral](https://reactbits.dev/components/infinite-spiral) | — | An endlessly looping 3D helix of images with customizable motion, depth, spacing and interaction. |
| [Lanyard](https://reactbits.dev/components/lanyard) | `@react-three/drei`, `@react-three/fiber`, `@react-three/rapier`, `meshline`, `three` | Swinging 3D lanyard / badge card with realistic inertial motion. |
| [LineSidebar](https://reactbits.dev/components/line-sidebar) | — | Static list navigation with a cursor-proximity effect that shifts and highlights nearby items. |
| [MagicBento](https://reactbits.dev/components/magic-bento) | `gsap` | Interactive bento grid tiles expand + animate with various options. |
| [Masonry](https://reactbits.dev/components/masonry) | `gsap` | Responsive masonry layout with animated reflow + gaps optimization. |
| [ModelViewer](https://reactbits.dev/components/model-viewer) | `@react-three/drei`, `@react-three/fiber`, `three` | Three.js model viewer with orbit controls and lighting presets. |
| [MorphSlider](https://reactbits.dev/components/morph-slider) | `gsap`, `ogl` | WebGL slider that melts between images with a displacement transition. |
| [OptionWheel](https://reactbits.dev/components/option-wheel) | — | Curved option picker that spins via scroll, drag, or arrow keys, fading and tilting items away from the selection. |
| [PillNav](https://reactbits.dev/components/pill-nav) | `gsap`, `react-router-dom` | Minimal pill nav with sliding active highlight + smooth easing. |
| [PixelCard](https://reactbits.dev/components/pixel-card) | — | Card content revealed through pixel expansion transition. |
| [ProfileCard](https://reactbits.dev/components/profile-card) | — | Animated profile card glare with 3D hover effect. |
| [ReflectiveCard](https://reactbits.dev/components/reflective-card) | `lucide-react` | Card with dynamic webcam reflection and glare effects that respond to cursor movement. |
| [ScrollStack](https://reactbits.dev/components/scroll-stack) | `lenis` | Overlapping card stack reveals on scroll with depth layering. |
| [SpecularButton](https://reactbits.dev/components/specular-button) | `ogl` | Glass button with a shader-driven specular rim light that sweeps around the edge and follows the cursor. |
| [SpotlightCard](https://reactbits.dev/components/spotlight-card) | — | Dynamic spotlight follows cursor casting gradient illumination. |
| [Stack](https://reactbits.dev/components/stack) | `motion` | Layered stack with swipe animations, autoplay and smooth transitions. |
| [StaggeredMenu](https://reactbits.dev/components/staggered-menu) | `gsap` | Menu with staggered item animations and smooth transitions on open/close. |
| [Stepper](https://reactbits.dev/components/stepper) | `motion` | Animated multi-step progress indicator with active state transitions. |
| [TiltedCard](https://reactbits.dev/components/tilted-card) | `motion` | 3D perspective tilt card reacting to pointer. |

## 背景 Backgrounds（56）

| 组件 | 依赖 | 简介（官方英文） |
|------|------|------|
| [AcidSquares](https://reactbits.dev/backgrounds/acid-squares) | `ogl` | A crystalline corridor of stacked squares receding into depth. |
| [AeroShards](https://reactbits.dev/backgrounds/aero-shards) | `vgpu` | A GPU-driven wind sculpture of folded foil shards with crisp detail, content-safe placements, and responsive pointer interactions. |
| [Aurora](https://reactbits.dev/backgrounds/aurora) | `ogl` | Flowing aurora gradient background. |
| [Balatro](https://reactbits.dev/backgrounds/balatro) | `ogl` | The balatro shader, fully customizalbe and interactive. |
| [Ballpit](https://reactbits.dev/backgrounds/ballpit) | `three` | Physics ball pit simulation with bouncing colorful spheres. |
| [Beams](https://reactbits.dev/backgrounds/beams) | `@react-three/drei`, `@react-three/fiber`, `three` | Crossing animated ribbons with customizable properties. |
| [ColorBends](https://reactbits.dev/backgrounds/color-bends) | `three` | Vibrant color bends with smooth flowing animation. |
| [CRTWarp](https://reactbits.dev/backgrounds/crt-warp) | `three` | Full-canvas CRT plasma with curved distortion, scanlines, bloom and pointer interaction. |
| [DarkVeil](https://reactbits.dev/backgrounds/dark-veil) | `ogl` | Subtle dark background with a smooth animation and postprocessing. |
| [Dither](https://reactbits.dev/backgrounds/dither) | `@react-three/fiber`, `@react-three/postprocessing`, `postprocessing`, `three` | Retro dithered noise shader background. |
| [DotField](https://reactbits.dev/backgrounds/dot-field) | — | Interactive dot grid with cursor bulge, glow, sparkle, and wave effects. |
| [DotGrid](https://reactbits.dev/backgrounds/dot-grid) | `gsap` | Animated dot grid with cursor interactions. |
| [EvilEye](https://reactbits.dev/backgrounds/evil-eye) | `ogl` | Procedural evil eye shader with animated iris, slit pupil, and fiery outer glow. |
| [FaultyTerminal](https://reactbits.dev/backgrounds/faulty-terminal) | `ogl` | Terminal CRT scanline squares effect with flicker + noise. |
| [Ferrofluid](https://reactbits.dev/backgrounds/ferrofluid) | `ogl` | A churning magnetic fluid traced by glowing contour lines, with a cursor magnet. |
| [FloatingLines](https://reactbits.dev/backgrounds/floating-lines) | `three` | 3D floating lines that react to cursor movement. |
| [Galaxy](https://reactbits.dev/backgrounds/galaxy) | `ogl` | Parallax realistic starfield with pointer interactions. |
| [GhostFibers](https://reactbits.dev/backgrounds/ghost-fibers) | `ogl` | A deep-blue recursive fiber field with luminous bands, radial twisting and soft atmospheric glow. |
| [GradientBlinds](https://reactbits.dev/backgrounds/gradient-blinds) | `ogl` | Layered gradient blinds with spotlight and noise distortion. |
| [GradientWaves](https://reactbits.dev/backgrounds/gradient-waves) | `ogl` | Raymarched sine waves rolling toward a soft, hazy horizon. |
| [Grainient](https://reactbits.dev/backgrounds/grainient) | `ogl` | Grainy gradient swirls with soft wave distortion. |
| [GridDistortion](https://reactbits.dev/backgrounds/grid-distortion) | `three` | Warped grid mesh distorts smoothly reacting to cursor. |
| [GridMotion](https://reactbits.dev/backgrounds/grid-motion) | `gsap` | Perspective moving grid lines based on cusror position. |
| [GridScan](https://reactbits.dev/backgrounds/grid-scan) | `face-api.js`, `postprocessing`, `three` | Animated grid room 3D scan effect and cool interactions. |
| [Hyperspeed](https://reactbits.dev/backgrounds/hyperspeed) | `postprocessing`, `three` | Animated lines continuously moving to simulate hyperspace travel on click hold. |
| [Iridescence](https://reactbits.dev/backgrounds/iridescence) | `ogl` | Slick iridescent shader with shifting waves. |
| [LetterGlitch](https://reactbits.dev/backgrounds/letter-glitch) | — | Matrix style letter animation. |
| [Lightfall](https://reactbits.dev/backgrounds/lightfall) | `ogl` | Colorful light streaks raining down a glowing tunnel with a cursor light. |
| [Lightning](https://reactbits.dev/backgrounds/lightning) | — | Procedural lightning bolts with branching and glow flicker. |
| [LightPillar](https://reactbits.dev/backgrounds/light-pillar) | `three` | Vertical pillar of light with glow effects. |
| [LightRays](https://reactbits.dev/backgrounds/light-rays) | `ogl` | Volumetric light rays/beams with customizable direction. |
| [LightTunnel](https://reactbits.dev/backgrounds/light-tunnel) | `ogl` | A radial fibre-optic tunnel with light pulses racing into depth. |
| [LineWaves](https://reactbits.dev/backgrounds/line-waves) | `ogl` | Animated line wave pattern with colorful warped distortion. |
| [LiquidChrome](https://reactbits.dev/backgrounds/liquid-chrome) | `ogl` | Liquid metallic chrome shader with flowing reflective surface. |
| [LiquidEther](https://reactbits.dev/backgrounds/liquid-ether) | `three` | Interactive liquid shader with flowing distortion and customizable colors. |
| [MoltenMetal](https://reactbits.dev/backgrounds/molten-metal) | `ogl` | Swirling caustic plasma filaments with molten, white-hot cores. |
| [Orb](https://reactbits.dev/backgrounds/orb) | `ogl` | Floating energy orb with customizable hover effect. |
| [Particles](https://reactbits.dev/backgrounds/particles) | `ogl` | Configurable particle system. |
| [PixelBlast](https://reactbits.dev/backgrounds/pixel-blast) | `postprocessing`, `three` | Exploding pixel particle bursts with optional liquid postprocessing. |
| [PixelSnow](https://reactbits.dev/backgrounds/pixel-snow) | `three` | Falling pixelated snow effect with customizable density and speed. |
| [Plasma](https://reactbits.dev/backgrounds/plasma) | `ogl` | Organic plasma gradients swirl + morph with smooth turbulence. |
| [PlasmaWave](https://reactbits.dev/backgrounds/plasma-wave) | `ogl` | Raymarched plasma waves with dual-wave interference and OGL. |
| [Prism](https://reactbits.dev/backgrounds/prism) | `ogl` | Rotating prism with configurable intensity, size, and colors. |
| [PrismaticBurst](https://reactbits.dev/backgrounds/prismatic-burst) | `ogl` | Burst of light rays with controllable color, distortion, amount. |
| [Radar](https://reactbits.dev/backgrounds/radar) | `ogl` | Radar sweep effect with concentric rings, radial spokes, and a rotating beam. |
| [RippleGrid](https://reactbits.dev/backgrounds/ripple-grid) | `ogl` | A grid that continuously animates with a ripple effect. |
| [Scanner](https://reactbits.dev/backgrounds/scanner) | `ogl` | Calm interference bands sweeping across the screen like an oscilloscope. |
| [ShapeGrid](https://reactbits.dev/backgrounds/shape-grid) | — | Animated grid with shape variants (square, hexagon, circle, triangle) + direction customization. |
| [SideRays](https://reactbits.dev/backgrounds/side-rays) | `ogl` | Animated light rays emanating from the side with customizable colors and speed. |
| [Silk](https://reactbits.dev/backgrounds/silk) | `@react-three/fiber`, `three` | Smooth waves background with soft lighting. |
| [SlicedWaves](https://reactbits.dev/backgrounds/sliced-waves) | `ogl` | A grid of soft glowing bars rippling like a slatted equalizer. |
| [SoftAurora](https://reactbits.dev/backgrounds/soft-aurora) | `ogl` | Soft aurora borealis shader with 3D Perlin noise and cosine gradient palettes. |
| [Threads](https://reactbits.dev/backgrounds/threads) | `ogl` | Animated pattern of lines forming a fabric-like motion. |
| [Topography](https://reactbits.dev/backgrounds/topography) | `ogl` | A living contour map with glowing, elevation-tinted lines. |
| [Waves](https://reactbits.dev/backgrounds/waves) | — | Layered lines that form smooth wave patterns with animation. |
| [WebThreads](https://reactbits.dev/backgrounds/web-threads) | `ogl` | Glowing sine threads woven through a luminous convergence point. |
