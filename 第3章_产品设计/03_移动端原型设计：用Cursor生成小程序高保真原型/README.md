# 移动端小程序原型

本节提供可安装的 `pm-miniapp-prototype` Skill、课程原型示例和规则资料。Skill 根据原有课程规则、提示词和验收清单整理；示例沿用 CityCup 咖啡零售案例，展示商品、订单、会员和门店业务。

## 配套资料

| 文件 | 用途 |
| --- | --- |
| [Skill](skills/pm-miniapp-prototype/SKILL.md) | 让 AI 按本节工作流创建、修改原型 |
| [项目规则](skills/pm-miniapp-prototype/references/项目规则.md) | 业务对象、页面与迭代约束 |
| [提示词模板](skills/pm-miniapp-prototype/references/提示词模板.md) | 通用需求输入模板 |
| [验收清单](skills/pm-miniapp-prototype/references/验收清单.md) | 按需验收新生成的原型 |
| [AI 原型用户规则](AI原型用户规则.md) | 可复用的设计偏好 |
| [实操提示词](实操提示词.md) | 本节直接可用的练习输入 |
| [原型示例](示例/小程序原型.html) | 本地浏览器可打开的交互示例 |
| [完整资料包](移动端小程序原型资料包.zip) | 下载后解压，包含 Skill、示例和全部本地资源 |

## Skill 安装指令

将下面内容发送给支持 Skill 安装的 AI 编程助手：

```text
帮我安装这个 skills：
https://github.com/shangbianai/pm-ai-guide/tree/main/%E7%AC%AC3%E7%AB%A0_%E4%BA%A7%E5%93%81%E8%AE%BE%E8%AE%A1/03_%E7%A7%BB%E5%8A%A8%E7%AB%AF%E5%8E%9F%E5%9E%8B%E8%AE%BE%E8%AE%A1%EF%BC%9A%E7%94%A8Cursor%E7%94%9F%E6%88%90%E5%B0%8F%E7%A8%8B%E5%BA%8F%E9%AB%98%E4%BF%9D%E7%9C%9F%E5%8E%9F%E5%9E%8B/skills/pm-miniapp-prototype
```

也可下载资料包，将 `skills/pm-miniapp-prototype` 整个目录复制到工具支持的 Skill 目录，保持 `SKILL.md` 和 `references` 相对路径。Codex 的用户级目录通常为 `~/.codex/skills/`。若工具不支持 Skill 自动发现，可以直接要求它读取本节 `SKILL.md` 并按要求完成任务。

## 如何运行

1. 下载完整资料包并解压，保留目录结构。
2. 打开 `示例/小程序原型.html`，体验页面目录、底部导航、高低保真切换和商品交互。
3. 阅读实操提示词，替换业务需求，让 AI 生成自己的原型。

GitHub 文件页展示 HTML 源码，不能在文件页直接操作原型；请下载后在浏览器打开。示例使用模拟数据，部分操作仅展示提示或弹层；验收清单是练习目标，不代表示例具备生产系统功能。数据修改不会写入真实服务，刷新可能恢复默认数据。

## 资料来源

本节示例与规则来自课程 `08_prototype_design_cursor` 原始配套资料。2026-09-29 补齐此前只有 `.gitkeep` 的章节目录，并将规则整理为独立 Skill。
