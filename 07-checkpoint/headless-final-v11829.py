# -*- coding: utf-8 -*-
"""S8b: headless Chromium 验证 opencode DAG 交互图（Linux/WSL 适配版 v1.18.29）
1. --dump-dom 三视图: zcount == 期望节点数（cytoscape layoutstop 后更新）
2. --screenshot 三视图截图（供 VLM 验证）
"""
import os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")

BASE = "/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag"
INT = os.path.join(BASE, "04-interactive")
OUT = os.path.join(BASE, "07-checkpoint", "screenshots")
os.makedirs(OUT, exist_ok=True)
CHROME = "chromium-browser"

def run_chrome(url, dump=True, shot=None, wait_ms=8000):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--virtual-time-budget={wait_ms}", "--hide-scrollbars"]
    if dump:
        cmd.append("--dump-dom")
    if shot:
        cmd.append(f"--screenshot={shot}")
        cmd.append("--window-size=1920,1080")
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, timeout=120)
    out = r.stdout.decode("utf-8", errors="replace") if r.stdout else ""
    # dump-dom 输出在 stdout；截图时 stdout 可能是警告日志
    return out

views = [
    ("view-official.html", "official", 36),
    ("view-diff.html", "diff", 46),
    ("view-modified.html", "modified", 119),
]

all_ok = True
for fname, name, exp in views:
    url = f"file:///{os.path.join(INT, fname)}"
    dom = run_chrome(url, dump=True, wait_ms=8000)
    m = re.search(r'id="zcount">([^<]*)<', dom)
    got = int(m.group(1)) if m and m.group(1).strip().isdigit() else None
    ok = got == exp
    all_ok = all_ok and ok
    print(f"{'OK ' if ok else 'FAIL'} {name}: zcount={got} expected={exp}")

# 截图三视图
for fname, name, exp in views:
    url = f"file:///{os.path.join(INT, fname)}"
    shot = os.path.join(OUT, f"final-v11829-{name}.png")
    run_chrome(url, dump=False, shot=shot, wait_ms=12000)
    size = os.path.getsize(shot) if os.path.exists(shot) else 0
    print(f"shot {name}: {size} bytes {'OK' if size > 20000 else 'TOO SMALL'}")

# 节点页五段验证
node_url = f"file:///{os.path.join(BASE, '02-nodes', 'oc-opencode.html')}"
dom = run_chrome(node_url, dump=True, wait_ms=5000)
h2_count = len(re.findall(r"<h2>", dom))
print(f"node page oc-opencode: h2 sections={h2_count} {'OK' if h2_count >= 4 else 'FAIL'}")
all_ok = all_ok and h2_count >= 4

print("\n=== " + ("ALL OK" if all_ok else "HAS FAILURES") + " ===")
