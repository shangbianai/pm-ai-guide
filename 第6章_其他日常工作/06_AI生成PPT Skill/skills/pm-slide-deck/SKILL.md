---
name: pm-slide-deck
description: 将内容转化为专业幻灯片图片。先生成带风格指令的大纲，再逐页生成幻灯片图片。当用户要求"生成幻灯片"、"制作演示文稿"、"生成 PPT"、"做 PPT"时触发。
version: 1.59.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - bun
        - npx
---

# 幻灯片生成器

将内容转化为专业幻灯片图片。本工具设计用于**阅读与分享**（自解释幻灯片、逻辑滚动流、适合社交媒体传播），而非现场演示——这一假设驱动了下方所有布局和信息密度的决策。

## 用户输入工具

当本 Skill 需要向用户提问时，遵循以下工具选择规则（按优先级）：

1. **优先使用运行时内置的用户输入工具**，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 等等效工具。
2. **降级方案**：如果不存在此类工具，输出编号的纯文本消息，请用户回复对应编号/答案。
3. **批量提问**：如果工具支持单次调用多个问题，将所有适用的问题合并为一次调用；如果只支持单问题，则按优先级逐个提问。

下文中的 `AskUserQuestion` 引用仅为示例——在其他运行时中请替换为对应的本地工具。

## 图片生成工具

本 Skill 支持四种图片生成后端，用户在生成图片前需选择使用哪个后端。

### 后端选择（步骤 7 前必需）

在步骤 7（生成图片）之前，通过 `AskUserQuestion` 询问用户选择图片生成后端：

| 选项 | 后端名称 | 说明 |
|------|----------|------|
| 1 | **豆包 Seedream**（doubao） | 火山引擎方舟平台，支持 16:9 高清，国内访问稳定 |
| 2 | **GPT-image-2**（openai） | OpenAI 图片生成，文字渲染质量高 |
| 3 | **Nano Banana**（gemini） | Google Gemini 2.0 Flash Image，免费额度充足 |
| 4 | **Grsai GPT-image-2**（grsai） | Grsai 平台国内节点，使用 GPT-image-2 模型，国内访问稳定 |

### API Key 检测与设置

根据用户选择的后端，按以下优先级检测对应的 API Key：

