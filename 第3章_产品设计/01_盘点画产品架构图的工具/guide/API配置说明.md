# arch-diagram Skill — 图片生成 API 配置指南

本文档教你如何配置 `arch-diagram` Skill 的 **C 模式（AI 直接出图）**，让 Skill 直接调用 OpenAI 兼容的图片生成 API，无需手动复制提示词到其他工具。

> 📋 **适用范围**：macOS / Windows / Linux，只要你有任意 OpenAI 兼容的图片生成 API（官方 OpenAI、第三方中转、自建服务均可）。

---

## 前提：已安装 arch-diagram Skill

确保 `SKILL.md` 和 `references/` 已复制到 Claude Code 的 skills 目录。

---

## 配置方式二选一

Skill 已经预读了 `OPENAI_API_KEY` 环境变量。你有两种方式告诉 Skill 你的 API 信息：

| 方式 | 适合场景 |
|------|----------|
| **A. 环境变量**（推荐） | 不想改 Skill 文件；多个 Skill 共用同一个 Key |
| **B. 直接改 Skill 文件** | 只用一次；不想污染全局环境变量 |

两种方式任选其一即可，下面分别说明。

---

## 方式 A：环境变量（推荐）

### macOS

打开 **终端（Terminal）**，运行：

```bash
# 写入 shell 配置文件（macOS 默认 zsh）
echo 'export OPENAI_API_KEY="你的API_KEY"' >> ~/.zshrc

# 如果用第三方中转，还需要设置中转地址（可选）
echo 'export OPENAI_BASE_URL="https://你的中转地址/v1"' >> ~/.zshrc

# 让配置立即生效
source ~/.zshrc
```

> 如果你的 Mac 用的是 bash（老系统），把 `~/.zshrc` 换成 `~/.bash_profile`。

### Windows（PowerShell）

打开 **PowerShell**，运行：

```powershell
# 写入用户级环境变量（永久生效）
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "你的API_KEY", "User")

# 如果用第三方中转（可选）
[Environment]::SetEnvironmentVariable("OPENAI_BASE_URL", "https://你的中转地址/v1", "User")
```

> ⚠️ 设置后需要 **重启 Claude Code**（或重启终端）才能生效。

### 验证环境变量是否生效

**macOS：**
```bash
echo $OPENAI_API_KEY
```

**Windows PowerShell：**
```powershell
echo $env:OPENAI_API_KEY
```

如果打印出了你的 Key，说明配置成功。

---

## 方式 B：直接改 Skill 文件

用文本编辑器打开 `~/.claude/skills/arch-diagram/SKILL.md`，找到 **模式 C** 里的配置区（约在第 218 行），把下面三行改成你自己的值：

```python
# ── 配置区 ──────────────────────────────────────────────
API_KEY  = "你的API_KEY"                        # 直接写死 Key
BASE_URL = "https://你的中转地址/v1"              # 第三方中转地址；官方 OpenAI 填 https://api.openai.com/v1
MODEL    = "你的模型名"                           # 如 gpt-image-1、gpt-image-2、dall-e-3
# ────────────────────────────────────────────────────────
```

> ⚠️ 如果直接把 Key 写在文件里，注意不要把这个文件上传到公开仓库。

---

## 可选：设置中转地址和模型名（环境变量方式）

如果你用的是第三方中转（而非官方 OpenAI），除了 `OPENAI_API_KEY`，还需要额外设置两个环境变量：

### macOS

```bash
echo 'export OPENAI_BASE_URL="https://你的中转地址/v1"' >> ~/.zshrc
echo 'export OPENAI_IMAGE_MODEL="你的模型名"' >> ~/.zshrc
source ~/.zshrc
```

### Windows PowerShell

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_BASE_URL", "https://你的中转地址/v1", "User")
[Environment]::SetEnvironmentVariable("OPENAI_IMAGE_MODEL", "你的模型名", "User")
```

> 如果设置了这个环境变量，Skill 会自动读取；如果没设置，Skill 会用默认值（官方 OpenAI + `gpt-image-1`）。不需要改 Skill 文件。

---

## 最终验证

在 Claude Code 中输入：

```
/arch-diagram 帮我画一张简单的三层架构图：用户端 App、API 网关、数据库
```

选择 **C 模式（AI 直接出图）**，如果 API 配置正确，约 15–30 秒后图片会保存在当前目录。

---

## 常见问题

| 现象 | 原因 | 解决 |
|------|------|------|
| 环境变量打印不出来 | 配置未生效或终端未重启 | macOS 运行 `source ~/.zshrc`；Windows 重启 Claude Code |
| `RuntimeError: 未检测到 API Key` | Skill 没读到环境变量 | 检查环境变量名是否拼错（必须为 `OPENAI_API_KEY`），确认后重启 Claude Code |
| `401 Unauthorized` | Key 无效或过期 | 检查 Key 是否正确、是否还有额度 |
| `404 Not Found` | 中转地址拼错或模型名错误 | 检查 `BASE_URL` 是否以 `/v1` 结尾，`MODEL` 是否与服务端一致 |
| 图片文字乱码 | 模型对中文渲染不稳定 | 重新生成一次，通常可解决 |
| `ModuleNotFoundError: requests` | Python 缺少 requests 库 | 终端运行 `pip install requests`（或 `pip3 install requests`） |

---

## 附：把本文档丢给 AI 帮你配

如果你不想手动操作，直接把下面这段话 **复制粘贴给 Claude Code / ChatGPT / 任何 AI 助手**，它会帮你完成配置：

> 请帮我配置 arch-diagram Skill 的图片生成 API。我的 API Key 是 `你的Key填这里`，中转地址是 `你的地址填这里`，模型名是 `你的模型名填这里`。我的系统是 macOS / Windows（二选一）。请按 setup-api-guide.md 里的步骤帮我完成配置。

AI 会帮你执行对应的命令或修改文件。
