#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


def markdown_tree(text):
    root = {"text": "思维导图", "children": []}
    stack = [(0, root)]
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        bullet = re.match(r"^[-*+]\s+(.+)$", line)
        if heading:
            level, label = len(heading.group(1)), heading.group(2).strip()
        elif bullet:
            indent = len(raw) - len(raw.lstrip())
            level, label = 7 + indent // 2, bullet.group(1).strip()
        else:
            continue
        node = {"text": label, "children": []}
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent = stack[-1][1] if stack else root
        parent["children"].append(node)
        stack.append((level, node))
    if len(root["children"]) == 1:
        return root["children"][0]
    return root


def main():
    parser = argparse.ArgumentParser(description="Render a product mind map with Markmap")
    parser.add_argument("input")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--title", default="产品思维导图")
    parser.add_argument("--no-screenshot", action="store_true")
    args = parser.parse_args()

    source = Path(args.input).expanduser().resolve()
    if not source.exists() or source.suffix.lower() != ".md":
        raise SystemExit("input must be an existing Markdown file")
    output = Path(args.output_dir).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    markdown = source.read_text(encoding="utf-8")
    if not re.search(r"^#\s+.+", markdown, flags=re.M):
        markdown = f"# {args.title}\n\n" + markdown

    md_path = output / "mind-map.md"
    md_path.write_text(markdown, encoding="utf-8")
    (output / "mind-map.json").write_text(
        json.dumps(markdown_tree(markdown), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    html_path = output / "mind-map.html"
    subprocess.run([
        "npx", "-y", "markmap-cli@0.18.12", str(md_path),
        "--offline", "--no-open", "-o", str(html_path),
    ], check=True)

    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if not args.no_screenshot and chrome.exists():
        subprocess.run([
            str(chrome), "--headless", "--disable-gpu", "--hide-scrollbars",
            "--window-size=1600,1000",
            f"--screenshot={output / 'mind-map.png'}",
            html_path.as_uri(),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(html_path)


if __name__ == "__main__":
    main()
