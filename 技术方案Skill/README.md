# 技术方案 Skill · proposal-master

> 配套 Claude Code Skill：`proposal-master`（长技术方案生成器）

---

## 这个 Skill 解决什么问题

引导用户从零开始生成完整的长篇技术方案文档（.docx）——项目申报书、技术方案书、投标文件、可研报告、白皮书等。覆盖从需求澄清、大纲生成、任务拆解、分模块写作、图片管理、内容审查到 docx 合成排版全流程，不限于特定行业。

只要需求指向「结构化长文档写作」，无论用什么词描述（写方案 / 写申报书 / 写标书 / 做可研报告 / docx 排版），都会触发这个 Skill。

---

## 核心特点

- **需求澄清门禁**：缺关键信息（文档类型 / 用途受众 / 主题 / 篇幅格式）时不直接生成，先问清楚
- **8 阶段逐阶段闸门**：每阶段产出后停下等用户确认，不一次性自动跑完
- **选项驱动**：有限选项一律走原生选择控件，不让用户打字
- **人机分工透明**：明确 AI 能做什么、人必须定什么（数据核实、商务报价、最终拍板）
- **docx 排版自动化**：pandoc + 6 个 Python 脚本，处理中文字体、三线表、目录、封面、引号、编号等坑

---

## 文件说明

```
技术方案Skill/
├── README.md              ← 本文件
├── SKILL.md               ← Skill 主指令（8 阶段工作流 + 核心原则）
├── scripts/               ← docx 合成排版脚本（依赖 python-docx）
│   ├── make_reference.py      生成带中文字体的 reference.docx
│   ├── strip_reference.py     从已有 docx 提取样式
│   ├── fix_quotes.py          ASCII 引号 → 中文配对引号
│   ├── renumber_h3.py         统一 H3 编号
│   ├── apply_postprocess.py   docx 后处理（图片 / 表格 / 字体）
│   └── add_cover.py           把封面插到目录之前
├── references/            ← 参考文档（排版阶段必读）
│   ├── formatting-spec.md     GB/T 9704 公文格式规范
│   ├── pandoc-guide.md        Pandoc 中文转换 8 类坑与对策
│   └── examples.md            各阶段交互范式 + 常见问题速查
└── evals/
    └── evals.json             Skill 质量评测用例
```

> 这些脚本已封装好中文字体(eastAsia)、三线表、图片行高、引号、标题编号等坑的正确处理。**直接调用，不要在会话里另写一套。**

---

## 安装 Skill

整个 Skill 目录需**完整安装**（含 `scripts/` 和 `references/`，`SKILL.md` 会引用它们）。
注意：安装到本地的目录名必须是 `proposal-master`（与 `SKILL.md` 里 `name` 一致），不是「技术方案Skill」。

**Windows PowerShell：**
```powershell
$dst = "$env:USERPROFILE\.claude\skills\proposal-master"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Path 技术方案Skill\* -Destination $dst -Recurse -Force
```

**macOS / Linux：**
```bash
mkdir -p ~/.claude/skills/proposal-master
cp -R 技术方案Skill/* ~/.claude/skills/proposal-master/
```

安装后重启 Claude Code，输入 `/proposal-master` 触发。

---

## 使用方式

直接输入触发，Skill 会逐阶段引导你完成：

```
/proposal-master
```

Skill 先问清楚文档类型、用途受众、主题、篇幅格式，然后逐阶段推进：

> 阶段 0 需求澄清 → 1 大纲生成 → 2 任务拆解 → 3 写作提示词 → 4 分模块写作 → 5 图片管理 → 6 内容审查 → 7 文档合成 → 8 排版收尾

每个阶段产出后停下等你确认，可随时暂停、从任意阶段切入（已有大纲直接进阶段 2、已有素材进阶段 6/7）。

---

## 依赖

- **pandoc**：Markdown → docx 转换（合成阶段需要，`pandoc --version` 检查）
- **python-docx**：后处理脚本依赖，`pip install python-docx`
- **arch-diagram**（可选）：架构图 / 流程图生成，已安装则在阶段 5 自动调用

---

## 适用场景

写方案、写申报书、写投标文件、写项目申请书、做可研报告、docx 排版、写标书、需要写一份完整的长篇技术文档。
