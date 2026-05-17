# 用户反馈系统 · 维护手册

## 架构概览

```
用户浏览器 → http://服务器IP:3000 → 提交表单
    ↓ POST /api/feedback
server.js (Node.js)
    ├─ ① 写入飞书多维表格（新记录）
    └─ ② 执行 openclaw agent CLI（本地命令行）
         ↓
    OpenClaw Agent（完整工具权限）
         ├─ ③ AI 分析反馈（分类/痛点/优先级/回复草稿/方案）
         ├─ ④ 更新多维表格记录
         └─ ⑤ 飞书群聊通知（带记录链接）
```

> Agent 通过 `openclaw agent --agent main --message "..."` 命令行触发，不走 HTTP API。这样 Agent 有完整的 exec/工具权限，处理可靠。

## 文件位置

所有文件在服务器 `115.190.184.176` 上：

| 文件 | 路径 | 用途 |
|------|------|------|
| 反馈服务 | `/root/feedback-server/server.js` | 前端页面 + API + 触发逻辑 |
| OpenClaw 配置 | `/root/.openclaw/openclaw.json` | 网关、飞书通道、模型配置 |
| OpenClaw 人设 | `/root/.openclaw/workspace/SOUL.md` | Agent 的人格和行为准则 |

---

## 一、前端页面维护

### 修改页面文案/样式

编辑 `/root/feedback-server/server.js`，找到 `renderPage` 函数（约第 180 行），HTML 和 CSS 都在里面。

改完后重启：
```bash
systemctl restart feedback-server
```

### 修改验证码

验证码逻辑在 `server.js` 头部 `createCaptcha()` 函数。当前是简单加法，想换题型改那几行就行。

### 页面访问地址

`http://115.190.184.176:3000/`

如果要绑定域名，在云控制台加 DNS 解析到 `115.190.184.176`，再配 nginx 反向代理。

---

## 二、更换多维表格

如果换了新的多维表格，需要改 3 个地方：

### 1. server.js（约第 10 行）

```javascript
const FEISHU = {
  // ...
  bitableToken: "新的app_token",   // ← 改这里
  tableId: "新的table_id",         // ← 改这里
};
```

### 2. 多维表格链接（约第 17 行）

```javascript
const BITABLE_URL =
  "https://新域名.feishu.cn/base/新token" +
  "?table=新table_id&record=__RECORD_ID__&view=新view_id";
```

> `__RECORD_ID__` 是占位符，不要改它。

### 3. buildMethodology 函数（约第 90 行）

把 `app_token=` 和 `table_id=` 的值更新为新的。

### 多维表格字段要求

新表格必须有以下字段（字段名必须一致，类型必须是文本，除了两个选择字段）：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 用户吐槽的内容 | 文本 | 用户提交的反馈 |
| 用户昵称 | 文本 |  |
| 用户邮箱 | 文本 |  |
| 反馈时间 | 日期 | 自动生成 |
| AI 解析状态 | 单选：未处理/已处理 | Agent 处理后标记 |
| 反馈分类 | 文本 | Agent 分类：功能需求/体验问题/Bug反馈/性能问题/其他建议 |
| 核心痛点 | 文本 | Agent 分析填入 |
| 优先级 | 文本 | 高/中/低 |
| AI 拟定回复草稿 | 文本 | Agent 生成 |
| 解决方案建议 | 文本 | Agent 生成 |
| 回复状态 | 单选：待回复/已回复 | 默认"待回复"，人工确认后改 |

改完重启：
```bash
systemctl restart feedback-server
```

### 调整处理逻辑和通知格式

编辑 `server.js` 的 `buildMethodology` 函数（约第 90 行），里面的内容会**随每次反馈请求一起发给 Agent**，不依赖 SOUL.md。

可调整：
- 分类框架（2.1 节）
- 优先级判断标准（2.2 节）
- 回复草稿准则（2.4 节）
- 群通知格式（Step 4 节）

改完重启 `systemctl restart feedback-server`。

---

## 三、更换 OpenClaw（小龙虾）

### 换 AI 模型

