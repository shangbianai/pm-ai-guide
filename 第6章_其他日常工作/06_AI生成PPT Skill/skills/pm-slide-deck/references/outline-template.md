# 大纲模板

幻灯片大纲的标准结构及样式说明。

## 大纲格式

```markdown
# 幻灯片大纲

**主题**: [主题描述]
**风格**: [预设名称 或 "custom"]
**维度**: [质感] + [氛围] + [排版] + [密度]
**受众**: [目标受众]
**语言**: [输出语言]
**页数**: N 页
**生成时间**: YYYY-MM-DD HH:mm

---

<STYLE_INSTRUCTIONS>
设计美学: [2-3 句话，综合各维度特征的描述]

背景:
  质感: [来自质感维度]
  基础色: [来自氛围维度色板]

排版:
  标题: [来自排版维度 - 描述视觉外观]
  正文: [来自排版维度 - 描述视觉外观]

色彩方案:
  主文字: [名称] ([十六进制]) - [用途]
  背景: [名称] ([十六进制]) - [用途]
  强调色 1: [名称] ([十六进制]) - [用途]
  强调色 2: [名称] ([十六进制]) - [用途]

视觉元素:
  - [元素 1，来自质感 + 氛围组合]
  - [元素 2，附带渲染指引]
  - ...

密度指南:
  - 每页内容量: [来自密度维度]
  - 留白: [来自密度维度]

样式规则:
  宜: [来自维度组合的指引]
  忌: [来自维度组合的反模式]
</STYLE_INSTRUCTIONS>

---

[后续为各页幻灯片条目...]
```

## 从维度构建 STYLE_INSTRUCTIONS

使用自定义维度或预设时，通过组合以下内容构建 STYLE_INSTRUCTIONS：

### 1. 设计美学

将四个维度的特征综合为 2-3 句话：

| 质感 | 贡献内容 |
|---------|--------------|
| clean | "干净利落的数字精确感，边缘清晰锐利" |
| grid | "技术网格覆盖层，工程级精确感" |
| organic | "手绘质感，柔和纹理" |
| pixel | "粗犷像素美学，8-bit 风格魅力" |
| paper | "陈旧纸张质感，复古韵味" |

| 氛围 | 贡献内容 |
|------|--------------|
| professional | "专业海军蓝与金色色板" |
| warm | "温暖的大地色系，营造亲切氛围" |
| cool | "冷静理性的蓝色与灰色" |
| vibrant | "大胆高饱和色彩，充满活力" |
| dark | "深邃电影感背景，发光点缀" |
| neutral | "极简灰阶，精致优雅" |

### 2. 背景

来自 `references/dimensions/texture.md`：
- 质感描述
- 来自氛围色板的基础色

### 3. 排版

来自 `references/dimensions/typography.md`：
- 标题视觉描述（不要写字体名称）
- 正文视觉描述（不要写字体名称）

**重要**：为图像生成描述外观时，使用 "粗体几何无衬线体，O 为完美圆形" 这样的描述，而非 "Inter 字体"。

### 4. 色彩方案

来自 `references/dimensions/mood.md`：
- 复制所选氛围的色板规格
- 包含十六进制色值和用途说明

### 5. 视觉元素

综合质感和氛围特征：

| 组合 | 视觉元素 |
|-------------|-----------------|
| clean + professional | 简洁图表、线框图标、结构化网格 |
| grid + cool | 技术示意图、尺寸标注线、蓝图 |
| organic + warm | 手绘图标、笔触、涂鸦 |
| pixel + vibrant | 像素风图标、复古游戏元素 |
| paper + warm | 复古邮票、陈旧元素、棕褐色叠加 |

### 6. 密度指南

来自 `references/dimensions/density.md`：
- 每页内容量限制
- 留白要求
- 元素数量指南

### 7. 样式规则

综合各维度专属规则：

**按质感的「宜」规则**：
- clean：保持锐利边缘，使用网格对齐
- grid：展示精确尺寸，使用技术图表
- organic：允许不完美，微妙重叠分层
- pixel：保持锯齿边缘，使用块状元素
- paper：添加微妙做旧效果，使用暖色调

