// @ts-nocheck
import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync, copyFileSync } from "fs";
import { join, basename, resolve } from "path";

type BackendType = "doubao" | "openai" | "gemini" | "grsai";

const BACKEND_CONFIG: Record<BackendType, { apiUrl: string; model: string; label: string }> = {
  doubao: {
    apiUrl: "https://ark.cn-beijing.volces.com/api/v3/images/generations",
    model: "doubao-seedream-5-0-260128",
    label: "豆包 Seedream",
  },
  openai: {
    apiUrl: "https://api.openai.com/v1/images/generations",
    model: "gpt-image-2",
    label: "OpenAI GPT-image-2",
  },
  gemini: {
    apiUrl: "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent",
    model: "gemini-2.0-flash-exp",
    label: "Gemini 2.0 Flash Exp",
  },
  grsai: {
    apiUrl: "https://grsai.dakka.com.cn/v1/api/generate",
    model: "gpt-image-2",
    label: "Grsai GPT-image-2（国内节点）",
  },
};

const OPENAI_SUPPORTED_SIZES = ["1024x1024", "1536x1024", "1024x1536"];
const DEFAULT_SIZE = "1672x941";
const FALLBACK_SIZE = "1536x1024";
const DOUBAO_MIN_PIXELS = 3686400;
const DOUBAO_SIZE = "2560x1440";

interface SlideTask {
  promptFile: string;
  outputFile: string;
  index: number;
}

function loadEnv(): Record<string, string> {
  const env: Record<string, string> = {};
  const candidates = [
    join(process.cwd(), ".env"),
    join(import.meta.dir, "..", "..", "..", "..", ".env"),
    join(import.meta.dir, "..", ".env"),
  ];

  for (const p of candidates) {
    if (existsSync(p)) {
      const content = readFileSync(p, "utf-8");
      for (const line of content.split("\n")) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith("#")) continue;
        const eqIndex = trimmed.indexOf("=");
        if (eqIndex > 0) {
          const key = trimmed.slice(0, eqIndex).trim();
          let val = trimmed.slice(eqIndex + 1).trim();
          if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
            val = val.slice(1, -1);
          }
          env[key] = val;
        }
      }
      break;
    }
  }

  for (const [k, v] of Object.entries(process.env)) {
    if (v !== undefined) env[k] = v;
  }

  return env;
}

function getApiKey(env: Record<string, string>, backend: BackendType): string | null {
  switch (backend) {
    case "doubao":
      return env.ARK_API_KEY || env.DOUBAO_API_KEY || null;
    case "openai":
      return env.OPENAI_API_KEY || null;
    case "gemini":
      return env.GEMINI_API_KEY || env.GOOGLE_API_KEY || null;
    case "grsai":
      return env.GRSAI_API_KEY || null;
  }
}

function printApiKeyHint(backend: BackendType): void {
  switch (backend) {
    case "doubao":
      console.error("请在 .env 文件中设置 ARK_API_KEY 或 DOUBAO_API_KEY，或通过环境变量传入。");
      console.error("获取方式：https://console.volcengine.com/ark");
      break;
    case "openai":
      console.error("请设置 OPENAI_API_KEY，获取方式：https://platform.openai.com/api-keys");
      break;
    case "gemini":
      console.error("请设置 GEMINI_API_KEY 或 GOOGLE_API_KEY，获取方式：https://aistudio.google.com/apikey");
      break;
    case "grsai":
      console.error("请设置 GRSAI_API_KEY，获取方式：联系 Grsai 平台获取 API Key");
      break;
  }
}

function parseArgs(): { promptsDir: string; outputDir: string; size: string; batchSize: number; retry: boolean; backend: BackendType } {
  const args = process.argv.slice(2);
  let promptsDir = "";
  let outputDir = "";
  let size = DEFAULT_SIZE;
  let batchSize = 1;
  let retry = false;
  let backend: BackendType = "doubao";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--output-dir" && args[i + 1]) {
      outputDir = args[++i];
    } else if (args[i] === "--size" && args[i + 1]) {
      size = args[++i];
    } else if (args[i] === "--batch-size" && args[i + 1]) {
      batchSize = Math.min(8, Math.max(1, parseInt(args[++i], 10) || 1));
    } else if (args[i] === "--retry") {
      retry = true;
    } else if (args[i] === "--backend" && args[i + 1]) {
      const val = args[++i] as BackendType;
      if (val !== "doubao" && val !== "openai" && val !== "gemini" && val !== "grsai") {
        console.error(`不支持的后端：${val}，可选值：doubao, openai, gemini, grsai`);
        process.exit(1);
      }
      backend = val;
    } else if (!args[i].startsWith("-") && !promptsDir) {
      promptsDir = args[i];
    }
  }

  if (!promptsDir) {
    console.error("用法：bun generate-slides.ts <提示词目录> [--output-dir 输出目录] [--size 尺寸] [--batch-size N] [--retry] [--backend doubao|openai|gemini|grsai]");
    process.exit(1);
  }

  if (!outputDir) {
    outputDir = join(promptsDir, "..");
  }

  return { promptsDir, outputDir, size, batchSize, retry, backend };
}