编辑 `/root/.openclaw/openclaw.json`，在 `models.providers` 下修改：

```json
"models": {
  "providers": {
    "zai": {
      "baseUrl": "新API地址",
      "api": "openai-completions",
      "models": [{
        "id": "新模型ID",
        "name": "新模型名称",
        "contextWindow": 128000,
        "maxTokens": 8192
      }]
    }
  }
}
```

### 换 API Key

`/root/.openclaw/openclaw.json` 的 `env.ZAI_API_KEY` 和 `/root/.openclaw/.env` 的 `ANTHROPIC_API_KEY` 都要改。

### 换飞书应用

如果换了飞书 App：

1. `/root/.openclaw/openclaw.json` → `channels.feishu.appId` / `appSecret`
2. `/root/.openclaw/.env` → `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
3. `/root/feedback-server/server.js` → `FEISHU.appId` / `appSecret`

### 重启 Gateway
```bash
systemctl --user restart openclaw-gateway
systemctl restart feedback-server
```

### 查看 Gateway 状态
```bash
openclaw status
openclaw status --deep   # 详细诊断
journalctl --user -u openclaw-gateway -f  # 实时日志
```

---

## 四、通知群聊管理

### 换通知群聊

1. 新建飞书群，把 Bot（龙振东）拉入
2. 获取群 chat_id（`oc_` 开头）

获取方法（二选一）：
- 在群里发消息，查 Bot 日志：`journalctl --user -u openclaw-gateway -f | grep chat_id`
- 或用 lark-cli：`lark-cli im +chat-search --query "群名称"`

3. 更新 server.js：
```javascript
const GROUP_CHAT_ID = "oc_新chat_id";  // 约第 19 行
```

4. 重启：
```bash
systemctl restart feedback-server
```

### Bot 群聊行为配置

OpenClaw 已恢复默认配置，**不需额外修改**。默认行为：群聊中只有被 @ 才会响应。反馈处理走的是本地 API 直连（`localhost:18789`），与群聊行为无关。

---

## 五、服务器运维

### 服务管理

```bash
# 反馈服务
systemctl status feedback-server     # 查看状态
systemctl restart feedback-server    # 重启
systemctl stop feedback-server       # 停止
systemctl start feedback-server      # 启动
journalctl -u feedback-server -f     # 实时日志

# OpenClaw 网关（注意是 --user）
systemctl --user status openclaw-gateway
systemctl --user restart openclaw-gateway
journalctl --user -u openclaw-gateway -f
```

### 端口与防火墙

- 反馈页面：TCP 3000（需要在云安全组放行）
- OpenClaw Gateway：TCP 18789（仅本地访问，不需放行）

云控制台 → 安全组 → 入方向规则，确认 TCP 3000 已放行。

### 监控

```bash
# 检查两个服务是否都在
systemctl is-active feedback-server
systemctl --user is-active openclaw-gateway

# 测试反馈页面
curl -s http://127.0.0.1:3000/ | head -5

# 测试 OpenClaw API
curl -s http://127.0.0.1:18789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 0da376b4c168e1a346ab5c57e9218af7128b35bb1f9ca23a" \
  -d '{"model":"glm-4.7","messages":[{"role":"user","content":"回复OK"}],"max_tokens":20}'
```

---

## 六、故障排查

| 症状 | 检查 |
|------|------|
| 页面打不开 | `systemctl is-active feedback-server`；云安全组 TCP 3000 是否放行 |
| 提交后没反应 | `journalctl -u feedback-server -f` 看日志；检查飞书 API 是否正常 |
| 提交成功但 Bot 不处理 | `systemctl --user is-active openclaw-gateway`；检查 Chat Completions API 是否正常 |
| Bot 处理了但群没通知 | 检查 `GROUP_CHAT_ID` 是否正确；Bot 是否在群里 |
| Bot 回复格式/内容有问题 | 编辑 server.js 的 `buildMethodology` 函数，改通知格式和指令 |
| 验证码报错 | 可能过期（5分钟TTL），用户需刷新页面 |
| 反馈分类未写入 | 确认多维表格有"反馈分类"字段（文本类型），字段名完全一致 |
