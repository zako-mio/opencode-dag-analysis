# -*- coding: utf-8 -*-
"""
S3g: 过滤悬空边（引用不存在节点的边）+ 重算拓扑 + 无环
修复: official/diff/modified-dag.json
"""
import json, os, sys
from collections import deque

sys.stdout.reconfigure(encoding="utf-8")

DATA = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\01-dag-data"

def clean_dag(dag):
    nids = {n["id"] for n in dag["nodes"]}
    removed = []
    kept = []
    for e in dag["edges"]:
        if e["from"] not in nids or e["to"] not in nids:
            removed.append(e)
        else:
            kept.append(e)
    dag["edges"] = kept

    # 重算拓扑
    def topo_layer(nodes, edges):
        out_deg = {n["id"]: 0 for n in nodes}
        adj_in = {n["id"]: [] for n in nodes}
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

    def has_cycle(nodes, edges):
        in_deg = {n["id"]: 0 for n in nodes}
        adj = {n["id"]: [] for n in nodes}
        for e in edges:
            if e["from"] in in_deg and e["to"] in in_deg:
                in_deg[e["to"]] += 1
                adj[e["from"]].append(e["to"])
        q = deque([nid for nid, d in in_deg.items() if d == 0])
        visited = 0
        while q:
            n = q.popleft()
            visited += 1
            for to in adj[n]:
                in_deg[to] -= 1
                if in_deg[to] == 0:
                    q.append(to)
        return visited != len(nids)

    lm = topo_layer(dag["nodes"], dag["edges"])
    for n in dag["nodes"]:
        n["layer"] = lm.get(n["id"], 0)
    dag["stats"]["layers"] = max(lm.values()) + 1
    dag["stats"]["edges"] = len(kept)
    dag["stats"]["has_cycle"] = has_cycle(dag["nodes"], dag["edges"])
    return removed

for fn in ("official-dag.json", "diff-dag.json", "modified-dag.json"):
    fp = os.path.join(DATA, fn)
    with open(fp, encoding="utf-8") as f:
        dag = json.load(f)
    removed = clean_dag(dag)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(dag, f, ensure_ascii=False, indent=2)
    print(f"{fn}: removed {len(removed)} dangling edges, edges={len(dag['edges'])}, layers={dag['stats']['layers']}, cycle={dag['stats']['has_cycle']}")
    for e in removed[:20]:
        print(f"  removed: {e['from']} -> {e['to']} [{e.get('mechanism','')}]")
