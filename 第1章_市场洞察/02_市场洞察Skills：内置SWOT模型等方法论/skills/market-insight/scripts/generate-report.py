#!/usr/bin/env python3
"""
市场洞察报告生成器
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


def render_swot_list(items):
    return "\n".join(f"<li>{escape(item)}</li>" for item in items)


def render_strategy_combo(combos):
    parts = []
    for combo in combos:
        label = escape(combo.get("label", ""))
        content = escape(combo.get("content", ""))
        parts.append(f'<div class="strat-item"><strong>{label}</strong>：{content}</div>')
    return "\n".join(parts)


def render_market_metrics(metrics):
    parts = []
    color_map = {"green": "green", "amber": "amber", "red": "red", "blue": "blue"}
    for m in metrics:
        color_cls = color_map.get(m.get("color", ""), "")
        parts.append(
            f'<div class="metric">'
            f'<div class="m-val {color_cls}">{escape(str(m.get("value", "")))}</div>'
            f'<div class="m-label">{escape(m.get("label", ""))}</div>'
            f'</div>'
        )
    return "\n".join(parts)


def render_key_players(players):
    parts = []
    for p in players:
        parts.append(
            f'<div class="player-card">'
            f'<div class="p-name">{escape(p.get("name", ""))}</div>'
            f'<div class="p-role">{escape(p.get("role", ""))}</div>'
            f'<div class="p-note">{escape(p.get("note", ""))}</div>'
            f'</div>'
        )
    return "\n".join(parts)


def render_env_factors(factors):
    parts = []
    for f in factors:
        title = escape(f.get("title", ""))
        items_html = ""
        for item in f.get("items", []):
            impact_cls = "impact-high" if item.get("impact") == "高" else "impact-mid" if item.get("impact") == "中" else "impact-low"
            items_html += (
                f'<li>{escape(item.get("text", ""))} '
                f'<span class="impact-tag {impact_cls}">{escape(str(item.get("impact", "")))}</span></li>'
            )
        card_type = f.get("type", "neutral")
        parts.append(
            f'<div class="env-card {card_type}">'
            f'<div class="e-head"><div class="e-title">{title}</div></div>'
            f'<ul>{items_html}</ul>'
            f'</div>'
        )
    return "\n".join(parts)


def render_kano_rows(items):
    type_cls = {
        "基本型": "type-must", "期望型": "type-expect", "兴奋型": "type-delight",
        "无差异型": "type-neutral", "反向型": "type-reverse"
    }
    rows = []
    for item in items:
        t = escape(item.get("type", ""))
        cls = type_cls.get(item.get("type", ""), "type-neutral")
        rows.append(
            f'<tr>'
            f'<td><span class="type-chip {cls}">{t}</span></td>'
            f'<td>{escape(item.get("need", ""))}</td>'
            f'<td>{escape(str(item.get("our_level", "")))}</td>'
            f'<td>{escape(str(item.get("competitor_level", "")))}</td>'
            f'<td>{escape(item.get("gap", ""))}</td>'
            f'<td>{escape(str(item.get("priority", "")))}</td>'
            f'</tr>'
        )
    return "\n".join(rows)


def render_insight_cards(cards):
    parts = []
    for card in cards:
        title = escape(card.get("category", ""))
        items_html = ""
        for it in card.get("items", []):
            items_html += (
                f'<div class="ins-item">'
                f'<div class="finding">{escape(it.get("finding", ""))}</div>'
                f'<div class="meta-line">依据：{escape(it.get("basis", ""))}</div>'
                f'<div class="meta-line">意味着：{escape(it.get("implication", ""))}</div>'
                f'</div>'
            )
        parts.append(
            f'<div class="ins-card"><h4>{title}</h4>{items_html}</div>'
        )
    return "\n".join(parts)


def render_business_judgment(data):
    html = ""

    value_items = []
    for item in data.get("value", {}).get("opportunities", []):
        color = item.get("color", "green")
        value_items.append(
            f'<div class="val-item"><div class="v-num" style="color:var(--{color})">{escape(str(item.get("value", "")))}</div>'
            f'<div class="v-label">{escape(item.get("name", ""))}</div></div>'
        )
    for item in data.get("value", {}).get("threats", []):
        value_items.append(
            f'<div class="val-item"><div class="v-num" style="color:var(--red)">{escape(str(item.get("loss", "")))}</div>'
            f'<div class="v-label">{escape(item.get("name", ""))}</div></div>'
        )
    html += (
        f'<div class="judge-block"><h4>业务价值评估</h4>'
        f'<div class="val-grid">{"".join(value_items)}</div></div>'
    )

    feas_items = []
    for item in data.get("feasibility", []):
        feas_items.append(
            f'<div class="judge-item"><strong>{escape(item.get("item", ""))}</strong>：{escape(item.get("detail", ""))}</div>'
        )
    html += f'<div class="judge-block"><h4>可行性判断</h4>{"".join(feas_items)}</div>'

    risk_items = []
    for r in data.get("risks", []):
        risk_items.append(
            f'<div class="risk-card">'
            f'<strong>{escape(r.get("risk", ""))}</strong><br>'
            f'{escape(r.get("detail", ""))}'
            f'<div class="risk-meta">触发条件：{escape(r.get("trigger", ""))} | 缓解：{escape(r.get("mitigation", ""))}</div>'
            f'</div>'
        )
    html += f'<div class="judge-block"><h4>风险预判</h4>{"".join(risk_items)}</div>'

    asmp_items = []
    for a in data.get("assumptions", []):
        asmp_items.append(
            f'<div class="judge-item">{escape(a.get("assumption", ""))} '
            f'— 验证：{escape(a.get("validation", ""))} | 置信度：{escape(str(a.get("confidence", "")))}</div>'
        )
    html += f'<div class="judge-block"><h4>关键假设</h4>{"".join(asmp_items)}</div>'

    return html


def render_top_actions(actions):
    parts = []
    for a in actions:
        p_cls = a.get("priority", "p2").lower()
        parts.append(
            f'<div class="act-card">'
            f'<span class="p-badge {p_cls}">{escape(str(a.get("priority", "")))}</span>'
            f'<div class="act-body"><strong>{escape(a.get("action", ""))}</strong> — {escape(a.get("effect", ""))}</div>'
            f'</div>'
        )
    return "\n".join(parts)


def render_decision_actions(actions):
    parts = []
    for a in actions:
        p_cls = a.get("priority", "p2").lower()
        parts.append(
            f'<div class="act-row">'
            f'<span class="p-badge {p_cls}">{escape(str(a.get("priority", "")))}</span>'
            f'<div class="act-content"><strong>{escape(a.get("action", ""))}</strong>'
            f'<div class="act-meta">预期效果：{escape(a.get("effect", ""))} | 所需资源：{escape(a.get("resource", ""))} | 周期：{escape(a.get("timeline", ""))}</div>'
            f'</div></div>'
        )
    return "\n".join(parts)


def render_not_do_list(items):
    parts = []
    for item in items:
        parts.append(
            f'<div class="notdo-item">'
            f'<div class="nd-icon">✕</div>'
            f'<div class="nd-body"><strong>{escape(item.get("item", ""))}</strong>'
            f'<div class="nd-reason">{escape(item.get("reason", ""))}</div>'
            f'</div></div>'
        )
    return "\n".join(parts)


def render_roadmap(phases):
    phase_cls = {"30天": "tl-now", "90天": "tl-mid", "半年": "tl-long"}
    parts = []
    for phase in phases:
        name = phase.get("phase", "")
        cls = phase_cls.get(name, "tl-now")
        actions = "".join(f"<li>{escape(a)}</li>" for a in phase.get("actions", []))
        parts.append(
            f'<div class="tl-phase {cls}"><h4>{escape(name)}</h4><ul>{actions}</ul></div>'
        )
    return "\n".join(parts)


def render_monitor_rows(items):
    rows = []
    for item in items:
        rows.append(
            f'<tr><td>{escape(item.get("signal", ""))}</td>'
            f'<td>{escape(item.get("focus", ""))}</td>'
            f'<td>{escape(item.get("source", ""))}</td>'
            f'<td>{escape(item.get("frequency", ""))}</td></tr>'
        )
    return "\n".join(rows)


def generate_report(data_json_path, output_path=None):
    with open(data_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    template = load_template()
    today = datetime.now().strftime("%Y-%m-%d")
    product = data.get("product", "未命名产品")

    replacements = {
        "{{TITLE}}": f"市场洞察报告 - {product}",
        "{{COVER_TITLE}}": escape(data.get("cover_title", f"市场洞察：{product}")),
        "{{COVER_LEAD}}": escape(data.get("cover_lead", f"基于多框架交叉分析的市场全景解读")),
        "{{DATE}}": today,
        "{{AUTHOR}}": data.get("author", "市场洞察大师 Skill"),
        "{{PURPOSE}}": data.get("purpose", "战略决策支持"),
        "{{EXECUTIVE_CONCLUSION}}": escape(data.get("executive_summary", {}).get("conclusion", "")),
        "{{TOP_ACTIONS}}": render_top_actions(data.get("executive_summary", {}).get("top_actions", [])),
        "{{MARKET_METRICS}}": render_market_metrics(data.get("market", {}).get("metrics", [])),
        "{{KEY_PLAYERS}}": render_key_players(data.get("market", {}).get("players", [])),
        "{{ENV_FACTORS}}": render_env_factors(data.get("environment", [])),
        "{{SWOT_S}}": render_swot_list(data.get("swot", {}).get("strengths", [])),
        "{{SWOT_W}}": render_swot_list(data.get("swot", {}).get("weaknesses", [])),
        "{{SWOT_O}}": render_swot_list(data.get("swot", {}).get("opportunities", [])),
        "{{SWOT_T}}": render_swot_list(data.get("swot", {}).get("threats", [])),
        "{{STRATEGY_COMBO}}": render_strategy_combo(data.get("swot", {}).get("strategy_combo", [])),
        "{{KANO_ROWS}}": render_kano_rows(data.get("kano", {}).get("items", [])),
        "{{INSIGHT_CARDS}}": render_insight_cards(data.get("insights", [])),
        "{{BUSINESS_JUDGMENT}}": render_business_judgment(data.get("business_judgment", {})),
        "{{DECISION_CONCLUSION}}": escape(data.get("decision", {}).get("conclusion", "")),
        "{{DECISION_ACTIONS}}": render_decision_actions(data.get("decision", {}).get("actions", [])),
        "{{NOT_DO_LIST}}": render_not_do_list(data.get("decision", {}).get("not_do", [])),
        "{{ROADMAP}}": render_roadmap(data.get("decision", {}).get("roadmap", [])),
        "{{MONITOR_ROWS}}": render_monitor_rows(data.get("monitor", [])),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)

    if not output_path:
        output_path = f"市场洞察报告_{product}_{today}.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"报告已生成：{output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python generate-report.py <data.json> [output.html]")
        print("\ndata.json 为分析结果的 JSON 文件")
        sys.exit(1)

    data_path = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    generate_report(data_path, output)
