# 第3章 01 · 产品架构图工具盘点

> 本节配套 Claude Code Skill：`arch-diagram`，以及 Codex Skill：`product-architecture-diagrams`

---

## 本节目标

用 AI 快速生成专业的产品架构图，掌握两条路径：

- **路径 A（推荐）**：Claude 直接生成精准的 SVG/HTML 架构图，文字和连线 100% 可控，浏览器打开即用，支持导出 PNG/PDF
- **路径 B**：生成优化好的图片提示词，粘贴到 ChatGPT Image 2 / Midjourney；配置 API Key 后可一键直出
- **路径 C**：Codex 生成绚烂分层 HTML 产品架构图，内置 PNG/JPG 导出，适合直接放入 PPT、文档或课程材料

---

## 文件说明

```
01_架构图工具盘点/
├── README.md              ← 本文件，使用说明
├── skill/
│   ├── SKILL.md           ← arch-diagram Skill 源文件
│   └── codex-product-architecture-diagrams/
│       ├── SKILL.md       ← Codex 产品架构图 Skill 源文件
│       ├── references/    ← 方法论、图型分类、HTML 导出规范
│       └── examples/      ← HTML Demo 与 PNG 预览图
└── guide/
    └── arch-diagram-guide.html  ← 图文教程（浏览器打开）
```

---

## 安装 Skill

```bash
# 方法一：直接复制 SKILL.md 到 skills 目录
cp skill/SKILL.md ~/.claude/skills/arch-diagram/SKILL.md

# 方法二：通过 skills.sh（如已发布）
npx skills add <url> --skill arch-diagram
```

安装后重启 Claude Code，即可使用 `/arch-diagram` 命令。

### Codex Skill

```bash
cp -R skill/codex-product-architecture-diagrams ~/.codex/skills/product-architecture-diagrams
```

安装后可在 Codex 中使用：

```text
用 $product-architecture-diagrams 帮我画一个智能风控产品架构图，包含用户端、运营端、风控评分、报告生成、模型训练、标签系统、数据仓库、监控运维。
```

---

## 使用方式

### 基础用法

直接输入：
```
/arch-diagram
```

Skill 会引导你描述系统架构，然后选择输出模式。

### 有现成文档时

把 PRD、需求文档、代码直接粘贴给 Claude，Skill 自动提炼架构信息，无需手动描述。

### 生成效果示例

路径 A 输出的 HTML 文件支持：
- 深色主题，语义化配色（前端青色 / 后端绿色 / 数据库紫色 / 消息队列橙色）
- 右上角 `⋯` 按钮一键导出 PNG / PDF
- 所有文字、箭头、层级 100% 精准

---

## 主要工具对比

| 工具 | 适用场景 | 精度 | 学习成本 |
|------|---------|------|---------|
| `/arch-diagram`（路径A） | 正式交付、文档归档 | ★★★★★ | 低（描述即可）|
| `$product-architecture-diagrams`（路径C） | 分层产品架构图、PPT/课程配图 | ★★★★★ | 低（描述即可）|
| ChatGPT Image 2（路径B） | 课程演示、探索风格 | ★★★ | 低 |
| Mermaid | 技术文档嵌入 | ★★★★ | 中 |
| draw.io / Excalidraw | 精细手工调整 | ★★★★★ | 高 |

---

## 配置 API Key（路径B 直连模式）

在 Claude Code 中运行：
```
/update-config
```
告诉它：`set OPENAI_API_KEY=你的key`

API Key 获取地址：[platform.openai.com/api-keys](https://platform.openai.com/api-keys)

> 注意：gpt-image-1 需要 OpenAI 账号达到 Tier 1（已完成付款验证）才能调用。

---

## 延伸阅读

- [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) — SVG 设计规范参考来源
- [OpenAI Image Generation API](https://platform.openai.com/docs/guides/image-generation) — gpt-image-1 官方文档
