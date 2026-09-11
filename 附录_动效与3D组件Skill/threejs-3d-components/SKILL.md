---
name: "threejs-3d-components"
description: "3D/WebGL 组件目录与安装引导（threeui 104 个 Three.js shader 组件 + React Three Fiber / drei 生态速查）。当用户要做 3D hero、WebGL 背景、shader 效果、Three.js 沉浸式网站，或提到 threeui、R3F、react-three-fiber、drei 时使用。"
---

# threejs-3d-components

网页需要真 3D（Three.js/WebGL）时的**选型 + 安装引导**，覆盖三个层次：

1. **threeui**：Design+Code 的 3D shader 组件库（Community 版 MIT），npm 即装即用，最快出效果
2. **React Three Fiber + drei**：声明式搭建定制 3D 场景的事实标准
3. **原生 three.js**：完全控制，R3F 不满足时再用

## 何时调用

- 用户要"3D 首屏 / WebGL 背景 / shader 动效 / 沉浸式滚动网站"
- 用户点名 threeui、R3F、react-three-fiber、drei
- react-bits 的单个背景组件满足不了，需要成体系 3D 方案时

不适用：常规 2D 动效（文字动画、跑马灯、过渡）→ 用 `animated-components` 技能。

## 选型逻辑

| 场景 | 选择 |
|------|------|
| 要现成的 3D hero/背景/按钮，快出效果 | threeui（npm 装完即用，104 个条目含完整落地页） |
| 场景需要定制建模、交互逻辑、动画编排 | R3F + drei |
| 非 React 项目 / 需要极限性能与自定义渲染管线 | 原生 three.js |
| 只是静态渐变/噪点背景 | 别上 3D，CSS 或 react-bits 的轻量组件即可 |

## threeui 安装

```bash
npm install @designcodeio/threeui
```

```tsx
import { AtTheHorizon } from "@designcodeio/threeui";
import "@designcodeio/threeui/style.css";   // 必须！共享样式，漏了渲染异常
```

完整组件清单（按分类 + npm 导出名）→ [references/threeui-catalog.md](references/threeui-catalog.md)。
要改 shader 源码时用 CLI 拉源文件进项目：`npx @designcodeio/threeui-cli add <组件id>`（OAuth 登录）。
边界：本目录只含 Community（MIT）；官网另有 Pro 付费版（全站共 378 个），商用注意区分。

## R3F 起步与 drei 速查

```bash
npm install three @react-three/fiber @react-three/drei
```

- R3F 版本与 React 大版本对应（v8 ↔ React 18，v9 ↔ React 19），以官方文档为准
- drei 的 helper 分类速查（相机/控制/材质/staging/性能等）→ [references/r3f-drei-catalog.md](references/r3f-drei-catalog.md)
- drei 使用独立的 `three-stdlib` 而非 `three/examples/jsm`，一般无需手动处理

## 性能与降级（3D 场景必查清单）

- **WebGL 可用性检测**：不可用时给静态图/渐变降级，不能白屏
- **移动端**：`dpr` 限制在 `[1, 2]`，移动端关掉重后处理；全屏 shader 场景注意发热与掉帧
- **懒加载**：3D 场景用 `React.lazy` + IntersectionObserver，滚到可视区再挂载
- **`prefers-reduced-motion`**：装饰性 3D 动画要停或降级为静态帧
- **一个页面一个 Canvas**：多个 WebGL 上下文（threeui 组件 + react-bits ogl 背景 + 手写 three）会互相挤爆显存，同类只留一个
- 3D 是装饰不是内容：关键信息必须有 DOM 文本兜底（SEO + 可访问性）

## 常见坑

- threeui 忘引 `style.css` 是最高频错误
- three 版本与 R3F/drei 的兼容矩阵要对齐，锁版本升级
- Next.js SSR 下 Canvas 要 `"use client"`，drei 的 `Html` 组件只在客户端渲染
- shader 组件多为全屏绝对定位，注意与页面内容的层级（z-index）和事件穿透（pointer-events）
