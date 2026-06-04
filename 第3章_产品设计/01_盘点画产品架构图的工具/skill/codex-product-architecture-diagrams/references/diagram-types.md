# Product Architecture Diagram Types

Choose the diagram type by audience and question. Hybrid diagrams are allowed, but name the primary type.

## 1. Layered Product Platform Diagram

Best for: screenshot-like platform architecture, SaaS/product backend planning, feature/module inventory, and the default "产品架构图" request.

Typical layers:

- 用户/渠道层: Web, App, mini program, open API, admin console.
- 接入/网关层: API gateway, auth, routing, throttling, protocol conversion.
- 应用层: product-facing systems and business applications.
- 业务能力层: stable core capabilities.
- 支撑平台层: reusable internal platforms and common services.
- 数据层: master data, operational DB, data warehouse/lake, feature store, model data.
- 技术平台层: infra, middleware, DevOps, observability, security.
- 治理/运维: cross-cutting or side rail.

Use when the user wants a full product architecture like the first and third screenshots. For this skill, this type should usually be rendered as a polished HTML/SVG chart, not only Mermaid.

## 2. Business/Application/Data/Technology Relationship Map

Best for: explaining how strategy, business process, application services, data, and technology fit together.

Domains:

- 业务架构: business model, value flow, business process, org/capability.
- 应用架构: application structure, application interaction, application service.
- 数据架构: data model, data technology, data governance.
- 技术架构: technical components, deployment, infrastructure.

Use sparse boxes and verb-labeled dashed arrows. This matches the second screenshot.

## 3. Capability Map

Best for: product planning, roadmap scope, platform boundaries, buy/build decisions.

Structure:

- Rows by capability group: core, support, governance, intelligence, data.
- Columns by domain or lifecycle: acquire, serve, operate, analyze, grow.
- No heavy arrows unless showing dependency.

Use when the user provides many functions but no process.

## 4. Value Flow / Business Flow Architecture

Best for: business stakeholders, explaining how value is created end to end.

Structure:

- Business model -> value stream -> business process -> capabilities -> products/services.
- Add supporting data/tech platforms below or beside the flow.

Use when the user says "业务架构", "商业模式", "价值流", "端到端流程".

## 5. Swimlane Product Architecture

Best for: multi-role collaboration or cross-system workflows.

Lanes:

- User/role lanes: customer, operator, admin, partner.
- System lanes: frontend, gateway, business service, data service, external platform.

Use when the key question is "who does what with which system".

## 6. C4-Style Product/System View

Best for: engineering alignment and progressive technical detail.

Levels:

- Context: users, external systems, the product boundary.
- Container: apps/services/datastores.
- Component: major modules inside a service/product.
- Code: only when specifically requested.

Use when the user asks for technical architecture, system boundaries, service dependencies, or implementation planning.

## 7. AI/Data Product Architecture

Best for: AI agents, model platforms, analytics products, risk engines, recommendation, search.

Common layers:

- Experience layer: user-facing app/pages/dialogue/visualization.
- Orchestration/service layer: agent, workflow, API, report generation, policy engine.
- Modeling/analysis layer: models, rules, feature engineering, training/evaluation.
- Data processing layer: structured/unstructured processing, labeling, feature store.
- Platform layer: LLM, AutoML, vector DB, warehouse/lake, MLOps, monitoring.

Use when the product depends on data/model intelligence like the fourth screenshot.

## 8. Presentation Architecture Poster

Best for: direct reuse in slides, reports, WeChat articles, sales materials, internal reviews.

Structure:

- A strong title bar.
- 5-7 horizontal layer bands.
- Left labels for layers.
- Center module groups with vivid fills.
- Optional right side rail for monitoring/governance/DevOps.
- Export buttons in HTML for PNG/JPG.

Use when the user says "像截图", "绚烂", "好看", "可下载图片", "HTML", "JPG", "PNG", or wants a diagram that can be pasted into a document.

## Selection Heuristic

- If the user gives screenshots, mirror the closest visual form first.
- If the user gives modules only, make a layered platform diagram and render it in HTML unless they ask for Mermaid.
- If the user gives business concepts and relationships, make a relationship map.
- If the user gives user roles/processes, make a swimlane or value-flow diagram.
- If the user gives services/infra, make a C4/container or technical layered diagram.
- If the user says "产品架构图" with no extra detail, produce a polished layered HTML chart plus a short note about two alternative views.
