# arch-diagram 演示提示词

录制视频前可直接复制使用，三个场景覆盖 Skill 的完整能力。

---

## 演示 1 — 模式 A：直接生成 HTML 架构图

**使用场景**：展示 Claude 不依赖任何外部 API，直接输出可交付的 HTML 文件。

**输入提示词：**

```
帮我画一张外卖 App 的产品架构图。

用户端：iOS App、Android App、商家管理后台（Web）
后端服务：API 网关、用户服务、订单服务、餐厅服务、配送调度服务
数据存储：MySQL、Redis
外部依赖：微信/支付宝支付、高德地图、短信服务

选 A 模式，直接生成 HTML 文件。
```

**预期效果**：Claude 生成 `waimai-architecture.html`，浏览器打开可看到深色科技风 SVG 图，支持导出 PNG/PDF。

---

## 演示 2 — 模式 B：仅生成提示词（无需 API）

**使用场景**：展示 Skill 的提示词优化能力，适合演示给没有 API 的学员。

**输入提示词：**

```
帮我画一张 SaaS 产品的多租户架构图。

模块包括：Web 前端、移动端 App、API Gateway、Auth 认证服务、
租户管理、核心业务服务、PostgreSQL、OSS 对象存储、Elasticsearch。

要深色科技风格。我现在没有 API Key，先给我生成提示词就好。
```

**预期效果**：Skill 输出中英双语提示词，可直接复制到 ChatGPT 或 Midjourney 使用。

---

## 演示 3 — 模式 C：直接调 API 生成图片

**使用场景**：展示接入 API 后的完整自动化流程，是最有冲击力的演示。

**输入提示词：**

```
帮我用 AI 图片模式画一张云原生微服务架构图。

包含：Kubernetes 集群（内有 API Gateway、用户服务、订单服务、
通知服务、Auth 服务）、PostgreSQL、Redis、Kafka、外部 CDN。
集群外有移动端 App 和 Web 平台作为入口。

深色科技风，直接调 API 生成图片。
```

**预期效果**：Skill 检测到 API Key 已配置，确认后调用 API，约 20 秒后输出 `architecture-diagram.png`（1536×1024 高清）。

---

## 录制建议

- **演示 1** 先跑，让观众看到从对话到 HTML 文件的完整过程（约 30 秒）
- **演示 2** 展示提示词质量，可打开 ChatGPT 粘贴验证效果
- **演示 3** 最后压轴，等待 API 返回时可以讲解背后的原理
