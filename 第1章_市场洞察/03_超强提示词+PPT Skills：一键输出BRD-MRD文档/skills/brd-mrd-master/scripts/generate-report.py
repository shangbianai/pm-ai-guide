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


def _data_table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = ""
    for row in rows:
        tr += "<tr>" + "".join(f"<td>{e(row.get(h,''))}</td>" for h in headers) + "</tr>"
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
        f'{_data_table(["年份","收入预测","关键假设"], bm.get("revenue_forecast",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">成本结构</h3>'
        f'{_data_table(["成本类目","类型","估算金额","说明"], bm.get("cost_structure",[]))}'
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
        f'{_data_table(["功能","优先级","开发成本","业务影响","说明"], fp.get("priority_matrix",[]))}'
    ))

    # Ch7 运营策略
    os_ = d.get("operation_strategy", {})
    parts.append(_section("Chapter 07", "运营策略", "回答：怎么获客？怎么增长？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">获客渠道</h3>'
        f'{_data_table(["渠道","类型","预估成本","预期效果"], os_.get("channels",[]))}'
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
        f'{_data_table(["岗位","人数","阶段","职责说明"], rr.get("team",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">预算估算</h3>'
        f'{_data_table(["类目","金额","说明"], rr.get("budget",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">时间规划</h3>'
        f'{_data_table(["里程碑","目标时间","交付物"], rr.get("timeline",[]))}'
    ))

    # Ch10 成功指标
    sm = d.get("success_metrics", {})
    parts.append(_section("Chapter 10", "成功指标", "回答：怎么判断做成了？",
        f'<div class="hl-box hl-blue"><p><strong>北极星指标</strong>：{e(sm.get("north_star",""))}</p></div>'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">阶段性 KPI</h3>'
        f'{_data_table(["阶段","指标","目标值","时间"], sm.get("kpis",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">关键里程碑</h3>'
        f'{_data_table(["里程碑","目标日期","达成标准"], sm.get("milestones",[]))}'
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
        f'{_data_table(["需求","类型","重要性","现有方案","满意度"], un.get("core_needs",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">痛点优先级</h3>'
        f'{_data_table(["痛点","频率","严重度","影响范围","优先级"], un.get("pain_priority",[]))}'
    ))

    # Ch4 竞品分析
    ca = d.get("competitor_analysis", {})
    swot = ca.get("swot_comparison", {})
    parts.append(_section("Chapter 04", "竞品分析", "回答：谁在做？做得怎么样？我们的机会在哪？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">直接竞品</h3>'
        f'{_data_table(["竞品","市场份额","优势","劣势","定价"], ca.get("direct",[]))}'
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
        f'{_data_table(["功能建议","优先级","用户需求强度","竞品差距","开发成本"], ps.get("feature_priorities",[]))}'
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
        f'{_data_table(["渠道","类型","优先级","说明"], gtm.get("channels",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">推广策略</h3>'
        f'{_data_table(["策略","阶段","预算占比","预期效果"], gtm.get("promotion",[]))}'
    ))

    # Ch7 数据支撑
    ds = d.get("data_support", {})
    parts.append(_section("Chapter 07", "数据支撑", "回答：结论从哪来？",
        f'<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">行业数据</h3>'
        f'{_data_table(["来源","数据内容","年份","相关性"], ds.get("industry_data",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">用户调研</h3>'
        f'{_data_table(["方法","样本量","关键发现","置信度"], ds.get("user_research",[]))}'
        f'<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">市场预测</h3>'
        f'{_data_table(["指标","当前值","1年后预测","3年后预测","假设"], ds.get("market_forecast",[]))}'
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

    print(f"报告已生成：{output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python generate-report.py <data.json> [output.html]")
        print("\ndata.json 为分析结果的 JSON 文件（BRD 或 MRD 格式）")
        sys.exit(1)

    data_path = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    generate_report(data_path, output)
