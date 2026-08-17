# -*- coding: utf-8 -*-
"""
S3d: 重建 diff-dag（使用修正后的装配层边）
基于 modified-dag 的最终边，重算 diff 图（官方 + 改造染色 + 外部）
输出: 更新 01-dag-data/diff-dag.json
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")

with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    mod = json.load(f)
with open(os.path.join(DATA, "official-dag.json"), encoding="utf-8") as f:
    off = json.load(f)

# 装配层节点（mod 中 layer_type=assembly）
asm_nodes = [n for n in mod["nodes"] if n.get("layer_type") == "assembly"]
ext_nodes = [n for n in mod["nodes"] if n.get("layer_type") == "external"]

# 被装配层引用的包
asm_to_pkg = [e for e in mod["edges"] if e.get("mechanism") == "assembly-to-pkg"]
used_pkgs = set(e["from"] for e in asm_to_pkg)

# diff 节点：官方包（official/modified 染色）+ 外部服务
diff_nodes = []
for n in off["nodes"]:
    nn = dict(n)
    nn["status"] = "modified" if n["id"] in used_pkgs else "official"
    diff_nodes.append(nn)
for en in ext_nodes:
    en2 = dict(en)
    en2["status"] = "external"
    diff_nodes.append(en2)

# diff 边：官方边 + 外部服务边
diff_edges = [dict(e) for e in off["edges"]]
for e in mod["edges"]:
    if e.get("mechanism") == "external" and e["from"] in {en["id"] for en in ext_nodes} and e["to"] in {n["id"] for n in diff_nodes}:
        diff_edges.append(e)
    if e.get("mechanism") == "assembly-to-pkg":
        diff_edges.append(e)

# 去重
seen = set()
dedup = []
for e in diff_edges:
    key = (e["from"], e["to"], e.get("mechanism", ""))
    if key in seen:
        continue
    seen.add(key)
    dedup.append(e)

# 拓扑 + 无环
def topo_layer(nodes, edges):
    in_deg = {n["id"]: 0 for n in nodes}
    adj = {n["id"]: [] for n in nodes}
    for e in edges:
        if e["from"] in in_deg and e["to"] in in_deg:
            in_deg[e["to"]] += 1
            adj[e["from"]].append(e["to"])
    layer = {}
    frontier = [nid for nid, d in in_deg.items() if d == 0]
    l = 0
    while frontier:
        for nid in frontier:
            layer[nid] = l
        nxt = []
        for nid in frontier:
            for to in adj[nid]:
                in_deg[to] -= 1
                if in_deg[to] == 0:
                    nxt.append(to)
        frontier = nxt
        l += 1
    if len(layer) != len(nodes):
        for nid in nodes:
            if nid["id"] not in layer:
                layer[nid["id"]] = l
    return layer

def has_cycle(nodes, edges):
    in_deg = {n["id"]: 0 for n in nodes}
    adj = {n["id"]: [] for n in nodes}
    for e in edges:
        if e["from"] in in_deg and e["to"] in in_deg:
            in_deg[e["to"]] += 1
            adj[e["from"]].append(e["to"])
    from collections import deque
    q = deque([nid for nid, d in in_deg.items() if d == 0])
    visited = 0
    while q:
        n = q.popleft()
        visited += 1
        for to in adj[n]:
            in_deg[to] -= 1
            if in_deg[to] == 0:
                q.append(to)
    return visited != len(nodes)

layer_map = topo_layer(diff_nodes, dedup)
for n in diff_nodes:
    n["layer"] = layer_map.get(n["id"], 0)

diff_dag = {
    "name": "diff",
    "title": "官方 + 改造对比 DAG（改造点染色）",
    "version_note": "官方 v1.18.14 基线；改造点 = ~/.config/opencode 装配层引用（修改黄/外部绿）",
    "nodes": diff_nodes,
    "edges": dedup,
    "groups": list(dict.fromkeys(n["group"] for n in diff_nodes)),
    "stats": {
        "nodes": len(diff_nodes),
        "edges": len(dedup),
        "layers": max(layer_map.values()) + 1,
        "groups": len(set(n["group"] for n in diff_nodes)),
        "has_cycle": has_cycle(diff_nodes, dedup),
        "modified_pkgs": len(used_pkgs),
        "official_pkgs": sum(1 for n in diff_nodes if n["status"] == "official"),
        "external_nodes": sum(1 for n in diff_nodes if n["status"] == "external"),
    },
}

with open(os.path.join(DATA, "diff-dag.json"), "w", encoding="utf-8") as f:
    json.dump(diff_dag, f, ensure_ascii=False, indent=2)
print("diff updated:", json.dumps(diff_dag["stats"], ensure_ascii=False))
print("modified packages:", sorted(used_pkgs))
