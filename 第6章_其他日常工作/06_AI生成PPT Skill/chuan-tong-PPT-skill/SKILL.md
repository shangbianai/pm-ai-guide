---
name: shangbian-ppt-template
description: Create or rewrite PowerPoint decks in the 熵变智元 blue-white corporate report template style. Use when the user asks to make a 熵变智元 branded enterprise platform, technology company, AI company, industrial internet, or corporate introduction deck with automatic logo replacement and image 2 generated slide illustrations while preserving editable PPT layout.
---

# 熵变智元 PPT Template

Use this skill to create PPTX decks in the 熵变智元 branded blue-white corporate report style. The deck must use a source-template-first route:

- Directly duplicate source slides from `assets/source-template.pptx` for cover, agenda, section dividers, report pages, and ending pages. Do not approximate these pages by rebuilding them from scratch.
- Template-following for slide structure, typography, logo chrome, page markers, title bars, spacing, and page rhythm.
- `image 2` image generation only for new raster illustrations that must match the slide topic and the target image frame.
- Generated illustrations must be integrated into the slide composition, not pasted as floating decorations. Each image needs a clear role such as evidence scene, capability metaphor, workflow snapshot, or closing atmosphere.
- Emoji-style pictorial accents are optional and must never be the main content. If the user asks for emoji 配图, use them only as small supporting accents after building real diagrams, charts, tables, or structured content.
- Real logo assets for branding. Never generate, redraw, or approximate a logo.
- Source-brand logos and company text from the bundled source deck must be replaced or removed in final outputs.

## Required Assets

The source template is bundled at `assets/source-template.pptx`.

Default brand assets:

- Default horizontal logo: `assets/shangbianzhiyuan-logo-horizontal.png`
- Icon-only logo: `assets/shangbianzhiyuan-icon.png`
- Vertical fallback lockup: `assets/shangbianzhiyuan-logo-vertical.png`

When creating a deck, also use the `presentations:Presentations` skill and its template-following mode. Treat `assets/source-template.pptx` as the reference/template PPTX.

## Read As Needed

- Read `references/layout-patterns.md` before mapping output slides to source slides.
- Read `references/style-guide.md` before writing or editing slide content.
- Read `references/authoring-rules.md` before replacing logos, generating images, or exporting the final PPTX.

## Workflow

1. Collect the user's topic, intended audience, page count, outline/content, company name, and logo file if provided.
2. Build a slide plan with one role per slide: cover, agenda, section divider, standard content, architecture/platform diagram, large visual, case/demo, conclusion, or ending.
3. Map every output slide to a source slide from `references/layout-patterns.md`; use duplicated source slides rather than creating new visual systems.
4. Use template-following mode from the presentations skill:
   - inspect the bundled template,
   - create `template-frame-map.json`,
   - prepare `template-starter.pptx`,
   - edit inherited elements in place,
   - render final previews for QA.
5. Replace all logo slots with the user's logo when supplied; otherwise use `assets/shangbianzhiyuan-logo-horizontal.png`. Preserve the source logo box, alignment, and scale behavior.
6. For slides needing new visuals, generate raster images with `image 2` using the slide message and exact target frame. Insert the result into inherited image frames or bounded source image zones.
7. Bind every generated image to nearby content: align it with a chart/card/flow node, add a short editable caption if useful, and keep it inside a deliberate image frame or image+insight module.
8. Add restrained emphasis to text. Bold important conclusion phrases and use red only for risk, pressure, warning, or decisive contrast. Use blue for positive capability or strategic keywords.
9. Keep text concise enough to fit existing inherited text boxes. Prefer shortening copy, splitting slides, or remapping to a more suitable source slide over shrinking typography.
10. Render the final deck and inspect for text overflow, broken image crops, missing logos, source-brand remnants, inconsistent page markers, unwanted placeholders, and style drift.

## Hard Rules

- Do not rebuild the template from vibes, screenshots, or a brand palette. Duplicate and edit source slides.
- Preserve the original cover, agenda, section-divider, and ending-page silhouettes unless the user explicitly asks to redesign.
- Agenda pages should use the template's large typography and clean list structure. Do not fill agenda pages with emoji icons by default.
- Content pages must contain real analysis structures: cards, matrices, timelines, charts, tables, or diagrams. Do not leave a large blank area with only emoji or decorative icons.
- Generated illustrations must be content-aware. Do not drop a generic image into an empty corner. If the illustration does not clarify the slide's message, remove it or regenerate it.
- If a page has an illustration, the layout must explicitly reserve space for it: use an image card, a side panel, an evidence block, or an integrated visual module with consistent margins.
- Use 1-3 text emphasis points per content slide. Do not over-highlight whole paragraphs.
- Do not use generated images for logos, charts with exact data, screenshots, official UI, QR codes, or evidence.
- Do not place new free-floating elements over inherited placeholders unless the frame map explicitly allows that bounded insertion.
- Do not leave any source-brand logos, company names, slogans, website text, or co-branding visible unless the user explicitly requests co-branding.
- Default to 熵变智元 branding and the horizontal logo asset when the user does not supply a different logo.
- Use image generation for illustrative scene/technology/industry imagery when it improves relevance, but keep PPT text editable.

## Deliverable

Return the final `.pptx` path and mention whether a custom logo and generated images were used. Keep scratch previews and maps available for follow-up inspection but do not attach them unless asked.
