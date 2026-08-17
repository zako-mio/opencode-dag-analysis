# -*- coding: utf-8 -*-
"""截图验证官方包和外部服务页"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
OUT = os.path.join(BASE, "07-checkpoint", "screenshots")

for pid, label in [("oc-core", "pkg-core"), ("ext-deepseek-api", "ext-deepseek"), ("skill-openspec-propose", "asm-propose")]:
    fp = os.path.join(BASE, "02-nodes", f"{pid}.html")
    url = "file:///" + fp.replace(chr(92), "/")
    shot = os.path.join(OUT, f"final2-{label}.png")
    r = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=10000", f"--screenshot={shot}", "--window-size=1200,1800", url],
        capture_output=True, timeout=60)
    size = os.path.getsize(shot) if os.path.exists(shot) else 0
    print(f"{pid}: {size} bytes")
