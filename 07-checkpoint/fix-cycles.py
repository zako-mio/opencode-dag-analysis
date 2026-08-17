# -*- coding: utf-8 -*-
"""
S3j: 环修复 — 打破 modified-dag 的环
策略（0816 环修复方法论适配）:
1. skill-relation 双向边：保留 evidence 更强/语义更明确的方向，删除反向（same-family < references < workflow < mandates）
2. assembly-to-pkg 方向修正：装配依赖包（from=包, to=装配），但 skill-relation 若反向指向包则删
3. delegate 环：agent-drawio-worker -> agent-plan/build 删除（子Agent 不应反向委派主Agent）
4. 修复后重算拓扑+无环校验
"""
import json, os, sys
from collections import deque

sys.stdout.reconfigure(encoding="utf-8")

DATA = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\01-dag-data"
fp = os.path.join(DATA, "modified-dag.json")
with open(fp, encoding="utf-8") as f:
    dag = json.load(f)

nids = {n["id"] for n in dag["nodes"]}

REL_STRENGTH = {"same-family": 1, "references": 2, "workflow": 3, "mandates": 4}

def find_edge(frm, to):
    for e in dag["edges"]:
        if e["from"] == frm and e["to"] == to:
            return e
    return None

removed = []  # (index, edge, why)
# 1. skill-relation 双向去重
sr_edges = [(i, e) for i, e in enumerate(dag["edges"]) if e.get("mechanism") == "skill-relation"]
pairs = {}
for i, e in sr_edges:
    key = tuple(sorted([e["from"], e["to"]]))
    pairs.setdefault(key, []).append((i, e))

for key, items in pairs.items():
    if len(items) < 2:
        continue
    # 有双向：保留 strength 高的一条，其余删除
    ranked = sorted(items, key=lambda x: REL_STRENGTH.get(x[1].get("relation", ""), 0), reverse=True)
    keep = ranked[0]
    for i, e in ranked[1:]:
        removed.append((i, e, f"双向保留 {keep[1]['from']}->{keep[1]['to']}"))

# 2. delegate 反向环：子Agent -> 主Agent 删除
sub_agents = {"agent-pdf-worker", "agent-drawio-worker", "agent-general", "agent-explore", "agent-reflection-worker"}
main_agents = {"agent-plan", "agent-build"}
for i, e in list(enumerate(dag["edges"])):
    if e.get("mechanism") == "delegate" and e["from"] in sub_agents and e["to"] in main_agents:
        removed.append((i, e, "子Agent 不应反向委派主Agent"))

# 3. 包 -> skill 的反向 assembly-to-pkg（包不依赖 skill）
for i, e in list(enumerate(dag["edges"])):
    if e.get("mechanism") == "assembly-to-pkg":
        # from 应为包, to 应为装配；若 from 是 skill/agent（装配），to 是包，这是合法的（装配依赖包）
        # 但若 from 是包 to 是装配，则反向了（包不应依赖装配）——理论不会有，但 skill-relation 反向时可能
        pass

# 执行删除（按 index 降序）
remove_idx = sorted(set(i for i, e, why in removed), reverse=True)
for i in remove_idx:
    dag["edges"].pop(i)

# 再处理可能的残余环：迭代删除"最小语义"边直到无环（兜底）
def has_cycle_edges(edges):
    in_deg = {nid: 0 for nid in nids}
    adj = {nid: [] for nid in nids}
    for e in edges:
        if e["from"] in nids and e["to"] in nids:
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
    return visited != len(nids), visited

cyc, _ = has_cycle_edges(dag["edges"])
rounds = 0
while cyc and rounds < 20:
    rounds += 1
    # 找语义最弱的边删除
    best = None
    best_score = 999
    for i, e in enumerate(dag["edges"]):
        score = {"skill-relation": 1, "assembly-to-pkg": 2, "instruction-load": 3, "external": 4, "delegate": 4, "skill-mandate": 4, "hook-mount": 4,
                 "semantic-dep": 5, "workspace-dep": 6, "import": 6}.get(e.get("mechanism", ""), 5)
        if score < best_score:
            best_score = score
            best = i
    if best is not None:
        removed.append((best, dag["edges"][best], f"环修复兜底 round {rounds}"))
        dag["edges"].pop(best)
    cyc, _ = has_cycle_edges(dag["edges"])

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

lm = topo_layer(dag["nodes"], dag["edges"])
for n in dag["nodes"]:
    n["layer"] = lm.get(n["id"], 0)

dag["stats"]["layers"] = max(lm.values()) + 1
dag["stats"]["edges"] = len(dag["edges"])
cyc_final, _ = has_cycle_edges(dag["edges"])
dag["stats"]["has_cycle"] = cyc_final
dag["stats"]["skill_rel_edges"] = sum(1 for e in dag["edges"] if e.get("mechanism") == "skill-relation")

with open(fp, "w", encoding="utf-8") as f:
    json.dump(dag, f, ensure_ascii=False, indent=2)

print(f"removed {len(removed)} edges (unique idx {len(remove_idx)} + loop {rounds})")
print(f"final: nodes={dag['stats']['nodes']} edges={dag['stats']['edges']} layers={dag['stats']['layers']} cycle={cyc_final} skill_rel={dag['stats']['skill_rel_edges']}")
for i, e, why in removed[:20]:
    print(f"  REMOVED {e['from']}->{e['to']} [{e.get('mechanism','')}] : {why}")
