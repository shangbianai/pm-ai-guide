#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
import urllib.request


def main():
    parser = argparse.ArgumentParser(description="Generate an image with Ark Seedream/image2.")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--model", default="doubao-seedream-5-0-260128")
    parser.add_argument("--size", default="2K")
    parser.add_argument("--format", default="png", choices=["png", "jpeg", "webp"])
    args = parser.parse_args()

    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("ARK_API_KEY is required.", file=sys.stderr)
        return 2

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "output_format": args.format,
        "watermark": False,
    }
    request = urllib.request.Request(
        "https://ark.cn-beijing.volces.com/api/v3/images/generations",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    item = result.get("data", [{}])[0]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    if item.get("b64_json"):
        with open(args.out, "wb") as file:
            file.write(base64.b64decode(item["b64_json"]))
    elif item.get("url"):
        urllib.request.urlretrieve(item["url"], args.out)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
