# JSON Schema

```json
{
  "title": "用户体验旅程地图标题",
  "persona": "具体目标用户",
  "scenario": "触发场景",
  "core_task": "从开始到结束的完整任务",
  "evidence_note": "资料范围与模拟说明",
  "stages": [
    {
      "name": "阶段名称",
      "goal": "用户目标",
      "actions": "关键动作",
      "touchpoints": "主要触点",
      "thoughts": "用户想法",
      "emotion": -2,
      "pain": "主要痛点",
      "evidence_status": "已验证事实|合理推断|待验证假设",
      "evidence": "证据内容或验证说明",
      "opportunity": "产品机会",
      "impact": 5,
      "frequency": 4,
      "current_solution": 2
    }
  ],
  "research_questions": [
    "下一轮需要验证的问题"
  ]
}
```

约束：

- `stages` 为 5—7 项。
- `emotion` 为 -2 到 2 的整数。
- `impact`、`frequency`、`current_solution` 为 1 到 5 的整数。
- 机会优先级由渲染器计算，不在输入中硬编码。
- 材料不足时，在 `evidence_status` 和 `evidence` 中明确标记。
