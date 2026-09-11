# Magic UI 组件全量目录

> 数据来源：[magicuidesign/magicui](https://github.com/magicuidesign/magicui)（~21k⭐，MIT）
> 抓取日期：2026-09-08，共 **78 个组件**（以 [magicui.design](https://magicui.design) 为准）。

## 安装方式

前提：React/Next.js + Tailwind 项目，且已初始化 shadcn：

```bash
npx shadcn@latest init            # 每个项目仅一次
npx shadcn@latest add @magicui/<slug>   # slug 见下表
# 等价写法：npx shadcn@latest add https://magicui.design/r/<slug>
```

默认安装路径 `@/components/ui/<slug>`。若文档提示需要额外 CSS keyframes，务必同步加入 `globals.css`。

## 高频组件（按用途家族精选）

- **跑马灯/社交证明**：`marquee`、`avatar-circles`、`bento-grid`
- **Hero 视觉锚点**：`globe`、`warp-background`、`animated-grid-pattern`、`retro-grid`
- **文字动画**：`animated-shiny-text`、`aurora-text`、`number-ticker`、`text-animate`、`blur-fade`
- **按钮/边框发光**：`shimmer-button`、`border-beam`、`magic-card`、`shine-border`
- **滚动显现**：`blur-fade`、`scroll-progress`
- **氛围背景**：`particles`、`dot-pattern`、`grid-pattern`、`flickering-grid`、`meteors`、`sparkles-text`

## 全量组件表（按字母序）

| slug（安装名） | 组件 | 依赖 | 简介（官方英文） |
|------|------|------|------|
| `android` | Android | — | A mockup of an Android device. |
| `animated-beam` | Animated Beam | `motion` | An animated beam of light which travels along a path. Useful for showcasing the integration features of a website. |
| `animated-circular-progress-bar` | Animated Circular Progress Bar | — | Animated Circular Progress Bar is a component that displays a circular gauge with a percentage value. |
| `animated-gradient-text` | Animated Gradient Text | — | An animated gradient background which transitions between colors for text. |
| `animated-grid-pattern` | Animated Grid Pattern | `motion` | A animated background grid pattern made with SVGs, fully customizable using Tailwind CSS. |
| `animated-list` | Animated List | `motion` | A list that animates each item in sequence with a delay. Used to showcase notifications or events on your landing page. |
| `animated-shiny-text` | Animated Shiny Text | — | A light glare effect which pans across text making it appear as if it is shimmering. |
| `animated-theme-toggler` | Theme Toggler | `lucide-react` | Theme toggle with View Transitions and animated clip-path masks (circle, polygons, star), optional viewport-centered origin. |
| `aurora-text` | Aurora Text | — | A beautiful aurora text effect |
| `avatar-circles` | Avatar Circles | — | Overlapping circles of avatars. |
| `backlight` | Backlight | — | A backlight glow effect for videos, images, and SVGs. |
| `bento-grid` | Bento Grid | `@radix-ui/react-icons` | Bento grid is a layout used to showcase the features of a product in a simple and elegant way. |
| `blur-fade` | Blur Fade | `motion` | Blur fade in and out animation. Used to smoothly fade in and out content. |
| `border-beam` | Border Beam | `motion` | An animated beam of light which travels along the border of its container. |
| `client-tweet-card` | Client Tweet Card | `react-tweet` | A client-side version of the tweet card that displays a tweet with the author's name, handle, and profile picture. |
| `code-comparison` | Code Comparison | `shiki`, `next-themes` | A component which compares two code snippets. |
| `comic-text` | Comic Text | `motion` | Comic text animation |
| `confetti` | Confetti | `canvas-confetti`, `@types/canvas-confetti` | Confetti animations are best used to delight your users when something special happens |
| `cool-mode` | Cool Mode | — | Cool mode effect for buttons, links, and other DOMs |
| `dia-text-reveal` | Dia Text Reveal | `motion` | A horizontal color band sweeps across text, revealing a gradient shine before settling on the base color. |
| `dock` | Dock | `motion` | An implementation of the MacOS dock using react + tailwindcss + motion |
| `dot-pattern` | Dot Pattern | — | A background dot pattern made with SVGs, fully customizable using Tailwind CSS. |
| `dotted-map` | Dotted Map | `svg-dotted-map` | A component with a dotted map. |
| `file-tree` | File Tree | — | A component used to showcase the folder and file structure of a directory. |
| `flickering-grid` | Flickering Grid | — | A flickering grid background made with SVGs, fully customizable using Tailwind CSS. |
| `floating-3d-particles` | Floating 3D Particles | — | A canvas-based pseudo-3D particle field with perspective projection, continuous rotation and buoyant drift. |
| `glare-hover` | Glare Hover | — | A diagonal glare on hover using a ::before gradient and CSS variables (angle, size, duration, color). |
| `globe` | Globe | `cobe@^0.6.4`, `motion` | An autorotating, interactive, and highly performant globe made using WebGL. |
| `glyph-matrix` | Glyph Matrix | — | An animated grid of subtly shifting glyphs with fade effect and theme support. |
| `grid-pattern` | Grid Pattern | — | A background grid pattern made with SVGs, fully customizable using Tailwind CSS. |
| `hero-video-dialog` | Hero Video Dialog | `motion` | A hero video dialog component. |
| `hexagon-pattern` | Hexagon Pattern | — | A background hexagon pattern made with SVGs, fully customizable using Tailwind CSS. |
| `highlighter` | Highlighter | `motion`, `rough-notation` | A text highlighter that mimics the effect of a human-drawn marker stroke. |
| `hyper-text` | Hyper Text | `motion` | A text animation that scrambles letters before revealing the final text. |
| `icon-cloud` | Icon Cloud | `lucide-react` | An interactive 3D tag cloud component |
| `interactive-grid-pattern` | Interactive Grid Pattern | — | A interactive background grid pattern made with SVGs, fully customizable using Tailwind CSS. |
| `interactive-hover-button` | interactive-hover-button | — |  |
| `iphone` | iPhone | — | A mockup of the iPhone |
| `kinetic-text` | Kinetic Text | — | A text component that animates font weight of characters on hover. |
| `lens` | Lens | `motion` | A interactive component that enables zooming into images, videos and other elements. |
| `light-rays` | Light Rays | `motion` | A component with animated light rays which shine down from above. |
| `line-shadow-text` | Line Shadow Text | `motion` | A text component with a moving line shadow. |
| `magic-card` | Magic Card | `motion`, `next-themes` | A spotlight effect that follows your mouse cursor and highlights borders on hover. |
| `marquee` | Marquee | — | An infinite scrolling component that can be used to display text, images, or videos. |
| `meteors` | Meteors | — | A meteor shower effect. |
| `morphing-text` | Morphing Text | — | A dynamic text morphing component for Magic UI. |
| `neon-gradient-card` | Neon Gradient Card | — | A beautiful neon card effect |
| `noise-texture` | Noise Texture | — | An SVG fractal noise layer using feTurbulence, desaturation, and contrast controls for subtle texture overlays. |
| `number-ticker` | Number Ticker | `motion` | Animate numbers to count up or down to a target number |
| `orbiting-circles` | Orbiting Circles | — | A collection of circles which move in orbit along a circular path |
| `particles` | Particles | — | Particles are a fun way to add some visual flair to your website. They can be used to create a sense of depth, movement, and interactivity. |
| `pixel-image` | Pixel Image | — | A component that displays an image with a pixelated effect, creating a retro aesthetic. |
| `pointer` | Pointer | `motion` | A component that displays a pointer when hovering over an element |
| `progressive-blur` | Progressive Blur | — | The Progressive Blur component adds a smooth blur gradient effect to scrollable content, indicating more content below or above. |
| `pulsating-button` | Pulsating Button | — | An animated pulsating button useful for capturing attention of users. |
| `rainbow-button` | Rainbow Button | — | An animated button with a rainbow effect. |
| `retro-grid` | Retro Grid | — | An animated scrolling retro grid effect |
| `ripple` | Ripple | — | An animated ripple effect typically used behind elements to emphasize them. |
| `ripple-button` | Ripple Button | — | An animated button with ripple useful for user engagement. |
| `safari` | Safari | — | A safari browser mockup to showcase your website. |
| `scroll-based-velocity` | Scroll Based Velocity | `motion` | Scrolling text whose speed changes based on scroll speed |
| `scroll-progress` | Scroll Progress | `motion` | Animated Scroll Progress for your pages |
| `shimmer-button` | Shimmer Button | — | A button with a shimmering light which travels around the perimeter. |
| `shine-border` | Shine Border | — | Shine border is an animated background border effect. |
| `shiny-button` | Shiny Button | `motion` | A shiny button component with dynamic styles in the dark mode or light mode. |
| `smooth-cursor` | smooth-cursor | `motion` | A customizable, physics-based smooth cursor animation component with spring animations and rotation effects |
| `sparkles-text` | Sparkles Text | `motion` | A dynamic text that generates continuous sparkles with smooth transitions, perfect for highlighting text with animated stars. |
| `spinning-text` | Spinning Text | `motion` | The Spinning Text component animates text in a circular motion with customizable speed, direction, color, and transitions for dynamic and engaging effects. |
| `striped-pattern` | Striped Pattern | — | A background striped pattern made with SVGs, fully customizable using Tailwind CSS. |
| `terminal` | Terminal | — | A terminal component |
| `text-3d-flip` | Text 3D Flip | `motion` | A text effect that flips each letter in 3D with a staggered animation on hover. |
| `text-animate` | Text Animate | `motion` | A text animation component that animates text using a variety of different animations. |
| `text-reveal` | Text Reveal | `motion` | Fade in text as you scroll down the page. |
| `tweet-card` | Tweet Card | `react-tweet` | A card that displays a tweet with the author's name, handle, and profile picture. |
| `typing-animation` | Typing Animation | `motion` | Characters appearing in typed animation |
| `video-text` | Video Text | — | A component that displays text with a video playing in the background. |
| `warp-background` | Warp Background | `motion` | A card with a time warping background effect. |
| `word-rotate` | Word Rotate | `motion` | A vertical rotation of words |
