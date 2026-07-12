const http = require("http");
const { exec } = require("child_process");

// ── Config ──────────────────────────────────────────────
const PORT = 3000;
const FEISHU = {
  appId: "cli_a936473608f81cd6",
  appSecret: "wAgl71K85NIm2UV9aPIz5ffY0ReiShVt",
  baseUrl: "https://open.feishu.cn/open-apis",
  bitableToken: "Z8b9bx9tNaF1zuswoPMcPd6zneb",
  tableId: "tbl8BxHVSLAdWSen",
};
const BITABLE_URL =
  "https://zcnotzbbokcu.feishu.cn/base/Z8b9bx9tNaF1zuswoPMcPd6zneb" +
  "?table=tbl8BxHVSLAdWSen&record=__RECORD_ID__&view=vewqhZJKDD";
const GROUP_CHAT_ID = "oc_bb0fa72a86cbd644db3127d8a32c36bc";
const OPENCLAW = {
  url: "http://127.0.0.1:18789/v1/chat/completions",
  token: "0da376b4c168e1a346ab5c57e9218af7128b35bb1f9ca23a",
};

// ── Helpers ─────────────────────────────────────────────
function json(res, data, status = 200) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(data, null, 2));
}

function readBody(req) {
  return new Promise((resolve) => {
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", () => {
      try { resolve(JSON.parse(body)); } catch { resolve(body); }
    });
  });
}

function httpFetch(url, opts = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const proto = u.protocol === "https:" ? require("https") : require("http");
    const r = proto.request(u, { method: opts.method || "GET", headers: opts.headers || {} }, (res) => {
      let d = "";
      res.on("data", (c) => (d += c));
      res.on("end", () => { try { resolve(JSON.parse(d)); } catch { resolve(d); } });
    });
    r.on("error", reject);
    if (opts.body) r.write(opts.body);
    r.end();
  });
}

// ── Feishu API ──────────────────────────────────────────
async function feishuToken() {
  const r = await httpFetch(`${FEISHU.baseUrl}/auth/v3/tenant_access_token/internal`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ app_id: FEISHU.appId, app_secret: FEISHU.appSecret }),
  });
  if (r.code !== 0) throw new Error(`Feishu auth: ${r.msg}`);
  return r.tenant_access_token;
}

async function createRecord(token, fields) {
  const r = await httpFetch(
    `${FEISHU.baseUrl}/bitable/v1/apps/${FEISHU.bitableToken}/tables/${FEISHU.tableId}/records`,
    {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ fields }),
    }
  );
  if (r.code !== 0) throw new Error(`Bitable: ${r.msg}`);
  return r.data.record.record_id;
}

// ── Processing Methodology ──────────────────────────────
function buildMethodology(recordId, nickname, email, content) {
  const url = BITABLE_URL.replace("__RECORD_ID__", recordId);
  return [
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "📩 新用户反馈 · 请立即处理",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "",
    `记录ID: ${recordId}`,
    `用户昵称: ${nickname || "匿名用户"}`,
    email ? `用户邮箱: ${email}` : "用户邮箱: （未提供）",
    `反馈内容: ${content}`,
    "",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "📋 处理流程",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "",
    "【1】获取 token",
    "curl POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    `body: {"app_id":"cli_a936473608f81cd6","app_secret":"wAgl71K85NIm2UV9aPIz5ffY0ReiShVt"}`,
    "",
    "【2】分析 · 按以下方法论",
    "",
    "  分类（选一）：",
    "    功能需求 | 体验问题 | Bug反馈 | 性能问题 | 其他建议",
    "",
    "  优先级：",
    "    高 = 核心流程受阻 / 多数用户 / 有deadline",
    "    中 = 部分用户 / 非核心 / 有workaround",
    "    低 = 边缘场景 / 纯建议",
    "",
    "  痛点提炼（1-2句，挖掘背后需求，不是复述问题）：",
    "    差：用户说搜索不好用",
    "    好：检索结果与意图匹配度低，中文语义理解不足",
    "",
    "  回复草稿准则：",
    "    a. 共情开头——感谢+理解困扰",
    "    b. 明确表态——Bug/已有计划/纳入评估",
    "    c. 可操作建议——临时方案或替代路径",
    "    d. 后续通道——何时有反馈、如何跟进",
    "    语气：真诚、像同事，不像客服模板",
    "",
    "  方案建议（短期/中期/长期）：",
    "    短期 <2周：可快速修的点",
    "    中期 2-8周：需要开发周期的改进",
    "    长期：方向性思考",
    "",
    "【3】更新 Bitable · curl PUT",
    `  record_id=${recordId} app_token=${FEISHU.bitableToken} table_id=${FEISHU.tableId}`,
    "  更新字段：",
    "    AI 解析状态 = 已处理",
    "    反馈分类 = 功能需求/体验问题/Bug反馈/性能问题/其他建议（填入分类名）",
    "    核心痛点 = ...",
    "    优先级 = 高/中/低",
    "    AI 拟定回复草稿 = ...",
    "    解决方案建议 = ...",
    "  注意：中文字段名必须完全一致，JSON 内换行用 \\\\n",
    "",
    "【4】群聊通知 · curl POST im/v1/messages?receive_id_type=chat_id",
    `  receive_id=${GROUP_CHAT_ID}`,
    "  msg_type=text, content 为以下格式：",
    "",
    "  反馈已处理",
    "",
    "  用户：xxx（未填则写「匿名用户」）",
    "  （邮箱：xxx@email —— 如果邮箱为空则省略此行）",
    "  分类：功能需求 / 体验问题 / Bug反馈 / 性能问题 / 其他建议",
    "  痛点：xxx",
    "  优先级：高 / 中 / 低",
    "  AI 回复草稿：已写入多为表格，人工确认后发送",
    `  详情：${url}`,
    "",
    "  注意：必须包含 🔗 链接；不要额外发散（如问项目关联）；控制在 10 行内",
    "",
    `app_id=cli_a936473608f81cd6 app_secret=wAgl71K85NIm2UV9aPIz5ffY0ReiShVt`,
    `bitable_token=${FEISHU.bitableToken} table_id=${FEISHU.tableId}`,
    `group_chat_id=${GROUP_CHAT_ID}`,
  ].join("\n");
}

