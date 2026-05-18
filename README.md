# 产品经理 AI 提效超级实用指南

> 帮助 3-5 年产品经理从传统工作流升级为 AI 增强型产品经理的系统实战课程。

## 项目简介

本仓库是「产品经理 AI 提效超级实用指南」系列课程的配套资料库，包含课程计划、Skills 模板、参考文档和示例输出等完整内容。

课程核心理念：**不是学工具，是换工作流**。通过 Claude Code Skills、Cursor、Gemini 等 AI 工具，将市场洞察、需求调研、产品设计、项目管理等日常工作效率提升数倍。

## 课程体系

### 序章：认知升级
- 8 个真实场景：普通 PM 和 AI 增强型 PM 的差距
- 传统产品经理为何需要学 AI
- 谁适合学
- 课程交付物总览
- 课前准备：安装并配置 AI 工具

### 第 1 章：市场洞察
- Gemini Gem：业务资料一键变问题清单
- **市场洞察 Skills**：内置 SWOT / PESTEL / KANO 等方法论，输出叙事驱动的 HTML 报告
- 超强提示词 + PPT Skills：一键输出 BRD/MRD 文档
- Coze 实践：零代码做市场洞察 Agent

### 第 2 章：需求调研
- **需求整理 Skills**：把碎片化需求整理成结构化功能清单
- **竞品分析 Skills**：用 AI Skills 找机会点和差异化
- 用龙虾盯着竞品网站自动推送报告
- 对接产品接口：洞察用户反馈一键转化需求

### 第 3 章：产品设计
- 产品架构图工具盘点
- 原型设计：AI 工具盘点与实战
- 移动端 / Web 端原型设计（Cursor 实战）
- 业务流程图：Mermaid + 业务流程图系统
- 需求文档：结合自身业务写 PRD
- 需求评审大师核心 Skills

### 第 4 章：产品运营与管理
- 产品命名 Skills
- 验收测试：AI Agent 自动化测试
- 向上管理 / 向领导汇报 Skills
- 运营数据复盘 Skills

### 第 5 章：项目管理
- AI 项目导师：PMBOK 蒸馏成 Skill
- 综合项目管理 Skills
- 进度管理：生成项目甘特图和进度表格
- 沟通管理 Skills
- Claude Code 一键自动生成工单报表
- 基于 Claude 的项目复盘实操

### 第 6 章：其他日常工作
- Claude Code 高效搞定文件管理
- 龙虾做需求管理：飞书一句话新增需求
- 会议纪要：Gemini Gem 一键生成 PRD 等
- 日报助手：日报自动化的 2 个 AI 方法
- AI 效率工具实战：Markdown 转 Word/PDF
- **PPT 生成 Skills**：AI 一键生成幻灯片图片并合并为 PPTX/PDF

### 第 7 章：新天地
- 课程资料分享：内部资料与知识库
- 新认知：任何事都先考虑能否用 AI 替代或辅助
- 新兴趣：Vibe Coding 分享 N 个产品项目
- 新链接：常用 AI 工具 + 书籍 + KOL + 社群

## 已完成的 Skills

所有 Skill 统一采用 **JSON 数据 + Python 脚本 + HTML 模板** 架构：AI 分析结果整理为 JSON → `generate-report.py` 基于模板渲染 → 输出精美 HTML 报告。

### 🏪 市场洞察 Skill（market-insight）

位置：`第1章_市场洞察/02_市场洞察Skills：内置SWOT模型等方法论/skills/market-insight/`

内置 SWOT / PESTEL / KANO 等分析框架，覆盖市场全景、外部环境、内部能力、用户需求、业务判断五大维度，输出叙事驱动的 HTML 报告。

```
skills/market-insight/
├── SKILL.md              # Skill 主指令文件（7 章报告结构）
├── reference/            # 参考文档
│   ├── swot-guide.md     # SWOT 分析详细指南
│   ├── pestel-guide.md   # PESTEL 六维度详解
│   └── kano-guide.md     # KANO 需求分类指南
├── scripts/
│   └── generate-report.py  # 报告生成器（JSON → HTML）
└── assets/
    └── report-template.html  # HTML 报告模板
```

### 📋 BRD/MRD 一键输出大师（brd-mrd-master）

位置：`第1章_市场洞察/03_超强提示词+PPT Skills：一键输出BRD-MRD文档/skills/brd-mrd-master/`

一键输出专业级 BRD（商业需求文档）和/或 MRD（市场需求文档）HTML 报告。BRD 覆盖 10 章（执行摘要→成功指标），MRD 覆盖 7 章（市场机会→数据支撑），支持同时生成两份。

```
skills/brd-mrd-master/
├── SKILL.md              # Skill 主指令文件（BRD 10章 + MRD 7章 + 完整 JSON 结构）
├── reference/
│   ├── brd-guide.md              # BRD 编写方法论指南
│   ├── mrd-guide.md              # MRD 编写方法论指南
│   └── industry-analysis-framework.md  # 行业分析框架（TAM/SAM/SOM、波特五力等）
├── scripts/
│   └── generate-report.py  # 支持 BRD/MRD 两种文档类型的报告生成器
└── assets/
    └── report-template.html
```

### 📝 需求整理与管理 Skill（pm-requirements）

位置：`第2章_需求调研/01_把用户声音VoC变成需求池/skills/pm-requirements/`

将碎片化需求（聊天记录、会议纪要、老板口头需求、用户反馈）整理成结构化功能清单，支持增量更新和需求评分排序。

```
skills/pm-requirements/
├── SKILL.md              # Skill 主指令文件（初始化模式 + 增量更新模式）
└── references/
    └── scoring-rules.md  # 需求评分规则
```

