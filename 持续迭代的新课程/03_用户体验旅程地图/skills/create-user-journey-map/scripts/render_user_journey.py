#!/usr/bin/env python3
import argparse
import html
import json
from pathlib import Path


def esc(value):
    return html.escape(str(value or ""))


def clamp(value, low, high):
    return max(low, min(high, int(value)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    stages = data.get("stages", [])
    if not 5 <= len(stages) <= 7:
        raise ValueError("stages 必须包含 5—7 个阶段")

    normalized = []
    for stage in stages:
        item = dict(stage)
        item["emotion"] = clamp(item.get("emotion", 0), -2, 2)
        item["impact"] = clamp(item.get("impact", 1), 1, 5)
        item["frequency"] = clamp(item.get("frequency", 1), 1, 5)
        item["current_solution"] = clamp(item.get("current_solution", 1), 1, 5)
        item["priority"] = item["impact"] * item["frequency"] * (6 - item["current_solution"])
        normalized.append(item)

    cards = []
    for index, stage in enumerate(normalized, 1):
        emotion_class = "bad" if stage["emotion"] < 0 else "good" if stage["emotion"] > 0 else "mid"
        detail = json.dumps(stage, ensure_ascii=False)
        cards.append(f"""
        <article class="stage" data-detail='{esc(detail)}'>
          <span class="number">{index}</span><h2>{esc(stage.get("name"))}</h2>
          <p class="goal">{esc(stage.get("goal"))}</p>
          <div class="emotion"><b class="{emotion_class}">{stage["emotion"]}</b><span>情绪评分</span></div>
          <h3>主要痛点</h3><p>{esc(stage.get("pain"))}</p>
          <span class="tag">{esc(stage.get("evidence_status"))}</span>
          <div class="rank"><strong>机会优先级 {stage["priority"]}</strong><i style="width:{stage["priority"]}%"></i></div>
        </article>""")

    width = 1100
    step = width / max(1, len(normalized) - 1)
    points = []
    labels = []
    for i, stage in enumerate(normalized):
        x = 80 + i * step
        y = 225 - (stage["emotion"] + 2) * 48
        points.append(f"{x:.1f},{y:.1f}")
        labels.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7"/><text x="{x:.1f}" y="252">{esc(stage.get("name"))}</text>')

    payload = json.dumps(normalized, ensure_ascii=False).replace("</", "<\\/")
    output = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(data.get("title"))}</title>
<style>
:root{{--bg:#050914;--panel:#0d1829;--ink:#f6f9ff;--muted:#97abc3;--cyan:#23d3ee;--yellow:#ffd84f;--green:#63e6a6;--red:#ff6c79;--line:rgba(255,255,255,.14)}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}}main{{width:min(1440px,94vw);margin:auto;padding:42px 0}}h1{{font-size:48px;margin:8px 0}}.meta{{color:var(--muted);line-height:1.7}}.journey{{display:grid;grid-template-columns:repeat({len(normalized)},minmax(180px,1fr));gap:9px;overflow:auto;margin-top:26px}}.stage{{min-height:390px;padding:16px 16px 76px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(150deg,#101e33,#08111f);position:relative;cursor:pointer;transition:.2s}}.stage:hover{{transform:translateY(-7px);border-color:var(--cyan)}}.number{{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--cyan);color:#041018;font-weight:900}}.stage h2{{font-size:20px}}.goal,.stage p{{color:var(--muted);font-size:13px;line-height:1.5}}.emotion{{padding:9px;background:#050b15;border-radius:10px;margin:14px 0;display:flex;gap:8px;align-items:center}}.emotion b{{font-size:28px}}.bad{{color:var(--red)}}.good{{color:var(--green)}}.mid{{color:var(--yellow)}}.stage h3{{font-size:12px;color:var(--yellow)}}.tag{{font-size:10px;padding:4px 7px;border:1px solid var(--line);border-radius:999px}}.rank{{position:absolute;left:16px;right:16px;bottom:18px}}.rank i{{display:block;height:7px;background:linear-gradient(90deg,var(--cyan),var(--green));border-radius:9px;margin-top:7px}}.curve{{margin-top:20px;padding:20px;border:1px solid var(--line);border-radius:18px;background:#08111f}}svg{{width:100%;height:270px}}polyline{{fill:none;stroke:var(--cyan);stroke-width:4}}circle{{fill:var(--bg);stroke:var(--yellow);stroke-width:4}}text{{fill:var(--muted);font-size:12px;text-anchor:middle}}.overlay{{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(0,4,12,.8);padding:24px}}.overlay.open{{display:flex}}.dialog{{width:min(900px,96vw);background:#0b1729;border:1px solid #31526e;border-radius:20px;padding:24px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.grid div{{border:1px solid var(--line);padding:12px;border-radius:10px}}.grid b{{display:block;color:var(--cyan);font-size:12px;margin-bottom:5px}}button{{float:right;background:#08111f;border:1px solid var(--line);color:#fff;border-radius:50%;width:34px;height:34px}}@media(max-width:800px){{.journey{{grid-template-columns:repeat({len(normalized)},76vw)}}.grid{{grid-template-columns:1fr}}}}
</style></head><body><main><div style="color:var(--cyan);font-weight:800">USER JOURNEY MAP</div><h1>{esc(data.get("title"))}</h1><p class="meta">目标用户：{esc(data.get("persona"))}<br>核心任务：{esc(data.get("core_task"))}<br>{esc(data.get("evidence_note"))}</p><section class="journey">{''.join(cards)}</section><section class="curve"><h2>用户情绪曲线</h2><svg viewBox="0 0 1260 270"><polyline points="{' '.join(points)}"/>{''.join(labels)}</svg></section></main><div class="overlay" id="overlay"><div class="dialog"><button id="close">×</button><h2 id="title"></h2><div class="grid" id="grid"></div></div></div><script>const stages={payload};const overlay=document.getElementById("overlay"),grid=document.getElementById("grid");document.querySelectorAll(".stage").forEach((el,i)=>el.onclick=()=>{{const d=stages[i];document.getElementById("title").textContent=d.name;grid.innerHTML=[["用户目标",d.goal],["关键动作",d.actions],["主要触点",d.touchpoints],["用户想法",d.thoughts],["主要痛点",d.pain],["证据状态",d.evidence_status+"｜"+d.evidence],["产品机会",d.opportunity],["机会优先级",d.priority]].map(x=>`<div><b>${{x[0]}}</b>${{x[1]}}</div>`).join("");overlay.classList.add("open")}});document.getElementById("close").onclick=()=>overlay.classList.remove("open");overlay.onclick=e=>{{if(e.target===overlay)overlay.classList.remove("open")}};</script></body></html>"""
    target = Path(args.output).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output, encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
