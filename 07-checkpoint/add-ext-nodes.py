# -*- coding: utf-8 -*-
"""
S3h: 补全 modified 图的外部服务节点（动态添加匹配到的 ext-* 节点）
外部节点从边的 from 中自动收集（不在节点清单的补建）
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

DATA = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\01-dag-data"

fp = os.path.join(DATA, "modified-dag.json")
with open(fp, encoding="utf-8") as f:
    dag = json.load(f)

nids = {n["id"] for n in dag["nodes"]}

# 收集边中引用但节点不存在的 id
missing = {}
for e in dag["edges"]:
    if e["from"] not in nids:
        missing.setdefault(e["from"], {"kind": "external", "count": 0})
        missing[e["from"]]["count"] += 1
    if e["to"] not in nids:
        missing.setdefault(e["to"], {"kind": "external", "count": 0})
        missing[e["to"]]["count"] += 1

# 外部节点显示名映射
EXT_NAMES = {
    "ext-bun": "Bun 运行时", "ext-typescript": "TypeScript", "ext-dotnet": ".NET SDK",
    "ext-openxml": "OpenXML", "ext-python": "Python", "ext-gh": "GitHub CLI",
    "ext-openspec-cli": "OpenSpec CLI", "ext-node": "Node.js", "ext-slack": "Slack",
    "ext-jsx-email": "JSX Email", "ext-drizzle": "Drizzle ORM", "ext-effect": "Effect",
    "ext-solid": "SolidJS", "ext-yargs": "yargs", "ext-hono": "Hono",
    "ext-opentui": "OpenTUI", "ext-vite": "Vite", "ext-astro": "Astro",
    "ext-electron": "Electron", "ext-cloudflare": "Cloudflare", "ext-effect-platform": "Effect Platform",
    "ext-acorn": "acorn", "ext-lark-cli": "lark-cli",
}

added = []
for mid, info in missing.items():
    if mid in nids:
        continue
    dag["nodes"].append({
        "id": mid,
        "name": EXT_NAMES.get(mid, mid),
        "short": EXT_NAMES.get(mid, mid),
        "group": "X-外部服务",
        "group_name": "X-外部服务",
        "kind": "external",
        "layer_type": "external",
        "implementation": f"外部服务（被 {info['count']} 个装配组件依赖）",
        "provides": "",
        "layer": 0,
        "status": "external",
    })
    nids.add(mid)
    added.append(mid)

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

dag["stats"]["nodes"] = len(dag["nodes"])
dag["stats"]["layers"] = max(lm.values()) + 1
dag["stats"]["groups"] = len(set(n["group"] for n in dag["nodes"]))
dag["stats"]["ext_nodes"] = sum(1 for n in dag["nodes"] if n.get("layer_type") == "external")

with open(fp, "w", encoding="utf-8") as f:
    json.dump(dag, f, ensure_ascii=False, indent=2)

print(f"added {len(added)} external nodes: {added}")
print(f"modified stats: nodes={dag['stats']['nodes']} edges={dag['stats']['edges']} layers={dag['stats']['layers']} ext={dag['stats']['ext_nodes']}")