function triggerOpenClaw(recordId, nickname, email, content) {
  const prompt = buildMethodology(recordId, nickname, email, content)
    .replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/`/g, "\\`").replace(/\$/g, "\\$");
  const cmd = `openclaw agent --agent main --message "${prompt}" --json`;

  return new Promise((resolve) => {
    exec(cmd, { timeout: 120000, maxBuffer: 2 * 1024 * 1024 }, (err, stdout) => {
      if (err) { console.error("Agent error:", recordId, err.message); return resolve(null); }
      try {
        const r = JSON.parse(stdout);
        console.log("Agent done:", recordId, r.status);
        resolve(r);
      } catch {
        console.log("Agent raw:", recordId, stdout.slice(0, 300));
        resolve(null);
      }
    });
  });
}

// ── HTML Page ───────────────────────────────────────────
function renderPage() {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>用户反馈</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#fafaf8;--card:#fff;--ink:#1c1917;--muted:#78716c;--border:#e7e5e4;--accent:#2d6a4f;--ahover:#1b4d38;--alight:#f0f7f3;--danger:#dc2626;--radius:10px;--shadow-lg:0 4px 24px rgba(0,0,0,.07),0 1px 4px rgba(0,0,0,.05)}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--ink);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;-webkit-font-smoothing:antialiased}
.card{background:var(--card);border-radius:16px;box-shadow:var(--shadow-lg);border:1px solid var(--border);padding:clamp(24px,5vw,40px);width:100%;max-width:440px;transition:transform .3s,opacity .3s}
.card.animating{transform:scale(.98);opacity:.7}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:24px}
.brand-dot{width:8px;height:8px;border-radius:50%;background:var(--accent);flex-shrink:0}
.brand-text{font-size:15px;font-weight:600;letter-spacing:-.01em}
h1{font-size:clamp(20px,4vw,24px);font-weight:650;letter-spacing:-.02em;margin-bottom:6px}
.desc{font-size:14px;color:var(--muted);line-height:1.55;margin-bottom:28px}
.field{margin-bottom:20px}
label{display:block;font-size:13px;font-weight:550;margin-bottom:6px}
input,textarea{width:100%;padding:10px 14px;border:1px solid var(--border);border-radius:var(--radius);font-size:15px;font-family:inherit;color:var(--ink);background:var(--bg);transition:border-color .2s,box-shadow .2s,background .2s;outline:none;-webkit-appearance:none}
input:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--alight);background:var(--card)}
input::placeholder,textarea::placeholder{color:#a8a29e}
textarea{resize:vertical;min-height:130px;line-height:1.6}
button[type=submit]{width:100%;padding:12px;background:var(--accent);color:#fff;border:none;border-radius:var(--radius);font-size:15px;font-weight:550;cursor:pointer;transition:background .2s,transform .15s,opacity .2s;display:flex;align-items:center;justify-content:center;gap:8px}
button[type=submit]:hover{background:var(--ahover)}
button[type=submit]:active{transform:scale(.985)}
button[type=submit]:disabled{opacity:.6;cursor:not-allowed;transform:none}
.spinner{width:18px;height:18px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:spin .6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.status{text-align:center;padding:32px 16px;display:none}
.status.visible{display:block}
.status-icon{width:56px;height:56px;border-radius:50%;background:var(--alight);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;animation:popIn .4s cubic-bezier(.175,.885,.32,1.275)}
.status-icon svg{width:28px;height:28px;color:var(--accent)}
@keyframes popIn{0%{transform:scale(0);opacity:0}80%{transform:scale(1.08)}to{transform:scale(1);opacity:1}}
.status-title{font-size:18px;font-weight:650;margin-bottom:6px}
.status-desc{font-size:14px;color:var(--muted);line-height:1.55}
.error-msg{margin-top:8px;font-size:13px;color:var(--danger);text-align:center;display:none}
.error-msg.visible{display:block}
.footer{text-align:center;margin-top:24px;font-size:12px;color:var(--muted)}
.honeypot{position:absolute;left:-9999px;opacity:0;height:0;overflow:hidden}
</style>
</head>
<body>
<div class="card" id="card">
<div id="formArea">
<div class="brand"><div class="brand-dot"></div><span class="brand-text">AI PM Course</span></div>
<h1>提交反馈</h1>
<p class="desc">遇到问题或有改进建议？请告诉我们，我们会尽快处理。</p>
<form id="form" novalidate>
<div class="field"><label for="nickname">昵称 <span style="color:var(--muted);font-weight:400">(选填)</span></label><input id="nickname" name="nickname" placeholder="你的称呼" autocomplete="name"></div>
<div class="field"><label for="email">邮箱 <span style="color:var(--muted);font-weight:400">(选填)</span></label><input id="email" name="email" type="email" placeholder="如需回复请留下邮箱"></div>
<div class="field"><label for="content">反馈内容</label><textarea id="content" name="content" placeholder="请详细描述你遇到的问题或改进建议……" required></textarea></div>
<div class="honeypot"><input type="text" name="_website" tabindex="-1" autocomplete="off"></div>
<div class="error-msg" id="errorMsg"></div>
<button type="submit" id="submitBtn"><span id="btnText">提交反馈</span><span class="spinner" id="spinner" style="display:none"></span></button>
</form>
<div class="footer">你的反馈会帮助我们持续改进</div>
</div>
<div class="status" id="statusArea">
<div class="status-icon"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg></div>
<div class="status-title">反馈已提交</div>
<div class="status-desc">感谢你的反馈，我们会尽快处理。如需跟进，将通过邮箱联系你。</div>
</div>
</div>
<script>
function L(l){sb.disabled=l;bt.textContent=l?"提交中":"提交反馈";sp.style.display=l?"inline-block":"none";em.classList.remove("visible")}
function E(m){em.textContent=m;em.classList.add("visible")}
function S(){card.classList.add("animating");setTimeout(function(){fa.style.display="none";sa.classList.add("visible");card.classList.remove("animating")},250)}
var card=document.getElementById("card"),fa=document.getElementById("formArea"),sa=document.getElementById("statusArea"),em=document.getElementById("errorMsg"),sb=document.getElementById("submitBtn"),bt=document.getElementById("btnText"),sp=document.getElementById("spinner");
document.getElementById("form").addEventListener("submit",function(e){e.preventDefault();L(true);
var n=document.getElementById("nickname").value.trim(),eml=document.getElementById("email").value.trim(),c=document.getElementById("content").value.trim();
if(!c){E("请填写反馈内容");L(false);return}
if(eml&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(eml)){E("邮箱格式不正确");L(false);return}
fetch("/api/feedback",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({nickname:n,email:eml,content:c})}).then(function(r){if(!r.ok)return r.json().then(function(d){throw new Error(d.error||"提交失败")});S()}).catch(function(err){E(err.message||"网络错误");L(false)})});
</script>
</body>
</html>`;
}

// ── Server ──────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.writeHead(204); return res.end(); }

  if (req.method === "GET" && req.url === "/") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    return res.end(renderPage());
  }

  if (req.method === "POST" && req.url === "/api/feedback") {
    try {
      const body = await readBody(req);
      const { nickname, email, content, _website } = body || {};

      if (_website !== undefined && _website !== "") {
        return json(res, { error: "提交失败" }, 400);
      }
      if (!content) {
        return json(res, { error: "请填写反馈内容" }, 400);
      }

      const token = await feishuToken();
      const recordId = await createRecord(token, {
        "用户吐槽的内容": content,
        "用户昵称": nickname || "匿名用户",
        "用户邮箱": email || "",
      });

      triggerOpenClaw(recordId, nickname, email, content).then((r) =>
        console.log("OpenClaw triggered:", recordId, typeof r === "object" ? "OK" : "str")
      ).catch((e) =>
        console.error("OpenClaw trigger error:", recordId, e.message)
      );

      return json(res, { success: true, recordId });
    } catch (err) {
      console.error("Feedback error:", err);
      return json(res, { error: err.message }, 500);
    }
  }

  json(res, { error: "Not found" }, 404);
});

server.listen(PORT, "0.0.0.0", () => {
  console.log("Feedback server: http://0.0.0.0:" + PORT);
});