function discoverTasks(promptsDir: string, outputDir: string, retry: boolean): SlideTask[] {
  if (!existsSync(promptsDir)) {
    console.error(`提示词目录不存在：${promptsDir}`);
    process.exit(1);
  }

  const files = readdirSync(promptsDir).filter((f) => /^\d+-slide-.*\.md$/i.test(f)).sort();

  if (files.length === 0) {
    console.error(`未找到提示词文件：${promptsDir}`);
    console.error("期望格式：01-slide-*.md, 02-slide-*.md 等");
    process.exit(1);
  }

  const tasks: SlideTask[] = [];

  for (const f of files) {
    const match = f.match(/^(\d+)-slide-.*\.md$/i);
    if (!match) continue;
    const idx = parseInt(match[1], 10);
    const baseName = f.replace(/\.md$/i, "");
    const outputFile = join(outputDir, `${baseName}.png`);

    if (!retry && existsSync(outputFile)) {
      console.log(`跳过（已存在）：${baseName}.png`);
      continue;
    }

    tasks.push({
      promptFile: join(promptsDir, f),
      outputFile,
      index: idx,
    });
  }

  return tasks;
}

function readPrompt(filePath: string): string {
  const content = readFileSync(filePath, "utf-8");
  return content.trim();
}

async function generateImage(prompt: string, apiKey: string, size: string, backend: BackendType): Promise<Buffer> {
  const config = BACKEND_CONFIG[backend];
  let actualSize = size;

  if (backend === "doubao") {
    const [w, h] = size.split("x").map(Number);
    if (w * h < DOUBAO_MIN_PIXELS) {
      console.log(`  豆包 API 要求最少 ${DOUBAO_MIN_PIXELS} 像素，已自动升档为 ${DOUBAO_SIZE}`);
      actualSize = DOUBAO_SIZE;
    }
  }

  switch (backend) {
    case "doubao":
      return generateImageDoubao(prompt, apiKey, actualSize, config.apiUrl, config.model);
    case "openai":
      return generateImageOpenai(prompt, apiKey, actualSize, config.apiUrl, config.model);
    case "gemini":
      return generateImageGemini(prompt, apiKey, config.apiUrl);
    case "grsai":
      return generateImageGrsai(prompt, apiKey, actualSize, config.apiUrl, config.model);
  }
}

async function generateImageDoubao(prompt: string, apiKey: string, size: string, apiUrl: string, model: string): Promise<Buffer> {
  const response = await fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      prompt,
      sequential_image_generation: "disabled",
      response_format: "b64_json",
      size,
      stream: false,
      watermark: false,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API 请求失败 (${response.status})：${errorText}`);
  }

  const data = await response.json() as any;

  if (data.data && data.data.length > 0) {
    const item = data.data[0];
    if (item.b64_json) {
      return Buffer.from(item.b64_json, "base64");
    }
    if (item.url) {
      const imgResp = await fetch(item.url);
      if (!imgResp.ok) throw new Error(`下载图片失败 (${imgResp.status})`);
      const arrayBuf = await imgResp.arrayBuffer();
      return Buffer.from(arrayBuf);
    }
  }

  throw new Error("API 返回数据中未找到图片");
}

async function generateImageOpenai(prompt: string, apiKey: string, size: string, apiUrl: string, model: string): Promise<Buffer> {
  const actualSize = OPENAI_SUPPORTED_SIZES.includes(size) ? size : FALLBACK_SIZE;
  if (size !== actualSize) {
    console.log(`  OpenAI 不支持尺寸 ${size}，已自动转为 ${actualSize}`);
  }

  const response = await fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      prompt,
      n: 1,
      size: actualSize,
      response_format: "b64_json",
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API 请求失败 (${response.status})：${errorText}`);
  }

  const data = await response.json() as any;

  if (data.data && data.data.length > 0) {
    const item = data.data[0];
    if (item.b64_json) {
      return Buffer.from(item.b64_json, "base64");
    }
    if (item.url) {
      const imgResp = await fetch(item.url);
      if (!imgResp.ok) throw new Error(`下载图片失败 (${imgResp.status})`);
      const arrayBuf = await imgResp.arrayBuffer();
      return Buffer.from(arrayBuf);
    }
  }

  throw new Error("API 返回数据中未找到图片");
}

