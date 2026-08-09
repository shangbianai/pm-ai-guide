#!/usr/bin/env python3
import html
import json
import sys
from pathlib import Path


def esc(value):
    return html.escape(str(value or ""))


def refs(items):
    return " ".join(f'<button class="ref" data-ref="{esc(x)}">{esc(x)}</button>' for x in items)


def main():
    if len(sys.argv) != 3:
        print("Usage: render_research_report.py input.json output.html", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    meta = data["meta"]
    evidence = {x["id"]: x for x in data["evidence"]}
    evidence_json = json.dumps(evidence, ensure_ascii=False).replace("</", "<\\/")
    facts = sum(x.get("status") == "已验证事实" for x in data["findings"])
    inferences = sum(x.get("status") == "合理推断" for x in data["findings"])
    hypotheses = sum(x.get("status") == "待验证假设" for x in data["findings"])

    persona = "".join(f'<article><small>{esc(x["dimension"])}</small><p>{esc(x["statement"])}</p>{refs(x["evidence_ids"])}</article>' for x in data["persona"]["claims"])
    findings = "".join(f'<article class="finding"><span class="status {"fact" if x["status"]=="已验证事实" else "infer" if x["status"]=="合理推断" else "hyp"}">{esc(x["status"])}</span><h3>{esc(x["statement"])}</h3><p>{esc(x["why_it_matters"])}</p>{refs(x.get("evidence_ids", []))}</article>' for x in data["findings"])
    journey = "".join(f'<article class="stage"><div class="emotion e{x["emotion"]+2}">{x["emotion"]:+d}</div><small>{esc(x["status"])}</small><h3>{esc(x["stage"])}</h3><b>{esc(x["goal"])}</b><p>{esc(x["actions"])}</p><div class="pain">断点：{esc(x["pain"])}</div><div class="opp">机会：{esc(x["opportunity"])}</div>{refs(x.get("evidence_ids", []))}</article>' for x in data["journey"])
    opportunities = "".join(f'<tr><td><strong>0{esc(x["rank"])}</strong></td><td><b>{esc(x["outcome"])}</b><small>{esc(x["why_now"])}</small></td><td>{x["impact"]}</td><td>{x["frequency"]}</td><td>{x["risk"]}</td><td>{esc(x["next_test"])}</td><td>{refs(x["evidence_ids"])}</td></tr>' for x in data["opportunities"])
    contradictions = "".join(f'<li><b>{esc(x["description"])}</b><span>{esc(x["handling"])}</span>{refs(x["evidence_ids"])}</li>' for x in data["contradictions"])
    questions = "".join(f'<li>{esc(x)}</li>' for x in data["next_questions"])
    limitations = "".join(f'<li>{esc(x)}</li>' for x in meta["limitations"])

    doc = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(meta["title"])}</title><style>
