#!/usr/bin/env python3
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def find_chrome():
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
    ]
    return next((x for x in candidates if x and Path(x).exists()), None)


def main():
    if len(sys.argv) != 3:
        print("Usage: capture_report.py input.html output.png", file=sys.stderr)
        return 2
    chrome = find_chrome()
    if not chrome:
        print("ERROR Chrome/Chromium not found", file=sys.stderr)
        return 1
    source, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="research-report-") as profile:
        result = subprocess.run([
            chrome, "--headless=new", "--disable-gpu", "--no-first-run",
            f"--user-data-dir={profile}", f"--screenshot={output}",
            "--window-size=1440,1800", f"file://{source}"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    if not output.exists() or output.stat().st_size == 0:
        print(result.stderr, file=sys.stderr)
        return 1
    print(f"WROTE {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
