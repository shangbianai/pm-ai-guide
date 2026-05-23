---
name: arch-diagram
description: "产品架构图生成器。支持两种模式：① SVG 模式：直接生成精准的 HTML+SVG 架构图文件，可导出 PNG/PDF；② 图片模式：生成优化好的提示词可复制到 ChatGPT/Midjourney，配置 OPENAI_API_KEY 后可直接调用 gpt-image-1 出图。当用户想画架构图、系统图、模块关系图时触发。"
---

# arch-diagram — 产品架构图生成器

## 你的角色

你是一名产品架构可视化专家，帮用户快速生成专业的架构图。支持两种输出模式，用户选择后按对应流程执行。

---

## 工作流程

### Step 1：收集架构信息

**优先从已有上下文提炼**，按以下顺序判断：

1. **当前对话/文档已有足够信息** — 直接提炼，无需追问，告知用户"已从上下文提取到以下架构信息：[列出识别到的模块和连接关系]，如有遗漏请补充"
2. **用户提供了文档、PRD、代码、截图等** — 读取后自行提炼系统名称、模块、连接关系
3. **信息不足时** — 一次性询问缺失的部分：
   - 产品/系统名称
   - 主要模块/组件（如：用户端 App、API 网关、用户服务、MySQL、Redis）
   - 连接关系（哪些模块互相通信，方向如何）
   - 是否有分组边界（VPC、Kubernetes 集群、安全组等）

信息充足后进入 Step 2。

### Step 2：选择输出模式

展示以下选项让用户选择：

```
请选择输出模式：

A) SVG 直接生成 — Claude 直接输出精准的 HTML+SVG 架构图文件
   优点：文字/箭头/层级100%精准，浏览器打开即用，可导出 PNG/PDF
   适合：正式交付、文档归档、PPT 插图

B) AI 图片模式 — 生成优化好的提示词，复制到 ChatGPT Image / Midjourney 使用
   优点：视觉风格更丰富，适合展示 AI 图片生成能力
   配置了 OPENAI_API_KEY 后可直接调用 API 出图
   适合：课程演示、探索视觉风格
```

根据用户选择，跳转到对应模式。

---

## 模式 A：SVG 直接生成

### A1 — 规划布局

在生成代码前，在脑中规划：
- 画布尺寸（默认 1000×680，复杂图可扩至 1200×800）
- 各组件的 x/y 坐标，确保不重叠
- 绘制顺序：先画箭头，再画组件（利用 SVG 渲染顺序遮挡箭头端点）

**垂直间距规则：**
- 标准组件高度 60px，大组件 80–120px
- 组件间最小垂直间隔 40px
- 图例放在所有边界框外部，距最低边界至少 20px

### A2 — 生成 HTML 文件

将完整 HTML 写入当前目录，文件命名：`[系统名小写]-architecture.html`

**设计规范：**

配色（语义化）：

| 组件类型 | 填充色 | 描边色 |
|---------|--------|--------|
| 前端/客户端 | `rgba(8, 51, 68, 0.4)` | `#22d3ee` |
| 后端/服务 | `rgba(6, 78, 59, 0.4)` | `#34d399` |
| 数据库/存储 | `rgba(76, 29, 149, 0.4)` | `#a78bfa` |
| 云服务 | `rgba(120, 53, 15, 0.3)` | `#fbbf24` |
| 安全/认证 | `rgba(136, 19, 55, 0.4)` | `#fb7185` |
| 消息队列 | `rgba(251, 146, 60, 0.3)` | `#fb923c` |
| 外部/通用 | `rgba(30, 41, 59, 0.5)` | `#94a3b8` |

背景：`#020617`，40×40px 网格，线条 `#1e293b`

字体：JetBrains Mono（Google Fonts），组件名 12px/600，子标签 9px/#94a3b8

组件框画法（先画不透明底层遮挡箭头，再画带色彩表层）：
```svg
<rect x="X" y="Y" width="W" height="H" rx="6" fill="#0f172a"/>
<rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<text x="CX" y="Y+20" fill="white" font-size="12" font-weight="600" text-anchor="middle">名称</text>
<text x="CX" y="Y+36" fill="#94a3b8" font-size="9" text-anchor="middle">子标签</text>
```

箭头（在所有组件之前绘制）：
```svg
<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
</marker>
<line x1="X1" y1="Y1" x2="X2" y2="Y2" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrowhead)"/>
```

