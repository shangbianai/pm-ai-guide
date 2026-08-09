#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def find_chrome():
    candidates = [
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    return next((x for x in candidates if x and Path(x).exists()), None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=1300)
    args = parser.parse_args()
    chrome = find_chrome()
    if not chrome:
        print("未找到 Chrome/Chromium；HTML 已可直接展示，跳过 PNG。", file=sys.stderr)
        return 3
    source = Path(args.input).resolve()
    target = Path(args.output).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([
        chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
        f"--window-size={args.width},{args.height}",
        f"--screenshot={target}", source.as_uri()
    ])
    if result.returncode or not target.exists():
        return result.returncode or 1
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
