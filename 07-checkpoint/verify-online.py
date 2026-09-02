# -*- coding: utf-8 -*-
"""验证线上 GitHub Pages 三图渲染"""
import os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
OUT = os.path.join(BASE, "07-checkpoint", "screenshots")
os.makedirs(OUT, exist_ok=True)

views = [
    ("view-official.html", "online-official", 35),
    ("view-diff.html", "online-diff", 43),
    ("view-modified.html", "online-modified", 104),
]
for fname, label, exp in views:
    url = f"https://zako-mio.github.io/opencode-dag-analysis/04-interactive/{fname}"
    shot = os.path.join(OUT, f"{label}.png")
    r = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=20000", f"--screenshot={shot}", "--window-size=1920,1080", url],
        capture_output=True, timeout=120)
    # dump-dom 验证 zcount
    r2 = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=20000", "--dump-dom", url],
        capture_output=True, timeout=120)
    dom = r2.stdout.decode("utf-8", errors="replace")
    zc = re.findall(r'id="zcount">([^<]*)<', dom)
    got = int(zc[0]) if zc and zc[0].strip().isdigit() else None
    size = os.path.getsize(shot) if os.path.exists(shot) else 0
    status = "OK" if got == exp else "FAIL"
    print(f"{status} {label}: zcount={got} expected={exp} shot={size} bytes")
