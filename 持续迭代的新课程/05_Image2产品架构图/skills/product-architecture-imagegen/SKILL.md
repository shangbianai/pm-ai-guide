---
name: product-architecture-imagegen
description: Generate polished product architecture images from natural-language product descriptions using image 2 and a numbered catalog of 16 bundled visual references. Use when the user asks to create, draw, redesign, or explore a 产品架构图、平台架构图、业务架构图、AI产品架构图、能力地图 or multi-role platform diagram; when they need prompt optimization; or when they want to preview, choose, auto-match, or randomly select an architecture visual style.
---

# Product Architecture Imagegen

Turn a rough product description into an optimized architecture brief, let the user choose one of 16 visual references, then generate a business-ready bitmap with image 2.

## Core Workflow

1. Read [prompt-optimization.md](references/prompt-optimization.md) and convert the user's natural language into an `Architecture Brief`.
2. Determine the style mode:
   - Explicit `01-16`: use that style immediately.
   - No style and no auto instruction: enter preview mode and stop after presenting choices.
   - `auto`, `默认`, `你决定`, `直接生成`: auto-match and continue without waiting.
   - `random`, `随机`, `给我惊喜`: select an eligible random style.
3. Follow [selection-rules.md](references/selection-rules.md).
4. Load only the selected entry from [style-manifest.json](references/style-manifest.json).
5. Inspect the selected `assets/style-XX.png` with `view_image` before generation. Treat it as a **style/composition reference**, never as the product-content source.
6. Load and follow the installed `imagegen` skill. Use the built-in image generation path (image 2). Do not silently switch models or use a CLI/API fallback.
7. Build the final prompt from the Architecture Brief plus the selected style's `layout` and `prompt_cues`.
8. Generate the image, inspect text, hierarchy, relationships and reference adherence, then make at most one targeted correction when a single defect is obvious.
9. Save project-bound outputs outside the skill folder. Deliver the PNG, the final prompt, the selected style number/name and any assumptions.

## Preview Mode

When the user gives a product description but no style choice:

1. Return a compact Architecture Brief.
2. Show the absolute-path image `assets/style-contact-sheet.png` inline.
3. Link the absolute paths of:
   - `references/style-catalog.md`
   - `references/style-catalog.pdf`
4. Ask the user to reply with `01-16`, `auto`, or `random`.
5. Do not generate the final architecture image in that turn.

The catalog is the required visual selection surface. Do not describe sixteen styles only as a text list when the preview assets are available.

## Prompt Upgrade Rules

- Separate external roles, channels, business capabilities, application/platform services, data, models/algorithms, infrastructure and cross-cutting governance.
- Keep one abstraction level per visual group.
- Use short Chinese labels, normally 2-8 characters; preserve recognized technical abbreviations.
- Use relationship verbs such as `采集`, `支撑`, `调用`, `编排`, `沉淀`, `反馈`, `治理`.
- Mark inferred domain modules as assumptions when source information is incomplete.
- Reduce each visible group to 3-7 modules. Preserve extra details in the delivered prompt rather than overcrowding the image.
- Require every exact label to be horizontal, front-facing and verbatim.

## Reference Fidelity

Preserve from the selected image:

- composition and spatial metaphor;
- shape language, line style and visual density;
- palette logic and typography mood;
- arrow placement and governance treatment.

Replace from the selected image:

- product name and subtitle;
- every role, module, layer, value and relationship label;
- domain-specific icons when they no longer fit.

Explicitly prohibit old reference-product labels from leaking into the new image.

## Auto and Random Helpers

Run from the skill directory:

```bash
python scripts/recommend_style.py --mode auto --text "<architecture brief>"
python scripts/recommend_style.py --mode random --text "<user request>"
```

If auto matching produces no keyword score, use `06 居中对称咨询阶梯`.

## Catalog Maintenance

The files `references/style-catalog.md`, `references/style-catalog.pdf` and `assets/style-contact-sheet.png` are generated from `references/style-manifest.json` plus `assets/style-01.png` through `assets/style-16.png`.

After replacing a reference image or editing the manifest, rebuild them with:

```bash
python scripts/build_catalog.py
```

Do not renumber styles casually. The number is a stable user-facing interface.

## Output Contract

Always report:

- selected style number and name;
- final saved image path;
- final reusable prompt;
- assumptions or omitted low-priority modules.

For Chinese text-heavy images, state only when relevant that exact-text SVG/HTML can be produced as a separate deterministic follow-up. Do not substitute SVG for image 2 when the user asked for image generation.
