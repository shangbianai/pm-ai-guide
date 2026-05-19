#!/usr/bin/env python3
"""pm-slide-deck: 幻灯片图片生成脚本（Python 版）

支持四种后端：doubao / openai / gemini / grsai
默认并发数 5，通过 --batch-size 调整

用法：
    python generate-slides.py <提示词目录> [--output-dir 输出目录] [--size 尺寸] [--batch-size N] [--retry] [--backend doubao|openai|gemini|grsai]

示例：
    python generate-slides.py prompts/
    python generate-slides.py prompts/ --output-dir ../output --batch-size 5 --backend doubao
"""

import argparse
import base64
import json
import os
import re
import shutil
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

BACKEND_CONFIG = {
    "doubao": {
        "api_url": "https://ark.cn-beijing.volces.com/api/v3/images/generations",
        "model": "doubao-seedream-5-0-260128",
        "label": "豆包 Seedream",
    },
    "openai": {
        "api_url": "https://api.openai.com/v1/images/generations",
        "model": "gpt-image-2",
        "label": "OpenAI GPT-image-2",
    },
    "gemini": {
        "api_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent",
        "model": "gemini-2.0-flash-exp",
        "label": "Gemini 2.0 Flash Exp",
    },
    "grsai": {
        "api_url": "https://grsai.dakka.com.cn/v1/api/generate",
        "model": "gpt-image-2",
        "label": "Grsai GPT-image-2（国内节点）",
    },
}

OPENAI_SUPPORTED_SIZES = ["1024x1024", "1536x1024", "1024x1536"]
DEFAULT_SIZE = "1672x941"
FALLBACK_SIZE = "1536x1024"


def load_env():
    env = {}
    candidates = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent.parent.parent / ".env",
        Path(__file__).resolve().parent.parent / ".env",
    ]

    for p in candidates:
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                trimmed = line.strip()
                if not trimmed or trimmed.startswith("#"):
                    continue
                eq_idx = trimmed.index("=") if "=" in trimmed else -1
                if eq_idx > 0:
                    key = trimmed[:eq_idx].strip()
                    val = trimmed[eq_idx + 1:].strip()
                    if (val.startswith('"') and val.endswith('"')) or (
                        val.startswith("'") and val.endswith("'")
                    ):
                        val = val[1:-1]
                    env[key] = val
            break

    for k, v in os.environ.items():
        env[k] = v

    return env


def get_api_key(env, backend):
    if backend == "doubao":
        return env.get("ARK_API_KEY") or env.get("DOUBAO_API_KEY")
    if backend == "openai":
        return env.get("OPENAI_API_KEY")
    if backend == "gemini":
        return env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY")
    if backend == "grsai":
        return env.get("GRSAI_API_KEY")
    return None


def print_api_key_hint(backend):
    hints = {
        "doubao": "请在 .env 文件中设置 ARK_API_KEY 或 DOUBAO_API_KEY\n获取方式：https://console.volcengine.com/ark",
        "openai": "请设置 OPENAI_API_KEY\n获取方式：https://platform.openai.com/api-keys",
        "gemini": "请设置 GEMINI_API_KEY 或 GOOGLE_API_KEY\n获取方式：https://aistudio.google.com/apikey",
        "grsai": "请设置 GRSAI_API_KEY\n获取方式：联系 Grsai 平台获取 API Key",
    }
    print(hints.get(backend, ""), file=sys.stderr)


def api_request_json(url, headers, body, timeout=120):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def generate_image_doubao(prompt, api_key, size, config):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = {
        "model": config["model"],
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": "b64_json",
        "size": size,
        "stream": False,
        "watermark": False,
    }
    data = api_request_json(config["api_url"], headers, body)
    if data.get("data") and len(data["data"]) > 0:
        item = data["data"][0]
        if item.get("b64_json"):
            return base64.b64decode(item["b64_json"])
        if item.get("url"):
            return download_url(item["url"])
    raise RuntimeError("API 返回数据中未找到图片")


def generate_image_openai(prompt, api_key, size, config):
    actual_size = size if size in OPENAI_SUPPORTED_SIZES else FALLBACK_SIZE
    if size != actual_size:
        print(f"  OpenAI 不支持尺寸 {size}，已自动转为 {actual_size}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = {
        "model": config["model"],
        "prompt": prompt,
        "n": 1,
        "size": actual_size,
        "response_format": "b64_json",
    }
    data = api_request_json(config["api_url"], headers, body)
    if data.get("data") and len(data["data"]) > 0:
        item = data["data"][0]
        if item.get("b64_json"):
            return base64.b64decode(item["b64_json"])
        if item.get("url"):
            return download_url(item["url"])
    raise RuntimeError("API 返回数据中未找到图片")


def generate_image_gemini(prompt, api_key, config):
    url = f"{config['api_url']}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }
    data = api_request_json(url, headers, body)
    candidates = data.get("candidates", [])
    if candidates:
        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            inline = part.get("inlineData", {})
            mime = inline.get("mimeType", "")
            if mime.startswith("image/"):
                return base64.b64decode(inline["data"])
    raise RuntimeError("API 返回数据中未找到图片")


def generate_image_grsai(prompt, api_key, size, config):
    actual_size = size if size in OPENAI_SUPPORTED_SIZES else FALLBACK_SIZE
    if size != actual_size:
        print(f"  Grsai 不支持尺寸 {size}，已自动转为 {actual_size}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = {
        "model": config["model"],
        "prompt": prompt,
        "images": [],
        "aspectRatio": actual_size,
        "replyType": "json",
    }
    data = api_request_json(config["api_url"], headers, body, timeout=180)
    if data.get("status") == "succeeded" and data.get("results"):
        url = data["results"][0].get("url")
        if url:
            return download_url(url)
    raise RuntimeError(f"API 返回数据中未找到图片，状态：{data.get('status', 'unknown')}")


