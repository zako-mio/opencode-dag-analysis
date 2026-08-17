# -*- coding: utf-8 -*-
"""
S3f: 修正拓扑分层 — out_deg Kahn（源头=Layer 0）
边语义: from=依赖方, to=被依赖方（A→B 表示 A 依赖 B）
分层规则: out_deg=0（不依赖任何内部包的源头）→ Layer 0，逐层向外
修复: official/diff/modified-dag.json 的 layer 字段
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

DATA = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\01-dag-data"

def relayer(nodes, edges):
    """out_deg Kahn：from=依赖方, to=被依赖方"""
    out_deg = {n["id"]: 0 for n in nodes}
    adj_in = {n["id"]: [] for n in nodes}  # 指向该节点的边（被谁依赖）
    for e in edges:
        if e["from"] in out_deg and e["to"] in out_deg:
            out_deg[e["from"]] += 1
            adj_in[e["to"]].append(e["from"])
    layer = {}
    frontier = [nid for nid, d in out_deg.items() if d == 0]
    l = 0
    while frontier:
        for nid in frontier:
            layer[nid] = l
        nxt = []
        for nid in frontier:
            for src in adj_in[nid]:
                out_deg[src] -= 1
                if out_deg[src] == 0:
                    nxt.append(src)
        frontier = nxt
        l += 1
    if len(layer) != len(nodes):
        for n in nodes:
            if n["id"] not in layer:
                layer[n["id"]] = l
    return layer

for fn in ("official-dag.json", "diff-dag.json", "modified-dag.json"):
    fp = os.path.join(DATA, fn)
    with open(fp, encoding="utf-8") as f:
        dag = json.load(f)
    lm = relayer(dag["nodes"], dag["edges"])
    for n in dag["nodes"]:
        n["layer"] = lm.get(n["id"], 0)
    dag["stats"]["layers"] = max(lm.values()) + 1
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(dag, f, ensure_ascii=False, indent=2)
    print(f"{fn}: layers={dag['stats']['layers']}")

# 验证
with open(os.path.join(DATA, "official-dag.json"), encoding="utf-8") as f:
    d = json.load(f)
print("\nlayer 0:", sorted([n["id"] for n in d["nodes"] if n["layer"] == 0]))
print("layer 5:", sorted([n["id"] for n in d["nodes"] if n["layer"] == d["stats"]["layers"] - 1]))
