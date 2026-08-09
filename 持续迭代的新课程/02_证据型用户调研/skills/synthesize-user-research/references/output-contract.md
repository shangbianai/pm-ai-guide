# 输出契约

`research-bundle.json` 使用以下结构。允许增加字段，不要删除必填字段。

```json
{
  "meta": {
    "title": "研究标题",
    "subject": "具体研究对象",
    "scenario": "具体场景",
    "core_task": "从开始到结束的任务",
    "synthetic": true,
    "limitations": ["研究限制"]
  },
  "sources": [
    {
      "id": "SRC-001",
      "name": "文件名",
      "type": "audio|transcript|image|notes|table|other",
      "status": "已读取|部分读取|读取失败",
      "privacy": "脱敏说明"
    }
  ],
  "evidence": [
    {
      "id": "E-001",
      "source_id": "SRC-001",
      "locator": "00:42 或第 5 行或画面左下角",
      "kind": "用户原话|观察事实|数据记录|图片线索",
      "content": "短证据内容"
    }
  ],
  "contradictions": [
    {
      "description": "素材之间的矛盾或身份重复候选",
      "evidence_ids": ["E-001", "E-009"],
      "handling": "不自动合并；下一步如何确认"
    }
  ],
  "findings": [
    {
      "id": "F-001",
      "status": "已验证事实|合理推断|待验证假设",
      "statement": "洞察",
      "why_it_matters": "对用户或决策的影响",
      "evidence_ids": ["E-001"],
      "validation": "假设的验证方式；事实可留空"
    }
  ],
  "persona": {
    "label": "角色名称",
    "claims": [
      {
        "dimension": "目标|行为|痛点|限制|工具|决策标准",
        "statement": "画像声明",
        "evidence_ids": ["E-001"]
      }
    ]
  },
  "journey": [
    {
      "stage": "阶段名称",
      "goal": "用户目标",
      "actions": "关键动作",
      "touchpoints": "触点",
      "emotion": -1,
      "pain": "痛点",
      "status": "已验证事实|合理推断|待验证假设",
      "evidence_ids": ["E-001"],
      "opportunity": "应改善的用户结果"
    }
  ],
  "opportunities": [
    {
      "rank": 1,
      "outcome": "期望改善的用户结果",
      "why_now": "排序理由",
      "impact": 5,
      "frequency": 4,
      "risk": 2,
      "evidence_ids": ["E-001", "E-002"],
      "next_test": "最小验证动作"
    }
  ],
  "feishu_sync": {
    "requested": true,
    "upload_all_sources": true,
    "numbered_h1": true,
    "evidence_display": "id+description+source+locator",
    "highlight_policy": "critical-risks-only",
    "document_title": "飞书文档标题",
    "transcript": {
      "source_id": "SRC-002",
      "local_path": "相对 research-bundle.json 的转写文件路径",
      "mode": "inline_text",
      "section_title": "完整访谈转写"
    },
    "materials_table": {
      "enabled": true,
      "rows": [
        {
          "source_id": "SRC-001",
          "file_name": "interview.mp3",
          "type": "音频",
          "summary": "原始访谈录音",
          "evidence_ids": ["E-001"],
          "presentation": "附件"
        }
      ]
    },
    "media": [
      {
        "source_id": "SRC-001",
        "local_path": "相对 research-bundle.json 的音频路径",
        "mode": "attachment",
        "media_type": "audio",
        "caption": "原始访谈音频",
        "evidence_ids": ["E-001"]
      },
      {
        "source_id": "SRC-005",
        "local_path": "相对 research-bundle.json 的图片路径",
        "mode": "embed",
        "media_type": "image",
        "caption": "SRC-005｜现场照片说明｜关联证据 E-017",
        "evidence_ids": ["E-017"]
      }
    ]
  },
  "next_questions": ["下一轮研究问题"]
}
```

约束：

- `sources`、`evidence` 的 ID 唯一。
- `journey` 为 5—7 个阶段，`emotion` 为 -2 到 2 的整数。
- `impact`、`frequency`、`risk` 为 1 到 5 的整数。
- `opportunities` 至少 3 项并按 `rank` 排序。
- `next_questions` 至少 5 项。
- `已验证事实`和`合理推断`必须有有效证据引用。
- 不可识别或证据不足的字段不要猜测。
- `feishu_sync.requested=true` 时，必须指定一份写入正文的完整转写、至少一份音频附件，并列出所有作为图片证据的配图。
- `feishu_sync` 中的路径相对 `research-bundle.json` 解析；同步前必须检查文件存在且可读。
- 每个媒体项必须关联来源编号和证据编号；图片 caption 必须同时出现两者。
- `upload_all_sources=true` 时，`media` 和 `materials_table.rows` 必须分别覆盖 `sources` 中每一个已读取来源；转写即使已写入正文，也必须保留原文件附件。
- `numbered_h1` 必须为 `true`，`evidence_display` 必须为 `id+description+source+locator`。
- 素材表每行必须包含非空的内容摘要和飞书呈现方式，不能只列文件名。
