#!/usr/bin/env python3
"""
综合项目管理报告生成器
读取 report-template.html 模板，将项目管理分析数据填充后输出最终 HTML 报告。
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
        '<div class="act-card"><span class="p-badge {}">'
        '{}</span><div class="act-body">'
        '<strong>{}</strong> — {}</div></div>'.format(
            a.get("priority", "P2").lower(),
            e(a.get("priority", "")),
            e(a.get("action", "")),
            e(a.get("effect", ""))
        )
        for a in actions
    )


def _action_rows(actions, has_deadline=True, timeline_key="deadline"):
    rows = ""
    for a in actions:
        pri = a.get("priority", "P2").lower()
        action_text = e(a.get("action", ""))
        effect_text = e(a.get("expected_effect", ""))
        owner_text = e(a.get("owner", ""))
        if has_deadline:
            time_val = e(a.get(timeline_key, ""))
            meta = "负责人：{} | 截止：{}".format(owner_text, time_val)
        else:
            time_val = e(a.get(timeline_key, ""))
            meta = "负责人：{} | 周期：{}".format(owner_text, time_val)
        rows += (
            '<div class="act-row"><span class="p-badge {}">{}</span>'
            '<div class="act-content"><strong>{}</strong>'
            '<div class="act-meta">{} | {}</div>'
            '</div></div>'.format(pri, e(a.get("priority", "")), action_text, meta, effect_text)
        )
    return rows


def _long_term_actions(actions):
    rows = ""
    for a in actions:
        pri = a.get("priority", "P2").lower()
        action_text = e(a.get("action", ""))
        effect_text = e(a.get("expected_effect", ""))
        milestone_text = e(a.get("milestone", ""))
        meta = "关联里程碑：{}".format(milestone_text)
        rows += (
            '<div class="act-row"><span class="p-badge {}">{}</span>'
            '<div class="act-content"><strong>{}</strong>'
            '<div class="act-meta">{} | {}</div>'
            '</div></div>'.format(pri, e(a.get("priority", "")), action_text, meta, effect_text)
        )
    return rows


def _not_do(items):
    return "\n".join(
        '<div class="notdo-item"><div class="nd-icon">✕</div>'
        '<div class="nd-body"><strong>{}</strong>'
        '<div class="nd-reason">{}</div></div></div>'.format(
            e(i.get("item", "")),
            e(i.get("reason", ""))
        )
        for i in items
    )


def _metric_row(metrics):
    cards = ""
    for m in metrics:
        color = m.get("color", "")
        value = m.get("value", "")
        label = m.get("label", "")
        cards += (
            '<div class="metric"><div class="m-val {}">{}</div>'
            '<div class="m-label">{}</div></div>'.format(color, value, label)
        )
    return '<div class="metric-row">{}</div>'.format(cards)


def _data_table(cols, rows):
    if cols and isinstance(cols[0], (list, tuple)):
        pairs = cols
    else:
        pairs = [(h, h) for h in cols]
    th = "".join("<th>{}</th>".format(label) for label, _ in pairs)
    tr = ""
    for row in rows:
        tr += "<tr>" + "".join("<td>{}</td>".format(e(row.get(key, ""))) for _, key in pairs) + "</tr>"
    return '<table class="data-table"><thead><tr>{}</tr></thead><tbody>{}</tbody></table>'.format(th, tr)


def _section(num, title, desc, body):
    return (
        '<div class="s"><div class="s-head"><div class="s-num">{}</div>'
        '<h2>{}</h2><div class="s-desc">{}</div></div>{}</div>'.format(
            num, title, desc, body
        )
    )


def _styled_list(items):
    return '<ul class="styled-list">' + "".join("<li>{}</li>".format(e(i)) for i in items) + "</ul>"


def _insight_items(findings):
    rows = ""
    for f in findings:
        finding_text = e(f.get("finding", ""))
        data_text = e(f.get("data", ""))
        rows += (
            '<div class="ins-item"><div class="finding">{}</div>'
            '<div class="meta-line">依据：{}</div></div>'.format(finding_text, data_text)
        )
    return rows


def _verdict(label, text, actions):
    return (
        '<div class="verdict"><div class="label">{}</div>'
        '<div class="v-text">{}</div>'
        '<div class="top-actions">{}</div></div>'.format(label, text, _top_actions(actions))
    )


def _decision_box(conclusion):
    return (
        '<div class="decision-box"><div class="label">Decision · 决策建议</div>'
        '<div class="one-liner">{}</div></div>'.format(e(conclusion))
    )


def _tag_cls(val, high="高"):
    if val == high:
        return "tag-high"
    if val == "中":
        return "tag-mid"
    return "tag-low"


def _workload_badge(workload):
    if workload == "高":
        return "tag-high"
    if workload == "中":
        return "tag-mid"
    return "tag-low"


# ═══ 主构建函数 ═══

def _build_report(d):
    today = datetime.now().strftime("%Y-%m-%d")
    product = d.get("product", "未命名项目")
    parts = []

    # Cover
    period = d.get("period", "")
    parts.append(
        '<header class="cover"><div class="tag">PROJECT MANAGEMENT REPORT</div>'
        '<h1>{}</h1>'
        '<div class="lead">{}</div>'
        '<div class="meta-row"><span>{}</span><span>综合项目管理 Skill</span>'
        '<span>{}</span></div></header>'.format(
            e(d.get("cover_title", "项目管理：{}".format(product))),
            e(d.get("cover_lead", "")),
            today,
            e(period)
        )
    )

    # Module 0: 执行摘要
    es = d.get("executive_summary", {})
    overall = e(es.get("overall_evaluation", ""))
    findings_html = _insight_items(es.get("top_findings", []))
    parts.append(_verdict(
        "Executive Summary · 执行摘要",
        "{}<br><br>{}".format(overall, findings_html),
        es.get("top_actions", [])
    ))

    # Module 1: 项目全景
    po = d.get("project_overview", {})
    parts.append(_section("Module 01", "项目全景", "项目目标、范围、约束、成功标准",
        '<div class="hl-box hl-blue"><p><strong>项目目标</strong>：{}</p></div>'
        '<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">项目范围</h3>'
        '<p style="margin-bottom:20px">{}</p>'
        '<h3 style="margin:0 0 12px;font-size:15px;font-weight:700;color:var(--red)">约束条件</h3>'
        '{}'
        '<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">成功标准</h3>'
        '{}'.format(
            e(po.get("goal", "")),
            e(po.get("scope", "")),
            _styled_list(po.get("constraints", [])),
            _styled_list(po.get("success_criteria", []))
        )
    ))

    # Module 2: WBS 任务分解
    wbs = d.get("wbs", {})
    wbs_phases_html = ""
    for phase in wbs.get("phases", []):
        phase_name = e(phase.get("phase", ""))
        task_headers = [("任务","task"),("负责人","owner"),("工作量","effort"),("依赖","dependencies"),("优先级","priority"),("交付物","deliverable")]
        tasks_html = _data_table(task_headers, phase.get("tasks", []))
        wbs_phases_html += (
            '<div class="tl-phase tl-now"><h4>{}</h4>{}</div>'.format(phase_name, tasks_html)
        )
    parts.append(_section("Module 02", "任务分解（WBS）", "工作分解结构，拆解到可执行粒度（单任务 ≤ 3人天）",
        '<div class="timeline">{}</div>'.format(wbs_phases_html)
    ))

    # Module 3: 里程碑规划
    milestones = d.get("milestones", [])
    ms_headers = [("里程碑","milestone"),("目标日期","target_date"),("交付物","deliverable"),("依赖关系","dependencies"),("风险","risk_flag")]
    parts.append(_section("Module 03", "里程碑规划", "关键里程碑、依赖关系、时间线",
        _data_table(ms_headers, milestones)
    ))

    # Module 4: 资源分配
    ra = d.get("resource_allocation", {})
    team_headers = [("角色","role"),("姓名","name"),("投入比例","allocation"),("参与阶段","phases"),("工作负载","workload")]
    parts.append(_section("Module 04", "资源分配", "人力分配矩阵 + 资源负载分析",
        '<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">团队分配矩阵</h3>'
        '{}'
        '<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">资源负载分析</h3>'
        '<div class="hl-box hl-blue"><p>{}</p></div>'.format(
            _data_table(team_headers, ra.get("team", [])),
            e(ra.get("workload_analysis", ""))
        )
    ))

    # Module 5: 风险管理
    rm = d.get("risk_management", {})
    risk_cards = ""
    for r in rm.get("risks", []):
        cat = e(r.get("category", ""))
        risk_desc = e(r.get("risk", ""))
        prob = e(r.get("probability", ""))
        imp = e(r.get("impact", ""))
        mit = e(r.get("mitigation", ""))
        owner = e(r.get("owner", ""))
        prob_cls = _tag_cls(r.get("probability", ""))
        imp_cls = _tag_cls(r.get("impact", ""))
        risk_cards += (
            '<div class="risk-card"><div class="rc-head">'
            '<strong>{}风险</strong>：{}</div>'
            '<div class="rc-meta">概率：<span class="{}">{}</span> | '
            '影响：<span class="{}">{}</span> | 负责人：{}</div>'
            '<div class="rc-mit">应对措施：{}</div></div>'.format(
                cat, risk_desc, prob_cls, prob, imp_cls, imp, owner, mit
            )
        )
    parts.append(_section("Module 05", "风险管理", "风险登记册 + 应对策略",
        '<div class="risk-grid">{}</div>'.format(risk_cards)
    ))

    # Module 6: 质量保障
    qa = d.get("quality_assurance", {})
    parts.append(_section("Module 06", "质量保障", "质量标准 + 检查点 + 验收标准",
        '<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">质量标准</h3>'
        '{}'
        '<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">检查点</h3>'
        '{}'.format(
            _styled_list(qa.get("standards", [])),
            _data_table([("检查点","checkpoint"),("验收标准","criteria"),("检查方式","method"),("时机","timing")], qa.get("checkpoints", []))
        )
    ))

    # Module 7: 沟通管理
    comm = d.get("communication", {})
    sh_headers = [("干系人角色","role"),("姓名","name"),("利益","interest"),("权力","power"),("沟通策略","strategy")]
    parts.append(_section("Module 07", "沟通管理", "干系人矩阵 + 沟通计划",
        '<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">干系人矩阵</h3>'
        '{}'
        '<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">沟通计划</h3>'
        '{}'.format(
            _data_table(sh_headers, comm.get("stakeholders", [])),
            _data_table([("会议","meeting"),("频率","frequency"),("参与者","participants"),("目的","purpose")], comm.get("plan", []))
        )
    ))

    # Module 8: 进度跟踪
    pt = d.get("progress_tracking", {})
    alerts_html = ""
    for al in pt.get("alerts", []):
        sev = al.get("severity", "中")
        sev_cls = _tag_cls(sev)
        alerts_html += (
            '<div class="risk-card"><div class="rc-head">'
            '<strong>预警</strong>：{}</div>'
            '<div class="rc-meta">严重程度：<span class="{}">{}</span></div>'
            '<div class="rc-mit">{}</div></div>'.format(
                e(al.get("signal", "")), sev_cls, e(sev), e(al.get("detail", ""))
            )
        )
    parts.append(_section("Module 08", "进度跟踪", "偏差分析 + 预警信号",
        '<div class="hl-box hl-blue"><p><strong>整体状态</strong>：{}</p></div>'
        '<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700;color:var(--red)">预警信号</h3>'
        '<div class="risk-grid">{}</div>'
        '<h3 style="margin:20px 0 12px;font-size:15px;font-weight:700">改进建议</h3>'
        '{}'.format(
            e(pt.get("overall_status", "")),
            alerts_html,
            _styled_list(pt.get("recommendations", []))
        )
    ))

    # Module 9: 行动方案
    ap = d.get("action_plan", {})
    short_html = _action_rows(ap.get("short_term", []), has_deadline=True, timeline_key="deadline")
    mid_html = _action_rows(ap.get("mid_term", []), has_deadline=False, timeline_key="timeline")
    long_html = _long_term_actions(ap.get("long_term", []))
    parts.append(_section("Module 09", "行动方案", "短期 / 中期 / 长期行动 + NOT TO DO",
        '<h3 style="margin:0 0 12px;font-size:15px;font-weight:700">短期行动</h3>'
        '<div class="act-list">{}</div>'
        '<h3 style="margin:24px 0 12px;font-size:15px;font-weight:700">中期行动</h3>'
        '<div class="act-list">{}</div>'
        '<h3 style="margin:24px 0 12px;font-size:15px;font-weight:700">长期行动</h3>'
        '<div class="act-list">{}</div>'
        '<h3 style="margin:24px 0 12px;font-size:15px;font-weight:700;color:var(--red)">NOT TO DO</h3>'
        '{}'.format(short_html, mid_html, long_html, _not_do(ap.get("not_to_do", [])))
    ))

    # Footer
    parts.append(
        '<div class="report-footer"><p>由「综合项目管理大师」生成 · {}</p>'
        '<p style="margin-top:4px;">本报告基于项目信息与AI分析生成，关键数据建议结合实际情况确认</p></div>'.format(today)
    )
    return "\n".join(parts), "项目管理报告 - {}".format(product)


# ═══ 主入口 ═══

def generate_report(data_json_path, output_path=None):
    with open(data_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    template = load_template()
    content, title = _build_report(data)

    html = template.replace("{{TITLE}}", title).replace("{{CONTENT}}", content)

    if not output_path:
        today = datetime.now().strftime("%Y-%m-%d")
        product = data.get("product", "未命名项目")
        output_path = "项目管理报告_{}_{}.html".format(product, today)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("报告已生成：{}".format(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python generate-report.py <data.json> [output.html]")
        print("\ndata.json 为项目管理分析结果的 JSON 文件")
        sys.exit(1)

    data_path = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    generate_report(data_path, output)
