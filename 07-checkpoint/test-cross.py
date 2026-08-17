# -*- coding: utf-8 -*-
"""对照测试：official 页面 + diff 数据"""
import os, re, subprocess, sys, json
sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\04-interactive"

# 读 official 页面
off = open(os.path.join(BASE, "view-official.html"), encoding="utf-8").read()
off_m = re.search(r"const DATA = (\{.*?\});\nconst GROUP_COLORS", off, re.S)
off_data = json.loads(off_m.group(1))

# 读 diff 页面数据
diff = open(os.path.join(BASE, "view-diff.html"), encoding="utf-8").read()
diff_m = re.search(r"const DATA = (\{.*?\});\nconst GROUP_COLORS", diff, re.S)
diff_data = json.loads(diff_m.group(1))

# 测试1: official 页面 + diff 全部节点（43）
t1 = off.replace(off_m.group(1), json.dumps(diff_data, ensure_ascii=False))
t1_fp = os.path.join(BASE, "_test_official_with_diff_data.html")
with open(t1_fp, "w", encoding="utf-8") as f:
    f.write(t1)

# 测试2: official 页面 + official 数据但加 mod 类
off_data2 = json.loads(json.dumps(off_data))
for n in off_data2["nodes"][:10]:
    n["classes"] = (n.get("classes", "") + " mod").strip()
t2 = off.replace(off_m.group(1), json.dumps(off_data2, ensure_ascii=False))
t2_fp = os.path.join(BASE, "_test_official_with_mod_class.html")
with open(t2_fp, "w", encoding="utf-8") as f:
    f.write(t2)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for fp, label in [(t1_fp, "official-page+diff-data"), (t2_fp, "official-page+mod-class")]:
    url = "file:///" + fp.replace(chr(92), "/")
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--virtual-time-budget=15000", "--dump-dom", url],
                       capture_output=True, timeout=90)
    out = r.stdout.decode("utf-8", errors="replace")
    zc = re.findall(r'id="zcount">([^<]*)<', out)
    print(f"{label}: zcount={zc}")
