# -*- coding: utf-8 -*-
"""验证 zcount + 截图（virtual time 长）"""
import os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
INT = os.path.join(BASE, "04-interactive")
OUT = os.path.join(BASE, "07-checkpoint", "screenshots")
os.makedirs(OUT, exist_ok=True)

def run(url, shot=None, budget=15000):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--virtual-time-budget={budget}"]
    if shot:
        cmd.append(f"--screenshot={shot}")
        cmd.append("--window-size=1920,1080")
    else:
        cmd.append("--dump-dom")
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, timeout=120)
    return r.stdout.decode("utf-8", errors="replace") if r.stdout else ""

views = [
    ("view-official.html", "official", 35),
    ("view-diff.html", "diff", 43),
    ("view-modified.html", "modified", 104),
]
for fname, name, exp in views:
    url = "file:///" + os.path.join(INT, fname).replace(chr(92), "/")
    dom = run(url, budget=15000)
    zc = re.findall(r'id="zcount">([^<]*)<', dom)
    got = int(zc[0]) if zc and zc[0].strip().isdigit() else None
    ok = got == exp
    print(f"{'OK ' if ok else 'FAIL'} {name}: zcount={got} expected={exp}")

for fname, name, exp in views:
    url = "file:///" + os.path.join(INT, fname).replace(chr(92), "/")
    shot = os.path.join(OUT, f"final2-{name}.png")
    run(url, shot=shot, budget=20000)
    size = os.path.getsize(shot) if os.path.exists(shot) else 0
    print(f"shot {name}: {size} bytes")
