#!/usr/bin/env python3
import argparse
import html
import json
import random
import subprocess
import time
from pathlib import Path

PALETTE = {
    "blue": ("#a5d8ff", "#1971c2"),
    "yellow": ("#ffec99", "#e67700"),
    "green": ("#b2f2bb", "#2b8a3e"),
    "violet": ("#d0bfff", "#6741d9"),
    "red": ("#ffc9c9", "#c92a2a"),
    "gray": ("#e9ecef", "#495057"),
}


def base_element(element_id, kind, x, y, width, height, seed):
    return {
        "id": element_id, "type": kind, "x": x, "y": y, "width": width, "height": height,
        "angle": 0, "strokeWidth": 2, "strokeStyle": "solid", "roughness": 2,
        "opacity": 100, "groupIds": [], "frameId": None, "index": element_id,
        "roundness": {"type": 3}, "seed": seed, "version": 1,
        "versionNonce": seed * 13 + 7, "isDeleted": False, "boundElements": [],
        "updated": int(time.time() * 1000), "link": None, "locked": False,
    }


def rect(element_id, x, y, width, height, fill, stroke, seed):
    item = base_element(element_id, "rectangle", x, y, width, height, seed)
    item.update({"strokeColor": stroke, "backgroundColor": fill, "fillStyle": "solid"})
    return item


def arrow_element(element_id, x, y, width, height, stroke, seed):
    item = base_element(element_id, "arrow", x, y, width, height, seed)
    item.update({
        "strokeColor": stroke, "backgroundColor": "transparent", "fillStyle": "hachure",
        "points": [[0, 0], [width * .45, height * .25], [width, height]],
        "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
    })
    return item


def text_element(element_id, x, y, width, text, size, color, seed, align="left"):
    lines = text.splitlines() or [text]
    height = max(size * 1.35, len(lines) * size * 1.25)
    item = base_element(element_id, "text", x, y, width, height, seed)
    item.update({
        "strokeColor": color, "backgroundColor": "transparent", "fillStyle": "solid",
        "text": text, "fontSize": size, "fontFamily": 5, "textAlign": align,
        "verticalAlign": "top", "containerId": None, "originalText": text,
        "autoResize": True, "lineHeight": 1.25,
    })
    return item