### 🔍 竞品分析 Skill（pm-compete）

位置：`第2章_需求调研/02_竞品分析1：用AI Skills帮你找机会点和差异化/skills/pm-compete/`

横向对比竞品，输出功能对比矩阵、用户口碑对比、定位图、价值曲线（含 ERRC 行动框架）和机会点建议。

```
skills/pm-compete/
└── SKILL.md              # Skill 主指令文件（初始化分析 + 增量更新）
```

### 📊 运营数据复盘 Skill（ops-data-review）

位置：`第4章_产品运营与管理/04_运营数据复盘Skill/skills/ops-data-review/`

基于产品运营数据，运用 AARRR 全链路与 HEART 体验框架，输出结构化复盘报告，包含指标仪表盘、漏斗分析、留存分析、商业化分析、问题诊断与行动方案。

```
skills/ops-data-review/
├── SKILL.md              # Skill 主指令文件（12 个模块 + 完整 JSON 结构）
├── reference/
│   ├── data-analysis-framework.md  # 数据分析框架（AARRR、HEART、5-Why、同比环比等）
│   └── metrics-system.md           # 运营指标体系（北极星、留存、商业化、NPS 等）
├── scripts/
│   └── generate-report.py  # 运营数据复盘报告生成器
└── assets/
    └── report-template.html
```

### 📐 综合项目管理 Skill（project-management-master）

位置：`第5章_项目管理/02_综合项目管理Skills/skills/project-management-master/`

实战型项目管理 Skill（非 PMBOK 理论课），覆盖 WBS 任务分解、里程碑规划、资源分配、风险管理、质量保障、沟通管理全流程，输出可执行的项目管理报告。

```
skills/project-management-master/
├── SKILL.md              # Skill 主指令文件（10 个模块 + 完整 JSON 结构）
├── reference/
│   ├── agile-framework.md          # 敏捷项目管理框架（Scrum/看板/混合模式）
│   └── stakeholder-management.md   # 干系人管理（权力-利益矩阵、沟通策略）
├── scripts/
│   └── generate-report.py  # 项目管理报告生成器
└── assets/
    └── report-template.html
```

### 🎨 PPT 生成 Skill（pm-slide-deck）

位置：`第6章_其他日常工作/06_AI生成PPT Skill/skills/pm-slide-deck/`

将内容转化为专业幻灯片图片。通过豆包 Seedream 模型渲染图片，最终合并为 PPTX/PDF。

**4 个自定义维度**（5×7×5×3 = 525 种组合）：质感（clean / grid / organic / pixel / paper）、氛围（professional / warm / cool / vibrant / dark / neutral / macaron）、排版（geometric / humanist / handwritten / editorial / technical）、密度（minimal / balanced / dense）。

**17 种预设风格**（维度组合的最佳实践）：

| 预设 | 中文名称 | 适用场景 |
|------|----------|----------|
| blueprint | 技术蓝图 | 架构设计、系统设计 |
| chalkboard | 粉笔黑板 | 教育、教程 |
| corporate | 商务精英 | 投资人演示、商业提案 |
| minimal | 极简主义 | 高管简报 |
| sketch-notes | 手绘笔记 | 教育、教程 |
| hand-drawn-edu | 手绘教学 | 教育图表、流程说明 |
| watercolor | 水彩画 | 生活方式、健康 |
| dark-atmospheric | 暗黑氛围 | 娱乐、游戏 |
| notion | Notion 风格 | 产品演示、SaaS |
| bold-editorial | 大胆杂志风 | 产品发布、主题演讲 |
| editorial-infographic | 编辑信息图 | 技术解读、研究报告 |
| fantasy-animation | 奇幻动画 | 教育叙事 |
| intuition-machine | 直觉机器 | 技术文档、学术 |
| pixel-art | 像素艺术 | 游戏、开发者演讲 |
| scientific | 科学严谨 | 生物、化学、医学 |
| vector-illustration | 矢量插画 | 创意、儿童内容 |
| vintage | 复古怀旧 | 历史、文化遗产 |

```
skills/pm-slide-deck/
├── SKILL.md              # Skill 主指令文件（9 步工作流 + 确认门控）
├── scripts/
│   ├── merge-to-pptx.ts  # 幻灯片合并为 PowerPoint
│   └── merge-to-pdf.ts   # 幻灯片合并为 PDF
└── references/           # 参考文档
    ├── styles/           # 17 种预设风格详细规格
    ├── dimensions/       # 4 维度规格（质感/氛围/排版/密度）
    ├── config/           # EXTEND.md 偏好配置
    ├── analysis-framework.md    # 内容分析框架
    ├── outline-template.md      # 大纲结构模板
    ├── base-prompt.md           # 图片生成基础提示词
    ├── layouts.md               # 24 种布局图鉴
    ├── design-guidelines.md     # 排版与色彩设计指南
    ├── content-rules.md         # 内容准则
    ├── modification-guide.md    # 幻灯片修改工作流
    └── confirmation.md          # 各确认步骤的选项文案
```

### 通用使用方式

1. 在 Claude Code / Cursor 中激活对应 Skill
2. 提供产品/项目信息及业务背景
3. AI 自动完成框架分析，整理结果为 JSON 数据
4. 通过 `python3 generate-report.py data.json output.html` 生成 HTML 报告

## 参考资源

- `pm-skills-sc/`：PM Skills 参考仓库（65 项技能 + 36 个工作流），源自 [Osiris/pm-skills-sc](https://github.com/Osiris/pm-skills-sc)

## 仓库信息

- **组织**：shangbianai
- **可见性**：私有
- **用途**：课程内部资料，请勿外传
