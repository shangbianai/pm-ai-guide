---
name: prioritize-assumptions
description: "使用影响 × 风险 (Impact × Risk) 矩阵对假设进行优先级排序，并为每个假设建议实验方案。在筛选假设列表、决定优先测试项或应用假设优先级画布时使用。"
---

## 假设优先级排序
使用影响 × 风险矩阵筛选假设，并建议针对性的实验方案。
### 上下文
您正在协助为 **$ARGUMENTS** 进行假设优先级排序。
如果用户提供了包含假设或研究数据的文件，请先阅读。
### 领域背景
**ICE** 非常适合假设优先级排序：影响 (Impact = 机会分数 × 客户数量) × 信心 (Confidence, 1–10) × 难易度 (Ease, 1–10)。机会分数 (Opportunity Score) = 重要性 × (1 − 满意度)，归一化为 0–1 (Dan Olsen)。**RICE** 则将影响分为触达率 (Reach) × 影响 (Impact)。有关完整公式和模板，请参阅 `prioritization-frameworks` 技能。
### 指导说明
用户将提供待排序的假设列表。请应用以下框架：
1. **针对每个假设**，从两个维度进行评估：
   - **影响**：验证此假设所创造的价值以及受影响的客户数量（在 ICE 中：影响 = 机会分数 × 客户数量）
   - **风险**：定义为 (1 - 信心) × 工作量
2. **使用影响 × 风险矩阵对每个假设进行分类**：
   - **低影响，低风险** → 暂缓测试，直到处理完更高优先级的假设
   - **高影响，低风险** → 直接实施（低风险，高回报）
   - **低影响，高风险** → 拒绝该想法（不值得投入）
   - **高影响，高风险** → 设计实验进行测试
3. **对于需要测试的每个假设**，建议一个满足以下条件的实验：
   - 以最小的投入实现最大的验证学习
   - 测量实际行为，而非观点
   - 具有明确的成功指标和阈值
4. **展示结果**为优先级矩阵或表格。
请逐步思考。如果输出内容较多，请保存为 markdown 文件。

---

### 延伸阅读

- [Assumption Prioritization Canvas: How to Identify And Test The Right Assumptions](https://www.productcompass.pm/p/assumption-prioritization-canvas)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (视频课程)
