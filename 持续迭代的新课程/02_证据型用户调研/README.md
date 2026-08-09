# 用户调研报告（同步飞书文档）

Skill：`synthesize-user-research`

将现场访谈录音、完整转写、照片、观察笔记、问卷和业务表格等混合素材，整理成完整的用户调研报告。结果不只有研究结论，还保留可回溯的证据台账，并可将报告正文、原始配图、访谈音频附件、原始文件和完整转写一次同步到飞书文档。

> 请使用 `$synthesize-user-research`，读取我提供的现场录音、照片、转写、观察笔记和工单表格，生成完整的用户调研报告。请严格区分已验证事实、合理推断和待验证假设，并将报告正文、原始照片、访谈音频附件和完整转写同步到飞书文档。

## 飞书 CLI

飞书同步使用官方 `lark-cli`：

```bash
npm install -g @larksuite/cli
npx -y skills add https://open.feishu.cn --skill -y
lark-cli config init --new
lark-cli auth login --recommend
lark-cli auth status
```

- [飞书 CLI 官方仓库](https://github.com/larksuite/cli)
- [官方 README](https://github.com/larksuite/cli/blob/main/README.md)
- [飞书官方安装指南](https://open.feishu.cn/document/no_class/mcp-archive/feishu-cli-installation-guide)
- [飞书 CLI 能力与常用命令](https://open.feishu.cn/document/mcp_open_tools/feishu-cli-let-ai-actually-do-your-work-in-feishu)

参考成果：`../统一教学案例/research-report.html`。
