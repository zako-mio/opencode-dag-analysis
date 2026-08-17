# -*- coding: utf-8 -*-
"""
S3b: 增强装配层 → 包/外部服务 边匹配（关键词映射）
基于 depends_on_raw 自由文本 + SKILL.md 依赖信息，用关键词表映射到包/外部服务
输出: 更新 modified-dag.json 的边
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
CKPT = os.path.join(BASE, "07-checkpoint")
DATA = os.path.join(BASE, "01-dag-data")

# ============ 读入 ============
with open(os.path.join(CKPT, "s1-package-semantics.json"), encoding="utf-8") as f:
    pkg_sem = json.load(f)
with open(os.path.join(CKPT, "s2-assembly-semantics.json"), encoding="utf-8") as f:
    asm = json.load(f)
asm_comp = asm["components"]

# 包名 → 包 id
PKG_KEYWORDS = {
    "opencode": "oc-opencode", "core": "oc-core", "schema": "oc-schema",
    "llm": "oc-llm", "plugin": "oc-plugin", "sdk": "oc-sdk", "sdk-next": "oc-sdk-next",
    "server": "oc-server", "protocol": "oc-protocol", "client": "oc-client",
    "tui": "oc-tui", "ui": "oc-ui", "session-ui": "oc-session-ui", "app": "oc-app",
    "desktop": "oc-desktop", "cli": "oc-cli", "web": "oc-web", "enterprise": "oc-enterprise",
    "storybook": "oc-storybook", "codemode": "oc-codemode", "function": "oc-function",
    "http-recorder": "oc-http-recorder", "script": "oc-script",
    "effect-sqlite-node": "oc-effect-sqlite-node", "effect-drizzle-sqlite": "oc-effect-drizzle-sqlite",
    "console": "oc-console-core", "stats": "oc-stats-core", "slack": "oc-slack",
}
# 注意：core/sdk/server/ui 等短词需避免误匹配（用边界或长词优先）
# 外部服务关键词
EXT_KEYWORDS = {
    "deepseek": "ext-deepseek-api", "GLM": "ext-glm-api", "glm": "ext-glm-api",
    "高德": "ext-amap-api", "amap": "ext-amap-api",
    "飞书": "ext-lark-api", "lark": "ext-lark-api", "feishu": "ext-lark-api",
    "Chrome": "ext-chrome", "chrome": "ext-chrome",
    "drawio-mcp": "ext-drawio-service", "draw.io": "ext-drawio-service", "drawio-reference": "ext-drawio-service",
    "pdf-reader": "ext-sylphx-pdf", "sylphx": "ext-sylphx-pdf",
    "@opencode-ai/plugin": "ext-opencode-plugin",
    "OpenXML": "ext-openxml", "dotnet": "ext-dotnet", ".NET": "ext-dotnet",
    "gh cli": "ext-gh", "GitHub": "ext-gh", "github": "ext-gh",
    "lark-cli": "ext-lark-cli",
    "openspec CLI": "ext-openspec-cli", "openspec": "ext-openspec-cli",
    "acorn": "ext-acorn", "typescript": "ext-typescript",
}

# 组装节点信息
asm_info = {}
for cid, c in asm_comp.items():
    deps = c.get("depends_on", [])
    if isinstance(deps, str):
        deps = [deps]
    asm_info[cid] = {
        "name": c.get("name", cid),
        "kind": c.get("kind", "skill"),
        "deps": deps,
        "implementation": c.get("implementation", ""),
        "provides": c.get("provides", ""),
        "evidence": c.get("evidence", ""),
    }

# 生成边
new_edges = []
def match_dep(dep_str, nid):
    dep_str_l = dep_str.lower()
    # 包匹配（长词优先，避免 core/sdk 误伤）
    for kw, pid in sorted(PKG_KEYWORDS.items(), key=lambda x: -len(x[0])):
        if kw in dep_str_l:
            new_edges.append({"from": pid, "to": nid, "mechanism": "assembly-to-pkg", "evidence": f"{nid} depends_on 含 {kw}", "dep_raw": dep_str[:80]})
    # 外部匹配
    for kw, eid in sorted(EXT_KEYWORDS.items(), key=lambda x: -len(x[0])):
        if kw.lower() in dep_str_l:
            new_edges.append({"from": eid, "to": nid, "mechanism": "external", "evidence": f"{nid} depends_on 含 {kw}", "dep_raw": dep_str[:80]})

for cid, info in asm_info.items():
    for dep in info["deps"]:
        dep_str = dep if isinstance(dep, str) else json.dumps(dep, ensure_ascii=False)
        match_dep(dep_str, cid)

# 去重
seen = set()
dedup = []
for e in new_edges:
    key = (e["from"], e["to"], e.get("mechanism", ""))
    if key in seen:
        continue
    seen.add(key)
    dedup.append(e)

# ============ 重建 modified-dag ============
with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    mod = json.load(f)

# 保留原有包级边，替换装配边
pkg_edges = [e for e in mod["edges"] if e.get("mechanism") in ("workspace-dep", "import", "semantic-dep")]
# 原有装配边（保留 13 条中不在 dedup 的）
old_asm_edges = [e for e in mod["edges"] if e.get("mechanism") not in ("workspace-dep", "import", "semantic-dep")]
# 合并：dedup 新装配边 + old 中不在 dedup 的
new_asm = list(dedup)
new_asm_keys = {(e["from"], e["to"], e.get("mechanism", "")) for e in new_asm}
for e in old_asm_edges:
    key = (e["from"], e["to"], e.get("mechanism", ""))
    if key not in new_asm_keys:
        new_asm.append(e)

mod["edges"] = pkg_edges + new_asm

# 重算拓扑分层
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

layer_map = topo_layer(mod["nodes"], mod["edges"])
for n in mod["nodes"]:
    n["layer"] = layer_map.get(n["id"], 0)

mod["stats"] = {
    "nodes": len(mod["nodes"]),
    "edges": len(mod["edges"]),
    "layers": max(layer_map.values()) + 1,
    "groups": len(set(n["group"] for n in mod["nodes"])),
    "has_cycle": has_cycle(mod["nodes"], mod["edges"]),
    "pkg_nodes": sum(1 for n in mod["nodes"] if n.get("layer_type") == "package"),
    "asm_nodes": sum(1 for n in mod["nodes"] if n.get("layer_type") == "assembly"),
    "ext_nodes": sum(1 for n in mod["nodes"] if n.get("layer_type") == "external"),
    "pkg_edges": len(pkg_edges),
    "asm_edges": sum(1 for e in mod["edges"] if e.get("mechanism") in ("assembly-to-pkg", "delegate", "skill-mandate", "hook-mount", "instruction-load")),
    "ext_edges": sum(1 for e in mod["edges"] if e.get("mechanism") == "external"),
}

with open(os.path.join(DATA, "modified-dag.json"), "w", encoding="utf-8") as f:
    json.dump(mod, f, ensure_ascii=False, indent=2)
print("modified updated:", json.dumps(mod["stats"], ensure_ascii=False))
print("\nassembly-to-pkg edges:")
for e in sorted(dedup, key=lambda x: (x["from"], x["to"])):
    if e["mechanism"] == "assembly-to-pkg":
        print(f"  {e['from']} -> {e['to']}")