def generate_image(prompt, api_key, size, backend):
    config = BACKEND_CONFIG[backend]
    if backend == "doubao":
        return generate_image_doubao(prompt, api_key, size, config)
    if backend == "openai":
        return generate_image_openai(prompt, api_key, size, config)
    if backend == "gemini":
        return generate_image_gemini(prompt, api_key, config)
    if backend == "grsai":
        return generate_image_grsai(prompt, api_key, size, config)


def download_url(url, retries=3):
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                return resp.read()
        except Exception:
            if i == retries - 1:
                raise
    raise RuntimeError("下载失败")


def backup_if_exists(file_path):
    if not os.path.exists(file_path):
        return
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    p = Path(file_path)
    backup_path = str(p.parent / f"{p.stem}-backup-{ts}{p.suffix}")
    shutil.copy2(file_path, backup_path)
    print(f"  已备份：{Path(backup_path).name}")


def process_single_task(task, api_key, size, backend):
    prompt = Path(task["prompt_file"]).read_text(encoding="utf-8").strip()
    file_name = Path(task["output_file"]).name

    try:
        backup_if_exists(task["output_file"])
        image_data = generate_image(prompt, api_key, size, backend)
        Path(task["output_file"]).write_bytes(image_data)
        size_kb = len(image_data) // 1024
        return {"ok": True, "index": task["index"], "file": file_name, "size_kb": size_kb}
    except Exception as e:
        return {"ok": False, "index": task["index"], "file": file_name, "error": str(e)}


def discover_tasks(prompts_dir, output_dir, retry):
    prompts_path = Path(prompts_dir)
    if not prompts_path.exists():
        print(f"提示词目录不存在：{prompts_dir}", file=sys.stderr)
        sys.exit(1)

    files = sorted(
        f for f in prompts_path.iterdir()
        if re.match(r"^\d+-slide-.*\.md$", f.name, re.IGNORECASE)
    )

    if not files:
        print(f"未找到提示词文件：{prompts_dir}", file=sys.stderr)
        print("期望格式：01-slide-*.md, 02-slide-*.md 等", file=sys.stderr)
        sys.exit(1)

    tasks = []
    for f in files:
        m = re.match(r"^(\d+)-slide-.*\.md$", f.name, re.IGNORECASE)
        if not m:
            continue
        idx = int(m.group(1))
        base_name = f.stem
        output_file = str(Path(output_dir) / f"{base_name}.png")

        if not retry and os.path.exists(output_file):
            print(f"跳过（已存在）：{base_name}.png")
            continue

        tasks.append({
            "prompt_file": str(f),
            "output_file": output_file,
            "index": idx,
        })

    return tasks


def main():
    parser = argparse.ArgumentParser(description="pm-slide-deck 幻灯片图片生成")
    parser.add_argument("prompts_dir", help="提示词目录")
    parser.add_argument("--output-dir", help="输出目录（默认为提示词目录的上级）")
    parser.add_argument("--size", default=DEFAULT_SIZE, help=f"图片尺寸（默认 {DEFAULT_SIZE}，16:9）")
    parser.add_argument("--batch-size", type=int, default=5, help="并发数（默认 5，最大 8）")
    parser.add_argument("--retry", action="store_true", help="重新生成已存在的图片")
    parser.add_argument("--backend", choices=["doubao", "openai", "gemini", "grsai"], default="doubao")
    args = parser.parse_args()

    batch_size = max(1, min(8, args.batch_size))
    config = BACKEND_CONFIG[args.backend]

    env = load_env()
    api_key = get_api_key(env, args.backend)
    if not api_key:
        print(f"未找到 {config['label']} API Key。", file=sys.stderr)
        print_api_key_hint(args.backend)
        sys.exit(1)

    output_dir = args.output_dir or str(Path(args.prompts_dir).parent)
    os.makedirs(output_dir, exist_ok=True)

    tasks = discover_tasks(args.prompts_dir, output_dir, args.retry)
    if not tasks:
        print("没有需要生成的幻灯片（所有图片均已存在）。")
        return

    print(f"找到 {len(tasks)} 张待生成的幻灯片")
    print(f"后端：{config['label']} ({args.backend})")
    print(f"模型：{config['model']}")
    if args.backend != "gemini":
        print(f"尺寸：{args.size}")
    print(f"并发：{batch_size}")
    print()

    total_success = 0
    total_failed = 0

    for i in range(0, len(tasks), batch_size):
        batch = tasks[i : i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(tasks) + batch_size - 1) // batch_size
        print(f"--- 批次 {batch_num}/{total_batches}（{len(batch)} 张）---")

        with ThreadPoolExecutor(max_workers=len(batch)) as executor:
            futures = {
                executor.submit(process_single_task, t, api_key, args.size, args.backend): t
                for t in batch
            }
            for future in as_completed(futures):
                result = future.result()
                if result["ok"]:
                    print(f"  ✓ [{result['index']}] {result['file']} ({result['size_kb']} KB)")
                    total_success += 1
                else:
                    print(f"  ✗ [{result['index']}] {result['file']}：{result['error']}")
                    total_failed += 1

    print()
    print("===== 生成完成 =====")
    print(f"成功：{total_success}/{len(tasks)}")
    if total_failed > 0:
        print(f"失败：{total_failed}/{len(tasks)}")
        print("提示：使用 --retry 参数可仅重新生成失败的幻灯片")


if __name__ == "__main__":
    main()
