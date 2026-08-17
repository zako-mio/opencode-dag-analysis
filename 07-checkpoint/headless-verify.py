# -*- coding: utf-8 -*-
"""
S5b: headless + VLM 验证 opencode DAG 交互图渲染
验证: 三个交互视图 DOM 节点数 + 截图 + 节点页五段
"""
import sys, json, subprocess

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
INT = BASE + r"\04-interactive"
NODES = BASE + r"\02-nodes"

import os

def run_harness(py_code):
    """通过 browser-harness 执行 Python 代码"""
    p = subprocess.run(
        ["browser-harness.exe"],
        input=py_code,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=90,
    )
    return p.stdout, p.stderr

# 1. 启动 Chrome（若未运行）
subprocess.run(
    ["powershell", "-ExecutionPolicy", "Bypass", "-File", os.path.expanduser(r"~\.config\opencode\scripts\chrome-debug.ps1")],
    capture_output=True, timeout=30,
)

results = []

# 2. 验证三个视图
views = [
    ("view-official.html", "official", 35),
    ("view-diff.html", "diff", 43),
    ("view-modified.html", "modified", 104),
]
for fname, name, exp_nodes in views:
    url = "file:///" + os.path.join(INT, fname).replace("\\", "/")
    py = f"""
from browser_harness import *
new_tab("{url}")
wait_for_load()
import time
time.sleep(3)
# 等 cytoscape 渲染
info = js("() => {{ const cy = window.cy; return cy ? cy.nodes().length : -1; }}")
print("NODES:" + str(info))
"""
    out, err = run_harness(py)
    m_nodes = None
    for line in out.splitlines():
        if line.startswith("NODES:"):
            m_nodes = int(line.split(":")[1])
    results.append((name, exp_nodes, m_nodes, out[-300:] if out else "", err[-200:] if err else ""))

for name, exp, got, out, err in results:
    status = "✅" if got == exp else "❌"
    print(f"{status} {name}: expected={exp} got={got}")
    if got != exp:
        print(f"  out tail: {out}")
        print(f"  err: {err}")

# 3. 截图三图（供 VLM 参考）
for fname, name in views:
    url = "file:///" + os.path.join(INT, fname).replace("\\", "/")
    shot_path = os.path.join(BASE, "07-checkpoint", f"shot-{name}.png")
    py = f"""
from browser_harness import *
new_tab("{url}")
wait_for_load()
import time
time.sleep(4)
capture_screenshot("{shot_path}")
print("SHOT_OK")
"""
    out, err = run_harness(py)
    print(f"  screenshot {name}: {'OK' if 'SHOT_OK' in out else 'FAIL'}")

# 4. 验证一个节点页（五段）
node_url = "file:///" + os.path.join(NODES, "oc-opencode.html").replace("\\", "/")
py = f"""
from browser_harness import *
new_tab("{node_url}")
wait_for_load()
import time
time.sleep(2)
h = js("() => document.querySelectorAll('h2').length")
print("H2:" + str(h))
text = js("() => document.body.innerText.slice(0, 200)")
print("TEXT:" + text)
"""
out, err = run_harness(py)
h2 = None
for line in out.splitlines():
    if line.startswith("H2:"):
        h2 = int(line.split(":")[1])
print(f"✅ node page h2 sections: {h2}" if h2 and h2 >= 4 else f"❌ node page h2: {h2}")
if h2 is None:
    print("  err:", err[-300:])

print("\n=== S5b headless 验证完成 ===")
