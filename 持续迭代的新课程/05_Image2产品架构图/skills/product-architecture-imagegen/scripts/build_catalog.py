#!/usr/bin/env python3
"""Build Markdown, contact sheet and PDF catalogs from the style manifest."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
REFERENCES = ROOT / "references"
MANIFEST = REFERENCES / "style-manifest.json"


def load_styles() -> list[dict]:
    styles = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ids = [style["id"] for style in styles]
    if ids != [f"{index:02d}" for index in range(1, 17)]:
        raise ValueError(f"Style IDs must be stable 01-16, got {ids}")
    for style in styles:
        image_path = ROOT / style["asset"]
        if not image_path.exists():
            raise FileNotFoundError(image_path)
    return styles


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size, index=0)
    return ImageFont.load_default()


def build_contact_sheet(styles: list[dict]) -> Path:
    canvas_w, canvas_h = 2400, 1600
    cols, rows = 4, 4
    margin, gutter = 48, 24
    header_h = 108
    cell_w = (canvas_w - margin * 2 - gutter * (cols - 1)) // cols
    cell_h = (canvas_h - header_h - margin - gutter * (rows - 1)) // rows
    background = Image.new("RGB", (canvas_w, canvas_h), "#F4F7FB")
    draw = ImageDraw.Draw(background)
    title_font = find_font(44, bold=True)
    label_font = find_font(26, bold=True)
    small_font = find_font(18)
    draw.text((margin, 28), "产品架构图 Image 2 风格目录｜01-16", fill="#0B1F4D", font=title_font)

    for index, style in enumerate(styles):
        row, col = divmod(index, cols)
        x = margin + col * (cell_w + gutter)
        y = header_h + row * (cell_h + gutter)
        draw.rounded_rectangle((x, y, x + cell_w, y + cell_h), radius=18, fill="#FFFFFF", outline="#D8E1F0", width=2)
        image_path = ROOT / style["asset"]
        with Image.open(image_path) as source:
            thumb = ImageOps.contain(source.convert("RGB"), (cell_w - 24, cell_h - 82), method=Image.Resampling.LANCZOS)
        tx = x + (cell_w - thumb.width) // 2
        ty = y + 12
        background.paste(thumb, (tx, ty))
        label_y = y + cell_h - 61
        draw.text((x + 16, label_y), style["id"], fill="#155EEF", font=label_font)
        draw.text((x + 70, label_y + 2), style["name"], fill="#172B4D", font=small_font)

    output = ASSETS / "style-contact-sheet.png"
    background.save(output, quality=95)
    return output


def build_markdown(styles: list[dict]) -> Path:
    lines = [
        "# 产品架构图 Image 2 风格目录",
        "",
        "选择 `01-16`、`auto`（按内容匹配）或 `random`（灵感随机）。编号是稳定接口。",
        "",
        "![16种风格总览](../assets/style-contact-sheet.png)",
        "",
    ]
    for style in styles:
        lines.extend(
            [
                f"## {style['id']}｜{style['name']}",
                "",
                f"![{style['id']} {style['name']}](../{style['asset']})",
                "",
                f"- 构图：{style['layout']}",
                f"- 适合：{style['recommended_for']}",
                f"- 提示词线索：{style['prompt_cues']}",
                "",
            ]
        )
    output = REFERENCES / "style-catalog.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def draw_fitted_image(pdf: canvas.Canvas, image_path: Path, box: tuple[float, float, float, float]) -> None:
    x, y, width, height = box
    with Image.open(image_path) as image:
        rgb = image.convert("RGB")
        iw, ih = rgb.size
        max_pixels_w = max(1, int(width * 2))
        max_pixels_h = max(1, int(height * 2))
        rgb.thumbnail((max_pixels_w, max_pixels_h), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        rgb.save(buffer, format="JPEG", quality=86, optimize=True)
        buffer.seek(0)
    scale = min(width / iw, height / ih)
    draw_w, draw_h = iw * scale, ih * scale
    pdf.drawImage(ImageReader(buffer), x + (width - draw_w) / 2, y + (height - draw_h) / 2, draw_w, draw_h, preserveAspectRatio=True)


def build_pdf(styles: list[dict], contact_sheet: Path) -> Path:
    output = REFERENCES / "style-catalog.pdf"
    page_w, page_h = landscape(A4)
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    pdf = canvas.Canvas(str(output), pagesize=(page_w, page_h))
    pdf.setTitle("产品架构图 Image 2 风格目录")

    pdf.setFillColorRGB(0.04, 0.12, 0.30)
    pdf.setFont("STSong-Light", 26)
    pdf.drawString(42, page_h - 48, "产品架构图 Image 2 风格目录")
    pdf.setFillColorRGB(0.23, 0.31, 0.45)
    pdf.setFont("STSong-Light", 12)
    pdf.drawString(42, page_h - 72, "选择 01-16、auto（按内容匹配）或 random（灵感随机）")
    draw_fitted_image(pdf, contact_sheet, (42, 42, page_w - 84, page_h - 130))
    pdf.showPage()

    for style in styles:
        pdf.setFillColorRGB(0.04, 0.12, 0.30)
        pdf.setFont("STSong-Light", 24)
        pdf.drawString(42, page_h - 48, f"{style['id']}｜{style['name']}")
        pdf.setFillColorRGB(0.20, 0.29, 0.43)
        pdf.setFont("STSong-Light", 11)
        pdf.drawString(42, page_h - 72, f"适合：{style['recommended_for']}")
        image_path = ROOT / style["asset"]
        draw_fitted_image(pdf, image_path, (42, 108, page_w - 84, page_h - 205))
        pdf.setFillColorRGB(0.12, 0.20, 0.33)
        pdf.setFont("STSong-Light", 10)
        pdf.drawString(42, 84, f"构图：{style['layout']}")
        prompt_text = f"提示词线索：{style['prompt_cues']}"
        max_chars = 55
        for line_index in range(0, len(prompt_text), max_chars):
            pdf.drawString(42, 66 - (line_index // max_chars) * 14, prompt_text[line_index: line_index + max_chars])
        pdf.setFillColorRGB(0.36, 0.43, 0.55)
        pdf.setFont("STSong-Light", 9)
        pdf.drawRightString(page_w - 42, 28, f"STYLE {style['id']} / 16")
        pdf.showPage()

    pdf.save()
    return output


def main() -> int:
    styles = load_styles()
    contact_sheet = build_contact_sheet(styles)
    markdown = build_markdown(styles)
    pdf = build_pdf(styles, contact_sheet)
    print(contact_sheet)
    print(markdown)
    print(pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
