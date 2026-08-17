# -*- coding: utf-8 -*-
"""
S3e: 统一边方向语义 — A→B 表示 A 依赖 B（from=依赖方, to=被依赖方，与 0816 一致）
修复: official-dag.json / diff-dag.json / modified-dag.json 的所有边方向
注意: 外部服务边（ext-xxx -> 装配）保持 ext 为被依赖方是对的（装配依赖外部服务）
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

DATA = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\01-dag-data"

def flip_edges(dag):
    """翻转包间边方向；external 边保持（ext 是被依赖方）"""
    new_edges = []
    for e in dag["edges"]:
        mech = e.get("mechanism", "")
        if mech == "external":
            new_edges.append(e)  # ext 是被依赖方，保持
        else:
            # 翻转: from<->to
            ne = dict(e)
            ne["from"], ne["to"] = e["to"], e["from"]
            new_edges.append(ne)
    dag["edges"] = new_edges
    return dag

for fn in ("official-dag.json", "diff-dag.json", "modified-dag.json"):
    fp = os.path.join(DATA, fn)
    with open(fp, encoding="utf-8") as f:
        dag = json.load(f)
    flip_edges(dag)
    # 重算拓扑（方向翻转后拓扑层也应重新算：被依赖方先于依赖方）
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
    lm = topo_layer(dag["nodes"], dag["edges"])
    for n in dag["nodes"]:
        n["layer"] = lm.get(n["id"], 0)
    dag["stats"]["layers"] = max(lm.values()) + 1
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(dag, f, ensure_ascii=False, indent=2)
    print(f"{fn}: flipped, edges={len(dag['edges'])}, layers={dag['stats']['layers']}")