def build(spec):
    random.seed(42)
    width, margin, gap, top = 1600, 70, 24, 180
    columns = spec.get("columns", [])[:5]
    if not columns:
        raise SystemExit("spec.columns must contain at least one column")
    column_width = (width - margin * 2 - gap * (len(columns) - 1)) / len(columns)
    item_h, item_gap = 100, 18
    max_items = max(len(column.get("items", [])) for column in columns)
    height = top + 100 + max_items * (item_h + item_gap) + 120
    elements, svg_blocks, connector_blocks = [], [], []
    title = str(spec.get("title", "讨论白板"))
    subtitle = str(spec.get("subtitle", "从讨论到产品共识"))
    elements.append(text_element("a00", margin, 48, 1200, title, 42, "#1f2937", 11))
    elements.append(text_element("a01", margin, 108, 1200, subtitle, 20, "#667085", 12))
    svg_blocks.append(f'<text x="{margin}" y="82" class="board-title">{html.escape(title)}</text>')
    svg_blocks.append(f'<text x="{margin}" y="122" class="board-subtitle">{html.escape(subtitle)}</text>')

    for column_index, column in enumerate(columns):
        x = margin + column_index * (column_width + gap)
        fill, stroke = PALETTE.get(column.get("color", "gray"), PALETTE["gray"])
        header_id = f"b{column_index:02d}"
        header = rect(header_id, x, top, column_width, 66, fill, stroke, 100 + column_index)
        header["angle"] = (-0.006 if column_index % 2 == 0 else 0.007)
        elements.append(header)
        elements.append(text_element(f"{header_id}t", x + 18, top + 18, column_width - 36, str(column.get("title", "")), 24, "#1f2937", 200 + column_index))
        header_angle = -0.4 if column_index % 2 == 0 else 0.4
        svg_blocks.append(f'<g class="note header" transform="rotate({header_angle} {x+column_width/2:.1f} {top+33})"><rect x="{x:.1f}" y="{top}" width="{column_width:.1f}" height="66" rx="{12 + column_index * 3}" fill="{fill}" stroke="{stroke}"/><text x="{x+18:.1f}" y="{top+42}" class="header-text">{html.escape(str(column.get("title","")))}</text></g>')
        for item_index, item_text in enumerate(column.get("items", [])):
            y = top + 86 + item_index * (item_h + item_gap)
            item_id = f"c{column_index:02d}{item_index:02d}"
            card = rect(item_id, x, y, column_width, item_h, "#fffdf8", stroke, 300 + column_index * 20 + item_index)
            angle = (-0.006, 0.004, -0.003)[item_index % 3]
            card["angle"] = angle
            elements.append(card)
            elements.append(text_element(f"{item_id}t", x + 16, y + 18, column_width - 32, str(item_text), 20, "#243042", 500 + column_index * 20 + item_index))
            safe_text = html.escape(str(item_text))
            card_angle = (-0.5, 0.35, -0.2)[item_index % 3]
            corner = (7, 18, 2)[item_index % 3]
            dash = ' stroke-dasharray="9 5"' if column_index == 1 and item_index == 1 else ""
            svg_blocks.append(f'<g class="note" transform="rotate({card_angle} {x+column_width/2:.1f} {y+item_h/2})"><rect x="{x:.1f}" y="{y}" width="{column_width:.1f}" height="{item_h}" rx="{corner}" fill="#fffdf8" stroke="{stroke}"{dash}/><foreignObject x="{x+16:.1f}" y="{y+14}" width="{column_width-32:.1f}" height="{item_h-24}"><div xmlns="http://www.w3.org/1999/xhtml" class="note-text">{safe_text}</div></foreignObject></g>')

    for connection_index, connection in enumerate(spec.get("connections", [])):
        try:
            source_column, source_item = connection["from"]
            target_column, target_item = connection["to"]
            sx = margin + source_column * (column_width + gap) + column_width
            sy = top + 86 + source_item * (item_h + item_gap) + item_h / 2
            tx = margin + target_column * (column_width + gap)
            ty = top + 86 + target_item * (item_h + item_gap) + item_h / 2
        except (KeyError, TypeError, ValueError, IndexError):
            continue
        connector_color = str(connection.get("color", "#495057"))
        label = html.escape(str(connection.get("label", "")))
        dx, dy = tx - sx, ty - sy
        elements.append(arrow_element(f"d{connection_index:02d}", sx, sy, dx, dy, connector_color, 800 + connection_index))
        bend = 38 if connection_index % 2 == 0 else -38
        mx = (sx + tx) / 2
        connector_blocks.append(f'<path class="connector" d="M {sx:.1f} {sy:.1f} C {mx:.1f} {sy+bend:.1f}, {mx:.1f} {ty-bend:.1f}, {tx:.1f} {ty:.1f}" stroke="{connector_color}" marker-end="url(#arrow)"/>')
        if label:
            connector_blocks.append(f'<text x="{mx:.1f}" y="{(sy+ty)/2-8:.1f}" text-anchor="middle" class="connector-label">{label}</text>')

    excalidraw = {
        "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"viewBackgroundColor": "#fffdf6", "gridSize": 20, "gridStep": 5, "gridModeEnabled": False},
        "files": {},
    }
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="2" seed="8"/><feDisplacementMap in="SourceGraphic" scale="1.6"/></filter>
  <pattern id="hachureBackground" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(34)">
    <rect width="18" height="18" fill="#fffdf6"/>
    <path d="M 0 2 H 18 M 0 15 H 18" stroke="#f2d675" stroke-width="1.1" opacity=".48"/>
  </pattern>
  <pattern id="hachureNote" width="13" height="13" patternUnits="userSpaceOnUse" patternTransform="rotate(32)">
    <rect width="13" height="13" fill="#fffdf8"/>
    <path d="M 0 3 H 13" stroke="#eadca5" stroke-width="1" opacity=".48"/>
  </pattern>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker>
