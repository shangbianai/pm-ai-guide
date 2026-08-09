---
name: create-discussion-whiteboard
description: Turn meeting discussions, leadership instructions, cross-department communication, workshops, product alignment, or brainstorming into a hand-drawn discussion whiteboard. Use when the user asks for Excalidraw、手绘白板、讨论白板、跨部门对齐图、汇报沟通图, or wants editable .excalidraw, SVG, PNG, JPG, HTML preview, and structured JSON outputs.
---

# 讨论白板生成

使用 MIT 开源的 [Excalidraw](https://github.com/excalidraw/excalidraw) 文件格式输出可继续编辑的手绘式白板。

## 默认板式

按讨论推进顺序组织四个区域：

1. `已知事实`：原话、数据、约束和背景。
2. `问题分歧`：不同角色的关注点、冲突和阻塞。
3. `决策共识`：已确认的原则、范围和取舍。
4. `行动计划`：负责人、时间、验证方式和待确认项。

根据材料调整栏目，但不要把事实和建议混在同一张便签。

## 工作流

1. 保留原始表达，去掉重复和口语噪声。
2. 每张便签只写一个信息点，建议 8—28 个汉字。
3. 使用统一颜色语义：蓝色事实、黄色问题、绿色决策、紫色行动、红色风险。
4. 只有存在真实关系时才画箭头，并为关系写短标签。
5. 先生成结构 JSON：

```json
{
  "title": "AI 销售助手需求对齐",
  "subtitle": "会议讨论 → 产品团队",
  "columns": [
    {"title": "已知事实", "color": "blue", "items": ["线索来自四个渠道"]},
    {"title": "问题分歧", "color": "yellow", "items": ["自动发送存在误发风险"]},
    {"title": "决策共识", "color": "green", "items": ["高风险动作必须人工确认"]},
    {"title": "行动计划", "color": "violet", "items": ["补充异常流程与验收标准"]}
  ]
}
```

6. 运行：

```bash
python3 scripts/render_discussion_whiteboard.py board.json --output-dir ./whiteboard-output
```

7. 验收 `.excalidraw`、SVG、PNG、JPG、HTML 和结构 JSON。

## 验收

- 观众能否在 10 秒内说出讨论主题和结论。
- 是否把未确认事项误写成共识。
- 是否保留关键约束、风险和角色差异。
- 行动项是否可执行；缺失负责人或时间必须标记待确认。
- `.excalidraw` 文件能否导入 Excalidraw 继续编辑。
