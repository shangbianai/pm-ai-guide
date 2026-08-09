---
name: create-user-journey-map
description: 把用户访谈、客服反馈、行为数据、观察记录或业务资料整理成有证据状态、情绪曲线、体验断点和产品机会的用户体验旅程地图，并输出结构化 JSON、交互式单文件 HTML、PNG，以及需要时的可编辑 Excel。用户提到用户体验地图、用户旅程地图、Customer Journey Map、体验断点、情绪曲线、触点分析、用户研究可视化或直播演示体验分析时使用。
---

# 用户体验旅程地图

## 交付物

必须输出：

- `user-journey.json`：唯一结构化数据源。
- `user-journey.html`：表格式交互地图，点击阶段查看证据、痛点和机会。

Chrome 可用时同时输出：

- `user-journey.png`：适合 PPT、直播和汇报。

用户需要协作编辑或研究底稿时，再输出：

- `user-journey.xlsx`：可编辑表格、情绪曲线和机会优先级图。

## 工作流

1. 锁定一个具体用户、一个具体场景和一个从开始到结束的核心任务。
2. 读取研究材料，将完整任务拆分为 5—7 个真实用户阶段；不要按公司部门或功能菜单拆分。
3. 每阶段填写目标、动作、触点、想法、情绪、痛点、证据状态、证据内容和产品机会。
4. 严格区分 `已验证事实`、`合理推断`、`待验证假设`。没有证据时保留待验证，不得编造。
5. 情绪使用 `-2` 至 `2`；机会优先级默认使用 `影响 × 频率 ×（6－当前解决程度）`。
6. 按 [schema.md](references/schema.md) 生成 JSON。
7. 运行：

```bash
python3 scripts/render_user_journey.py \
  --input /absolute/path/user-journey.json \
  --output /absolute/path/user-journey.html
```

8. 需要 PNG 时运行：

```bash
python3 scripts/capture_html.py \
  --input /absolute/path/user-journey.html \
  --output /absolute/path/user-journey.png \
  --width 1440 --height 1300
```

9. 需要 Excel 时使用表格工具，以相同 JSON 为数据源创建可编辑表格和两张图：情绪曲线、机会优先级。
10. 最终检查：阶段完整、情绪有依据、痛点与机会对应、假设未伪装成事实、关键断点和下一步验证明确。

## 判断标准

- 用户旅程地图关注“用户如何体验”，业务流程图关注“业务如何运行”，不要混淆。
- 一张地图只覆盖一个用户和一个核心任务。
- 情绪最低点不自动等于最高优先级。
- 产品机会先描述应改善的用户结果，不直接跳到具体按钮或页面。
- 最终必须给出 3 个关键体验断点和 5 个下一轮研究问题。
