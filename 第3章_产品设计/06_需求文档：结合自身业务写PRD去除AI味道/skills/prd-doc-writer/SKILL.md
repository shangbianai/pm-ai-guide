---
name: prd-doc-writer
description: Use this skill when the user wants to write, structure, rewrite, or polish a PRD/需求文档/功能需求说明书 from prototypes, business notes, meeting records, screenshots, process diagrams, feature lists, or rough requirements. It produces a professional Chinese PRD with revision history, scope, glossary, business process, page elements, business rules, functional details, non-functional requirements, launch/offline plan, acceptance criteria, and open questions while removing generic AI-sounding prose.
---

# PRD Doc Writer

## Core Rule

Write a PRD that can be reviewed by business, design, development, testing, operations, legal, finance, and support teams. Do not output generic “AI summary” prose. Prefer concrete structure, tables, rules, states, page fields, flows, and acceptance criteria.

## Workflow

1. Clarify the product, business goal, target users, scope, prototype/source material, and expected output format.
2. Read the PRD structure in `references/prd-template.md`.
3. If the user only has rough notes, first produce a “待确认问题” list before drafting.
4. Draft the PRD in Chinese Markdown using the template structure.
5. For each function module, include:
   - 功能描述
   - 业务流程
   - 页面/界面说明
   - 页面元素表
   - 业务规则
   - 状态与异常
   - 验收标准
6. If source material lacks a rule or detail, write it under “待确认问题”; do not invent fake certainty.
7. Before final output, run the quality checklist in `references/prd-quality-checklist.md`.

## Style

- Use precise product language, not promotional language.
- Use tables for fields, rules, versions, permissions, states, and acceptance criteria.
- Avoid vague phrases such as “提升用户体验”, “智能化赋能”, “打造闭环” unless followed by measurable rules or scenarios.
- Keep business judgment visible: scope, assumptions, risks, dependencies, and decisions must be explicit.

## Output

Default output is one Markdown PRD. If the user asks for supporting files, also provide:

- PRD 模板
- PRD 生成提示词
- 验收清单
- 待确认问题清单

