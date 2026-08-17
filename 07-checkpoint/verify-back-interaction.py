# -*- coding: utf-8 -*-
"""功能验证：oc-core 组级视图下钻/返回交互"""
import os, subprocess, sys, threading, http.server, socketserver, time

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
os.chdir(BASE)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

srv = socketserver.TCPServer(("127.0.0.1", 8768), QuietHandler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

def run_harness(py_code, timeout=45):
    p = subprocess.run(
        ["browser-harness.exe"],
        input=py_code,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    return p.stdout, p.stderr

url = "http://127.0.0.1:8768/02-nodes/oc-core.html"
py = (
    "from browser_harness import *\n"
    f'new_tab("{url}")\n'
    "wait_for_load()\n"
    "import time\n"
    "time.sleep(4)\n"
    # 1. 初始状态：返回按钮隐藏
    "r1 = js(\"document.getElementById('int-back-oc-core').style.display\")\n"
    "print('BACK_INITIAL:' + str(r1))\n"
    # 2. 触发组节点点击（找到第一个 grp 节点并触发 tap）
    "r2 = js(\"(() => { const cy = window.cyoc_core; if (!cy) return 'no-cy'; const grp = cy.nodes('.grp').first(); if (!grp) return 'no-grp'; grp.trigger('tap'); return 'tapped:' + grp.data('name'); })()\")\n"
    "print('TAP:' + str(r2))\n"
    "time.sleep(2)\n"
    # 3. 下钻后：返回按钮应显示
    "r3 = js(\"document.getElementById('int-back-oc-core').style.display\")\n"
    "print('BACK_AFTER_DRILL:' + str(r3))\n"
    # 4. 下钻后节点数（模块级）
    "r4 = js(\"(() => { const cy = window.cyoc_core; return cy ? cy.nodes().length : -1; })()\")\n"
    "print('NODES_AFTER_DRILL:' + str(r4))\n"
    # 5. 面包屑
    "r5 = js(\"document.getElementById('int-crumb-oc-core').textContent\")\n"
    "print('CRUMB:' + str(r5))\n"
    # 6. 点击返回按钮
    "r6 = js(\"document.getElementById('int-back-oc-core').click()\")\n"
    "print('CLICK_BACK:' + str(r6))\n"
    "time.sleep(2)\n"
    # 7. 返回后：按钮隐藏 + 组级节点数恢复
    "r7 = js(\"document.getElementById('int-back-oc-core').style.display\")\n"
    "print('BACK_AFTER_RETURN:' + str(r7))\n"
    "r8 = js(\"(() => { const cy = window.cyoc_core; return cy ? cy.nodes().length : -1; })()\")\n"
    "print('NODES_AFTER_RETURN:' + str(r8))\n"
    "r9 = js(\"document.getElementById('int-crumb-oc-core').textContent\")\n"
    "print('CRUMB_AFTER_RETURN:' + str(r9))\n"
)
out, err = run_harness(py)
for line in out.splitlines():
    if line.startswith(("BACK_INITIAL:", "TAP:", "BACK_AFTER_DRILL:", "NODES_AFTER_DRILL:", "CRUMB:", "CLICK_BACK:", "BACK_AFTER_RETURN:", "NODES_AFTER_RETURN:", "CRUMB_AFTER_RETURN:")):
        print(line)
if err.strip():
    print("STDERR:", err[-300:])

srv.shutdown()
print("=== done ===")
