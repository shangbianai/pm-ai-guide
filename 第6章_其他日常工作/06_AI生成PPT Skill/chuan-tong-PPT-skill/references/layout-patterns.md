# Layout Patterns

The bundled source deck is 16:9 with 38 slides. Use source-slide numbers from `assets/source-template.pptx` when building `template-frame-map.json`.

## Source Slide Families

| Role | Use Source Slides | Notes |
| --- | --- | --- |
| Cover | 1 | Blue lower band, skyline line art, centered title, bottom logo row. Best for first slide only. |
| Agenda | 2 | Large blue left wedge, `目录 / CONTENTS`, geometric pale background. |
| Section divider | 3, 6, 14, 32 | Centered grey-outlined title box, top/bottom blue vertical blocks. Use for major chapters. |
| Standard content | 4, 5, 8, 10, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 31, 34, 35, 36 | White report pages with top rule, left blue section number block, right logo chrome. Good for bullets, thesis, short analysis, conclusions. |
| Architecture or platform diagram | 7, 9, 11, 12, 16, 30, 33, 37 | Use when the slide needs layered systems, capability maps, ecosystem diagrams, or structured model visuals. |
| Large visual or demo | 15, 18, 25 | Use for screenshots, generated hero visuals, dashboards, product renderings, or full-width scenes. |
| Ending | 38 | Pale geometric background and centered slogan. |

## Mapping Heuristics

- Use a cover only once.
- Use an agenda when the deck has three or more chapters.
- Use section dividers before major chapters; keep the source divider's sparse style.
- Use standard content slides for text-first ideas. Keep each page to one message.
- Use architecture/platform slides when the title contains words like 平台, 架构, 体系, 能力, 流程, 数据, 生态, or 路径.
- Use large visual slides when the page needs emotional impact, product scene, city/park/industrial background, or dashboard-style demonstration.
- Use ending slide 38 for thanks, slogan, or contact close.

## Page Numbering

The source template uses blue chapter labels such as `1`, `2.1`, `3.5`, `4` in the top-left block. Preserve the block position and update text to match the output outline.

## Logo Slots

The recurring logo chrome is in the upper-right region. In many source layouts it appears as two inherited images around:

- right logo: x 1131, y 12, w 130, h 34 px
- left logo: x 1018, y 12, w 94, h 34 px

Use `assets/shangbianzhiyuan-logo-horizontal.png` as the default replacement logo. It is a high-contrast horizontal lockup chosen for small upper-right PPT slots. Replace the full upper-right brand group with this horizontal logo and preserve the original combined height and right alignment. When the user provides two logos, map them left-to-right into the two inherited slots.
