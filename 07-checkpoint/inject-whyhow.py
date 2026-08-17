# -*- coding: utf-8 -*-
"""
S4d: 内容深化 — 节点页七段 + 主页面全面升级
数据源: stage-03-whyhow-*.json（61 装配组件 why/how）+ 已有五段数据
输出: 更新 02-nodes/*.html（装配层加 ⑤为什么 ⑥怎么用）+ index.html 全面升级
"""
import json, os, sys, html

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")
CKPT = os.path.join(BASE, "07-checkpoint")
NODES = os.path.join(BASE, "02-nodes")

def load(fp, sig=False):
    with open(fp, encoding="utf-8-sig" if sig else "utf-8") as f:
        return json.load(f)

# ============ 读入 why/how 数据 ============
whyhow = {}
for fn in ("stage-03-whyhow-skills-a.json", "stage-03-whyhow-skills-b.json", "stage-03-whyhow-core.json"):
    data = load(os.path.join(CKPT, fn), sig=True)
    for item in data:
        iid = item.get("id", "")
        if iid:
            whyhow[iid] = item
print(f"whyhow components: {len(whyhow)}")

# 读 modified-dag（节点元数据）
with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    dag = json.load(f)
node_by_id = {n["id"]: n for n in dag["nodes"]}

# 读历史事件（主页面时间线）
with open(os.path.join(CKPT, "s2-assembly-semantics.json"), encoding="utf-8") as f:
    asm = json.load(f)
history = asm["history"]

def esc(s):
    return html.escape(str(s))

def list_html(x):
    if isinstance(x, list):
        return "<br>".join(f"· {esc(i)}" for i in x)
    return esc(x)

# ============ 为装配节点注入 why/how 到 modified-dag（供节点页生成） ============
injected = 0
for n in dag["nodes"]:
    nid = n["id"]
    if nid in whyhow:
        wh = whyhow[nid]
        n["why_history"] = wh.get("why_history", "")
        n["why_current"] = wh.get("why_current", "")
        n["how_trigger"] = wh.get("how_trigger", "")
        n["how_workflow"] = wh.get("how_workflow", "")
        n["how_collaboration"] = wh.get("how_collaboration", "")
        injected += 1
print(f"injected whyhow into {injected} nodes")

with open(os.path.join(DATA, "modified-dag.json"), "w", encoding="utf-8") as f:
    json.dump(dag, f, ensure_ascii=False, indent=2)
print("modified-dag.json updated with why/how")
