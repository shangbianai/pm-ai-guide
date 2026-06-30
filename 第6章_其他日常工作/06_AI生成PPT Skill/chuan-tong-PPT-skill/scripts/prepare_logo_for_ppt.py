#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image


def foreground_mask(im: Image.Image, white_threshold: int = 248) -> Image.Image:
    rgba = im.convert("RGBA")
    mask = Image.new("L", rgba.size, 0)
    src = rgba.load()
    dst = mask.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = src[x, y]
            if a > 8 and not (r >= white_threshold and g >= white_threshold and b >= white_threshold):
                dst[x, y] = a
    return mask


def main() -> None:
    parser = argparse.ArgumentParser(description="Trim an uploaded logo for PPT insertion without adding any border.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--padding", type=int, default=8)
    args = parser.parse_args()

    im = Image.open(args.input).convert("RGBA")
    mask = foreground_mask(im)
    bbox = mask.getbbox() or im.getbbox()
    if bbox is None:
        raise SystemExit("Input logo appears empty")

    left, top, right, bottom = bbox
    left = max(0, left - args.padding)
    top = max(0, top - args.padding)
    right = min(im.width, right + args.padding)
    bottom = min(im.height, bottom + args.padding)
    trimmed = im.crop((left, top, right, bottom))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    trimmed.save(args.output)
    print(args.output)


if __name__ == "__main__":
    main()
