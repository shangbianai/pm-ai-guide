# arch-diagram Skill — API 图片模式配置说明

本文档帮助你配置 `arch-diagram` Skill 的 **B 模式（AI 图片生成）**，让 Skill 直接调用 API 输出架构图图片，无需手动复制提示词。

---

## 前提：已安装 arch-diagram Skill

将 `SKILL.md` 复制到以下路径（Windows）：

```powershell
# 创建目录并复制
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\arch-diagram"
Copy-Item ".\skill\SKILL.md" "$env:USERPROFILE\.claude\skills\arch-diagram\SKILL.md"
```

---

## 第一步：获取 API Key

### 选项 A — 魔芋 AI（推荐试用，支持 gpt-image-2）

| 项目 | 值 |
|------|-----|
| 服务地址 | https://www.moyu.info |
| API 端点 | `https://www.moyu.info/v1/images/generations` |
| 模型名称 | `gpt-image-2` |
| 图片尺寸 | `1024x1024` / `1536x1024` / `1024x1536` |
| 图片质量 | `low` / `medium` / `high` / `auto` |

注册后在控制台获取 API Key（格式：`sk-xxxxxxxx`）。

### 选项 B — 官方 OpenAI

前往 https://platform.openai.com 获取 API Key，模型使用 `gpt-image-1`。

---

## 第二步：设置环境变量

打开 **PowerShell**，运行以下命令（Key 替换为你自己的）：

```powershell
# 魔芋 API（永久写入用户级环境变量，重启后依然有效）
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-你的Key", "User")

# 验证是否设置成功
[System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
```

---

## 第三步：修改 Skill 脚本中的配置区

找到 `~/.claude/skills/arch-diagram/SKILL.md`，定位到 **B3 节**里的配置区，修改三行：

```python
# ── 配置区 ──────────────────────────────────────────────
API_KEY  = os.environ.get("OPENAI_API_KEY")   # 环境变量名不变
BASE_URL = "https://www.moyu.info/v1"          # ← 改为魔芋地址
MODEL    = "gpt-image-2"                       # ← 改为 gpt-image-2
# ────────────────────────────────────────────────────────
```

如果用官方 OpenAI，三行保持默认不动即可。

---

## 第四步：验证

在 Claude Code 中输入：

```
/arch-diagram 帮我画一张简单的三层架构图：用户端 App、API 网关、数据库
```

选择 **C 模式（AI 直接出图）**，确认调用 API，稍等约 15–30 秒，图片应保存在当前目录。

---

## 常见问题

| 现象 | 原因 | 解决 |
|------|------|------|
| `RuntimeError: 请先设置 API Key` | 环境变量未在当前 shell 生效 | 重新开一个 PowerShell 窗口 |
| `401 Unauthorized` | Key 填错或过期 | 检查控制台余额和 Key 是否正确 |
| `requests` 模块找不到 | Python 未安装 requests | `pip install requests` |
| 图片文字乱码 | 极少数情况下模型渲染中文失败 | 重新生成一次，通常可解决 |
