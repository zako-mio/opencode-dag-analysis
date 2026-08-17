# -*- coding: utf-8 -*-
"""长 virtual-time 验证大图"""
import os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
INT = os.path.join(BASE, "04-interactive")

views = [
    ("view-diff.html", 43),
    ("view-modified.html", 104),
]
for fname, exp in views:
    url = "file:///" + os.path.join(INT, fname).replace(chr(92), "/")
    r = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=40000", "--dump-dom", url],
        capture_output=True, timeout=180)
    out = r.stdout.decode("utf-8", errors="replace")
    zc = re.findall(r'id="zcount">([^<]*)<', out)
    print(f"{fname}: zcount={zc} expected={exp}")
