# EXTEND.md 结构定义

`.pm-skills/pm-slide-deck/EXTEND.md` 中用户偏好设置的结构说明。

## 完整结构

```yaml
# 幻灯片偏好设置

## 默认值
style: blueprint              # 预设名称或 "custom"
audience: general             # beginners | intermediate | experts | executives | general
language: auto                # auto | en | zh | ja | 等
review: true                  # true = 生成前审查大纲
image_size: 1672x941           # 1672x941 (16:9 默认) — 豆包自动升档 2560x1440，OpenAI/Grsai 自动转为 1536x1024
generation_batch_size: 1      # 1-8，每批次调用豆包 API 的幻灯片数量

## 自定义维度（仅当 style: custom 时生效）
dimensions:
  texture: clean              # clean | grid | organic | pixel | paper
  mood: professional          # professional | warm | cool | vibrant | dark | neutral | macaron
  typography: geometric       # geometric | humanist | handwritten | editorial | technical
  density: balanced           # minimal | balanced | dense

## 自定义风格（可选）
custom_styles:
  my-style:
    texture: organic
    mood: warm
    typography: humanist
    density: minimal
    description: "我的自定义温暖友好风格"
```

## 字段说明

### 默认值

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|------|
| `style` | string | `blueprint` | 预设名称、`custom` 或自定义风格名称 |
| `audience` | string | `general` | 默认目标受众 |
| `language` | string | `auto` | 输出语言（auto = 根据输入自动检测） |
| `review` | boolean | `true` | 生成前展示大纲审查 |
| `image_size` | string | `1672x941` | 默认 16:9 尺寸。脚本按后端自动适配：豆包升档为 `2560x1440`（最低 3,686,400 像素），OpenAI/Grsai 转为 `1536x1024`，Gemini 不支持自定义 |
| `generation_batch_size` | int | 1 | 每批次调用豆包 API 的幻灯片图片数量。无效值自动限制在 1-8 范围内。用户当前请求可覆盖此值。 |

### API Key

豆包 API Key 不存储在 EXTEND.md 中，而是存储在 `.env` 文件的 `ARK_API_KEY` 字段中。详见 SKILL.md「图片生成工具 > API Key 检测与设置」章节。

### 自定义维度

仅当 `style: custom` 时使用。直接定义维度值。

| 字段 | 可选值 | 默认值 |
|-------|---------|---------|
| `texture` | clean, grid, organic, pixel, paper | clean |
| `mood` | professional, warm, cool, vibrant, dark, neutral, macaron | professional |
| `typography` | geometric, humanist, handwritten, editorial, technical | geometric |
| `density` | minimal, balanced, dense | balanced |

### 自定义风格

定义可复用的自定义维度组合。

```yaml
custom_styles:
  style-name:
    texture: <texture>
    mood: <mood>
    typography: <typography>
    density: <density>
    description: "可选描述"
```

使用方式：直接在 Skill 中指定 `--style style-name`

## 最简示例

### 仅更改默认风格

```yaml
style: sketch-notes
```

### 关闭生成前审查

```yaml
review: false
```

### 自定义默认维度

```yaml
style: custom
dimensions:
  texture: organic
  mood: professional
  typography: humanist
  density: minimal
```

### 定义可复用的自定义风格

```yaml
custom_styles:
  brand-style:
    texture: clean
    mood: vibrant
    typography: editorial
    density: balanced
    description: "公司品牌风格"
```

## 文件位置

优先级顺序（先找到的优先生效）：

1. `.pm-skills/pm-slide-deck/EXTEND.md`（项目级）
2. `$HOME/.pm-skills/pm-slide-deck/EXTEND.md`（用户级）

## 首次设置

当 EXTEND.md 不存在时，Skill 会引导初始偏好设置：

1. 首选风格（预设或自定义）
2. 默认受众
3. 语言偏好
4. 是否需要生成前审查
5. 保存位置（项目级或用户级）

在所选位置创建 EXTEND.md 文件。
