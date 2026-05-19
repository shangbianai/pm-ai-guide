#!/usr/bin/env python3
"""pm-slide-deck: 合并幻灯片图片为 PDF

用法：
    python merge-to-pdf.py <幻灯片目录> [--output 文件名.pdf]

依赖：
    pip install Pillow
"""

import argparse
import re
import sys
from pathlib import Path

from PIL import Image


def find_slide_images(dir_path):
    d = Path(dir_path)
    if not d.exists():
        print(f"目录不存在：{dir_path}", file=sys.stderr)
        sys.exit(1)

    slides = []
    for f in sorted(d.iterdir()):
        m = re.match(r"^(\d+)-slide-.*\.(png|jpg|jpeg)$", f.name, re.IGNORECASE)
        if m:
            slides.append({"filename": f.name, "path": str(f), "index": int(m.group(1))})

    slides.sort(key=lambda s: s["index"])

    if not slides:
        print(f"未找到幻灯片图片：{dir_path}", file=sys.stderr)
        print("期望格式：01-slide-*.png, 02-slide-*.png 等", file=sys.stderr)
        sys.exit(1)

    return slides


def create_pdf(slides, output_path, dpi=150):
    images = []
    first_image = None

    for slide in slides:
        img = Image.open(slide["path"])
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

        if first_image is None:
            first_image = img
        else:
            images.append(img)

        print(f"已添加：{slide['filename']}")

    if first_image is None:
        print("没有可合并的图片", file=sys.stderr)
        sys.exit(1)

    first_image.save(output_path, "PDF", resolution=dpi, save_all=True, append_images=images)

    print(f"\n已创建：{output_path}")
    print(f"总页数：{len(slides)}")


def main():
    parser = argparse.ArgumentParser(description="合并幻灯片图片为 PDF")
    parser.add_argument("dir", help="幻灯片目录")
    parser.add_argument("--output", "-o", help="输出文件名")
    parser.add_argument("--dpi", type=int, default=150, help="DPI（默认 150）")
    args = parser.parse_args()

    slides = find_slide_images(args.dir)

    dir_name = Path(args.dir).name
    if dir_name == "slide-deck":
        dir_name = Path(args.dir).parent.name

    output = args.output or str(Path(args.dir) / f"{dir_name}.pdf")

    print(f"在 {args.dir} 中找到 {len(slides)} 张幻灯片\n")
    create_pdf(slides, output, args.dpi)


if __name__ == "__main__":
    main()
