#!/usr/bin/env python3
"""
运营数据复盘报告生成器
读取 report-template.html 模板，将分析数据填充后输出最终 HTML 报告。
"""

import json
import sys
import os
from datetime import datetime
from html import escape


TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "report-template.html")


def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def e(text):
    return escape(str(text)) if text else ""


def _tag_cls(val, high="高"):
    return "tag-high" if val == high else "tag-mid" if val == "中" else "tag-low"


def _health_cls(val):
    if isinstance(val, str):
        return {"green": "green", "amber": "amber", "red": "red"}.get(val, "")
    return ""


def _section(num, title, desc, body):
    return (
        f'<div class="s"><div class="s-head"><div class="s-num">{num}</div>'
        f'<h2>{title}</h2><div class="s-desc">{desc}</div></div>{body}</div>'
    )


def _styled_list(items):
    return '<ul class="styled-list">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def _data_table(cols, rows):
    if cols and isinstance(cols[0], (list, tuple)):
        pairs = cols
    else:
        pairs = [(h, h) for h in cols]
    th = "".join(f"<th>{label}</th>" for label, _ in pairs)
    tr = ""
    for row in rows:
        tr += "<tr>" + "".join(f"<td>{e(row.get(key, ''))}</td>" for _, key in pairs) + "</tr>"
    return f'<table class="data-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def _metric_row(metrics):
    parts = []
    for m in metrics:
        trend_html = ""
        if m.get("trend"):
            th_cls = _health_cls(m.get("trend_health",""))
            trend_html = f' <span style="color:var(--{th_cls})">{e(m.get("trend",""))}</span>'
        parts.append(
            f'<div class="metric"><div class="m-val {_health_cls(m.get("health",""))}">'
            f'{e(m.get("value",""))}</div>'
            f'<div class="m-label">{e(m.get("label",""))}{trend_html}</div></div>'
        )
    return '<div class="metric-row">' + "\n".join(parts) + '</div>'


def _top_actions(actions):
    return "\n".join(
        f'<div class="act-card"><span class="p-badge {a.get("priority","p2").lower()}">'
        f'{e(a.get("priority",""))}</span><div class="act-body">'
        f'<strong>{e(a.get("action",""))}</strong> — {e(a.get("effect",""))}</div></div>'
        for a in actions
    )


def _verdict(label, text, actions):
    return (
        f'<div class="verdict"><div class="label">{label}</div>'
        f'<div class="v-text">{text}</div>'
        f'<div class="top-actions">{_top_actions(actions)}</div></div>'
    )


def _decision_box(conclusion):
    return (
        f'<div class="decision-box"><div class="label">Decision · 结论与行动</div>'
        f'<div class="one-liner">{e(conclusion)}</div></div>'
    )


def _action_rows(actions):
    return "\n".join(
        f'<div class="act-row"><span class="p-badge {a.get("priority","p2").lower()}">'
        f'{e(a.get("priority",""))}</span><div class="act-content">'
        f'<strong>{e(a.get("action",""))}</strong>'
        f'<div class="act-meta">预期效果：{e(a.get("expected_effect",""))} | '
        f'{e(a.get("owner",""))} {e(a.get("deadline","") or a.get("timeline",""))}</div>'
        f'</div></div>'
        for a in actions
    )


def _not_do(items):
    return "\n".join(
        f'<div class="notdo-item"><div class="nd-icon">✕</div>'
        f'<div class="nd-body"><strong>{e(i.get("item",""))}</strong>'
        f'<div class="nd-reason">{e(i.get("reason",""))}</div></div></div>'
        for i in items
    )


