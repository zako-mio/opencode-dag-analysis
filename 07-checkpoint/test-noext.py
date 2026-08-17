# -*- coding: utf-8 -*-
"""测试：diff 图去掉 external 节点后能否渲染"""
import os, re, subprocess, sys, json
sys.stdout.reconfigure(encoding="utf-8")

# 读 diff HTML，去掉 external 节点
fp = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\04-interactive\view-diff.html"
content = open(fp, encoding="utf-8").read()
m = re.search(r"const DATA = (\{.*?\});\nconst GROUP_COLORS", content, re.S)
data = json.loads(m.group(1))
# 去掉 external
kept = [n for n in data["nodes"] if "ext" not in n.get("classes", "")]
print(f"orig={len(data['nodes'])} kept={len(kept)}")
data["nodes"] = kept
# 生成测试页
test = content.replace(m.group(1), json.dumps(data, ensure_ascii=False))
test_fp = os.path.join(r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\04-interactive", "_test_noext.html")
with open(test_fp, "w", encoding="utf-8") as f:
    f.write(test)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
url = "file:///" + test_fp.replace(chr(92), "/")
r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--virtual-time-budget=15000", "--dump-dom", url],
                   capture_output=True, timeout=90)
out = r.stdout.decode("utf-8", errors="replace")
zc = re.findall(r'id="zcount">([^<]*)<', out)
print("no-ext zcount:", zc)
