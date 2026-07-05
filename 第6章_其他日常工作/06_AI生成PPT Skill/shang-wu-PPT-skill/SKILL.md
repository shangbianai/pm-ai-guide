---
name: dark-ai-html-ppt
description: Use when creating dark Chinese HTML presentation decks for AI/business sharing with brand logo, cover/body/transition/closing layouts, typewriter bottom-line reveal with keyboard sound, image2/Seedream-generated visuals, click-to-zoom images, and collapsible navigation controls.
---

# Dark AI HTML PPT

Create a dark, cinematic HTML presentation for Chinese AI/business sharing sessions. The deck should feel like a polished keynote, not a document dump.

## Workflow

1. Collect the event title, date, location, speaker/brand, section outline, QR codes, and any real photos.
2. Start from `templates/reference-3-pages-template.html` for production drafts, or open `examples/reference-3-pages.html` as the visual reference. Keep `templates/dark-ai-ppt.css` and `templates/dark-ai-ppt.js`. The reference/template file demonstrates cover, body, report, transition, and closing page types. When the deck must be shared as one offline file, use `templates/dark-ai-ppt-reference-standalone.html`, which inlines CSS, JS, images, and audio so it can be opened directly from the local filesystem.
3. Generate slide visuals with image2/Seedream. Prompts must match the slide idea, target aspect ratio, and tone. Do not ask the model to render exact QR codes, logos, or critical text; overlay those in HTML.
4. Use `scripts/generate_seedream_image.py` when the Ark API is available. It reads `ARK_API_KEY` from the environment.
5. Verify in the browser at desktop size and check that titles, images, bottom quotes, controls, and zoom behavior do not overlap.

## Layouts

- Cover: top-left logo, one large centered title, one light-gray subtitle with clear vertical spacing, and right-bottom one-line tags. For sharing decks, include topic/type, analysis theme, date, and presenter. Keep the cover to two visual text lines whenever possible.
- Body: use the unified report-style header on every正文页: a small vertical accent bar plus sequence number on the left, a one-line title, the brand lockup at the far right, and a white/green/gray gradient divider below. Do not mix cover-style centered titles into body pages. Under the divider, place a large left content rectangle and a right image2 visual in one row with exactly matching height. If text overflows, first shorten copy or reduce font size; do not enlarge the panel until the layout loses balance. Body copy uses Songti-style serif text around 16pt. The bottom summary is a short golden sentence; highlighted words use a translucent marker band that covers the lower part of the characters, not a simple underline.
- Report: use the same header system as Body. Prefer a polished dashboard made of data cards, charts, SVG diagrams, and one bottom insight. Keep side margins tight and balanced; do not reuse the sample topic verbatim.
- Transition: use one centered sentence only, usually one line and at most two lines. It should refocus attention, not explain. Use only a narrow key-phrase marker band beneath the emphasized words, with the band slightly overlapping the lower glyph area. Avoid extra horizontal/vertical rules, kicker labels, and explanatory bottom copy. If a demo label is needed, add one subtle light-gray note near the top such as “过渡页测试样例”.
- Closing: generate one full-slide image2 background with mood, line work, and reserved QR areas. Overlay exact critical text, brand logo, and QR codes in HTML so they remain readable and replaceable. QR cards must sit inside visible rectangular reserved areas; the QR itself is never baked into the generated image. The final slide should feel like a single designed image, not separate stacked cards.

## Interaction

- Bottom-line summary text is hidden by default. First blank-area click reveals it with a keyboard/typewriter sound. The next blank-area click advances.
- Right/down/space/enter advance; left/up/backspace go back.
- Click images with `data-zoom-src` to view full screen. In zoom mode, left/right arrows switch images.
- Right-bottom controls are collapsible and keep the same visual style as the reference deck.
- Keep controls compact by default. The collapsed state may show only the “…” button; expanded controls should remain smaller than slide content and never cover the bottom insight.
- Use a very tiny bottom progress marker instead of a full-width progress bar. Add a subtle lower-left page number for orientation.
- The middle page count in the controls opens a jump menu, so users can go directly to any slide while editing.
- Edit mode: include an `编辑` button. Mark editable text with `data-editable="stable-key"`. In edit mode, users can click text and modify it inline; changes are saved to localStorage for that HTML file.
- Annotation mode: include a `标注` button. It opens a compact color toolbar and lets the presenter draw on the current screen with a pen. Provide color choice, clear, and done actions. Do not advance slides while annotation mode is active.
- Logo replacement: mark logo images with `data-logo`. The `Logo` button lets users upload an image and globally replaces all marked logos in the current deck. Default to a horizontal brand lockup: logo mark on the left, Chinese brand name on the right. Keep exact brand logos as uploaded assets, not generated images.

## Style Rules

- Dark background, restrained green/gold accent, clean rounded panels, generous vertical spacing.
- Prefer one-line titles. If a title must wrap, keep it to two lines and reduce font size.
- Keep page labels small in the upper-left; never let labels collide with titles.
- Use translucent orange/green marker highlights behind key words. The highlight band should sit under the glyphs and cover roughly the lower third of the text.
- For body/report-style pages, keep the header clean and identical: accent index, title, logo, then one strong divider line. Do not crowd the title area.
- Body pages and report pages share the same header and divider system. The sequence mark, title baseline, right logo, and divider position should remain consistent across the deck.
- In fullscreen, keep the body/report layout close to the canvas edges with tight top/left margins, while preserving a clean title/divider/logo header.
- Put the important idea in the bottom-line quote, not in long paragraphs. Keep bottom-line spacing centered between the content above and the lower canvas edge; avoid letting controls cover it.
- Use generated images as visual explanation, not decoration. Each image should express the slide's core action or business scenario.
