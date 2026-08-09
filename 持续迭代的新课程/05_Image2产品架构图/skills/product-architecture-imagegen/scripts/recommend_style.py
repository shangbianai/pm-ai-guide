#!/usr/bin/env python3
"""Recommend one of the stable numbered architecture styles."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references" / "style-manifest.json"


def load_styles() -> list[dict]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def score_style(style: dict, text: str) -> int:
    lowered = text.lower()
    score = 0
    for keyword in style.get("keywords", []):
        key = keyword.lower()
        if key in lowered:
            score += 3 if len(key) >= 4 else 2
    for phrase in (style.get("name", ""), style.get("recommended_for", "")):
        for token in phrase.replace("、", " ").replace("，", " ").split():
            if len(token) >= 2 and token.lower() in lowered:
                score += 1
    return score


def eligible_random(styles: list[dict], text: str) -> list[dict]:
    lowered = text.lower()
    excluded: set[str] = set()
    if not any(key in lowered for key in ["多角色", "多端", "协同", "多边"]):
        excluded.add("15")
    if not any(key in lowered for key in ["供需", "撮合", "双边", "交易平台"]):
        excluded.add("16")
    if not any(key in lowered for key in ["销售", "营销", "线索", "商机", "转化"]):
        excluded.add("13")
    if not any(key in lowered for key in ["agent", "智能体", "工具调用"]):
        excluded.add("14")
    return [style for style in styles if style["id"] not in excluded] or styles


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["auto", "random"], default="auto")
    parser.add_argument("--text", default="")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    styles = load_styles()
    if args.mode == "random":
        rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
        chosen = rng.choice(eligible_random(styles, args.text))
        result = {"mode": "random", "selected": chosen, "reason": "eligible random selection"}
    else:
        ranked = sorted(
            ((score_style(style, args.text), style) for style in styles),
            key=lambda item: (-item[0], item[1]["id"]),
        )
        if not ranked or ranked[0][0] == 0:
            chosen = next(style for style in styles if style["id"] == "06")
            top = [{"score": 0, "id": chosen["id"], "name": chosen["name"]}]
            reason = "no keyword match; used stable default"
        else:
            chosen = ranked[0][1]
            top = [
                {"score": score, "id": style["id"], "name": style["name"]}
                for score, style in ranked[:3]
            ]
            reason = "highest keyword and scenario score"
        result = {"mode": "auto", "selected": chosen, "top_candidates": top, "reason": reason}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
