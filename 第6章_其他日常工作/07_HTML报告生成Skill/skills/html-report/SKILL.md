---
name: "html-report"
description: "将任意内容（调研、分析、研究总结）生成专业级单文件 HTML 报告。当用户要求生成 HTML 报告、可视化报告、网页版报告、行业调研报告，或要求把内容做成带目录导航和图表的网页时调用。"
---

# html-report

将任意内容输出为专业、清洁、可视化程度高、易读性强的单文件 HTML 报告。

## 何时调用

当出现以下任一场景时调用本技能：

- 用户要求生成「HTML 报告」「网页报告」「可视化报告」「网页版报告」
- 用户要求把调研、分析、研究内容做成「带目录的网页」
- 用户要求生成「行业调研报告」「市场分析报告」且希望以 HTML 形式交付
- 用户明确提到「左边目录，右边内容」「带图表的网页报告」
- 用户要求报告「可以在浏览器中标注/批注」

以下场景**不要**调用本技能：

- 主要交付物是 Word/PDF/PPT（用 `document-master` 或 `昊鼎经营分析`）
- 主要交付物是幻灯片演示（用 `frontend-slides`）
- 纯代码开发或数据处理任务

---

## 核心能力

基于 `assets/template.html` 生成单文件 HTML 报告，具备：

1. **左目录 + 右内容**：sticky 侧栏自动生成目录，滚动时高亮当前章节，移动端可折叠。
2. **专业排版**：渐变头图、圆角卡片、指标卡、表格、引用块、代码块，中文优先字体栈。
3. **可视化图表**：纯 SVG 原生 JS（柱状/折线/饼图/雷达/散点），零依赖，带 tooltip、图例切换、范围筛选。
4. **图示系统**：产业链三列、生命周期、金字塔梯队、流程链、思维导图等结构化图示。
5. **浏览器标注**：双功能——画笔涂鸦（拖动鼠标画轨迹）+ 文字高亮（选中文字高亮），四色可选，点击高亮即删除，localStorage 自动持久化。
6. **响应式**：三档断点（1180/900/640px），适配桌面、平板、手机。
7. **可换肤**：CSS 变量 `:root`，改一处即全局换色。

---

## 标准工作流

### Step 1：明确报告内容

确认：
- 报告标题、副标题、日期/作者等元信息
- 内容来源（用户提供素材，或 Agent 自行生成调研内容）
- 需要的图表类型与数据

### Step 2：读取模板

读取本技能目录下的 `assets/template.html`，理解其结构：

```
<head>
  <style> ... 设计系统 + 标注样式 ... </style>
</head>
<body>
  <div class="shell">
    <header class="hero"> ... 标题/meta（Agent 编辑）... </header>
    <div class="layout">
      <aside class="sidebar"> ... 目录（JS 自动生成）... </aside>
      <main class="content">
        <div id="metric-grid"></div>           ← 指标卡容器
        ... Agent 在此填入章节 HTML ...
      </main>
    </div>
  </div>
  <script>
    const REPORT_DATA = { ... };   ← 图表数据（Agent 编辑）
    const REF_LINKS = { ... };     ← 参考链接（Agent 编辑）
    function renderMetrics() { ... 指标卡数组（Agent 编辑）... }
    ... 图表/图示/目录/标注引擎（保持不动）...
  </script>
</body>
```

### Step 3：填充内容

按以下规范修改模板的四个位置：

#### A. Hero 头部（`<header class="hero">`）

```html
<header class="hero">
  <h1>报告标题</h1>
  <p>副标题或一句话摘要</p>
  <div class="meta">
    <span class="chip">研究时间：2026 年 X 月</span>
    <span class="chip">作者：XXX</span>
  </div>
</header>
```

#### B. 章节正文（`<main class="content">` 内）

在 `<div id="metric-grid">` 容器之后、`</main>` 之前填入章节。使用标准 HTML 标签：