async function generateImageGemini(prompt: string, apiKey: string, apiUrl: string): Promise<Buffer> {
  const url = `${apiUrl}?key=${apiKey}`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      contents: [{
        parts: [{ text: prompt }],
      }],
      generationConfig: {
        responseModalities: ["TEXT", "IMAGE"],
      },
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API 请求失败 (${response.status})：${errorText}`);
  }

  const data = await response.json() as any;

  const candidates = data.candidates;
  if (candidates && candidates.length > 0) {
    const parts = candidates[0].content?.parts;
    if (parts) {
      for (const part of parts) {
        if (part.inlineData && part.inlineData.mimeType && part.inlineData.mimeType.startsWith("image/")) {
          return Buffer.from(part.inlineData.data, "base64");
        }
      }
    }
  }

  throw new Error("API 返回数据中未找到图片");
}

async function generateImageGrsai(prompt: string, apiKey: string, size: string, apiUrl: string, model: string): Promise<Buffer> {
  const actualSize = OPENAI_SUPPORTED_SIZES.includes(size) ? size : FALLBACK_SIZE;
  if (size !== actualSize) {
    console.log(`  Grsai 不支持尺寸 ${size}，已自动转为 ${actualSize}`);
  }

  const response = await fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      prompt,
      images: [],
      aspectRatio: actualSize,
      replyType: "json",
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API 请求失败 (${response.status})：${errorText}`);
  }

  const data = await response.json() as any;

  if (data.status === "succeeded" && data.results && data.results.length > 0) {
    const url = data.results[0].url;
    if (url) {
      return downloadWithRetry(url);
    }
  }

  throw new Error(`API 返回数据中未找到图片，状态：${data.status || "unknown"}`);
}

async function downloadWithRetry(url: string, retries: number = 3): Promise<Buffer> {
  for (let i = 0; i < retries; i++) {
    try {
      const resp = await fetch(url);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const arrayBuf = await resp.arrayBuffer();
      return Buffer.from(arrayBuf);
    } catch (e) {
      if (i === retries - 1) throw e;
      await new Promise((r) => setTimeout(r, 2000 * (i + 1)));
    }
  }
  throw new Error("下载失败");
}

function backupIfExists(filePath: string) {
  if (!existsSync(filePath)) return;
  const ts = new Date().toISOString().replace(/[-:T]/g, "").slice(0, 14);
  const dir = join(filePath, "..");
  const ext = filePath.match(/\.\w+$/)?.[0] || "";
  const base = basename(filePath, ext);
  const backupPath = join(dir, `${base}-backup-${ts}${ext}`);
  copyFileSync(filePath, backupPath);
  console.log(`已备份：${basename(backupPath)}`);
}

async function processBatch(tasks: SlideTask[], apiKey: string, size: string, backend: BackendType): Promise<{ success: number; failed: number }> {
  let success = 0;
  let failed = 0;

  for (const task of tasks) {
    const prompt = readPrompt(task.promptFile);
    const fileName = basename(task.outputFile);

    console.log(`正在生成 [${task.index}]：${fileName}...`);

    try {
      backupIfExists(task.outputFile);
      const imageBuffer = await generateImage(prompt, apiKey, size, backend);
      writeFileSync(task.outputFile, imageBuffer);
      const sizeKB = Math.round(imageBuffer.length / 1024);
      console.log(`  ✓ 完成 (${sizeKB} KB)`);
      success++;
    } catch (err: any) {
      console.error(`  ✗ 失败：${err.message}`);
      failed++;
    }
  }

  return { success, failed };
}

async function main() {
  const { promptsDir, outputDir, size, batchSize, retry, backend } = parseArgs();
  const config = BACKEND_CONFIG[backend];

  const env = loadEnv();
  const apiKey = getApiKey(env, backend);

  if (!apiKey) {
    console.error(`未找到 ${config.label} API Key。`);
    printApiKeyHint(backend);
    process.exit(1);
  }

  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  const tasks = discoverTasks(promptsDir, outputDir, retry);

  if (tasks.length === 0) {
    console.log("没有需要生成的幻灯片（所有图片均已存在）。");
    return;
  }

  console.log(`找到 ${tasks.length} 张待生成的幻灯片`);
  console.log(`后端：${config.label} (${backend})`);
  console.log(`模型：${config.model}`);
  if (backend !== "gemini") {
    console.log(`尺寸：${size}`);
  }
  console.log("");

  let totalSuccess = 0;
  let totalFailed = 0;

  for (let i = 0; i < tasks.length; i += batchSize) {
    const batch = tasks.slice(i, i + batchSize);
    console.log(`--- 批次 ${Math.floor(i / batchSize) + 1}/${Math.ceil(tasks.length / batchSize)} ---`);

    const result = await processBatch(batch, apiKey, size, backend);
    totalSuccess += result.success;
    totalFailed += result.failed;
  }

  console.log("");
  console.log("===== 生成完成 =====");
  console.log(`成功：${totalSuccess}/${tasks.length}`);
  if (totalFailed > 0) {
    console.log(`失败：${totalFailed}/${tasks.length}`);
    console.log("提示：使用 --retry 参数可仅重新生成失败的幻灯片");
  }
}

main().catch((err) => {
  console.error("致命错误：", err.message);
  process.exit(1);
});
