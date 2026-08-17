# -*- coding: utf-8 -*-
"""验证 oc-core 组级视图返回逻辑"""
import os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"

fp = os.path.join(BASE, "02-nodes", "oc-core.html")
content = open(fp, encoding="utf-8").read()

# 静态检查
checks = {
    "back-button": 'int-back-oc-core' in content,
    "back-listener": 'addEventListener' in content,
    "crumb": 'int-crumb-oc-core' in content,
    "group-elems-copy": 'GROUP_ELEMS' in content,
    "return-restore": 'GROUP_ELEMS' in content and 'add(GROUP_ELEMS' in content,
}
for k, v in checks.items():
    print(f"{'OK' if v else 'FAIL'} {k}")

# headless 验证渲染 + 交互
url = "file:///" + fp.replace(chr(92), "/")
r = subprocess.run(
    [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
     "--enable-logging=stderr", "--virtual-time-budget=12000", "--dump-dom", url],
    capture_output=True, timeout=90)
out = r.stdout.decode("utf-8", errors="replace")
err = r.stderr.decode("utf-8", errors="replace")
print("canvas:", "<canvas" in out)
print("back button in dom:", 'id="int-back-oc-core"' in out)
js_err = [l for l in err.splitlines() if "Uncaught" in l]
print("js errors:", len(js_err))
for e in js_err[:3]:
    print("  " + e[:200])
