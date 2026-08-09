# HTML Export Requirements

Use this reference when generating polished product architecture diagrams as HTML.

## Required Structure

The HTML file must be standalone: embedded CSS and JavaScript, no external CDN dependency.

Required elements:

- `#captureArea`: the diagram region to export.
- `#exportPng`: button labeled `保存为 PNG`.
- `#exportJpg`: button labeled `保存为 JPG`.
- `#status`: small status text for success or fallback errors.

Recommended controls:

- Diagram type tabs when multiple classifications are shown.
- A `fit width` layout so the exported region has stable dimensions, usually 1200-1600px wide.

## Export Behavior

Prefer a reliable data-model canvas export for architecture diagrams:

1. Keep the diagram data as structured arrays: layers, module labels, side rails, domain groups.
2. Render the visible HTML from that data.
3. On export, draw the same data directly to a canvas with rectangles, text, and simple gradients.
4. For PNG, call `canvas.toDataURL("image/png")`.
5. For JPG, paint a white background first, then call `canvas.toDataURL("image/jpeg", 0.95)`.
6. Create a temporary `<a download>` element, click it, then remove it.
7. Update `#status`.

Use SVG `foreignObject` snapshot only as a secondary approach because local file pages and some browsers may taint the canvas:

1. Clone `#captureArea`.
2. Inline or preserve the CSS needed for the clone.
3. Wrap the clone inside an SVG `foreignObject`.
4. Draw the SVG image onto a canvas.

If canvas export is blocked, show a concise fallback message and keep the HTML diagram usable for browser screenshot/print.

## Verification

When tooling allows, verify:

- The page renders nonblank.
- Tabs switch the visible diagram.
- `保存为 PNG` and `保存为 JPG` run without JavaScript errors.
- Exported image dimensions match `#captureArea`.
- Chinese labels fit inside boxes at desktop width and do not overlap.

## Visual Rules

- Keep the diagram, not the toolbar, inside `#captureArea`.
- Use stable fixed export dimensions with responsive scaling outside the capture area.
- Use readable Chinese fonts and high contrast.
- Put layer names in a left column for layered diagrams.
- Keep module boxes aligned in rows; use grids instead of free-floating coordinates when possible.
- Use arrows only where they explain relationships. Layer order can imply support flow.
