# -*- coding: utf-8 -*-
"""DOM 验证外部服务页内容"""
import os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"

fp = os.path.join(BASE, "02-nodes", "ext-deepseek-api.html")
url = "file:///" + fp.replace(chr(92), "/")
r = subprocess.run(
    [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
     "--virtual-time-budget=8000", "--dump-dom", url],
    capture_output=True, timeout=60)
out = r.stdout.decode("utf-8", errors="replace")
checks = {
    "title": "<title>DeepSeek API · opencode DAG</title>" in out or "DeepSeek" in out,
    "why-label": "为什么需要" in out,
    "how-label": "怎么接入" in out,
    "current": "当前状态" in out,
    "usage": "装配层调用" in out,
    "h2-count>=6": len(re.findall(r"<h2>", out)) >= 6,
}
for k, v in checks.items():
    print(f"{'OK' if v else 'FAIL'} {k}")
print(f"h2 count: {len(re.findall(r'<h2>', out))}")
