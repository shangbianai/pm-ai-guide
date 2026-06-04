# Product Architecture Diagram Templates

Use these as starting points. Replace labels with the product's real modules. For user-facing deliverables, prefer the HTML patterns over Mermaid.

## HTML: Polished Layered Architecture

Create a standalone HTML file with this structure:

- `body` uses a neutral app background.
- `.toolbar` contains type tabs and export buttons.
- `#captureArea` is the only exported region.
- `.arch-title` is a full-width title bar.
- `.layer` rows are horizontal bands with a left `.layer-label` and right `.layer-content`.
- `.module` items are compact boxes with readable text.
- `.side-rail` may show monitoring/governance/DevOps as a vertical cross-cutting rail.

Minimum controls:

- `保存为 PNG`
- `保存为 JPG`
- A status text that reports success/fallback errors.

Use [html-export.md](html-export.md) for the export function.

## HTML: Type Variants

When demoing or offering alternatives, use one page with tabs:

- `分层平台图`: top-down product/platform layers.
- `业务关系图`: business/application/data/technology domains with dashed arrows.
- `能力地图`: capability groups in a matrix.
- `AI数据架构`: experience/service/model/data/platform layers.
- `C4容器图`: users, channels, services, datastores, external systems.

Each tab should keep the same export buttons and reuse `#captureArea`.

## Mermaid: Layered Platform Diagram

```mermaid
flowchart TB
  subgraph L1["用户/渠道层"]
    U1["用户 App"]
    U2["运营 Web"]
    U3["开放 API"]
  end
  G["统一接入网关<br/>认证 / 路由 / 限流 / 协议转换"]
  subgraph L2["应用层"]
    A1["订单管理"]
    A2["商品管理"]
    A3["统计报表"]
  end
  subgraph L3["业务能力平台"]
    C1["订单中心"]
    C2["调度中心"]
    C3["消息中心"]
    C4["规则中心"]
  end
  subgraph L4["支撑平台"]
    S1["会员中心"]
    S2["权限中心"]
    S3["地图服务"]
    S4["搜索中心"]
  end
  subgraph L5["数据与技术平台"]
    D1["主数据"]
    D2["数据仓库"]
    T1["缓存/消息队列"]
    T2["监控/日志/发布"]
  end
  L1 --> G --> L2 --> L3
  L3 --> L4
  L3 --> L5
```

## Mermaid: Business/Application/Data/Technology Map

```mermaid
flowchart TB
  subgraph B["业务架构"]
    B1["商业模式"] -->|"细化"| B2["价值流"] -->|"细化"| B3["业务流程"]
    B4["组织/角色"] -.->|"实施"| B3
    B5["业务能力"] -.->|"支撑"| B3
  end
  subgraph A["应用架构"]
    A1["应用结构"] <-->|"协作"| A2["应用交互"] -->|"实现"| A3["应用服务"]
  end
  subgraph D["数据架构"]
    D1["数据模型"]
    D2["数据技术"] -->|"实现"| D1
  end
  subgraph T["技术架构"]
    T1["技术组件"] -->|"实现"| T2["软件部署"]
    T3["基础设施"] -.->|"实现"| T2
  end
  A3 -.->|"支撑"| B5
  D1 -.->|"支撑"| A3
  T2 -.->|"支撑"| A1
```

## Mermaid: AI/Data Product Layered Diagram

```mermaid
flowchart TB
  Title["智能产品整体架构"]
  subgraph E["展现层"]
    E1["评估页面"]
    E2["智能体对话"]
    E3["可视化看板"]
  end
  subgraph S["服务层"]
    S0["业务智能体"]
    S1["评分服务"]
    S2["报告生成"]
    S3["策略推荐"]
  end
  subgraph M["建模分析层"]
    M1["业务风险模型"]
    M2["评分模型"]
    M3["政策匹配模型"]
    M4["LLM Agent"]
  end
  subgraph D["数据处理层"]
    D1["结构化处理"]
    D2["非结构化处理"]
    D3["标签系统"]
    D4["特征工程"]
  end
  subgraph P["平台层"]
    P1["模型训练平台"]
    P2["向量/图谱平台"]
    P3["数据仓库"]
    P4["MLOps/监控"]
  end
  Title --> E --> S --> M --> D --> P
```

## HTML/SVG Visual Style Guidance

When making a polished screenshot-like visual:

- Use a neutral canvas, 1px borders, 4-8px radius, and vivid but professional fills by layer.
- Use dashed boundaries for architecture domains and solid boxes for concrete modules.
- Use side rails for cross-cutting observability, governance, security, and DevOps.
- Keep color semantic: business warm, application blue, risk/service red, model orange, data pink/purple/green, technology yellow/gray, governance dark blue.
- Avoid decorative gradients, icons that do not add meaning, and overly rounded cards.
- Avoid one-note palettes. A product architecture poster may be colorful, but each color should encode layer/domain meaning.

## Final Response Pattern

When returning a diagram, include:

1. Diagram artifact or code.
2. `图型选择`: one sentence naming the type and why.
3. `阅读方式`: 2-4 bullets explaining top-down or left-right logic.
4. `假设`: only if the source material had gaps.