</defs>
<style>
.board-title{{font:700 46px "Kaiti SC","STKaiti","KaiTi","Comic Sans MS",cursive;fill:#111827;letter-spacing:2px}}
.board-subtitle{{font:22px "Kaiti SC","STKaiti","KaiTi",cursive;fill:#667085}}
.header-text{{font:700 26px "Kaiti SC","STKaiti","KaiTi","Comic Sans MS",cursive;fill:#1f2937}}
.note-text{{font:22px/1.42 "Kaiti SC","STKaiti","KaiTi","Comic Sans MS",cursive;color:#243042;display:flex;align-items:center;height:100%;overflow:hidden}}
.note:not(.header) rect{{fill:url(#hachureNote);stroke-width:2.2;filter:url(#rough)}}.note.header rect{{stroke-width:2.4;filter:url(#rough)}} body{{margin:0}}
.connector{{fill:none;stroke-width:3;stroke-linecap:round;stroke-dasharray:10 5;filter:url(#rough)}}
.connector-label{{font:700 18px "Kaiti SC","STKaiti","KaiTi",cursive;fill:#475569;paint-order:stroke;stroke:#fbfaf5;stroke-width:7px}}
</style><rect width="100%" height="100%" fill="url(#hachureBackground)"/>{''.join(connector_blocks)}{''.join(svg_blocks)}</svg>'''
    return excalidraw, svg, height


def main():
    parser = argparse.ArgumentParser(description="Render a hand-drawn discussion whiteboard")
    parser.add_argument("input")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--no-screenshot", action="store_true")
    args = parser.parse_args()
    source = Path(args.input).expanduser().resolve()
    spec = json.loads(source.read_text(encoding="utf-8"))
    output = Path(args.output_dir).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "whiteboard-source.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    excalidraw, svg, board_height = build(spec)
    excalidraw_text = json.dumps(excalidraw, ensure_ascii=False, indent=2)
    (output / "discussion-whiteboard.excalidraw").write_text(excalidraw_text + "\n", encoding="utf-8")
    (output / "discussion-whiteboard.svg").write_text(svg, encoding="utf-8")
    html_page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(str(spec.get("title","讨论白板")))}</title><style>
body{{margin:0;background:#e7edf4;font-family:-apple-system,"PingFang SC",sans-serif;color:#172033}}header{{position:sticky;top:0;z-index:2;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 18px;background:rgba(255,255,255,.94);border-bottom:1px solid #cad5e1}}h1{{font:700 20px "Kaiti SC","STKaiti","KaiTi",cursive;margin:0}}.actions{{display:flex;gap:8px;flex-wrap:wrap}}a{{border:1px solid #a8b7c7;border-radius:9px;padding:8px 11px;color:#184e77;text-decoration:none;font-weight:700;font-size:13px}}a.jpg{{background:#172033;color:#fff;border-color:#172033}}main{{padding:20px;overflow:auto}}.board{{width:max-content;min-width:100%;background:#fff;box-shadow:0 24px 70px rgba(37,56,77,.18)}}svg{{display:block;max-width:none}}
</style></head><body><header><h1>{html.escape(str(spec.get("title","讨论白板")))}</h1><div class="actions"><a href="discussion-whiteboard.excalidraw" download>下载可编辑源文件</a><a href="discussion-whiteboard.svg" download>下载 SVG</a><a class="jpg" href="discussion-whiteboard.jpg" download>下载 JPG 图片</a></div></header><main><div class="board">{svg}</div></main></body></html>'''
    html_path = output / "discussion-whiteboard.html"
    html_path.write_text(html_page, encoding="utf-8")
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if not args.no_screenshot and chrome.exists():
        subprocess.run([str(chrome), "--headless", "--disable-gpu", "--hide-scrollbars", f"--window-size=1600,{board_height}", f"--screenshot={output / 'discussion-whiteboard.png'}", (output / "discussion-whiteboard.svg").as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", str(output / "discussion-whiteboard.png"), "--out", str(output / "discussion-whiteboard.jpg")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(html_path)


if __name__ == "__main__":
    main()