| 元素 | 写法 | 说明 |
|------|------|------|
| 一级标题 | `<h1 id="section-id">标题</h1>` | 自动进入目录 |
| 二级标题 | `<h2 id="subsection-id">标题</h2>` | 自动进入目录 |
| 三级标题 | `<h3 id="h3-id">标题</h3>` | 进入目录（缩进显示） |
| 段落 | `<p>...</p>` | |
| 列表 | `<ul><li>...</li></ul>` 或 `<ol>` | |
| 表格 | `<div class="table-wrap"><table>...</table></div>` | 外层必须包 `.table-wrap` |
| 引用 | `<blockquote>...</blockquote>` | |
| 分隔线 | `<hr>` | |

#### C. 图表

在正文中放置图表占位：

```html
<h3 class="figure-title">图N 图表名称</h3>
<div id="figN" class="chart-root figure-card" data-chart="barline"></div>
```

`data-chart` 取值：`barline`（柱状/折线，可混排）、`pie`（饼图/环形）、`radar`（雷达）、`scatter`（散点）。

在 `<script>` 的 `REPORT_DATA` 中配置对应数据：

```js
const REPORT_DATA = {
  figN: {
    labels: ['2020','2021','2022','2023'],
    series: [
      { name: '市场规模(亿元)', type: 'bar', data: [82,97,114,136], color: '#2563eb' },
      { name: '增速(%)', type: 'line', data: [null,18.3,17.5,19.3], color: '#f97316', yAxis: 1 }
    ]
  }
};
```

各图表类型的数据结构详见 `assets/template.html` 中 `REPORT_DATA` 的示例。

#### D. 指标卡

修改 `renderMetrics()` 函数内的数组：

```js
function renderMetrics() {
  const grid = document.getElementById('metric-grid');
  clear(grid);
  [
    ['指标名', '数值', '说明'],
    ...
  ].forEach(item => { ... });
}
```

#### E. 参考链接（可选）

正文中的引用用 `<a class="anchor-link">Sn</a>`，在 `REF_LINKS` 配置：

```js
const REF_LINKS = {
  S1: { url: 'https://...', label: '来源名称' }
};
```

### Step 4：交付

将填充后的完整 HTML 写入 `.html` 单文件交付。模板为单文件零依赖，无需任何外部资源。

---

## 标注功能（模板内置）

报告内置浏览器标注能力，**无需 Agent 编写任何代码**：

- **激活标注**：右下角悬浮工具栏，点击「标注」按钮开启标注模式。
- **高亮**：选中正文文本 → 点工具栏四色按钮之一（黄/绿/蓝/粉）→ 文字高亮。
- **批注**：点击已有高亮 → 弹出浮层 → 输入批注 → 保存。
- **持久化**：localStorage 自动保存，刷新页面不丢失。
- **导出/导入**：工具栏支持导出标注 JSON、导入 JSON 恢复、清除全部。
- **标注列表**：工具栏「列表」按钮展开侧边面板，列出全部标注，点击跳转。

标注数据结构：`localStorage["html-report:annotations:{页面路径}"]`，值为 `{ html, notes }`。

---

## 设计原则

1. **零依赖单文件**：所有 CSS/JS 内联，不依赖任何外部库或 CDN。
2. **数据结构优先**：报告 = `REPORT_DATA`(JSON) + `<main>`(HTML) + `<header>`(元信息)。Agent 只需填这三处。
3. **中文优先排版**：字体栈 `-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`，行高 1.8+。
4. **可换肤**：改 `:root` 的 `--brand-primary` / `--brand-secondary` / `--brand-accent` 即全局换色。
5. **响应式**：三档断点自动适配，移动端目录可折叠。
6. **专业清洁**：留白充足、层级清晰、卡片化布局、低饱和配色。

---

## 文件清单

```
html-report/
├── SKILL.md              # 本文件
└── assets/
    └── template.html     # 完整 HTML 模板
```

按需可扩展 `scripts/`（辅助脚本）、`references/`（设计参考）。
