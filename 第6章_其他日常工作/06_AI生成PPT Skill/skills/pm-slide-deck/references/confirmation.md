# 确认问题

确认步骤的具体选项文案。SKILL.md 列出了需要提问的问题——本文件提供了 Claude Code 中使用的逐字选项。请根据运行环境的原生用户输入工具适配文案；核心意图比具体措辞更重要。

## 第一轮（每次必问）

将以下五个问题合并到一次 `AskUserQuestion` 调用中。

### Q1: 风格

```yaml
header: Style
question: 本次演示使用哪种视觉风格？
options:
  - label: "{recommended_preset}（推荐）"
    description: 基于内容分析的最佳匹配
  - label: "{alternative_preset}"
    description: "{alternative style description}"
  - label: 自定义维度
    description: 分别选择纹理、色调、字体、密度
```

### Q2: 受众

```yaml
header: Audience
question: 主要读者是谁？
options:
  - label: 大众读者（推荐）
    description: 广泛受众，通俗易懂
  - label: 初学者/学习者
    description: 教学导向，清晰讲解
  - label: 专家/专业人士
    description: 技术深度，领域知识
  - label: 高管/决策者
    description: 高层洞察，精简细节
```

### Q3: 页数

```yaml
header: Slides
question: 生成多少页幻灯片？
options:
  - label: "{N} 页（推荐）"
    description: 基于内容长度推荐
  - label: "更少（{N-3} 页）"
    description: 更加精简，减少细节
  - label: "更多（{N+3} 页）"
    description: 更加详细的拆解
```

### Q4: 审核大纲

```yaml
header: Outline
question: 是否在生成提示词前审核大纲？
options:
  - label: 是，审核大纲（推荐）
    description: 审核幻灯片标题和结构
  - label: 否，跳过大纲审核
    description: 直接进入提示词生成
```

### Q5: 审核提示词

```yaml
header: Prompts
question: 是否在生成图片前审核提示词？
options:
  - label: 是，审核提示词（推荐）
    description: 审核图片生成提示词
  - label: 否，跳过提示词审核
    description: 直接进入图片生成
```

## 第二轮 — 自定义维度

仅当第一轮 Q1 选择「自定义维度」时触发。将四个维度问题合并到一次调用中。

### 纹理

```yaml
header: Texture
question: 选择哪种视觉纹理？
options:
  - label: clean
    description: 纯色，无纹理
  - label: grid
    description: 微妙网格叠加，技术感
  - label: organic
    description: 柔和纹理，手绘质感
  - label: pixel
    description: 像素块，8-bit 复古美学
```

`paper` 也是有效选项——通过「其他」输入。

### 色调

```yaml
header: Mood
question: 选择哪种色彩风格？
options:
  - label: professional
    description: 冷调中性，海军蓝/金色
  - label: warm
    description: 大地色系，亲和友好
  - label: cool
    description: 蓝灰色调，理性分析感
  - label: vibrant
    description: 高饱和度，大胆鲜明
  - label: macaron
    description: 马卡龙色块搭配奶油底色
```

`dark`、`neutral` 可通过「其他」输入。

### 字体

```yaml
header: Typography
question: 选择哪种字体风格？
options:
  - label: geometric
    description: 现代无衬线体，干净利落
  - label: humanist
    description: 人文气息，易读友好
  - label: handwritten
    description: 马克笔/毛笔风格，有机自然
  - label: editorial
    description: 杂志排版风格，富有表现力
```

`technical` 可通过「其他」输入。

### 密度

```yaml
header: Density
question: 信息密度选择？
options:
  - label: balanced（推荐）
    description: 每页 2-3 个要点
  - label: minimal
    description: 单一焦点，最大化留白
  - label: dense
    description: 多个数据点，紧凑排列
```

## 大纲审核（第 4 步）

```yaml
header: Confirm
question: 准备好生成提示词了吗？
options:
  - label: 是，继续（推荐）
    description: 生成图片提示词
  - label: 先编辑大纲
    description: 我要先修改 outline.md 再继续
  - label: 重新生成大纲
    description: 用不同的方案重新创建大纲
```

## 提示词审核（第 6 步）

```yaml
header: Confirm
question: 准备好生成幻灯片图片了吗？
options:
  - label: 是，继续（推荐）
    description: 生成所有幻灯片图片
  - label: 先编辑提示词
    description: 我要先修改提示词再继续
  - label: 重新生成提示词
    description: 用不同的方案重新创建提示词
```

## 已有内容（第 1.3 步）

```yaml
header: Existing
question: 检测到已有内容，如何处理？
options:
  - label: 重新生成大纲
    description: 保留图片，仅重新生成大纲
  - label: 重新生成图片
    description: 保留大纲，仅重新生成图片
  - label: 备份后重新生成
    description: 备份到 {slug}-backup-{timestamp}，然后全部重新生成
  - label: 退出
    description: 取消，保持已有内容不变
```
