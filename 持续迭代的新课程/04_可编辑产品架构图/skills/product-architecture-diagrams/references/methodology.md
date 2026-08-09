# Product Architecture Diagram Methodology

Use this reference when the user asks for a method-driven product architecture diagram or when the source material is messy.

## Source Methodologies To Cite

- **Jesse James Garrett, The Elements of User Experience**: use the planes from abstract to concrete: strategy, scope, structure, skeleton, surface. In product architecture diagrams, map them to `business goal -> capability scope -> information/function structure -> interaction/process skeleton -> channels/UI`.
- **C4 model**: use progressive abstraction: system context, containers, components, code. In product architecture diagrams, use this as `external actors -> products/apps/services -> modules/capabilities -> implementation units`.
- **Enterprise architecture domains, common in TOGAF-style practice**: business, data, application, technology. Use this to avoid drawing only functions while forgetting data and infrastructure.
- **ArchiMate layered thinking**: business, application, technology layers with services/interfaces/realization relationships. Use this to name relationships such as `serves`, `realizes`, `supports`, and `accesses data`.
- **Capability mapping**: decompose the product into stable business capabilities rather than only current org teams or database tables. Capabilities should describe what the product must be able to do.

Useful public links:

- Garrett: http://www.jjg.net/elements/
- C4 model: https://c4model.com/
- The Open Group TOGAF: https://www.opengroup.org/togaf
- The Open Group ArchiMate: https://www.opengroup.org/archimate-forum/archimate-overview

## Decomposition Ladder

Use this ladder from abstract to concrete:

1. **Business intent**: business model, strategic goal, value proposition, key user/job.
2. **Experience/channel**: user roles, channels, touchpoints, surface products, admin portals.
3. **Business capabilities**: order, payment, risk control, dispatch, content, search, membership, analytics.
4. **Application services**: services/apps that expose or orchestrate capabilities.
5. **Data capabilities**: data model, master data, analytics, features, labels, warehouse/lake, governance.
6. **Technology platform**: gateway, identity, workflow, message queue, cache, storage, infra, AI/model platform.
7. **Operations/governance**: monitoring, logging, alerting, configuration, deployment, security, compliance.

## Architecture Questions

Ask or infer:

- Who are the external actors and product channels?
- What value flow or business process does the product serve?
- Which capabilities are core business differentiators, and which are support/platform capabilities?
- Which application services realize the capabilities?
- What data is produced, consumed, governed, or analyzed?
- What technical platforms enable reuse and reliability?
- What cross-cutting governance is needed: security, observability, DevOps, compliance, permissions?
- What is intentionally out of scope?

## Relationship Vocabulary

Use concise relationship verbs:

- `细化`: business model to value flow, value flow to process.
- `实现`: application/service realizes a capability; technology realizes deployment.
- `支撑`: platform supports business/application capabilities.
- `协作`: peer modules coordinate.
- `沉淀`: process or interaction produces data assets.
- `消费`: services consume models/data/API capabilities.
- `治理`: security/monitoring/configuration controls services.
- `反馈`: analytics or risk results feed product/business decisions.

## Common Mistakes To Avoid

- Listing every feature without showing architecture relationships.
- Mixing business capabilities, UI pages, APIs, and databases in the same undifferentiated row.
- Giving a capability matrix meaningful-looking row and column headers while the cells do not represent their intersections. Test a row by reading it left to right and a column by reading it top to bottom; both directions must remain semantically valid.
- Drawing org structure as product architecture unless the request is explicitly organizational.
- Overusing microservice names when the audience needs product capabilities.
- Hiding data, monitoring, permissions, or DevOps even when they are critical to the product.
- Using arrows everywhere without verbs; if the relationship cannot be named, remove or regroup it.
