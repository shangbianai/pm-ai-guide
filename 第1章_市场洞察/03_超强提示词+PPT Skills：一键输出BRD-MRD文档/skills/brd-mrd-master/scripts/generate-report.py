#!/usr/bin/env python3
"""
BRD/MRD 报告生成器
读取 report-template.html 模板，将分析数据填充后输出最终 HTML 报告。
支持 BRD、MRD 两种文档类型，通过 JSON 中的 type 字段区分。
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


# ═══ 通用渲染 ═══

def _top_actions(actions):
    return "\n".join(
        f'<div class="act-card"><span class="p-badge {a.get("priority","p2").lower()}">'
        f'{e(a.get("priority",""))}</span><div class="act-body">'
        f'<strong>{e(a.get("action",""))}</strong> — {e(a.get("effect",""))}</div></div>'
        for a in actions
    )


def _decision_actions(actions):
    return "\n".join(
        f'<div class="act-row"><span class="p-badge {a.get("priority","p2").lower()}">'
        f'{e(a.get("priority",""))}</span><div class="act-content">'
        f'<strong>{e(a.get("action",""))}</strong>'
        f'<div class="act-meta">预期效果：{e(a.get("effect",""))} | '
        f'所需资源：{e(a.get("resource",""))} | 周期：{e(a.get("timeline",""))}</div>'
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


def _metric_row(metrics):
    return '<div class="metric-row">' + "\n".join(
        f'<div class="metric"><div class="m-val {m.get("color","")}">'
        f'{e(m.get("value",""))}</div><div class="m-label">'
        f'{e(m.get("label",""))}</div></div>'
        for m in metrics
    ) + '</div>'


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


def _persona_cards(personas):
    cards = ""
    for p in personas:
        cards += (
            f'<div class="persona-card"><div class="pc-name">{e(p.get("name",""))}</div>'
            f'<div class="pc-meta">{e(p.get("role",""))} · {e(p.get("age_range","") or p.get("demographics",""))}</div>'
        )
        for key, label in [("needs","核心需求"),("pain_points","痛点"),("behavior","行为特征")]:
            if p.get(key):
                cards += f'<div class="pc-detail"><strong>{label}</strong>：{e(p.get(key,""))}</div>'
        cards += '</div>'
    return f'<div class="persona-grid">{cards}</div>'


def _section(num, title, desc, body):
    return (
        f'<div class="s"><div class="s-head"><div class="s-num">{num}</div>'
        f'<h2>{title}</h2><div class="s-desc">{desc}</div></div>{body}</div>'
    )


def _styled_list(items):
    return '<ul class="styled-list">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def _insight_items(findings, key_find="finding", key_basis="basis"):
    return "\n".join(
        f'<div class="ins-item"><div class="finding">{e(f.get(key_find,""))}</div>'
        f'<div class="meta-line">依据：{e(f.get(key_basis,""))}</div></div>'
        for f in findings
    )


def _verdict(label, text, actions):
    return (
        f'<div class="verdict"><div class="label">{label}</div>'
        f'<div class="v-text">{text}</div>'
        f'<div class="top-actions">{_top_actions(actions)}</div></div>'
    )


def _decision_box(conclusion):
    return (
        f'<div class="decision-box"><div class="label">Decision · 决策建议</div>'
        f'<div class="one-liner">{e(conclusion)}</div></div>'
    )


def _tag_cls(val, high="高"):
    return "tag-high" if val == high else "tag-mid" if val == "中" else "tag-low"


# ═══ BRD 10 章 ═══

def _build_brd(d):
    today = datetime.now().strftime("%Y-%m-%d")
    product = d.get("product", "未命名产品")
    cover_tag = d.get("cover_tag", "BUSINESS REQUIREMENT DOCUMENT")
    parts = []

    # Cover
    parts.append(
        f'<header class="cover"><div class="tag">{cover_tag}</div>'
        f'<h1>{e(d.get("cover_title", f"BRD：{product}"))}</h1>'
        f'<div class="lead">{e(d.get("cover_lead",""))}</div>'
        f'<div class="meta-row"><span>{today}</span><span>BRD/MRD 大师 Skill</span>'
        f'<span>{e(d.get("purpose",""))}</span></div></header>'
    )

    # Ch1 执行摘要
    es = d.get("executive_summary", {})
    parts.append(_verdict(
        "Executive Summary · 执行摘要",
        f'{e(es.get("overview",""))}<br><br>'
        f'<span style="font-size:16px;font-weight:600">一句话定位：{e(es.get("one_liner",""))}</span>',
        es.get("top_actions", [])
    ))

    # Ch2 项目背景
    bg = d.get("project_background", {})
    parts.append(_section("Chapter 02", "项目背景", "回答：为什么现在要做这件事？",
        f'<div class="hl-box hl-blue"><p>{e(bg.get("market_opportunity",""))}</p></div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700;color:var(--red)">核心痛点</h3>'
        f'{_styled_list(bg.get("pain_points",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700;color:var(--ink)">战略契合度</h3>'
        f'<p>{e(bg.get("strategic_fit",""))}</p>'
    ))

    # Ch3 市场分析
    ma = d.get("market_analysis", {})
    ms = ma.get("market_size", {})
    metrics = [
        {"value": ms.get("tam",{}).get("value",""), "label": "TAM · 总可触达市场", "color": "blue"},
        {"value": ms.get("sam",{}).get("value",""), "label": "SAM · 可服务市场", "color": "green"},
        {"value": ms.get("som",{}).get("value",""), "label": "SOM · 可获取市场", "color": "amber"},
    ]
    comps = "".join(
        f'<div class="player-card"><div class="p-name">{e(c.get("name",""))}</div>'
        f'<div class="p-role">{e(c.get("positioning",""))}</div>'
        f'<div class="p-note">{e(c.get("strength",""))}</div></div>'
        for c in ma.get("competitors", [])
    )
    trends = "".join(
        f'<li>{e(t.get("trend",""))} <span class="{_tag_cls(t.get("impact",""))}">'
        f'{e(t.get("impact",""))}</span></li>'
        for t in ma.get("trends", [])
    )
    parts.append(_section("Chapter 03", "市场分析", "回答：这个市场有多大？谁在玩？往哪走？",
        f'{_metric_row(metrics)}'
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">目标用户</h3>'
        f'<p style="margin-bottom:20px">{e(ma.get("target_users",""))}</p>'
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">竞品格局</h3>'
        f'<div class="player-grid">{comps}</div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">市场趋势</h3>'
        f'<ul class="styled-list">{trends}</ul>'
    ))

    # Ch4 商业模式
    bm = d.get("business_model", {})
    roi = bm.get("roi", {})
    parts.append(_section("Chapter 04", "商业模式", "回答：怎么赚钱？能赚多少？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">盈利模式</h3>'
        f'{_styled_list(bm.get("revenue_model",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">收入预测</h3>'
        f'{_data_table([("年份","year"),("收入预测","revenue"),("关键假设","note")], bm.get("revenue_forecast",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">成本结构</h3>'
        f'{_data_table([("成本类目","category"),("类型","type"),("估算金额","estimate"),("说明","note")], bm.get("cost_structure",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">ROI 分析</h3>'
        f'<div class="roi-grid">'
        f'<div class="roi-card"><div class="roi-val">{e(roi.get("breakeven",""))}</div><div class="roi-label">盈亏平衡点</div></div>'
        f'<div class="roi-card"><div class="roi-val">{e(roi.get("payback_period",""))}</div><div class="roi-label">投资回收期</div></div>'
        f'<div class="roi-card"><div class="roi-val">{e(roi.get("expected_roi",""))}</div><div class="roi-label">预期 ROI</div></div>'
        f'</div>'
    ))

    # Ch5 产品定位
    pp = d.get("product_positioning", {})
    parts.append(_section("Chapter 05", "产品定位", "回答：我们到底卖什么？跟别人有什么不一样？",
        f'<div class="hl-box hl-blue"><p><strong>核心价值主张</strong>：{e(pp.get("value_proposition",""))}</p></div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">差异化策略</h3>'
        f'{_styled_list(pp.get("differentiation",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">目标用户画像</h3>'
        f'{_persona_cards(pp.get("user_personas",[]))}'
    ))

    # Ch6 功能规划
    fp = d.get("feature_planning", {})
    phase_cls = {"Phase 1": "tl-now", "Phase 2": "tl-mid", "Phase 3": "tl-long"}
    tl = ""
    for rp in fp.get("roadmap", []):
        feats = "".join(f"<li>{e(f)}</li>" for f in rp.get("features", []))
        cls = phase_cls.get(rp.get("phase", ""), "tl-now")
        tl += (f'<div class="tl-phase {cls}"><h4>{e(rp.get("phase",""))} · {e(rp.get("timeline",""))}</h4>'
               f'<div class="phase-goal">目标：{e(rp.get("goal",""))}</div><ul>{feats}</ul></div>')
    parts.append(_section("Chapter 06", "功能规划", "回答：先做什么？后做什么？优先级怎么排？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">MVP 功能清单</h3>'
        f'{_styled_list(fp.get("mvp",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">分阶段路线图</h3>'
        f'<div class="timeline">{tl}</div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">优先级矩阵</h3>'
        f'{_data_table([("功能","feature"),("优先级","priority"),("开发成本","effort"),("业务影响","impact"),("说明","note")], fp.get("priority_matrix",[]))}'
    ))

    # Ch7 运营策略
    os_ = d.get("operation_strategy", {})
    parts.append(_section("Chapter 07", "运营策略", "回答：怎么获客？怎么增长？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">获客渠道</h3>'
        f'{_data_table([("渠道","channel"),("类型","type"),("预估成本","cost"),("预期效果","expectation")], os_.get("channels",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">增长策略</h3>'
        f'{_styled_list(os_.get("growth_strategy",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">合作伙伴</h3>'
        + "\n".join(
            f'<div class="partner-item"><strong>{e(p.get("partner",""))}</strong> · '
            f'{e(p.get("type",""))} — {e(p.get("value",""))}</div>'
            for p in os_.get("partnerships", [])
        )
    ))

    # Ch8 风险评估
    ra = data if False else d.get("risk_assessment", {})
    risk_cards = ""
    for r in ra.get("risks", []):
        risk_cards += (
            f'<div class="risk-card"><div class="rc-head">'
            f'<strong>{e(r.get("category",""))}风险</strong>：{e(r.get("risk",""))}</div>'
            f'<div class="rc-meta">概率：<span class="{_tag_cls(r.get("probability",""))}">'
            f'{e(r.get("probability",""))}</span> | 影响：<span class="{_tag_cls(r.get("impact",""))}">'
            f'{e(r.get("impact",""))}</span></div>'
            f'<div class="rc-mit">应对措施：{e(r.get("mitigation",""))}</div></div>'
        )
    parts.append(_section("Chapter 08", "风险评估", "回答：可能出什么问题？怎么应对？",
        f'<div class="risk-grid">{risk_cards}</div>'
    ))

    # Ch9 资源需求
    rr = d.get("resource_requirements", {})
    parts.append(_section("Chapter 09", "资源需求", "回答：需要多少人？多少钱？多长时间？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">团队配置</h3>'
        f'{_data_table([("岗位","role"),("人数","count"),("阶段","phase"),("职责说明","note")], rr.get("team",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">预算估算</h3>'
        f'{_data_table([("类目","category"),("金额","amount"),("说明","note")], rr.get("budget",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">时间规划</h3>'
        f'{_data_table([("里程碑","milestone"),("目标时间","date"),("交付物","deliverable")], rr.get("timeline",[]))}'
    ))

    # Ch10 成功指标
    sm = d.get("success_metrics", {})
    parts.append(_section("Chapter 10", "成功指标", "回答：怎么判断做成了？",
        f'<div class="hl-box hl-blue"><p><strong>北极星指标</strong>：{e(sm.get("north_star",""))}</p></div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">阶段性 KPI</h3>'
        f'{_data_table([("阶段","phase"),("指标","metric"),("目标值","target"),("时间","timeline")], sm.get("kpis",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">关键里程碑</h3>'
        f'{_data_table([("里程碑","milestone"),("目标日期","target_date"),("达成标准","success_criteria")], sm.get("milestones",[]))}'
    ))

    # 决策
    rec = d.get("recommendations", {})
    parts.append(_decision_box(rec.get("conclusion", "")))
    parts.append(_section("Chapter 11", "行动方案", "做什么、不做什么、什么时间做",
        f'<div class="act-list">{_decision_actions(rec.get("actions",[]))}</div>'
        f'<h3 style="margin:24px 0 12px;font-size:15px;font-weight:700;color:var(--red)">不建议做的事</h3>'
        f'{_not_do(rec.get("not_do",[]))}'
    ))

    # Footer
    parts.append(
        f'<div class="report-footer"><p>由「BRD/MRD 大师」生成 · {today}</p>'
        f'<p style="margin-top:4px;">本报告基于公开信息与AI分析生成，关键数据建议进一步验证</p></div>'
    )
    return "\n".join(parts), f"BRD 报告 - {product}"


# ═══ MRD 7 章 ═══

def _build_mrd(d):
    today = datetime.now().strftime("%Y-%m-%d")
    product = d.get("product", "未命名产品")
    cover_tag = d.get("cover_tag", "MARKET REQUIREMENT DOCUMENT")
    parts = []

    # Cover
    parts.append(
        f'<header class="cover"><div class="tag">{cover_tag}</div>'
        f'<h1>{e(d.get("cover_title", f"MRD：{product}"))}</h1>'
        f'<div class="lead">{e(d.get("cover_lead",""))}</div>'
        f'<div class="meta-row"><span>{today}</span><span>BRD/MRD 大师 Skill</span>'
        f'<span>{e(d.get("purpose",""))}</span></div></header>'
    )

    # Ch1 执行摘要
    es = d.get("executive_summary", {})
    parts.append(_verdict(
        "Executive Summary · 执行摘要",
        e(es.get("conclusion", "")),
        es.get("top_actions", [])
    ))

    # Ch2 市场机会评估
    mo = d.get("market_opportunity", {})
    ms = mo.get("market_size", {})
    gr = mo.get("growth_rate", {})
    pen = mo.get("penetration", {})
    metrics = [
        {"value": ms.get("tam",{}).get("value",""), "label": "TAM", "color": "blue"},
        {"value": ms.get("sam",{}).get("value",""), "label": "SAM", "color": "green"},
        {"value": ms.get("som",{}).get("value",""), "label": "SOM", "color": "amber"},
        {"value": gr.get("projected",""), "label": "预测增长率", "color": "green"},
        {"value": pen.get("current",""), "label": "当前渗透率", "color": "blue"},
    ]
    parts.append(_section("Chapter 02", "市场机会评估", "回答：这个市场值不值得进？",
        f'{_metric_row(metrics)}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">增长率</h3>'
        f'<p>历史增长率：{e(gr.get("historical",""))} | 预测增长率：{e(gr.get("projected",""))}</p>'
        f'<p>增长驱动因素：{e(gr.get("driver",""))}</p>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">渗透率分析</h3>'
        f'<p>当前渗透率：{e(pen.get("current",""))} | 潜在渗透率：{e(pen.get("potential",""))}</p>'
        f'<p>{e(pen.get("gap_analysis",""))}</p>'
    ))

    # Ch3 用户需求分析
    un = d.get("user_needs", {})
    parts.append(_section("Chapter 03", "用户需求分析", "回答：用户到底要什么？最痛的是什么？",
        f'{_persona_cards(un.get("personas",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">核心需求列表</h3>'
        f'{_data_table([("需求","need"),("类型","category"),("重要性","importance"),("现有方案","current_solution"),("满意度","satisfaction")], un.get("core_needs",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">痛点优先级</h3>'
        f'{_data_table([("痛点","pain"),("频率","frequency"),("严重度","severity"),("影响范围","affected_users"),("优先级","priority")], un.get("pain_priority",[]))}'
    ))

    # Ch4 竞品分析
    ca = d.get("competitor_analysis", {})
    swot = ca.get("swot_comparison", {})
    parts.append(_section("Chapter 04", "竞品分析", "回答：谁在做？做得怎么样？我们的机会在哪？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">直接竞品</h3>'
        f'{_data_table([("竞品","name"),("市场份额","market_share"),("优势","strengths"),("劣势","weaknesses"),("定价","pricing")], ca.get("direct",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">间接竞品</h3>'
        + "\n".join(
            f'<div class="ind-item"><strong>{e(i.get("name",""))}</strong> '
            f'<span class="{_tag_cls(i.get("threat_level",""))}">{e(i.get("threat_level",""))}</span>'
            f'<span style="margin-left:12px;font-size:12px;color:var(--ink-muted)">{e(i.get("note",""))}</span></div>'
            for i in ca.get("indirect", [])
        )
        + (f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">替代方案</h3>'
           f'{_styled_list(ca.get("alternatives",[]))}' if ca.get("alternatives") else '')
        + f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">SWOT 对比</h3>'
          f'<div class="swot-2col">'
          f'<div class="swot-box swot-s"><h3>▸ 优势</h3><ul>{"".join(f"<li>{e(s)}</li>" for s in swot.get("strengths",[]))}</ul></div>'
          f'<div class="swot-box swot-w"><h3>▸ 劣势</h3><ul>{"".join(f"<li>{e(w)}</li>" for w in swot.get("weaknesses",[]))}</ul></div>'
          f'<div class="swot-box swot-o"><h3>▸ 机会</h3><ul>{"".join(f"<li>{e(o)}</li>" for o in swot.get("opportunities",[]))}</ul></div>'
          f'<div class="swot-box swot-t"><h3>▸ 威胁</h3><ul>{"".join(f"<li>{e(t)}</li>" for t in swot.get("threats",[]))}</ul></div>'
          f'</div>'
    ))

    # Ch5 产品建议
    ps = d.get("product_suggestions", {})
    parts.append(_section("Chapter 05", "产品建议", "回答：应该做什么产品？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">功能需求优先级</h3>'
        f'{_data_table([("功能建议","feature"),("优先级","priority"),("用户需求强度","user_demand"),("竞品差距","competitive_gap"),("开发成本","effort")], ps.get("feature_priorities",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">用户体验建议</h3>'
        f'{_styled_list(ps.get("ux_suggestions",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">技术方向建议</h3>'
        f'{_styled_list(ps.get("tech_direction",[]))}'
    ))

    # Ch6 GTM策略
    gtm = d.get("gtm_strategy", {})
    pricing = gtm.get("pricing", {})
    parts.append(_section("Chapter 06", "GTM 策略建议", "回答：怎么推向市场？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">定价策略</h3>'
        f'<div class="hl-box hl-blue"><p>'
        f'<strong>模式</strong>：{e(pricing.get("model",""))} | '
        f'<strong>区间</strong>：{e(pricing.get("price_range",""))}<br>'
        f'<strong>竞品对比</strong>：{e(pricing.get("competitor_comparison",""))}<br>'
        f'<strong>定价逻辑</strong>：{e(pricing.get("rationale",""))}</p></div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">渠道策略</h3>'
        f'{_data_table([("渠道","channel"),("类型","type"),("优先级","priority"),("说明","note")], gtm.get("channels",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">推广策略</h3>'
        f'{_data_table([("策略","strategy"),("阶段","phase"),("预算占比","budget_allocation"),("预期效果","expected_effect")], gtm.get("promotion",[]))}'
    ))

    # Ch7 数据支撑
    ds = d.get("data_support", {})
    parts.append(_section("Chapter 07", "数据支撑", "回答：结论从哪来？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">行业数据</h3>'
        f'{_data_table([("来源","source"),("数据内容","data"),("年份","year"),("相关性","relevance")], ds.get("industry_data",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">用户调研</h3>'
        f'{_data_table([("方法","method"),("样本量","sample"),("关键发现","finding"),("置信度","confidence")], ds.get("user_research",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">市场预测</h3>'
        f'{_data_table([("指标","metric"),("当前值","current"),("1年后预测","projected_1y"),("3年后预测","projected_3y"),("假设","assumption")], ds.get("market_forecast",[]))}'
    ))

    # 决策
    rec = d.get("recommendations", {})
    parts.append(_decision_box(rec.get("conclusion", "")))
    parts.append(_section("Chapter 08", "行动方案", "做什么、不做什么",
        f'<div class="act-list">{_decision_actions(rec.get("actions",[]))}</div>'
        f'<h3 style="margin:24px 0 12px;font-size:15px;font-weight:700;color:var(--red)">不建议做的事</h3>'
        f'{_not_do(rec.get("not_do",[]))}'
    ))

    # Footer
    parts.append(
        f'<div class="report-footer"><p>由「BRD/MRD 大师」生成 · {today}</p>'
        f'<p style="margin-top:4px;">本报告基于公开信息与AI分析生成，关键数据建议进一步验证</p></div>'
    )
    return "\n".join(parts), f"MRD 报告 - {product}"


# ═══ BRD Markdown ═══

def _md_table(headers, rows):
    if not rows:
        return ""
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join("---" for _ in headers) + " |"
    body_lines = []
    for row in rows:
        body_lines.append("| " + " | ".join(str(row.get(k, "")).replace("|", "｜") for k in headers) + " |")
    return header_line + "\n" + sep_line + "\n" + "\n".join(body_lines) + "\n"


def _md_list(items):
    if not items:
        return ""
    lines = []
    for i in items:
        if isinstance(i, str):
            lines.append(f"- {i}")
        else:
            lines.append(f"- {i}")
    return "\n".join(lines) + "\n"


def _build_brd_md(d):
    today = datetime.now().strftime("%Y-%m-%d")
    product = d.get("product", "未命名产品")
    purpose = d.get("purpose", "")
    audience = d.get("audience", "")
    md = []

    # Title
    md.append(f"# BRD：{product}\n")
    md.append(f"> {d.get('cover_lead', '')}\n")
    md.append(f"**日期**：{today} | **目的**：{purpose} | **受众**：{audience}\n")
    md.append("---\n")

    # Ch1 执行摘要
    es = d.get("executive_summary", {})
    md.append("## Chapter 1：执行摘要\n")
    if es.get("overview"):
        md.append(f"{es['overview']}\n")
    if es.get("one_liner"):
        md.append(f"**一句话定位**：{es['one_liner']}\n")
    if es.get("core_values"):
        md.append("### 核心商业价值\n")
        for v in es["core_values"]:
            md.append(f"- {v.get('value', '')}")
        md.append("")
    if es.get("top_actions"):
        md.append("### 建议行动\n")
        md.append("| 优先级 | 行动 | 预期效果 |\n|--------|------|----------|")
        for a in es["top_actions"]:
            md.append(f"| {a.get('priority','')} | {a.get('action','')} | {a.get('effect','')} |")
        md.append("")

    # Ch2 项目背景
    bg = d.get("project_background", {})
    md.append("## Chapter 2：项目背景\n")
    if bg.get("market_opportunity"):
        md.append("### 市场机会\n")
        md.append(f"{bg['market_opportunity']}\n")
    if bg.get("pain_points"):
        md.append("### 核心痛点\n")
        for p in bg["pain_points"]:
            md.append(f"- {p}")
        md.append("")
    if bg.get("strategic_fit"):
        md.append("### 战略契合度\n")
        md.append(f"{bg['strategic_fit']}\n")

    # Ch3 市场分析
    ma = d.get("market_analysis", {})
    ms = ma.get("market_size", {})
    md.append("## Chapter 3：市场分析\n")
    md.append("### 市场规模\n")
    md.append("| 指标 | 数值 |")
    md.append("|------|------|")
    for key, label in [("tam", "TAM · 总可触达市场"), ("sam", "SAM · 可服务市场"), ("som", "SOM · 可获取市场")]:
        val = ms.get(key, {}).get("value", "")
        if val:
            md.append(f"| {label} | {val} |")
    md.append("")
    if ma.get("target_users"):
        md.append("### 目标用户\n")
        md.append(f"{ma['target_users']}\n")
    if ma.get("competitors"):
        md.append("### 竞品格局\n")
        md.append("| 竞品名 | 定位 | 核心优势 |")
        md.append("|--------|------|----------|")
        for c in ma["competitors"]:
            md.append(f"| {c.get('name','')} | {c.get('positioning','')} | {c.get('strength','')} |")
        md.append("")
    if ma.get("trends"):
        md.append("### 市场趋势\n")
        md.append("| 趋势 | 影响程度 | 对我们的影响 |")
        md.append("|------|----------|-------------|")
        for t in ma["trends"]:
            md.append(f"| {t.get('trend','')} | {t.get('impact','')} | {t.get('implication','')} |")
        md.append("")

    # Ch4 商业模式
    bm = d.get("business_model", {})
    roi = bm.get("roi", {})
    md.append("## Chapter 4：商业模式\n")
    if bm.get("revenue_model"):
        md.append("### 盈利模式\n")
        md.append(_md_list(bm["revenue_model"]))
    if bm.get("revenue_forecast"):
        md.append("### 收入预测\n")
        md.append(_md_table(["year", "revenue", "note"],
                            [{"year": r.get("year",""), "revenue": r.get("revenue",""), "note": r.get("note","")} for r in bm["revenue_forecast"]]))
    if bm.get("cost_structure"):
        md.append("### 成本结构\n")
        md.append(_md_table(["category", "type", "estimate", "note"],
                            [{"category": r.get("category",""), "type": r.get("type",""), "estimate": r.get("estimate",""), "note": r.get("note","")} for r in bm["cost_structure"]]))
    md.append("### ROI 分析\n")
    md.append(f"- **盈亏平衡点**：{roi.get('breakeven','')}")
    md.append(f"- **投资回收期**：{roi.get('payback_period','')}")
    md.append(f"- **预期 ROI**：{roi.get('expected_roi','')}\n")

    # Ch5 产品定位
    pp = d.get("product_positioning", {})
    md.append("## Chapter 5：产品定位\n")
    if pp.get("value_proposition"):
        md.append(f"### 核心价值主张\n\n{pp['value_proposition']}\n")
    if pp.get("differentiation"):
        md.append("### 差异化策略\n")
        md.append(_md_list(pp["differentiation"]))
    if pp.get("user_personas"):
        md.append("### 目标用户画像\n")
        for p in pp["user_personas"]:
            md.append(f"**{p.get('name','')}** · {p.get('role','')} · {p.get('age_range','')}")
            for key, label in [("needs","核心需求"),("pain_points","痛点"),("behavior","行为特征")]:
                if p.get(key):
                    md.append(f"- {label}：{p[key]}")
            md.append("")

    # Ch6 功能规划
    fp = d.get("feature_planning", {})
    md.append("## Chapter 6：功能规划\n")
    if fp.get("mvp"):
        md.append("### MVP 功能清单\n")
        md.append(_md_list(fp["mvp"]))
    if fp.get("roadmap"):
        md.append("### 分阶段路线图\n")
        for rp in fp["roadmap"]:
            md.append(f"**{rp.get('phase','')}** · {rp.get('timeline','')}")
            md.append(f"- 目标：{rp.get('goal','')}")
            for feat in rp.get("features", []):
                md.append(f"- {feat}")
            md.append("")
    if fp.get("priority_matrix"):
        md.append("### 优先级矩阵\n")
        md.append(_md_table(["feature", "priority", "effort", "impact", "note"],
                            [{"feature": r.get("feature",""), "priority": r.get("priority",""), "effort": r.get("effort",""), "impact": r.get("impact",""), "note": r.get("note","")} for r in fp["priority_matrix"]]))

    # Ch7 运营策略
    os_ = d.get("operation_strategy", {})
    md.append("## Chapter 7：运营策略\n")
    if os_.get("channels"):
        md.append("### 获客渠道\n")
        md.append(_md_table(["channel", "type", "cost", "expectation"],
                            [{"channel": r.get("channel",""), "type": r.get("type",""), "cost": r.get("cost",""), "expectation": r.get("expectation","")} for r in os_["channels"]]))
    if os_.get("growth_strategy"):
        md.append("### 增长策略\n")
        md.append(_md_list(os_["growth_strategy"]))
    if os_.get("partnerships"):
        md.append("### 合作伙伴\n")
        md.append("| 合作方 | 合作类型 | 合作价值 |\n|--------|----------|----------|")
        for p in os_["partnerships"]:
            md.append(f"| {p.get('partner','')} | {p.get('type','')} | {p.get('value','')} |")
        md.append("")

    # Ch8 风险评估
    ra = d.get("risk_assessment", {})
    md.append("## Chapter 8：风险评估\n")
    if ra.get("risks"):
        md.append("| 类别 | 风险描述 | 概率 | 影响 | 应对措施 |")
        md.append("|------|----------|------|------|----------|")
        for r in ra["risks"]:
            md.append(f"| {r.get('category','')} | {r.get('risk','')} | {r.get('probability','')} | {r.get('impact','')} | {r.get('mitigation','')} |")
        md.append("")

    # Ch9 资源需求
    rr = d.get("resource_requirements", {})
    md.append("## Chapter 9：资源需求\n")
    if rr.get("team"):
        md.append("### 团队配置\n")
        md.append(_md_table(["role", "count", "phase", "note"],
                            [{"role": r.get("role",""), "count": r.get("count",""), "phase": r.get("phase",""), "note": r.get("note","")} for r in rr["team"]]))
    if rr.get("budget"):
        md.append("### 预算估算\n")
        md.append(_md_table(["category", "amount", "note"],
                            [{"category": r.get("category",""), "amount": r.get("amount",""), "note": r.get("note","")} for r in rr["budget"]]))
    if rr.get("timeline"):
        md.append("### 时间规划\n")
        md.append(_md_table(["milestone", "date", "deliverable"],
                            [{"milestone": r.get("milestone",""), "date": r.get("date",""), "deliverable": r.get("deliverable","")} for r in rr["timeline"]]))

    # Ch10 成功指标
    sm = d.get("success_metrics", {})
    md.append("## Chapter 10：成功指标\n")
    if sm.get("north_star"):
        md.append(f"**北极星指标**：{sm['north_star']}\n")
    if sm.get("kpis"):
        md.append("### 阶段性 KPI\n")
        md.append(_md_table(["phase", "metric", "target", "timeline"],
                            [{"phase": r.get("phase",""), "metric": r.get("metric",""), "target": r.get("target",""), "timeline": r.get("timeline","")} for r in sm["kpis"]]))
    if sm.get("milestones"):
        md.append("### 关键里程碑\n")
        md.append(_md_table(["milestone", "target_date", "success_criteria"],
                            [{"milestone": r.get("milestone",""), "target_date": r.get("target_date",""), "success_criteria": r.get("success_criteria","")} for r in sm["milestones"]]))

    # 决策建议
    rec = d.get("recommendations", {})
    md.append("---\n")
    md.append("## 决策建议\n")
    if rec.get("conclusion"):
        md.append(f"**结论**：{rec['conclusion']}\n")
    if rec.get("actions"):
        md.append("### 行动方案\n")
        md.append("| 优先级 | 行动 | 预期效果 | 所需资源 | 周期 |")
        md.append("|--------|------|----------|----------|------|")
        for a in rec["actions"]:
            md.append(f"| {a.get('priority','')} | {a.get('action','')} | {a.get('effect','')} | {a.get('resource','')} | {a.get('timeline','')} |")
        md.append("")
    if rec.get("not_do"):
        md.append("### 不建议做的事\n")
        for item in rec["not_do"]:
            md.append(f"- **{item.get('item','')}**：{item.get('reason','')}")
        md.append("")

    md.append("---\n")
    md.append(f"*由「BRD/MRD 大师」生成 · {today} · 本报告基于公开信息与AI分析生成，关键数据建议进一步验证*\n")

    return "\n".join(md)


# ═══ MRD Markdown ═══

def _build_mrd_md(d):
    today = datetime.now().strftime("%Y-%m-%d")
    product = d.get("product", "未命名产品")
    purpose = d.get("purpose", "")
    audience = d.get("audience", "")
    md = []

    # Title
    md.append(f"# MRD：{product}\n")
    md.append(f"> {d.get('cover_lead', '')}\n")
    md.append(f"**日期**：{today} | **目的**：{purpose} | **受众**：{audience}\n")
    md.append("---\n")

    # Ch1 执行摘要
    es = d.get("executive_summary", {})
    md.append("## Chapter 1：执行摘要\n")
    if es.get("conclusion"):
        md.append(f"{es['conclusion']}\n")
    if es.get("top_findings"):
        md.append("### 核心发现\n")
        for f in es["top_findings"]:
            md.append(f"- **{f.get('finding','')}**（依据：{f.get('basis','')}）")
        md.append("")
    if es.get("top_actions"):
        md.append("### 建议行动\n")
        md.append("| 优先级 | 行动 | 预期效果 |\n|--------|------|----------|")
        for a in es["top_actions"]:
            md.append(f"| {a.get('priority','')} | {a.get('action','')} | {a.get('effect','')} |")
        md.append("")

    # Ch2 市场机会评估
    mo = d.get("market_opportunity", {})
    ms_ = mo.get("market_size", {})
    gr = mo.get("growth_rate", {})
    pen = mo.get("penetration", {})
    md.append("## Chapter 2：市场机会评估\n")
    md.append("### 市场规模\n")
    md.append("| 指标 | 数值 |")
    md.append("|------|------|")
    for key, label in [("tam", "TAM · 总可触达市场"), ("sam", "SAM · 可服务市场"), ("som", "SOM · 可获取市场")]:
        val = ms_.get(key, {}).get("value", "")
        if val:
            md.append(f"| {label} | {val} |")
    md.append("")
    if gr:
        md.append("### 增长率\n")
        md.append(f"- **历史增长率**：{gr.get('historical','')}")
        md.append(f"- **预测增长率**：{gr.get('projected','')}")
        md.append(f"- **增长驱动因素**：{gr.get('driver','')}\n")
    if pen:
        md.append("### 渗透率分析\n")
        md.append(f"- **当前渗透率**：{pen.get('current','')}")
        md.append(f"- **潜在渗透率**：{pen.get('potential','')}")
        md.append(f"- **差距分析**：{pen.get('gap_analysis','')}\n")

    # Ch3 用户需求分析
    un = d.get("user_needs", {})
    md.append("## Chapter 3：用户需求分析\n")
    if un.get("personas"):
        md.append("### 目标用户画像\n")
        for p in un["personas"]:
            md.append(f"**{p.get('name','')}** · {p.get('role','')} · {p.get('demographics','')}")
            for key, label in [("needs","核心需求"),("pain_points","痛点"),("behavior","行为特征")]:
                if p.get(key):
                    md.append(f"- {label}：{p[key]}")
            md.append("")
    if un.get("core_needs"):
        md.append("### 核心需求列表\n")
        md.append(_md_table(["need", "category", "importance", "current_solution", "satisfaction"],
                            [{"need": r.get("need",""), "category": r.get("category",""), "importance": r.get("importance",""), "current_solution": r.get("current_solution",""), "satisfaction": r.get("satisfaction","")} for r in un["core_needs"]]))
    if un.get("pain_priority"):
        md.append("### 痛点优先级\n")
        md.append(_md_table(["pain", "frequency", "severity", "affected_users", "priority"],
                            [{"pain": r.get("pain",""), "frequency": r.get("frequency",""), "severity": r.get("severity",""), "affected_users": r.get("affected_users",""), "priority": r.get("priority","")} for r in un["pain_priority"]]))

    # Ch4 竞品分析
    ca = d.get("competitor_analysis", {})
    swot = ca.get("swot_comparison", {})
    md.append("## Chapter 4：竞品分析\n")
    if ca.get("direct"):
        md.append("### 直接竞品\n")
        md.append("| 竞品 | 市场份额 | 优势 | 劣势 | 定价 |")
        md.append("|------|----------|------|------|------|")
        for c in ca["direct"]:
            strengths = "、".join(c.get("strengths", [])) if isinstance(c.get("strengths"), list) else c.get("strengths", "")
            weaknesses = "、".join(c.get("weaknesses", [])) if isinstance(c.get("weaknesses"), list) else c.get("weaknesses", "")
            md.append(f"| {c.get('name','')} | {c.get('market_share','')} | {strengths} | {weaknesses} | {c.get('pricing','')} |")
        md.append("")
    if ca.get("indirect"):
        md.append("### 间接竞品\n")
        md.append("| 竞品 | 威胁程度 | 说明 |")
        md.append("|------|----------|------|")
        for i in ca["indirect"]:
            md.append(f"| {i.get('name','')} | {i.get('threat_level','')} | {i.get('note','')} |")
        md.append("")
    if ca.get("alternatives"):
        md.append("### 替代方案\n")
        md.append(_md_list(ca["alternatives"]))
    if swot:
        md.append("### SWOT 对比\n")
        for key, label in [("strengths","优势"),("weaknesses","劣势"),("opportunities","机会"),("threats","威胁")]:
            items = swot.get(key, [])
            if items:
                md.append(f"**{label}**")
                for item in items:
                    md.append(f"- {item}")
                md.append("")

    # Ch5 产品建议
    ps = d.get("product_suggestions", {})
    md.append("## Chapter 5：产品建议\n")
    if ps.get("feature_priorities"):
        md.append("### 功能需求优先级\n")
        md.append(_md_table(["feature", "priority", "user_demand", "competitive_gap", "effort"],
                            [{"feature": r.get("feature",""), "priority": r.get("priority",""), "user_demand": r.get("user_demand",""), "competitive_gap": r.get("competitive_gap",""), "effort": r.get("effort","")} for r in ps["feature_priorities"]]))
    if ps.get("ux_suggestions"):
        md.append("### 用户体验建议\n")
        md.append(_md_list(ps["ux_suggestions"]))
    if ps.get("tech_direction"):
        md.append("### 技术方向建议\n")
        md.append(_md_list(ps["tech_direction"]))

    # Ch6 GTM策略
    gtm = d.get("gtm_strategy", {})
    pricing = gtm.get("pricing", {})
    md.append("## Chapter 6：GTM 策略建议\n")
    if pricing:
        md.append("### 定价策略\n")
        md.append(f"- **模式**：{pricing.get('model','')}")
        md.append(f"- **价格区间**：{pricing.get('price_range','')}")
        md.append(f"- **竞品对比**：{pricing.get('competitor_comparison','')}")
        md.append(f"- **定价逻辑**：{pricing.get('rationale','')}\n")
    if gtm.get("channels"):
        md.append("### 渠道策略\n")
        md.append(_md_table(["channel", "type", "priority", "note"],
                            [{"channel": r.get("channel",""), "type": r.get("type",""), "priority": r.get("priority",""), "note": r.get("note","")} for r in gtm["channels"]]))
    if gtm.get("promotion"):
        md.append("### 推广策略\n")
        md.append(_md_table(["strategy", "phase", "budget_allocation", "expected_effect"],
                            [{"strategy": r.get("strategy",""), "phase": r.get("phase",""), "budget_allocation": r.get("budget_allocation",""), "expected_effect": r.get("expected_effect","")} for r in gtm["promotion"]]))

    # Ch7 数据支撑
    ds = d.get("data_support", {})
    md.append("## Chapter 7：数据支撑\n")
    if ds.get("industry_data"):
        md.append("### 行业数据\n")
        md.append(_md_table(["source", "data", "year", "relevance"],
                            [{"source": r.get("source",""), "data": r.get("data",""), "year": r.get("year",""), "relevance": r.get("relevance","")} for r in ds["industry_data"]]))
    if ds.get("user_research"):
        md.append("### 用户调研\n")
        md.append(_md_table(["method", "sample", "finding", "confidence"],
                            [{"method": r.get("method",""), "sample": r.get("sample",""), "finding": r.get("finding",""), "confidence": r.get("confidence","")} for r in ds["user_research"]]))
    if ds.get("market_forecast"):
        md.append("### 市场预测\n")
        md.append(_md_table(["metric", "current", "projected_1y", "projected_3y", "assumption"],
                            [{"metric": r.get("metric",""), "current": r.get("current",""), "projected_1y": r.get("projected_1y",""), "projected_3y": r.get("projected_3y",""), "assumption": r.get("assumption","")} for r in ds["market_forecast"]]))

    # 决策建议
    rec = d.get("recommendations", {})
    md.append("---\n")
    md.append("## 决策建议\n")
    if rec.get("conclusion"):
        md.append(f"**结论**：{rec['conclusion']}\n")
    if rec.get("actions"):
        md.append("### 行动方案\n")
        md.append("| 优先级 | 行动 | 预期效果 | 所需资源 | 周期 |")
        md.append("|--------|------|----------|----------|------|")
        for a in rec["actions"]:
            md.append(f"| {a.get('priority','')} | {a.get('action','')} | {a.get('effect','')} | {a.get('resource','')} | {a.get('timeline','')} |")
        md.append("")
    if rec.get("not_do"):
        md.append("### 不建议做的事\n")
        for item in rec["not_do"]:
            md.append(f"- **{item.get('item','')}**：{item.get('reason','')}")
        md.append("")

    md.append("---\n")
    md.append(f"*由「BRD/MRD 大师」生成 · {today} · 本报告基于公开信息与AI分析生成，关键数据建议进一步验证*\n")

    return "\n".join(md)


# ═══ 主入口 ═══

def generate_report(data_json_path, output_path=None):
    with open(data_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    template = load_template()
    doc_type = data.get("type", "BRD")

    if doc_type == "MRD":
        content, title = _build_mrd(data)
    else:
        content, title = _build_brd(data)

    html = template.replace("{{TITLE}}", title).replace("{{CONTENT}}", content)

    if not output_path:
        today = datetime.now().strftime("%Y-%m-%d")
        product = data.get("product", "未命名产品")
        prefix = "BRD" if doc_type == "BRD" else "MRD"
        output_path = f"{prefix}报告_{product}_{today}.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 生成对应的 Markdown 文件
    md_path = os.path.splitext(output_path)[0] + ".md"
    if doc_type == "MRD":
        md_content = _build_mrd_md(data)
    else:
        md_content = _build_brd_md(data)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"HTML 报告已生成：{output_path}")
    print(f"Markdown 报告已生成：{md_path}")
    return output_path, md_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python generate-report.py <data.json> [output.html]")
        print("\ndata.json 为分析结果的 JSON 文件（BRD 或 MRD 格式）")
        sys.exit(1)

    data_path = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    generate_report(data_path, output)