**豆包 Seedream（doubao）**：
1. 环境变量 `ARK_API_KEY` 或 `DOUBAO_API_KEY`
2. `.env` 文件（当前工作目录 / 项目根目录 / Skill 目录）
3. 获取方式：[火山引擎方舟平台](https://console.volcengine.com/ark)
4. 存储键名：`ARK_API_KEY`

**GPT-image-2（openai）**：
1. 环境变量 `OPENAI_API_KEY`
2. `.env` 文件（同上查找顺序）
3. 获取方式：[OpenAI API Keys](https://platform.openai.com/api-keys)
4. 存储键名：`OPENAI_API_KEY`

**Nano Banana（gemini）**：
1. 环境变量 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY`
2. `.env` 文件（同上查找顺序）
3. 获取方式：[Google AI Studio](https://aistudio.google.com/apikey)
4. 存储键名：`GEMINI_API_KEY`

**Grsai GPT-image-2（grsai）**：
1. 环境变量 `GRSAI_API_KEY`
2. `.env` 文件（同上查找顺序）
3. 获取方式：联系 Grsai 平台获取 API Key
4. 存储键名：`GRSAI_API_KEY`

**⛔ 如果所选后端的 API Key 不可用，不允许跳过此步骤。** 必须在获得有效 Key 后才能继续图片生成。如果用户提供的 Key 不在 `.env` 中，将其追加到项目根目录的 `.env` 文件。

### 后端配置

| 配置项 | doubao | openai | gemini | grsai |
|--------|--------|--------|--------|-------|
| API 端点 | `https://ark.cn-beijing.volces.com/api/v3/images/generations` | `https://api.openai.com/v1/images/generations` | `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent` | `https://grsai.dakka.com.cn/v1/api/generate` |
| 模型 | `doubao-seedream-5-0-260128` | `gpt-image-2` | `gemini-2.0-flash-exp` | `gpt-image-2` |
| 响应格式 | `b64_json` | `b64_json` | `inlineData`（从 generateContent 响应中提取） | `json`（返回图片 URL） |
| 支持尺寸 | `1672x941`（默认 16:9）、`1280x720`、`1024x1024` 等 | `1024x1024`、`1536x1024`、`1024x1536`（默认 1672x941 自动转为 1536x1024） | 不支持自定义尺寸 | `1024x1024`、`1536x1024`、`1024x1536`（默认 1672x941 自动转为 1536x1024） |
| 水印 | 关闭 | 不适用 | 不适用 | 不适用 |

**⛔ 禁止用 SVG、HTML、Canvas 或其他代码渲染替代光栅图片生成。** 如果 API 不可用，告知用户——不要静默输出 SVG、内联 `<svg>` 标记或 HTML/CSS 图形作为替代。

**⛔ 禁止在已生成的位图上修补文字。** 不要使用 ImageMagick、Pillow、Canvas、SVG、HTML/CSS、OCR 脚本或任何其他程序化叠加方式来覆盖、重写、擦除、描边或替换幻灯片中的标题、要点或任何其他文字。如果文字有误或不清晰，用修正后的提示词重新生成。

**提示词文件要求（强制）**：在调用 API 之前，将每张图片的完整最终提示词写入 `prompts/` 目录下的独立文件（命名：`NN-slide-[slug].md`）。该文件是可复现记录，允许在不重新生成提示词的情况下重新生成图片。

## 批量生成策略

所有提示词文件保存并验证后，通过 `scripts/generate-slides.py` 脚本批量调用图片生成 API 生成幻灯片图片。优先使用 `python3` 运行 `.py` 脚本；如 Python 不可用，降级为 `bun` 运行 `.ts` 脚本。

脚本自动处理：
- 检测 `ARK_API_KEY` / `DOUBAO_API_KEY`（环境变量或 `.env` 文件）
- 扫描 `prompts/` 目录，跳过已有对应 PNG 的幻灯片
- 按 `--batch-size` 分批顺序生成（默认 1，即逐张生成）
- 已存在的文件自动备份后再覆盖
- 失败的幻灯片可使用 `--retry` 参数仅重新生成缺失/失败的图片

规则：

- 所有选中幻灯片的提示词文件存在于磁盘后，才能开始生成。
- 失败的项目通过 `--retry` 单独重试。
- 所有幻灯片图片生成完毕后才能合并 PPTX/PDF。

## 确认策略

默认行为：**生成前确认**。

- 显式 Skill 调用、文件路径、匹配的信号/预设、`EXTEND.md` 默认值仅作为**推荐输入**，均不授权跳过确认。
- 在用户完成步骤 2 之前，**不要**开始步骤 3 或后续步骤。
- 仅当当前请求明确要求跳过时才跳过确认，例如："直接生成"、"不用确认"、"跳过确认"、"按默认出幻灯片"或等效表述。
- 如果明确跳过确认，在生成前的下一次用户可见更新中说明假定的风格/受众/幻灯片数/语言/后端。

## 语言

以用户的语言回答问题、进度报告、错误消息和完成摘要。技术标识（风格名称、文件路径、代码）保持英文。

## 脚本目录

`{baseDir}` = 本 SKILL.md 所在目录。脚本运行优先级：`python3`（运行 `.py` 脚本）> `bun`（运行 `.ts` 脚本）> `npx -y bun`。

| 脚本 | 用途 |
|------|------|
| `scripts/generate-slides.py` | 调用图片生成 API 逐张生成幻灯片图片（Python 版，**优先使用**） |
| `scripts/merge-to-pptx.py` | 将幻灯片合并为 PowerPoint（Python 版，**优先使用**） |
| `scripts/merge-to-pdf.py` | 将幻灯片合并为 PDF（Python 版，**优先使用**） |
| `scripts/generate-slides.ts` | 调用图片生成 API 逐张生成幻灯片图片（TypeScript 版，需 bun） |
| `scripts/merge-to-pptx.ts` | 将幻灯片合并为 PowerPoint（TypeScript 版，需 bun） |
| `scripts/merge-to-pdf.ts` | 将幻灯片合并为 PDF（TypeScript 版，需 bun） |

## 选项

| 选项 | 说明 |
|------|------|
| `--style <名称>` | 预设风格（见下方预设列表）、`custom` 或自定义风格名称 |
| `--audience <类型>` | beginners / intermediate / experts / executives / general |
| `--lang <代码>` | 输出语言（en, zh, ja, ...） |
| `--slides <N>` | 目标幻灯片数量（建议 8-25，最多 30） |
| `--ref <文件...>` | 参考图片，应用于每张幻灯片（风格/调色板/构图/主题） |
| `--batch-size <n>` | 本次运行的图片生成批量大小。默认值：1。限制范围 1-8 |
| `--size <尺寸>` | 图片尺寸：`1672x941`（默认，16:9）、`1280x720`、`1024x1024` 等。注意：OpenAI/Grsai 后端仅支持 `1024x1024`、`1536x1024`、`1024x1536`，默认尺寸自动转为最接近的 `1536x1024`；Gemini 后端不支持自定义尺寸 |
| `--backend <名称>` | 图片生成后端：`doubao`（默认）、`openai`、`gemini`、`grsai` |
| `--retry` | 仅重新生成缺失或失败的幻灯片图片 |
| `--outline-only` | 生成大纲后停止 |
| `--prompts-only` | 生成提示词后停止（跳过图片生成） |
| `--images-only` | 直接跳到步骤 7；需要已有 `prompts/` 目录 |
| `--regenerate <N>` | 重新生成指定幻灯片：`3` 或 `2,5,8` |

## 风格系统

17 个预设风格，覆盖技术/教育/生活/编辑类场景。每个预设是四个维度（质感/氛围/排版/密度）的组合。如果用户在第一轮选择"自定义维度"，第二轮确认会逐个维度提问——选项和原文在 `references/confirmation.md` 中。

### 预设风格（17 个）

| 预设 | 维度组合 | 适用场景 |
|------|----------|----------|
| `blueprint`（默认） | grid + cool + technical + balanced | 架构设计、系统设计 |
| `chalkboard` | organic + warm + handwritten + balanced | 教育、教程 |
| `corporate` | clean + professional + geometric + balanced | 投资人演示、商业提案 |
| `minimal` | clean + neutral + geometric + minimal | 高管简报 |
| `sketch-notes` | organic + warm + handwritten + balanced | 教育、教程 |
| `hand-drawn-edu` | organic + macaron + handwritten + balanced | 教育图表、流程说明 |
| `watercolor` | organic + warm + humanist + minimal | 生活方式、健康 |
| `dark-atmospheric` | clean + dark + editorial + balanced | 娱乐、游戏 |
| `notion` | clean + neutral + geometric + dense | 产品演示、SaaS |
| `bold-editorial` | clean + vibrant + editorial + balanced | 产品发布、主题演讲 |
| `editorial-infographic` | clean + cool + editorial + dense | 技术解读、研究报告 |
| `fantasy-animation` | organic + vibrant + handwritten + minimal | 教育叙事 |
| `intuition-machine` | clean + cool + technical + dense | 技术文档、学术 |
| `pixel-art` | pixel + vibrant + technical + balanced | 游戏、开发者演讲 |
| `scientific` | clean + cool + technical + dense | 生物、化学、医学 |
| `vector-illustration` | clean + vibrant + humanist + balanced | 创意、儿童内容 |
| `vintage` | paper + warm + editorial + balanced | 历史、文化遗产 |

各预设详细规格：`references/styles/<preset>.md`。预设→维度映射：`references/dimensions/presets.md`。

### 维度（选择"自定义维度"时使用）

| 维度 | 选项 | 用途 |
|------|------|------|
| **Texture（质感）** | clean, grid, organic, pixel, paper | 背景处理 |
| **Mood（氛围）** | professional, warm, cool, vibrant, dark, neutral, macaron | 色彩温度 |
| **Typography（排版）** | geometric, humanist, handwritten, editorial, technical | 标题/正文风格 |
| **Density（密度）** | minimal, balanced, dense | 每页信息量 |

各维度详细规格：`references/dimensions/*.md`。

### 自动选择

将内容信号匹配到预设。选择源内容中出现的第一个信号关键词对应的预设；无匹配时回退到 `blueprint`。

| 源内容中的信号 | 预设 |
|---------------|------|
| tutorial, learn, education, guide, beginner | `sketch-notes` |
| hand-drawn, infographic, diagram, process, onboarding | `hand-drawn-edu` |
| classroom, teaching, school, chalkboard | `chalkboard` |
| architecture, system, data, analysis, technical | `blueprint` |
| creative, children, kids, cute | `vector-illustration` |
| briefing, academic, research, bilingual | `intuition-machine` |
| executive, minimal, clean, simple | `minimal` |
| saas, product, dashboard, metrics | `notion` |
| investor, quarterly, business, corporate | `corporate` |
| launch, marketing, keynote, magazine | `bold-editorial` |
| entertainment, music, gaming, atmospheric | `dark-atmospheric` |
| explainer, journalism, science communication | `editorial-infographic` |
| story, fantasy, animation, magical | `fantasy-animation` |
| gaming, retro, pixel, developer | `pixel-art` |
| biology, chemistry, medical, scientific | `scientific` |
| history, heritage, vintage, expedition | `vintage` |
| lifestyle, wellness, travel, artistic | `watercolor` |

### 幻灯片数量参考

| 源内容长度 | 建议幻灯片数 |
|-----------|-------------|
| < 1000 词 | 5-10 |
| 1000-3000 词 | 10-18 |
| 3000-5000 词 | 15-25 |
| > 5000 词 | 20-30（考虑拆分） |

## 参考图片

用户可提供参考图片来引导风格、调色板、布局或主题。

**接收方式**：通过 `--ref <文件...>` 或用户在对话中提供文件路径/粘贴图片。
- 文件路径 → 复制到 `{slide-deck-dir}/refs/NN-ref-{slug}.{ext}`
- 粘贴图片但无路径 → 询问路径，或以文字方式提取风格特征作为文本降级

**使用模式**（每个参考）：

| 模式 | 效果 |
|------|------|
| `direct` | 提取风格特征并附加到每张幻灯片的提示词中（豆包 API 通过文本提示词传递风格引导） |
| `style` | 提取风格特征（线条处理、质感、氛围）并附加到每张幻灯片的提示词中 |
| `palette` | 提取十六进制颜色值并附加到每张幻灯片的提示词中 |

在每张幻灯片的提示词前置信息中记录参考：

```yaml
references:
  - ref_id: 01
    filename: 01-ref-brand.png
    usage: direct
```

生成时验证文件是否存在。所有参考均以 `style`/`palette` 模式提取特征后嵌入提示词文本（豆包 API 通过文本提示词传递风格引导）。

## 文件布局

```
slide-deck/{topic-slug}/
├── source-{slug}.{ext}
├── outline.md
├── prompts/NN-slide-{slug}.md
├── NN-slide-{slug}.png
├── {topic-slug}.pptx
└── {topic-slug}.pdf
```

**Slug**：2-4 个单词，kebab-case 格式，从主题提取。"机器学习入门" → `intro-machine-learning`。

**备份规则**（适用于所有步骤）：如果要写入的文件已存在，先将旧文件重命名为 `<name>-backup-YYYYMMDD-HHMMSS.<ext>`。这保护了用户的编辑并支持回滚。

## 工作流程

复制此清单，完成时勾选：

```
- [ ] 步骤 1：初始化与分析
- [ ] 步骤 2：确认 ⚠️ 必需（第一轮；仅在选择"自定义维度"时有第二轮）
- [ ] 步骤 3：生成大纲
- [ ] 步骤 4：审阅大纲（条件性）
- [ ] 步骤 5：生成提示词
- [ ] 步骤 6：审阅提示词（条件性）
- [ ] 步骤 7：生成图片
- [ ] 步骤 8：合并为 PPTX/PDF
- [ ] 步骤 9：输出摘要
```

### 步骤 1：初始化与分析

**1.1 加载 EXTEND.md** —— 按顺序检查以下路径，先找到的优先：

| 路径 | 作用范围 |
|------|---------|
| `.pm-skills/pm-slide-deck/EXTEND.md` | 项目级 |
| `${XDG_CONFIG_HOME:-$HOME/.config}/pm-skills/pm-slide-deck/EXTEND.md` | XDG |
| `$HOME/.pm-skills/pm-slide-deck/EXTEND.md` | 用户主目录 |

如果找到，读取、解析并打印摘要（风格/受众/语言/审阅/批量大小）。如果没找到，使用默认值继续——首次设置不会阻塞 Skill。数据结构：`references/config/preferences-schema.md`。

**1.2 分析内容** —— 遵循 `references/analysis-framework.md`：分类内容、检测语言、记录风格选择信号、根据长度估算幻灯片数量（参见上方风格系统中的**幻灯片数量参考**）、生成主题 slug。将源内容保存为 `source.md`（如果已存在则遵循备份规则）。

**1.3 检查已有输出** ⚠️ 步骤 2 前必需。如果 `slide-deck/{topic-slug}/` 已存在，询问如何处理——四个选项（重新生成大纲/重新生成图片/备份后重新生成/退出），原文在 `references/confirmation.md` 中。

将分析结果保存到 `analysis.md`：主题、受众、信号、推荐风格和幻灯片数、语言检测。

### 步骤 2：确认 ⚠️ 必需

**硬门控**：此步骤按[确认策略](#确认策略)强制执行——在用户在此确认（或在当前请求中明确选择跳过，如"直接生成"）之前，不能开始步骤 3 及后续步骤。

**第一轮（始终执行）** —— 将六个问题合并为一次 `AskUserQuestion` 调用：风格、受众、幻灯片数、图片生成后端、是否审阅大纲、是否审阅提示词。选项原文在 `references/confirmation.md` 中。

提问前显示摘要：
- 内容类型 + 主题
- 检测到的语言
- 推荐风格（基于信号）
- 推荐幻灯片数（基于长度）

**第二轮（仅当第一轮选择"自定义维度"时）** —— 将四个维度问题合并：质感、氛围、排版、密度。选项原文在 `references/confirmation.md` 中。四个答案替代预设。

**确认后**：用最终选择更新 `analysis.md`，存储第 4/5 题的 `skip_outline_review` / `skip_prompt_review` 标志。

### 步骤 3：生成大纲

解析风格：预设 → `references/styles/{preset}.md`；自定义维度 → 组合 `references/dimensions/` 中的文件。从解析的风格构建 `STYLE_INSTRUCTIONS`，应用确认的受众 + 语言 + 幻灯片数，遵循 `references/outline-template.md`，保存为 `outline.md`。

如果 `--outline-only` 则在此停止。如果 `skip_outline_review` 则跳过步骤 4。

### 步骤 4：审阅大纲（条件性）

逐页显示表格（`# | 标题 | 类型 | 布局`）以及总数和解析的风格。询问：继续/先编辑大纲/重新生成——原文在 `references/confirmation.md` 中。

选择"先编辑大纲"时，告知用户编辑 `outline.md`，准备好后再问。选择"重新生成大纲"时，返回步骤 3。

### 步骤 5：生成提示词

对大纲中的每张幻灯片：
1. 读取 `references/base-prompt.md`
2. 从大纲中提取 `STYLE_INSTRUCTIONS`（不要重新读取风格文件）
3. 添加幻灯片的内容
4. 如果指定了 `Layout:`，引入 `references/layouts.md` 中的指导
5. 保存到 `prompts/NN-slide-{slug}.md`（适用备份规则）

如果 `--prompts-only` 则在此停止。如果 `skip_prompt_review` 则跳过步骤 6。

### 步骤 6：审阅提示词（条件性）

显示提示词索引（`# | 文件名 | 幻灯片标题`），询问：继续/先编辑提示词/重新生成——原文在 `references/confirmation.md` 中。分支逻辑同步骤 4。

### 步骤 7：生成图片

1. **选择后端**——如果步骤 2 中用户未指定后端，通过 `AskUserQuestion` 询问用户选择图片生成后端（豆包 Seedream / GPT-image-2 / Nano Banana / Grsai GPT-image-2）。
2. **检测 API Key**——根据所选后端，按「图片生成工具 > API Key 检测与设置」章节的优先级查找对应的 API Key。如果未找到，通过 `AskUserQuestion` 提示用户提供 Key，并写入项目根目录的 `.env` 文件。
3. 确认每个 `prompts/NN-slide-{slug}.md` 存在（强制要求；提示词文件是可复现记录）。
4. 运行生成脚本（优先 Python，降级 bun）：
   ```bash
   # 优先：Python 版（无需额外依赖）
   python3 {baseDir}/scripts/generate-slides.py <prompts-dir> --output-dir <slide-deck-dir> --backend <doubao|openai|gemini|grsai> [--size 1672x941] [--batch-size 1]
   
   # 降级：bun 版（需要 bun 已安装）
   ${BUN_X} {baseDir}/scripts/generate-slides.ts <prompts-dir> --output-dir <slide-deck-dir> --backend <doubao|openai|gemini|grsai> [--size 1672x941] [--batch-size 1]
   ```
5. 脚本会逐张调用对应后端的 API，报告进度为 `已生成 X/N`。已存在的 PNG 会自动备份。

`--regenerate N` 直接跳到此步骤，仅处理指定幻灯片。`--images-only` 从现有提示词开始。失败后可用 `--retry` 仅重新生成缺失的图片。

### 步骤 8：合并

```bash
# 优先：Python 版
python3 {baseDir}/scripts/merge-to-pptx.py <slide-deck-dir>
python3 {baseDir}/scripts/merge-to-pdf.py <slide-deck-dir>

# 降级：bun 版
# ${BUN_X} {baseDir}/scripts/merge-to-pptx.ts <slide-deck-dir>
# ${BUN_X} {baseDir}/scripts/merge-to-pdf.ts <slide-deck-dir>
```

### 步骤 9：摘要

```
幻灯片生成完成！
主题：[主题]
风格：[预设名称 或 "自定义: 质感+氛围+排版+密度"]
位置：[目录]
幻灯片数：N

- 01-slide-cover.png
- ...
- NN-slide-back-cover.png

大纲：outline.md
PPTX：{topic-slug}.pptx
PDF：{topic-slug}.pdf
```

## 幻灯片修改

| 操作 | 方法 |
|------|------|
| 编辑 | 先更新 `prompts/NN-slide-{slug}.md`，再 `--regenerate N` |
| 添加 | 在指定位置创建新提示词，生成图片，后续 `NN` 重新编号（slug 不变），更新 `outline.md`，重新合并 |
| 删除 | 删除 PNG + 提示词，后续重新编号，更新 `outline.md`，重新合并 |

重新生成图片前务必先更新提示词文件——这保持了提示词目录作为唯一事实来源，使变更可复现。重新编号只改变 `NN`；slug 保持不变，引用仍然有效。

文字修正策略：

- 如果幻灯片的标题、要点或其他渲染文字有拼写错误、乱码、难以辨认或视觉上偏弱，不要用代码修补位图。
- 对于文字修正的重新生成，写入新的提示词文件和新的输出路径，保留有瑕疵的候选供对比。
- 后处理仅限于裁剪、缩放、压缩或不改变文字和主要构图的格式转换。

详见 `references/modification-guide.md`。

## 参考文件

| 文件 | 内容 |
|------|------|
| `references/confirmation.md` | 各确认步骤的提问选项原文 |
| `references/analysis-framework.md` | 内容分析框架 |
| `references/outline-template.md` | 大纲结构 |
| `references/base-prompt.md` | 图片生成的基础提示词 |
| `references/layouts.md` | 布局选项 |
| `references/design-guidelines.md` | 受众、排版、色彩选择 |
| `references/content-rules.md` | 内容准则 |
| `references/modification-guide.md` | 编辑/添加/删除工作流 |
| `references/styles/<preset>.md` | 各预设风格的详细规格 |
| `references/dimensions/*.md` | 各维度的详细规格 |
| `references/config/preferences-schema.md` | EXTEND.md 数据结构 |

## 注意事项

- 每张幻灯片图片生成约需 10-30 秒；在幻灯片之间报告进度。
- 对于敏感公众人物，优先使用风格化替代方案以避免肖像权问题。
- API Key 存储在 `.env` 文件的 `ARK_API_KEY` 字段中，确保 `.env` 已加入 `.gitignore`。
- 三种后端的图片质量和生成速度各有差异，根据实际需求选择。豆包 Seedream 支持 16:9 高清输出（1672x941），GPT-image-2 文字渲染质量较高，Nano Banana 免费额度充足，Grsai 使用国内节点访问稳定。

## 修改偏好

EXTEND.md 位于步骤 1.1 列出的第一个匹配路径。两种修改方式：

- **直接编辑** —— 打开 EXTEND.md 修改字段。完整数据结构：`references/config/preferences-schema.md`。
- **常用修改项**：
  - `generation_batch_size: 1` —— 每批次调用豆包 API 的幻灯片数量（1-8）。
  - `image_size: 2K` —— 默认图片尺寸（`2K`、`1280x720`、`1024x1024`）。
  - `preferred_style: blueprint`、`preferred_audience: experts`、`language: zh`。
