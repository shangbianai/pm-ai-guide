---
name: product-architecture-diagrams
description: Create polished product architecture diagrams, business architecture maps, application/data/technology architecture views, platform layering diagrams, capability maps, and product system structure charts from product descriptions, PRDs, meeting notes, screenshots, or rough module lists. Use when Codex needs screenshot-like layered architecture charts, colorful HTML/SVG diagrams with PNG/JPG export, Mermaid drafts, FigJam/Figma-ready diagrams, or image-generation prompts while applying product architecture methodology and diagram-type classification.
---

# Product Architecture Diagrams

## Purpose

Turn unclear product/system material into a clear, presentation-ready product architecture diagram with the right level of abstraction, diagram type, labels, relationships, and visual style.

Default to a colorful, layered, screenshot-like HTML/SVG architecture chart when the user wants a product architecture diagram they can use directly. Keep the methodology strong, but make the artifact visually useful.

## Core Workflow

1. Clarify the diagram job silently when possible: audience, purpose, product scope, known modules, technical depth, output format, and whether the user wants a business-facing or engineering-facing view.
2. Classify the requested diagram using [diagram-types.md](references/diagram-types.md). If the user provides screenshots, infer the nearest type from the layout.
3. Apply the methodology checklist in [methodology.md](references/methodology.md): business intent, user/experience layers, capability decomposition, architecture domains, platform support, data flow, governance/operations.
4. Choose an output style from [templates.md](references/templates.md): layered platform, domain relationship, swimlane, capability matrix, C4-style, value-flow, AI/data, or hybrid.
5. Produce the artifact directly. Prefer **HTML/SVG with PNG/JPG export** for screenshot-like architecture charts; use Mermaid only for quick logical drafts or when the user explicitly requests Mermaid; use Figma/FigJam tools when the user explicitly asks for Figma or an editable board.
6. If producing HTML, follow [html-export.md](references/html-export.md): include `保存为 PNG` and `保存为 JPG` buttons, export the chart area, and verify the buttons when tooling is available.
7. Include a brief reading guide: what each layer/domain means, what is upstream/downstream, what is support vs core capability, and what assumptions were made.

## Diagram Selection

Use these defaults:

- **Business/product explanation**: business architecture or value-flow map.
- **PRD/module planning**: capability map plus layered product platform diagram.
- **Engineering alignment**: layered application/technology/data diagram or C4 context/container view.
- **Executive communication**: 3-5 architecture domains with sparse relationships.
- **Screenshot-like layered boxes**: default to a colorful HTML layered product architecture diagram with presentation, gateway, application, business capability, support platform, model/data platform, technology platform, and monitoring/governance side rail.
- **Unclear request**: provide one recommended diagram and optionally a second alternative if the material supports two valid views.

## Output Rules

- Use Chinese labels when the user's material is Chinese.
- Keep labels short: usually 2-8 Chinese characters or 1-4 English words.
- Separate **core business capability**, **support capability**, **technical support**, **data capability**, **operations/governance**, and **external actors**.
- For visual deliverables, use top-down horizontal layers, large colored layer bands, dashed architecture boundaries, and compact module boxes. This should resemble a presentation architecture screenshot, not a generic graph.
- Show relationships with verbs on edges when useful: `细化`, `实现`, `支撑`, `协作`, `监控`, `消费`, `沉淀`.
- Avoid mixing abstraction levels in one row. If unavoidable, group with clear boundaries.
- Prefer 4-7 major blocks per diagram and 3-9 items per block. Collapse long lists into `...` or "其他服务" unless detail is requested.
- When input is incomplete, create a useful draft and mark assumptions as `假设`.
- When creating Mermaid flowcharts, quote node labels that contain punctuation and keep syntax simple.

## Visual Deliverable Defaults

- Create a standalone `.html` file when the user asks for a usable architecture image, a more polished/绚烂 style, download/export, JPG/PNG, or screenshot-like chart.
- The first screen of the HTML should be the diagram itself, not a landing page or long explanation.
- Include a compact toolbar with diagram-type tabs and `保存为 PNG` / `保存为 JPG` buttons when multiple variants are useful.
- Use a vivid but professional palette: cyan/blue for access/application, rose/red for risk services, amber/orange for modeling, pink/purple for data/AI, green for data foundation, indigo/dark blue for monitoring/governance.
- Use image generation only when the user explicitly asks for a bitmap concept image or says to use imagegen/image 2. Prefer HTML/SVG for exact Chinese text, editable structure, and reliable PNG/JPG export. If using image generation, prompt for a clean layered product architecture chart and then also provide a text/HTML source when exact labels matter.

## Quality Checklist

Before finalizing, verify:

- The diagram has a clear main story: who uses what, what capabilities create value, what platforms support them, what data/technology enables them.
- Layers flow from user/business intent down to application, data, technology, operations, or from business model to implementation domains.
- Governance/monitoring/DevOps are shown as cross-cutting support when they affect many modules.
- The diagram can be read without a long explanation.
- The chosen style matches the audience: dense and precise for engineers, clean and domain-oriented for executives, process-oriented for business stakeholders.
- HTML exports work: PNG and JPG buttons create downloads or a clear fallback message.

## Reference Loading

- Load [methodology.md](references/methodology.md) when deciding decomposition logic or when the user asks for "方法论".
- Load [diagram-types.md](references/diagram-types.md) when choosing among multiple forms or matching screenshot styles.
- Load [templates.md](references/templates.md) when generating Mermaid/HTML/SVG structures.
- Load [html-export.md](references/html-export.md) when producing a polished HTML diagram or adding download buttons.