:root{{--ink:#171815;--muted:#71776d;--paper:#f4f5ef;--card:#fff;--lime:#dfff65;--line:#dfe3d8;--red:#e15b50;--amber:#d99b20;--blue:#4f78ff}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,"PingFang SC",sans-serif}}main{{max-width:1380px;margin:auto;padding:34px}}header{{background:var(--ink);color:white;border-radius:28px;padding:32px;display:grid;grid-template-columns:1fr auto;gap:20px}}header small{{color:#aab0a5;letter-spacing:.12em}}h1{{font-size:40px;margin:10px 0}}header p{{color:#c4c9bf}}.stats{{display:grid;grid-template-columns:repeat(3,100px);gap:10px}}.stat{{background:#292c27;border-radius:18px;padding:16px}}.stat b{{display:block;font-size:30px;color:var(--lime)}}section{{margin-top:28px}}.section-head{{display:flex;justify-content:space-between;align-items:end;margin-bottom:12px}}h2{{font-size:24px;margin:0}}.section-head p{{margin:0;color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}article{{background:white;border:1px solid var(--line);border-radius:18px;padding:18px}}article small{{color:var(--muted)}}article p{{line-height:1.55}}.status{{display:inline-block;border-radius:99px;padding:5px 9px;font-size:11px}}.fact{{background:#e9f8df;color:#35731f}}.infer{{background:#eaf0ff;color:#3559b5}}.hyp{{background:#fff2d5;color:#865c00}}.ref{{border:0;background:#eef0e9;border-radius:7px;padding:4px 7px;margin:2px;color:#4e5549;cursor:pointer}}.ref:hover{{background:var(--lime)}}.journey{{display:grid;grid-template-columns:repeat({len(data["journey"])},minmax(190px,1fr));gap:10px;overflow:auto;padding-bottom:8px}}.stage{{min-width:190px}}.emotion{{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;font-weight:800;margin-bottom:16px}}.e0{{background:#ffe5e1;color:#9a3027}}.e1{{background:#fff1d7;color:#805a06}}.e2{{background:#edf0e9}}.e3,.e4{{background:#e2f6d6;color:#387423}}.pain,.opp{{padding:10px;border-radius:10px;font-size:13px;margin:8px 0}}.pain{{background:#fff0ed}}.opp{{background:#eff7da}}table{{width:100%;border-collapse:separate;border-spacing:0 8px}}td,th{{padding:14px;text-align:left}}th{{color:var(--muted);font-size:12px}}td{{background:white;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}td:first-child{{border-left:1px solid var(--line);border-radius:14px 0 0 14px}}td:last-child{{border-right:1px solid var(--line);border-radius:0 14px 14px 0}}td small{{display:block;color:var(--muted);margin-top:5px}}.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}ul.panel{{margin:0;background:white;border:1px solid var(--line);border-radius:18px;padding:20px 20px 20px 38px}}ul.panel li{{margin:10px 0}}ul.panel span{{display:block;color:var(--muted);margin:4px 0}}.modal{{position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;place-items:center;padding:20px}}.modal.on{{display:grid}}.modal article{{max-width:620px;width:100%;box-shadow:0 30px 100px #0005}}.close{{float:right;border:0;background:#eee;border-radius:50%;width:32px;height:32px;cursor:pointer}}@media(max-width:800px){{main{{padding:16px}}header{{grid-template-columns:1fr}}h1{{font-size:30px}}.grid,.twocol{{grid-template-columns:1fr}}.stats{{grid-template-columns:repeat(3,1fr)}}}}
</style></head><body><main><header><div><small>EVIDENCE-BACKED RESEARCH</small><h1>{esc(meta["title"])}</h1><p>{esc(meta["subject"])} · {esc(meta["scenario"])} · 核心任务：{esc(meta["core_task"])}</p></div><div class="stats"><div class="stat"><b>{facts}</b><span>事实</span></div><div class="stat"><b>{inferences}</b><span>推断</span></div><div class="stat"><b>{hypotheses}</b><span>假设</span></div></div></header>
<section><div class="section-head"><h2>证据约束的客户画像</h2><p>{esc(data["persona"]["label"])}</p></div><div class="grid">{persona}</div></section>
<section><div class="section-head"><h2>关键发现</h2><p>点击证据编号查看来源</p></div><div class="grid">{findings}</div></section>
<section><div class="section-head"><h2>当前用户旅程</h2><p>情绪 -2 至 +2</p></div><div class="journey">{journey}</div></section>
<section><div class="section-head"><h2>机会排序</h2><p>先描述用户结果，再讨论功能</p></div><table><thead><tr><th>排名</th><th>机会</th><th>影响</th><th>频率</th><th>风险</th><th>下一步验证</th><th>证据</th></tr></thead><tbody>{opportunities}</tbody></table></section>
<section class="twocol"><div><div class="section-head"><h2>矛盾与数据问题</h2></div><ul class="panel">{contradictions or '<li>未发现明显矛盾</li>'}</ul></div><div><div class="section-head"><h2>下一轮研究问题</h2></div><ol class="panel">{questions}</ol></div></section>
<section><div class="section-head"><h2>研究限制</h2></div><ul class="panel">{limitations}</ul></section></main>
<div id="modal" class="modal"><article><button class="close">×</button><small id="kind"></small><h3 id="eid"></h3><p id="content"></p><p id="locator"></p></article></div><script>const evidence={evidence_json};const modal=document.querySelector('#modal');document.querySelectorAll('.ref').forEach(b=>b.onclick=()=>{{const e=evidence[b.dataset.ref];if(!e)return;document.querySelector('#kind').textContent=e.kind+' · '+e.source_id;document.querySelector('#eid').textContent=e.id;document.querySelector('#content').textContent=e.content;document.querySelector('#locator').textContent='定位：'+e.locator;modal.classList.add('on')}});document.querySelector('.close').onclick=()=>modal.classList.remove('on');modal.onclick=e=>{{if(e.target===modal)modal.classList.remove('on')}}</script></body></html>'''
    Path(sys.argv[2]).write_text(doc, encoding="utf-8")
    print(f"WROTE {sys.argv[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

