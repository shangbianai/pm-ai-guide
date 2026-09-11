---
name: "animated-components"
description: "2D 动效组件库目录与安装引导（react-bits 171 个组件 + Magic UI 78 个组件）。当用户要做落地页、营销站、个人主页、dashboard 的动效（文字动画、跑马灯、粒子背景、发光按钮、滚动显现），或提到 react-bits、Magic UI、动画组件、shadcn 动效、marquee、打字机效果时使用。"
---

# animated-components

给网页加动效时，优先从现成组件库选装，而不是手写 Framer Motion / GSAP。本技能是两个免费组件库的**全量目录 + 安装引导**：

- **react-bits**：171 个组件，量大面广，含大量 WebGL/shader 背景，极简依赖
- **Magic UI**：78 个组件，shadcn 生态正统，组件风格更"商务克制"

## 何时调用

- 用户要"炫酷的落地页 / hero 动效 / 文字动画 / 粒子背景 / 好看的按钮"
- 用户点名 react-bits、Magic UI，或拿两者组件截图/名称来问
- 页面已用 shadcn/ui + Tailwind，需要补充动效层

不适用：纯 3D 场景/WebGL 沉浸式网站 → 用 `threejs-3d-components` 技能；动效方向的艺术决策 → 配合 `frontend-design` 技能。

## 选型逻辑

| 场景 | 选择 |
|------|------|
| 要 shader/WebGL 背景、大量花活（粒子、液体、故障艺术） | react-bits（ogl 系背景是它的强项） |
| 项目已用 shadcn/ui，要克制、专业的动效 | Magic UI（registry 无缝集成） |
| 两个库都有同类组件（如 marquee、animated list、grid 背景） | **只选一个**，同一页面不要混搭两库实现同一种效果 |
| 需要完全定制的时间线/滚动叙事动画 | 不用组件库，直接写 motion / gsap |

动效密度原则（继承自 frontend-design）：一屏只保留一个视觉焦点级动效；大面积背景动效 + 多处文字动画同屏 = 典型 AI 生成感。装饰性动画必须响应 `prefers-reduced-motion`。

## 安装流程

1. 确认前提：React + Tailwind 项目；Magic UI 还需先 `npx shadcn@latest init`
2. 查目录选组件（重要：先读目录再动手，避免重造已有组件）：
   - react-bits → [references/react-bits-catalog.md](references/react-bits-catalog.md)
   - Magic UI → [references/magicui-catalog.md](references/magicui-catalog.md)
3. 用 CLI 安装（命令见各目录头部），或从官网复制源码
4. 按目录中的「依赖」列补装外部依赖（react-bits 的 `ogl`/`gsap`/`motion`/`three` 等按组件而非全量安装）
5. 集成时保持组件 API 不动，用 props / className 定制，不改内部实现（否则失去升级能力）

## 常见坑

- **Magic UI 的 CSS keyframes**：组件依赖的 `@keyframes` 要进 `globals.css`，漏掉则动画不生效
- **Tailwind v3 vs v4**：TW 变体组件的写法跟 Tailwind 大版本相关，装错版本类名不生效；用 CSS 变体（`-CSS`）可绕开
- **react-bits 用 `motion` 包而非 `framer-motion`**：新组件依赖写的是 `motion`（同一作者的后继包），别装错
- **`cn()` 工具函数**：Magic UI 组件依赖 `lib/utils.ts` 里的 `cn()`，shadcn init 过的项目已有，裸项目要手动补
- **WebGL 背景（ogl 系）**：注意移动端性能与 WebGL 不可用时的静态降级；一个页面最多一个全屏 WebGL 背景

## 许可证

- react-bits：MIT + Commons Clause——个人和商业项目免费使用，禁止把库本身打包出售
- Magic UI：MIT
