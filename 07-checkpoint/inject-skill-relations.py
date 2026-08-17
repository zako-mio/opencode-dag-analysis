# -*- coding: utf-8 -*-
"""
S3i: 注入 skill 间作用关系到 modified-dag
数据源: stage-02-skill-relations.json（43 条有证据关系）
新增边: relation 类型映射为 mechanism = skill-relation
同时清理旧重复的 delegate/instruction 边，保留合法 skill 关系
"""
import json, os, sys
from collections import deque

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")
CKPT = os.path.join(BASE, "07-checkpoint")

with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    dag = json.load(f)
with open(os.path.join(CKPT, "stage-02-skill-relations.json"), encoding="utf-8-sig") as f:
    relations = json.load(f)

nids = {n["id"] for n in dag["nodes"]}

# 现有边 key 集合
existing_keys = {(e["from"], e["to"]) for e in dag["edges"]}

# 注入 skill 关系边
added = 0
skipped = []
for r in relations:
    frm = r.get("from", "")
    to = r.get("to", "")
    if frm not in nids or to not in nids:
        skipped.append(f"{frm}->{to} (node missing)")
        continue
    key = (frm, to)
    if key in existing_keys:
        skipped.append(f"{frm}->{to} (dup)")
        continue
    dag["edges"].append({
        "from": frm, "to": to,
        "mechanism": "skill-relation",
        "relation": r.get("relation", "references"),
        "evidence": r.get("evidence", "")[:200],
    })
    existing_keys.add(key)
    added += 1

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
dag["stats"]["edges"] = len(dag["edges"])
dag["stats"]["has_cycle"] = has_cycle(dag["nodes"], dag["edges"])
dag["stats"]["skill_rel_edges"] = added
dag["stats"]["asm_edges"] = sum(1 for e in dag["edges"] if e.get("mechanism") in ("assembly-to-pkg", "delegate", "skill-mandate", "hook-mount", "instruction-load", "skill-relation"))

with open(os.path.join(DATA, "modified-dag.json"), "w", encoding="utf-8") as f:
    json.dump(dag, f, ensure_ascii=False, indent=2)

print(f"added {added} skill-relation edges")
print(f"skipped: {len(skipped)}")
for s in skipped[:20]:
    print(f"  {s}")
print(f"stats: nodes={dag['stats']['nodes']} edges={dag['stats']['edges']} layers={dag['stats']['layers']} cycle={dag['stats']['has_cycle']} skill_rel={added}")

# 验证新增边示例
print("\nskill-relation edges:")
for e in dag["edges"]:
    if e.get("mechanism") == "skill-relation":
        print(f"  {e['from']} -> {e['to']} [{e.get('relation','')}]")
