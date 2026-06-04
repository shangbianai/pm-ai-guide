# Codex 化产品架构图 Skill

这是面向 Codex 的产品架构图生成 skill，用于把产品描述、PRD、模块清单或截图风格要求，转成可直接用于汇报的分层产品架构图。

## 能做什么

- 自动判断产品架构图类型：分层平台图、业务关系图、能力地图、AI 数据架构、C4 容器图等。
- 默认生成绚烂的 HTML/SVG 分层架构图，而不是只输出 Mermaid。
- HTML 产物内置 `保存为 PNG` 和 `保存为 JPG`。
- 内置产品架构图方法论：用户体验五层面、C4、业务/应用/数据/技术域、ArchiMate 分层、能力地图。
- 支持在用户明确要求时生成 imagegen / Image 2 绘图提示词。

## 安装

复制整个目录到 Codex skills 目录：

```bash
cp -R codex-product-architecture-diagrams ~/.codex/skills/product-architecture-diagrams
```

然后在 Codex 中使用：

```text
用 $product-architecture-diagrams 帮我画一个智能风控产品架构图，包含用户端、运营端、风控评分、报告生成、模型训练、标签系统、数据仓库、监控运维。
```

## Demo

示例文件在 `examples/`：

- `product-architecture-diagrams-demo.html`
- `product-architecture-diagrams-demo-layered.png`
- `product-architecture-diagrams-demo-ai.png`
