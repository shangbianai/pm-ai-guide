---
name: create-product-mind-map
description: Turn meeting notes, long documents, research, product plans, requirements, brainstorming, or fragmented information into a structured product-manager mind map. Use when the user asks for 思维导图、脑图、信息梳理图、知识结构图、Markdown mind map, or wants interactive HTML, Markdown source, JSON hierarchy, and PNG output.
---

# 产品思维导图生成

基于 MIT 开源项目 [Markmap](https://github.com/markmap/markmap) 将结构化 Markdown 转成可缩放、可折叠的交互式思维导图。

## 输出原则

1. 先写中心问题，不直接堆主题词。
2. 一级分支保持同一抽象层级，通常控制在 3—7 个。
3. 每个节点只表达一个观点；长解释移到下一层。
4. 区分 `事实`、`判断`、`假设`、`待确认` 和 `行动`。
5. 产品场景优先包含：背景、用户、问题、方案、范围、风险、行动。
6. 不从原始材料中虚构责任人、日期、数据或决策。

## 工作流

1. 读取输入材料并去重、合并同义信息。
2. 生成层级清楚的 Markdown：

```markdown
# 中心问题
## 用户与场景
### 目标用户
- 具体内容
## 问题与证据
### 关键问题
- [事实] 已知信息
- [待确认] 缺失信息
## 产品行动
- [行动] 下一步
```

3. 保存为 `mind-map.md`。
4. 运行：

```bash
python3 scripts/render_mind_map.py mind-map.md --output-dir ./mind-map-output --title "思维导图标题"
```

5. 验收 `mind-map.html`、`mind-map.png`、`mind-map.json` 和 Markdown 源文件。

## 验收

- 一级分支是否回答中心问题。
- 是否存在重复分支或层级混乱。
- 事实与建议是否被混写。
- 最深层节点是否能用于讨论或行动。
- HTML 是否能缩放、折叠并离线打开。