def _build_report(d):
    today = datetime.now().strftime("%Y-%m-%d")
    product = d.get("product", "未命名产品")
    parts = []

    # ── Cover ──
    parts.append(
        f'<header class="cover"><div class="tag">OPS DATA REVIEW REPORT</div>'
        f'<h1>{e(d.get("cover_title", f"运营数据复盘：{product}"))}</h1>'
        f'<div class="lead">{e(d.get("cover_lead",""))}</div>'
        f'<div class="meta-row"><span>{today}</span><span>运营数据复盘 Skill</span>'
        f'<span>复盘周期：{e(d.get("period",""))}</span></div></header>'
    )

    # ── M0 执行摘要 ──
    es = d.get("executive_summary", {})
    findings = "\n".join(
        f'<div class="ins-item"><div class="finding">{e(f.get("finding",""))}</div>'
        f'<div class="meta-line">数据依据：{e(f.get("data",""))}</div></div>'
        for f in es.get("top_findings", [])
    )
    parts.append(_verdict(
        "Executive Summary · 执行摘要",
        f'{e(es.get("overall_evaluation",""))}<br><br>{findings}',
        es.get("top_actions", [])
    ))

    # ── M1 核心指标仪表盘 ──
    dash = d.get("dashboard", {})
    all_metrics = []
    for cat in dash.get("metrics", []):
        for m in cat.get("items", []):
            m_copy = dict(m)
            m_copy.setdefault("label", f"{cat.get('category','')} · {m.get('label','')}")
            all_metrics.append(m_copy)
    parts.append(_section("Module 01", "核心指标仪表盘",
        "关键数据卡片一览，红黄绿灯标识健康度",
        _metric_row(all_metrics)
    ))

    # ── M2 用户增长分析 ──
    ug = d.get("user_growth", {})
    growth_rows = "\n".join(
        f'<div class="metric"><div class="m-val blue">{e(p.get("value",""))}</div>'
        f'<div class="m-label">{e(p.get("period",""))}</div></div>'
        for p in ug.get("new_users_trend", [])
    )
    parts.append(_section("Module 02", "用户增长分析", "回答：用户从哪来？增长趋势如何？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">新增用户趋势</h3>'
        f'<div class="metric-row">{growth_rows}</div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">渠道来源分析</h3>'
        f'{_data_table([("渠道","channel"),("占比","proportion"),("质量","quality"),("说明","note")], ug.get("channel_analysis",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">激活漏斗</h3>'
        f'{_data_table([("步骤","step"),("转化率","conversion_rate"),("流失率","drop_rate")], ug.get("activation_funnel",[]))}'
    ))

    # ── M3 用户活跃分析 ──
    ua = d.get("user_activity", {})
    dm = ua.get("dau_mau", {})
    parts.append(_section("Module 03", "用户活跃分析", "回答：用户来了之后在做什么？活跃度如何？",
        f'<div class="hl-box hl-blue"><p>'
        f'<strong>DAU</strong>：{e(dm.get("dau",""))} | '
        f'<strong>MAU</strong>：{e(dm.get("mau",""))} | '
        f'<strong>DAU/MAU</strong>：{e(dm.get("ratio",""))} | '
        f'{e(dm.get("trend",""))}</p></div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">用户分层</h3>'
        f'{_data_table([("分群","segment"),("用户数","users"),("占比","proportion"),("趋势","trend")], ua.get("user_segments",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">功能使用热度</h3>'
        f'{_data_table([("功能","feature"),("使用率","usage_rate"),("使用频次","frequency"),("满意度","satisfaction")], ua.get("feature_heatmap",[]))}'
    ))

    # ── M4 转化漏斗分析 ──
    cf = d.get("conversion_funnel", {})
    bn = cf.get("bottleneck", {})
    parts.append(_section("Module 04", "转化漏斗分析", "回答：用户在哪个环节流失最多？",
        f'{_data_table([("步骤","step"),("用户数","users"),("累计转化率","cumulative_rate"),("该步流失率","drop_rate")], cf.get("funnel",[]))}'
        f'<div class="hl-box" style="background:var(--red-bg);border-left-color:var(--red);margin-top:20px">'
        f'<p><strong>⚠ 瓶颈定位</strong>：{e(bn.get("step",""))}（流失率 {e(bn.get("drop_rate",""))}）</p>'
        f'<p>可能原因：{e(" / ".join(bn.get("possible_reasons",[])))}</p></div>'
    ))

    # ── M5 留存分析 ──
    ret = d.get("retention", {})
    ret_rows = "\n".join(
        f'<div class="metric"><div class="m-val {_health_cls(r.get("status",""))}">'
        f'{e(r.get("value",""))}</div>'
        f'<div class="m-label">{e(r.get("type",""))}</div>'
        f'<div style="font-size:11px;color:var(--ink-muted)">基准：{e(r.get("benchmark",""))}</div></div>'
        for r in ret.get("data", [])
    )
    warnings = "\n".join(
        f'<div class="ins-item"><div class="finding" style="color:var(--red)">⚠ {e(w.get("signal",""))}</div>'
        f'<div class="meta-line">{e(w.get("detail",""))}</div></div>'
        for w in ret.get("warnings", [])
    )
    warnings_section = (f'<h3 style="margin:16px 0 12px;font-size:15px;font-weight:700;color:var(--red)">预警信号</h3>{warnings}' if warnings else "")
    parts.append(_section("Module 05", "留存分析", "回答：用户留下来了吗？留存趋势如何？",
        f'<div class="metric-row">{ret_rows}</div>'
        f'<h3 style="margin:16px 0 12px;font-size:15px;font-weight:700">健康度评估</h3>'
        f'<p>{e(ret.get("health_assessment",""))}</p>'
        f'{warnings_section}'
    ))

    # ── M6 商业化分析 ──
    mon = d.get("monetization", {})
    rev_rows = "\n".join(
        f'<div class="metric"><div class="m-val green">{e(r.get("revenue",""))}</div>'
        f'<div class="m-label">{e(r.get("period",""))}</div></div>'
        for r in mon.get("revenue_trend", [])
    )
    ltv = mon.get("ltv_estimate", {})
    parts.append(_section("Module 06", "商业化分析", "回答：赚钱了吗？赚钱效率如何？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">收入趋势</h3>'
        f'<div class="metric-row">{rev_rows}</div>'
        f'<div class="hl-box hl-green"><p>'
        f'<strong>ARPU</strong>：{e(mon.get("arpu",{}).get("current",""))}（{e(mon.get("arpu",{}).get("trend",""))}） | '
        f'<strong>ARPPU</strong>：{e(mon.get("arppu",{}).get("current",""))}（{e(mon.get("arppu",{}).get("trend",""))}）</p></div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">付费转化漏斗</h3>'
        f'{_data_table([("步骤","step"),("转化率","conversion_rate")], mon.get("pay_conversion_funnel",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">单位经济模型</h3>'
        f'<div class="roi-grid">'
        f'<div class="roi-card"><div class="roi-val">{e(ltv.get("value",""))}</div><div class="roi-label">LTV 估算</div></div>'
        f'<div class="roi-card"><div class="roi-val">{e(ltv.get("cac",""))}</div><div class="roi-label">CAC</div></div>'
        f'<div class="roi-card"><div class="roi-val">{e(ltv.get("ratio",""))}</div><div class="roi-label">LTV/CAC</div></div>'
        f'</div>'
    ))

    # ── M7 用户反馈分析 ──
    uf = d.get("user_feedback", {})
    themes = "\n".join(
        f'<div class="ins-item"><div class="finding">{e(t.get("theme",""))}'
        f' <span class="{_tag_cls(t.get("frequency","高"))}">{e(t.get("frequency",""))}</span>'
        f' <span class="{_tag_cls(t.get("sentiment","负面"))}">{e(t.get("sentiment",""))}</span></div>'
        f'<div class="meta-line">典型反馈：{e(t.get("sample",""))}</div></div>'
        for t in uf.get("top_themes", [])
    )
    pains = "\n".join(
        f'<div class="ins-item"><div class="finding" style="color:var(--red)">🔥 {e(p.get("cluster",""))}'
        f'（提及 {e(p.get("count",""))} 次）</div>'
        f'<div class="meta-line">严重度：<span class="{_tag_cls(p.get("severity",""))}">{e(p.get("severity",""))}</span>'
        f' | 影响范围：{e(p.get("affected_users",""))}</div></div>'
        for p in uf.get("pain_clusters", [])
    )
    nps = uf.get("nps", {})
    parts.append(_section("Module 07", "用户反馈分析", "回答：用户满意吗？高频痛点是什么？",
        f'<div class="hl-box hl-blue"><p>'
        f'<strong>当前 NPS</strong>：{e(nps.get("current",""))}（{e(nps.get("trend",""))}）</p></div>'
        f'<h3 style="margin:16px 0 12px;font-size:15px;font-weight:700">高频反馈主题</h3>'
        f'{themes}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700;color:var(--red)">痛点聚类</h3>'
        f'{pains}'
    ))

    # ── M8 跨维度交叉分析 ──
    ca = d.get("cross_analysis", {})
    parts.append(_section("Module 08", "跨维度交叉分析", "回答：不同维度的数据交叉后发现了什么？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">用户分群 × 行为特征</h3>'
        f'{_data_table([("分群","segment"),("行为特征","behavior"),("留存","retention"),("价值贡献","value")], ca.get("segment_behavior",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">渠道 × 质量 × 成本</h3>'
        f'{_data_table([("渠道","channel"),("质量评分","quality_score"),("CAC","cac"),("LTV","ltv"),("ROI","roi")], ca.get("channel_quality_cost",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">功能 × 留存影响</h3>'
        f'{_data_table([("功能","feature"),("使用率","usage_rate"),("对留存影响","retention_impact"),("满意度","satisfaction")], ca.get("feature_retention_impact",[]))}'
    ))

    # ── M9 问题诊断 ──
    pd = d.get("problem_diagnosis", {})
    probs = ""
    for p in pd.get("problems", []):
        urg_cls = p.get("urgency", "P2").lower()
        probs += (
            f'<div style="padding:18px;border-radius:var(--radius);border:1px solid var(--border);'
            f'background:var(--surface-raised);margin-bottom:12px">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">'
            f'<span class="p-badge {urg_cls}">{e(p.get("urgency",""))}</span>'
            f'<strong style="font-size:15px">{e(p.get("problem",""))}</strong></div>'
            f'<div class="ins-item" style="margin-bottom:6px"><div class="finding">数据证据</div>'
            f'<div class="meta-line">{e(p.get("data_evidence",""))}</div></div>'
            f'<div class="ins-item" style="margin-bottom:6px"><div class="finding">根因分析（5-Why）</div>'
            f'<div class="meta-line">{e(p.get("root_cause",""))}</div></div>'
            f'<div style="font-size:13px;color:var(--ink-muted)">'
            f'影响范围：{e(p.get("impact_scope",""))} | 建议方向：{e(p.get("suggested_direction",""))}</div>'
            f'</div>'
        )
    parts.append(_section("Module 09", "问题诊断与根因分析", "回答：当前最核心的问题是什么？为什么？",
        probs
    ))

    # ── M10 行动方案 ──
    ap = d.get("action_plan", {})
    parts.append(_section("Module 10", "行动方案", "回答：接下来做什么？不做什么？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700;color:var(--red)">短期优化（1-2周）</h3>'
        f'<div class="act-list">{_action_rows(ap.get("short_term",[]))}</div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700;color:var(--amber)">中期策略（1-3月）</h3>'
        f'<div class="act-list">{_action_rows(ap.get("mid_term",[]))}</div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700;color:var(--blue)">长期规划（3-6月）</h3>'
        f'<div class="act-list">{_action_rows(ap.get("long_term",[]))}</div>'
        f'<h3 style="margin:24px 0 12px;font-size:15px;font-weight:700;color:var(--red)">NOT TO DO</h3>'
        f'{_not_do(ap.get("not_to_do",[]))}'
    ))

    # ── M11 监测计划 ──
    mp = d.get("monitoring_plan", [])
    parts.append(_section("Module 11", "监测计划", "回答：怎么持续跟踪？看什么信号？",
        _data_table([("关键信号","signal"),("观察指标","metric"),("数据来源","source"),("检查频率","frequency")], mp)
    ))

    # ── Footer ──
    parts.append(
        f'<div class="report-footer"><p>由「运营数据复盘 Skill」生成 · {today}</p>'
        f'<p style="margin-top:4px;">本报告基于运营数据分析生成，关键结论建议结合业务上下文进一步验证</p></div>'
    )

    return "\n".join(parts), f"运营数据复盘 - {product}"


def generate_report(data_json_path, output_path=None):
    with open(data_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    template = load_template()
    content, title = _build_report(data)
    html = template.replace("{{TITLE}}", title).replace("{{CONTENT}}", content)

    if not output_path:
        today = datetime.now().strftime("%Y-%m-%d")
        product = data.get("product", "未命名产品")
        output_path = f"运营数据复盘报告_{product}_{today}.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"报告已生成：{output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python generate-report.py <data.json> [output.html]")
        print("\ndata.json 为运营数据复盘的 JSON 文件")
        sys.exit(1)

    data_path = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    generate_report(data_path, output)
