# 布局图鉴

单页幻灯片的可选布局提示。在大纲的 `// LAYOUT` 部分中指定。

## 幻灯片专用布局

| 布局 | 描述 | 最佳用途 |
|--------|-------------|----------|
| `title-hero` | 大号居中标题 + 副标题 | 封面页、章节分隔页 |
| `quote-callout` | 突出显示引言及出处 | 客户证言、关键洞察 |
| `key-stat` | 单个大号数字作为视觉焦点 | 影响力数据、关键指标 |
| `split-screen` | 半图半文 | 功能亮点、对比展示 |
| `icon-grid` | 图标与标签的网格排列 | 功能特性、能力展示、收益说明 |
| `two-columns` | 双栏均衡内容 | 成对信息、双重要点 |
| `three-columns` | 三栏内容 | 三重对比、分类展示 |
| `image-caption` | 全出血图片 + 文字叠加 | 视觉叙事、情感传达 |
| `agenda` | 带高亮的编号列表 | 会议议程、路线图 |
| `bullet-list` | 结构化要点列表 | 简单内容、条目清单 |

## 信息图衍生布局

| 布局 | 描述 | 最佳用途 |
|--------|-------------|----------|
| `linear-progression` | 从左到右的顺序流程 | 时间线、步骤说明 |
| `binary-comparison` | A 与 B 并排对比 | 前后对比、优劣势分析 |
| `comparison-matrix` | 多因素对比矩阵 | 功能对比 |
| `hierarchical-layers` | 金字塔或层叠结构 | 优先级、重要性层级 |
| `hub-spoke` | 中心节点向外辐射 | 概念图、生态体系 |
| `bento-grid` | 不同尺寸的磁贴排列 | 总览、摘要 |
| `funnel` | 逐级收窄的阶段 | 转化漏斗、筛选流程 |
| `dashboard` | 指标与图表/数字 | KPI 展示、数据面板 |
| `venn-diagram` | 重叠圆环 | 关系展示、交集分析 |
| `circular-flow` | 循环流程 | 周期性流程 |
| `winding-roadmap` | 带里程碑的曲线路径 | 旅程图、时间线 |
| `tree-branching` | 父子层级结构 | 组织架构、分类体系 |
| `iceberg` | 可见层与隐藏层 | 表面与深层分析 |
| `bridge` | 跨越间隙的连接 | 问题-解决方案 |

**用法**：在幻灯片的 `// LAYOUT` 部分添加 `Layout: <name>`。

## 布局选择技巧

**根据内容匹配布局**：
| 内容类型 | 推荐布局 |
|--------------|-------------------|
| 单一叙事 | `bullet-list`、`image-caption` |
| 两个概念 | `split-screen`、`binary-comparison` |
| 三个要点 | `three-columns`、`icon-grid` |
| 流程/步骤 | `linear-progression`、`winding-roadmap` |
| 数据/指标 | `dashboard`、`key-stat` |
| 关系展示 | `hub-spoke`、`venn-diagram` |
| 层级结构 | `hierarchical-layers`、`tree-branching` |

**布局编排模式**：
| 位置 | 推荐布局 |
|----------|-------------------|
| 开场 | `title-hero`、`agenda` |
| 中间 | 根据内容选择对应布局 |
| 结尾 | `quote-callout`、`key-stat` |

**常见错误避免**：
- 对 2 个要点使用 3 栏布局（会导致空栏）
- 在文字下方堆叠图表/表格（应使用并排排列）
- 在没有实际图片的情况下使用图片布局
- 仅为了强调而使用引言布局（仅用于带出处的真实引言）
