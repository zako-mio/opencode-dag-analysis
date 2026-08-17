# -*- coding: utf-8 -*-
"""验证 oc-core 组级内部 DAG 渲染"""
import os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"

# oc-core 节点页（组级视图）
for pid in ("oc-core", "oc-app", "oc-opencode"):
    fp = os.path.join(BASE, "02-nodes", f"{pid}.html")
    url = "file:///" + fp.replace(chr(92), "/")
    r = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--enable-logging=stderr", "--virtual-time-budget=12000", "--dump-dom", url],
        capture_output=True, timeout=90)
    out = r.stdout.decode("utf-8", errors="replace")
    err = r.stderr.decode("utf-8", errors="replace")
    has_int = "模块内部结构 DAG" in out
    has_canvas = "<canvas" in out
    has_group = "组级视图" in out
    js_err = [l for l in err.splitlines() if "Uncaught" in l]
    print(f"{pid}: int_dag={has_int} canvas={has_canvas} group_view={has_group} js_errors={len(js_err)}")
    for e in js_err[:3]:
        print("   " + e[:200])
