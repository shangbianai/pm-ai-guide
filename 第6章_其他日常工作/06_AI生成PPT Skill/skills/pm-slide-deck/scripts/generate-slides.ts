// @ts-nocheck
import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync, copyFileSync } from "fs";
import { join, basename, resolve } from "path";

const API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations";
const MODEL = "doubao-seedream-5-0-260128";

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

function getApiKey(env: Record<string, string>): string | null {
  return env.ARK_API_KEY || env.DOUBAO_API_KEY || null;
}

function parseArgs(): { promptsDir: string; outputDir: string; size: string; batchSize: number; retry: boolean } {
  const args = process.argv.slice(2);
  let promptsDir = "";
  let outputDir = "";
  let size = "2K";
  let batchSize = 1;
  let retry = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--output-dir" && args[i + 1]) {
      outputDir = args[++i];
    } else if (args[i] === "--size" && args[i + 1]) {
      size = args[++i];
    } else if (args[i] === "--batch-size" && args[i + 1]) {
      batchSize = Math.min(8, Math.max(1, parseInt(args[++i], 10) || 1));
    } else if (args[i] === "--retry") {
      retry = true;
    } else if (!args[i].startsWith("-") && !promptsDir) {
      promptsDir = args[i];
    }
  }

  if (!promptsDir) {
    console.error("用法：bun generate-slides.ts <提示词目录> [--output-dir 输出目录] [--size 尺寸] [--batch-size N] [--retry]");
    process.exit(1);
  }

  if (!outputDir) {
    outputDir = join(promptsDir, "..");
  }

  return { promptsDir, outputDir, size, batchSize, retry };
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

async function generateImage(prompt: string, apiKey: string, size: string): Promise<Buffer> {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: MODEL,
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

async function processBatch(tasks: SlideTask[], apiKey: string, size: string): Promise<{ success: number; failed: number }> {
  let success = 0;
  let failed = 0;

  for (const task of tasks) {
    const prompt = readPrompt(task.promptFile);
    const fileName = basename(task.outputFile);

    console.log(`正在生成 [${task.index}]：${fileName}...`);

    try {
      backupIfExists(task.outputFile);
      const imageBuffer = await generateImage(prompt, apiKey, size);
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
  const env = loadEnv();
  const apiKey = getApiKey(env);

  if (!apiKey) {
    console.error("未找到豆包 API Key。");
    console.error("请在 .env 文件中设置 ARK_API_KEY 或 DOUBAO_API_KEY，或通过环境变量传入。");
    console.error("获取方式：https://console.volcengine.com/ark");
    process.exit(1);
  }

  const { promptsDir, outputDir, size, batchSize, retry } = parseArgs();

  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  const tasks = discoverTasks(promptsDir, outputDir, retry);

  if (tasks.length === 0) {
    console.log("没有需要生成的幻灯片（所有图片均已存在）。");
    return;
  }

  console.log(`找到 ${tasks.length} 张待生成的幻灯片`);
  console.log(`模型：${MODEL}`);
  console.log(`尺寸：${size}`);
  console.log("");

  let totalSuccess = 0;
  let totalFailed = 0;

  for (let i = 0; i < tasks.length; i += batchSize) {
    const batch = tasks.slice(i, i + batchSize);
    console.log(`--- 批次 ${Math.floor(i / batchSize) + 1}/${Math.ceil(tasks.length / batchSize)} ---`);

    const result = await processBatch(batch, apiKey, size);
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