**按质感的「忌」规则**：
- clean：不要使用手绘元素
- grid：不要使用有机曲线
- organic：不要使用完美几何图形
- pixel：不要平滑边缘
- paper：不要使用明亮的数字色彩

## 封面页模板

```markdown
## Slide 1 of N

**Type**: Cover
**Filename**: 01-slide-cover.png

// NARRATIVE GOAL
[本页在叙事弧线中达成的目标]

// KEY CONTENT
Headline: [主标题]
Sub-headline: [辅助标语]

// VISUAL
[详细的视觉描述 - 具体元素、构图、氛围]

// LAYOUT
Layout: [可选：布局图鉴中的布局名称，例如 title-hero]
[构图、层级、空间安排]
```

## 内容页模板

```markdown
## Slide X of N

**Type**: Content
**Filename**: {NN}-slide-{slug}.png

// NARRATIVE GOAL
[本页在叙事弧线中达成的目标]

// KEY CONTENT
Headline: [主要信息 - 叙事式表达，而非标签]
Sub-headline: [补充上下文]
Body:
- [要点 1 及具体细节]
- [要点 2 及具体细节]
- [要点 3 及具体细节]

// VISUAL
[详细的视觉描述]

// LAYOUT
Layout: [可选：布局图鉴中的布局名称]
[构图、层级、空间安排]
```

## 封底页模板

```markdown
## Slide N of N

**Type**: Back Cover
**Filename**: {NN}-slide-back-cover.png

// NARRATIVE GOAL
[有意义的收尾 - 不仅仅是"谢谢"]

// KEY CONTENT
Headline: [令人印象深刻的结束语或行动号召]
Body: [可选的总结要点或下一步行动]

// VISUAL
[强化核心信息的视觉设计]

// LAYOUT
Layout: [可选：布局图鉴中的布局名称]
[简洁有力的构图]
```

## STYLE_INSTRUCTIONS 区块

`<STYLE_INSTRUCTIONS>` 区块是大纲中样式信息的唯一真实来源。

| 部分 | 内容 | 来源 |
|---------|---------|--------|
| 设计美学 | 整体视觉方向 | 综合所有维度 |
| 背景 | 基础色和质感细节 | 质感 + 氛围维度 |
| 排版 | 字体描述（视觉外观，非名称） | 排版维度 |
| 色彩方案 | 命名颜色含十六进制色值和用途 | 氛围维度 |
| 视觉元素 | 图形元素及渲染指引 | 质感 + 氛围维度 |
| 密度指南 | 内容量限制和留白 | 密度维度 |
| 样式规则 | 宜/忌指引 | 综合各维度 |

**重要**：
- 排版描述必须描述视觉外观（如 "圆润无衬线体"、"粗体几何风格"），因为图像生成器无法使用字体名称
- 提示词应从大纲中提取 STYLE_INSTRUCTIONS，而非重新读取样式文件

## 预设 → 维度对照

使用预设时，在 `references/dimensions/presets.md` 中查找对应维度：

| 预设 | 维度组合 |
|--------|------------|
| blueprint | grid + cool + technical + balanced |
| sketch-notes | organic + warm + handwritten + balanced |
| corporate | clean + professional + geometric + balanced |
| minimal | clean + neutral + geometric + minimal |
| ... | 完整映射见 presets.md |

## 章节分隔线

在以下位置之间使用 `---`（水平分隔线）：
- 头部元数据与 STYLE_INSTRUCTIONS 之间
- STYLE_INSTRUCTIONS 与第一页幻灯片之间
- 每页幻灯片条目之间

## 幻灯片编号

- 封面页始终为第 1 页
- 内容页使用连续编号
- 封底页始终为最后一页（第 N 页）
- 文件名前缀与页码对应：`01-`、`02-` 等

## 文件名 Slug

根据幻灯片内容生成有意义的 slug：

| 页面类型 | Slug 模式 | 示例 |
|------------|--------------|---------|
| 封面 | `cover` | `01-slide-cover.png` |
| 内容 | `{topic-slug}` | `02-slide-problem-statement.png` |
| 封底 | `back-cover` | `10-slide-back-cover.png` |

Slug 规则：
- 使用 kebab-case（小写、连字符）
- 从标题或主要主题提取
- 最多 30 个字符
- 同一套幻灯片内唯一
