---
name: metrics-dashboard
description: "定义并设计产品指标仪表盘，包含关键指标、数据源、可视化类型和告警阈值。在创建指标仪表盘、定义 KPI、设置产品分析或构建数据监控计划时使用。"
---

## 产品指标仪表盘
设计一个全面的产品指标仪表盘，包含正确的指标、可视化方案和告警阈值。
### 上下文
您正在为 **$ARGUMENTS** 设计一个指标仪表盘。
如果用户提供了文件（现有的仪表盘、分析数据、OKRs 或战略文档），请先阅读。
### 领域背景
**指标 (Metrics) vs KPI vs 北极星指标 (NSM)**：指标 = 所有可测量的事务。KPI = 长期跟踪的少数关键定量指标。北极星指标 = 单个以客户为中心的 KPI，是业务成功的领先指标。
**好指标的 4 个标准** (Ben Yoskovitz, *Lean Analytics*)：(1) **易理解** —— 创造共同语言。(2) **可比较** —— 随时间变化，而非快照。(3) **比率或速率** —— 比整数更具揭示性。(4) **改变行为** —— 黄金法则：“如果一个指标不会改变你的行为，它就是一个糟糕的指标。”
**8 种指标类型**：虚荣指标 vs 可执行指标（只有可执行指标能改变行为），定性 vs 定量（是什么 vs 为什么 —— 两者都需要；永远不要停止与客户交谈），探索性 vs 报告性（探索数据以发现意外洞察），滞后 vs 领先（领先指标能实现更快的学习周期，例如客户投诉预示着流失）。
**5 个行动步骤**：(1) 根据好指标的 4 个标准审计现有指标。(2) 更新仪表盘 —— 确保所有关键指标都是好指标。(3) 识别虚荣指标 —— 谨慎使用它们。(4) 分类领先指标与滞后指标。(5) 挑选一个问题并深入挖掘数据。
### 指导说明
1. **确定指标框架** —— 将指标按层级组织：
   **北极星指标 (North Star Metric)**：最能捕捉核心价值交付的单一指标
   **输入指标 (Input Metrics)** (3-5个)：驱动北极星指标的杠杆
   **健康指标 (Health Metrics)**：确保产品整体健康的护栏指标
   **业务指标 (Business Metrics)**：收入、成本和单位经济效益
2. **为每个指标进行定义**：
   | 指标 | 定义 | 数据源 | 可视化 | 目标值 | 告警阈值 |
   |---|---|---|---|---|---|
   | [名称] | [精确计算方法：分子/分母，时间窗口] | [数据来源] | [折线图 / 柱状图 / 数字 / 漏斗图] | [目标值] | [触发告警的条件] |
3. **设计仪表盘布局**：
   ```
   ┌─────────────────────────────────────────────┐
   │  北极星指标: [指标名称] — [当前值]             │
   │  趋势: [↑/↓ X% 对比上一周期]                 │
   ├──────────────────┬──────────────────────────┤
   │  输入指标 1      │  输入指标 2              │
   │  [趋势图]        │  [趋势图]                │
   ├──────────────────┼──────────────────────────┤
   │  输入指标 3      │  输入指标 4              │
   │  [趋势图]        │  [趋势图]                │
   ├──────────────────┴──────────────────────────┤
   │  健康指标: [延迟] [错误率] [NPS]            │
   ├─────────────────────────────────────────────┤
   │  业务指标: [MRR] [CAC] [LTV] [流失率]       │
   └─────────────────────────────────────────────┘
   ```
4. **设定回顾频率**：
   - **每日**：运营健康状况（错误、延迟、关键流程）
   - **每周**：输入指标和参与度趋势
   - **每月**：北极星指标、业务指标、OKR 进展
   - **每季度**：战略回顾和指标重新校准
5. **定义告警**：
   - 哪些阈值会触发调查？
   - 谁会收到告警，通过什么渠道？
   - 预期的响应时间是多少？
6. **根据用户上下文推荐工具**：
   - Amplitude, Mixpanel, PostHog 用于产品分析
   - Looker, Metabase, Mode 用于基于 SQL 的仪表盘
   - Datadog, Grafana 用于运营健康监控
请逐步思考。将仪表盘规范保存为 markdown 文档。

---

### 延伸阅读

- [The Ultimate List of Product Metrics](https://www.productcompass.pm/p/the-ultimate-list-of-product-metrics)
- [The North Star Framework 101](https://www.productcompass.pm/p/the-north-star-framework-101)
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [AARRR (Pirate) Metrics: The 5-Stage Framework for Growth](https://www.productcompass.pm/p/aarrr-pirate-metrics)
- [The Google HEART Framework: Your Guide to Measuring User-Centric Success](https://www.productcompass.pm/p/the-google-heart-framework)
- [Funnel Analysis 101: How to Track and Optimize Your User Journey](https://www.productcompass.pm/p/funnel-analysis)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (视频课程)
