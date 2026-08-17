# -*- coding: utf-8 -*-
"""验证主页面渲染"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
url = "file:///" + os.path.join(BASE, "index.html").replace(chr(92), "/")
shot = os.path.join(BASE, "07-checkpoint", "screenshots", "homepage.png")
r = subprocess.run(
    [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
     "--virtual-time-budget=8000", f"--screenshot={shot}", "--window-size=1400,2400", url],
    capture_output=True, timeout=60)
size = os.path.getsize(shot) if os.path.exists(shot) else 0
print(f"homepage screenshot: {size} bytes")
