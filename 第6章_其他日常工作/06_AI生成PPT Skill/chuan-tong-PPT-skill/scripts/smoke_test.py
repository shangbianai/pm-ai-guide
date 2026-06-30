#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "source-template.pptx"
DEFAULT_LOGO = ROOT / "assets" / "shangbianzhiyuan-logo-horizontal.png"
LOGO_PREP = ROOT / "scripts" / "prepare_logo_for_ppt.py"
SKILL = ROOT / "SKILL.md"
REFERENCES = [
    ROOT / "references" / "layout-patterns.md",
    ROOT / "references" / "style-guide.md",
    ROOT / "references" / "authoring-rules.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    require(TEMPLATE.exists(), "template asset is missing")
    require(TEMPLATE.stat().st_size > 1_000_000, "template asset looks too small")
    require(DEFAULT_LOGO.exists(), "default horizontal logo asset is missing")
    require(DEFAULT_LOGO.stat().st_size > 1_000, "default horizontal logo looks too small")
    require(LOGO_PREP.exists(), "logo preparation script is missing")
    require(SKILL.exists(), "SKILL.md is missing")
    for path in REFERENCES:
        require(path.exists(), f"{path.name} is missing")

    skill_text = SKILL.read_text(encoding="utf-8")
    require("image 2" in skill_text, "SKILL.md does not require image 2")
    require("logo" in skill_text.lower(), "SKILL.md does not mention logo handling")
    require("template-following" in skill_text, "SKILL.md does not require template-following")
    require("source-brand" in skill_text, "SKILL.md does not require source-brand cleanup")

    authoring = (ROOT / "references" / "authoring-rules.md").read_text(encoding="utf-8")
    require("Never use image generation for the logo" in authoring, "logo safety rule missing")
    require("target frame size/aspect ratio" in authoring, "image frame matching rule missing")
    require("shangbianzhiyuan-logo-horizontal.png" in authoring, "default logo rule missing")
    require("Do not draw a border" in authoring, "logo no-border rule missing")

    layout = (ROOT / "references" / "layout-patterns.md").read_text(encoding="utf-8")
    require("Cover" in layout and "Ending" in layout, "layout families are incomplete")
    require("1131" in layout and "1018" in layout, "logo slot coordinates are missing")

    with ZipFile(TEMPLATE) as pptx:
        slides = [
            name for name in pptx.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        ]
        require(len(slides) == 38, f"expected 38 slides, found {len(slides)}")
        presentation = pptx.read("ppt/presentation.xml").decode("utf-8", errors="ignore")
        require("embedTrueTypeFonts" in presentation, "embedded font evidence missing")
        media = [name for name in pptx.namelist() if name.startswith("ppt/media/")]
        require(len(media) >= 10, "template media assets look incomplete")

    print("OK: shangbian-ppt-template skill smoke test passed")


if __name__ == "__main__":
    main()