分组边界：普通分组用琥珀色虚线 `stroke-dasharray="8,4" rx="12"`，安全组用玫红色虚线 `stroke-dasharray="4,4" rx="6"`

**完整 HTML 模板：**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>[系统名] Architecture</title>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"
          integrity="sha384-ZZ1pncU3bQe8y31yfZdMFdSpttDoPmOZg2wguVK9almUodir1PghgT0eY7Mrty8H"
          crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js"
          integrity="sha384-en/ztfPSRkGfME4KIm05joYXynqzUgbsG5nMrj/xEFAHXkeZfO3yMK8QQ+mP7p1/"
          crossorigin="anonymous"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #020617; color: white; font-family: 'JetBrains Mono', monospace; padding: 24px; }
    .container { max-width: 1100px; margin: 0 auto; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .title-area { display: flex; align-items: center; gap: 12px; }
    .dot { width: 10px; height: 10px; background: #22d3ee; border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
    h1 { font-size: 22px; font-weight: 700; }
    .subtitle { font-size: 12px; color: #64748b; margin-top: 4px; }
    .toolbar { position: relative; }
    .toolbar-toggle { background: #1e293b; border: 1px solid #334155; color: #94a3b8; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-family: inherit; font-size: 13px; }
    .toolbar-toggle:hover { background: #334155; color: white; }
    .toolbar-actions { display: none; position: absolute; right: 0; top: 36px; background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 8px; gap: 6px; flex-direction: column; min-width: 140px; z-index: 10; }
    .toolbar-actions.open { display: flex; }
    .toolbar-actions button { background: #0f172a; border: 1px solid #334155; color: #94a3b8; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-family: inherit; font-size: 12px; text-align: left; }
    .toolbar-actions button:hover { background: #1e293b; color: white; }
    .diagram-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 20px; overflow: hidden; }
    svg { width: 100%; height: auto; display: block; }
    .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .card { background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 16px; }
    .card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
    .card-dot { width: 8px; height: 8px; border-radius: 50%; }
    .card-dot.cyan { background: #22d3ee; }
    .card-dot.green { background: #34d399; }
    .card-dot.violet { background: #a78bfa; }
    .card h3 { font-size: 12px; font-weight: 600; }
    .card ul { list-style: none; }
    .card li { font-size: 11px; color: #64748b; margin-bottom: 4px; }
    .footer { text-align: center; font-size: 10px; color: #334155; margin-top: 16px; }
    @media print { .toolbar { display: none !important; } }
  </style>
</head>
<body>
<div class="container" id="report-container">
  <div class="header">
    <div class="title-area">
      <div class="dot"></div>
      <div>
        <h1>[系统名] Architecture</h1>
        <div class="subtitle">[副标题]</div>
      </div>
    </div>
    <div class="toolbar">
      <button class="toolbar-toggle" onclick="this.nextElementSibling.classList.toggle('open')">⋯</button>
      <div class="toolbar-actions">
        <button onclick="copyAsImage()">📋 复制 PNG</button>
        <button onclick="downloadPNG()">🖼️ 下载 PNG</button>
        <button onclick="downloadPDF()">📄 下载 PDF</button>
      </div>
    </div>
  </div>

  <div class="diagram-card">
    <svg viewBox="0 0 1000 680" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
        </pattern>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
        </marker>
      </defs>
      <rect width="1000" height="680" fill="#020617"/>
      <rect width="1000" height="680" fill="url(#grid)"/>

      <!-- 箭头（先于组件绘制） -->

      <!-- 组件框 -->

      <!-- 图例 -->
    </svg>
  </div>

  <div class="cards">
    <div class="card">
      <div class="card-header"><div class="card-dot cyan"></div><h3>核心组件</h3></div>
      <ul><li>• 组件 1</li></ul>
    </div>
    <div class="card">
      <div class="card-header"><div class="card-dot green"></div><h3>数据流向</h3></div>
      <ul><li>• 流程 1</li></ul>
    </div>
    <div class="card">
      <div class="card-header"><div class="card-dot violet"></div><h3>技术栈</h3></div>
      <ul><li>• 技术 1</li></ul>
    </div>
  </div>
  <div class="footer">[系统名] · Architecture Diagram</div>
</div>
<script>
  function captureOptions() {
    const r = document.getElementById('report-container').getBoundingClientRect();
    const toolbar = document.querySelector('.toolbar');
    return { x: r.left+scrollX, y: r.top+scrollY, width: r.width, height: r.height, scale: 2, ignoreElements: el => el===toolbar };
  }
  function copyAsImage() {
    html2canvas(document.body, captureOptions()).then(c => c.toBlob(b => navigator.clipboard.write([new ClipboardItem({'image/png':b})])));
  }
  function downloadPNG() {
    html2canvas(document.body, captureOptions()).then(c => { const a=document.createElement('a'); a.download='architecture.png'; a.href=c.toDataURL(); a.click(); });
  }
  function downloadPDF() {
    html2canvas(document.body, captureOptions()).then(c => {
      const {jsPDF}=window.jspdf;
      const pdf=new jsPDF({orientation:'landscape',unit:'px',format:[c.width/2+64,c.height/2+64]});
      pdf.addImage(c.toDataURL('image/png'),'PNG',32,32,c.width/2,c.height/2);
      pdf.save('architecture.pdf');
    });
  }
</script>
</body>
</html>
```

生成后告知用户文件路径，提示用浏览器打开，可继续对话迭代调整。

---

## 模式 B：AI 图片提示词

### B1 — 询问风格偏好

如果用户未指定，询问偏好风格（默认深色科技风）：
- **深色科技风**（推荐，与 ChatGPT Image 配合最佳）
- **白底简洁风**（适合 PPT 插图、文档）
- **手绘白板风**（适合 Excalidraw 感的草图）

### B2 — 生成提示词

同时输出中英双语，格式如下：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 中文提示词（适合 ChatGPT）
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[内容]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 英文提示词（适合 Midjourney / DALL-E / API）
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[内容]

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 使用说明
━━━━━━━━━━━━━━━━━━━━━━━━━━━
• ChatGPT：直接粘贴中文提示词发送
• Midjourney：/imagine [英文提示词]
• 如需调整风格，告诉我即可
```

**提示词框架（深色科技风）：**
```
Professional software architecture diagram, dark theme.
Dark background (#020617), subtle grid overlay.
Rounded rectangle components with colored borders:
- [前端]: cyan border (#22d3ee), label "[名称]"
- [后端]: green border (#34d399), label "[名称]"
- [数据库]: purple border (#a78bfa), label "[名称]"
- [消息队列]: orange border (#fb923c), label "[名称]"
Directional arrows showing: [A→B, B→C 等连接关系]
White text labels, JetBrains Mono style monospace font.
Clean, professional, high-resolution, no watermarks, diagram only.
Style: AWS architecture diagram, tech blog illustration.
```

**提示词框架（白底简洁风）：**
```
Clean minimal software architecture diagram, white background.
Flat colored boxes with soft shadows, sans-serif labels.
Blue for frontend, green for backend, purple for database, orange for external.
Thin directional arrows: [连接关系]
Presentation-ready, Google Cloud architecture diagram style.
```

**提示词框架（手绘白板风）：**
```
Hand-drawn whiteboard architecture diagram, Excalidraw style.
Sketch-like boxes and rough arrows, black on white, marker-pen aesthetic.
Components: [列出模块]
Connections: [连接关系]
Clean scan quality, readable labels.
```

### B3 — 检查 API 配置并直接生成（可选）

运行检查：
```bash
echo $OPENAI_API_KEY
```

若已配置，询问用户是否直接调用 API 生成图片。确认后写入并执行以下脚本：

```python
import os, base64
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

prompt = """[插入 B2 生成的英文提示词]"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size="1536x1024",
    quality="high",
)

image_bytes = base64.b64decode(result.data[0].b64_json)
output_path = "architecture-diagram.png"
with open(output_path, "wb") as f:
    f.write(image_bytes)

print(f"✅ 架构图已保存：{output_path}（1536×1024，高质量）")
```

执行后告知用户图片路径。

---

## 注意事项

- **图片 AI 的局限**：文字标注和箭头方向控制有限，生成后如有文字偏差属正常，可在 ChatGPT 中追加描述迭代
- **精度要求高时**：推荐选模式 A（SVG），文字/箭头/层级 100% 精准
- **课程演示**：两种模式都适合，模式 B 更适合展示 ChatGPT Image 2 的能力
