# Authoring Rules

## Logo Replacement

If the user supplies a logo:

1. Use the original logo file directly.
2. Preserve transparency when available.
3. Replace every repeated upper-right logo slot and any cover/ending logo occurrence that represents the old brand.
4. Keep the source slot's height and right alignment. Use contain-fit, not cover-crop, unless the user asks for a crop.
5. For a single logo replacing two source logos, use the combined upper-right brand area and align the logo to the far right.
6. Never use image generation for the logo.
7. Never leave source-brand logos or company names visible in final renders unless the user explicitly wants co-branding.
8. Do not draw a border, grey box, placeholder rectangle, or visible container around the logo.

For uploaded logos with excess transparent or white margin, run `scripts/prepare_logo_for_ppt.py` to create a trimmed transparent PNG before insertion. Insert the processed logo as an image with `fit: "contain"` and no line/border.

If the user does not supply a logo, use `assets/shangbianzhiyuan-logo-horizontal.png`. This default asset is the high-contrast horizontal lockup: blue icon with black Chinese/English wordmark for readability in small upper-right PPT logo slots.

The preferred logo is the horizontal 熵变智元 lockup: icon on the left, Chinese and English wordmark on the right. Use the all-blue horizontal variant only when a monochrome blue brand treatment is requested. Use the icon-only asset only in tight square spaces.

## Source-Brand Cleanup

Final decks must not contain source-brand remnants:

- remove or replace all old logos,
- remove or rewrite old company names and slogans,
- replace old website/contact text,
- avoid co-branding unless explicitly requested.

This cleanup must be checked in rendered slide previews and, when practical, by searching final PPTX XML text.

## Image 2 Generation

Use `image 2` for newly generated raster illustrations when the source deck's existing image does not match the new slide topic.

Before generating or inserting an image, decide its slide role:

- `evidence scene`: shows the hiring/workplace/user scenario behind the claim,
- `capability metaphor`: visualizes an abstract capability such as AI judgment, data insight, or workflow orchestration,
- `workflow snapshot`: supports a process, path, funnel, or sequence,
- `atmosphere background`: used mainly on cover, section, or closing pages.

Do not use a generated image as a loose decoration. It must be visually connected to a nearby title, chart, card, matrix, or flow step. If the current template page has no natural image area, create a deliberate image module with a thin blue/grey outline, a white backing, and a short editable caption.

For each generated image, derive a short image brief before generation:

- slide number and title,
- target frame size/aspect ratio,
- core message,
- desired subject,
- required negative space,
- forbidden content.

Prompt pattern:

```text
Create a realistic enterprise technology illustration for a Chinese corporate PowerPoint slide.
Topic: <slide title and one-sentence message>.
Scene/content: <specific industry/platform/safety/data scenario>.
Style: clean blue-white corporate report aesthetic, credible, modern, not flashy.
Composition: <aspect ratio>, <left/right/top negative space>, suitable for cropping into <frame description>.
Avoid: readable text, fake logos, fake UI screenshots, fake charts with numbers, QR codes, watermarks.
```

After generation:

1. Crop/fit the image to the inherited image frame.
2. Keep image focus consistent with the slide title.
3. Place the image in a reserved visual zone, not on top of unrelated content.
4. Add an editable caption only when it helps connect the image to the slide argument.
5. Do not let the image cover title bars, page markers, logo chrome, chart labels, body text, or conclusions.
6. If the generated image contains unwanted text, marks, or malformed diagrams, regenerate or replace it.

## Text Emphasis

Use emphasis to create reading hierarchy:

- Use bold for the page's key conclusion, decisive contrast, or action phrase.
- Use red (`#C00000` or a close restrained corporate red) only for risks, compression, mismatch, declining value, or urgent constraints.
- Use primary blue (`#0061AE`) for positive capability, strategic keyword, or target state.
- Limit emphasis to 1-3 phrases per content slide.
- Do not highlight full paragraphs; split or shorten text instead.

## Choosing Template vs Image Generation

- Use template for all slide layout, title bars, page numbering, logo placement, dividers, text boxes, and editable content.
- Use the bundled source PPTX as the actual slide skeleton. Cover, agenda, transition pages, and ending pages should be duplicated from source slides, not reconstructed manually.
- Use image generation for atmosphere, industrial scenes, abstract data-platform backgrounds, capability ecosystem visuals, and non-evidence illustrations.
- Use emoji-style pictorial accents only for small in-slide illustrations when requested. They cannot replace substantive content. First build the chart, matrix, table, or structured analysis; then add any emoji accents sparingly.
- Use user-provided assets for real products, screenshots, logos, QR codes, certificates, people, and exact event information.

## Agenda And Closing Pages

- Agenda pages should preserve the large `目录 / CONTENTS` treatment and use a clean list on the right. Use larger readable chapter titles and avoid emoji by default.
- Closing pages should support a polished `谢谢观看` layout. Use image 2 or a supplied media image as a 16:9 background when useful, then overlay editable title text and clear QR placeholders.
- Never generate fake QR codes. Use placeholder boxes for personal WeChat and group QR codes unless the user supplies real QR images.

## QA Checklist

Before delivery, render all slides and check:

- The custom logo appears everywhere the old logo appeared.
- No source-brand logo or source-brand text remains accidentally.
- Page markers and top rules are consistent.
- Titles do not wrap unexpectedly.
- Body text is not clipped.
- Generated images match the slide topic and frame aspect ratio.
- Generated images contain no fake logos, fake UI text, fake numbers, or watermarks.
- No empty inherited placeholders remain.
