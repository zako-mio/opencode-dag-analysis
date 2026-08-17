# -*- coding: utf-8 -*-
"""
S3c: 修正装配层 → 包/外部服务 边匹配（全词边界 + 外部优先）
重写 build-dag-enhance 的匹配逻辑，避免 openspec CLI→oc-cli、Web端→oc-web、SDK→oc-sdk 等误配
输出: 更新 modified-dag.json 的边
"""
import json, os, sys, re

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
CKPT = os.path.join(BASE, "07-checkpoint")
DATA = os.path.join(BASE, "01-dag-data")

with open(os.path.join(CKPT, "s2-assembly-semantics.json"), encoding="utf-8") as f:
    asm = json.load(f)
asm_comp = asm["components"]

# ============ 外部服务（优先匹配，全词/短语级） ============
# (关键词, 外部 id) — 越具体越靠前
EXT_PATTERNS = [
    (r"deepseek", "ext-deepseek-api"),
    (r"GLM|glm", "ext-glm-api"),
    (r"高德|amap-jsapi-loader|AMAP_SECURITY", "ext-amap-api"),
    (r"飞书|feishu", "ext-lark-api"),
    (r"lark-cli", "ext-lark-api"),
    (r"Chrome|chrome", "ext-chrome"),
    (r"drawio-mcp|draw\.io|drawio-reference|DRAWIO_BASE_URL", "ext-drawio-service"),
    (r"pdf-reader|sylphx", "ext-sylphx-pdf"),
    (r"@opencode-ai/plugin", "ext-opencode-plugin"),
    (r"OpenXML|DocumentFormat\.OpenXml|ECMA-376", "ext-openxml"),
    (r"\.NET SDK|dotnet|System\.CommandLine|NuGet", "ext-dotnet"),
    (r"python-docx|Python 3\.13", "ext-python"),
    (r"gh CLI|GitHub|github", "ext-gh"),
    (r"openspec CLI|openspec", "ext-openspec-cli"),
    (r"acorn", "ext-acorn"),
    (r"typescript", "ext-typescript"),
    (r"node:sqlite|node:http", "ext-node"),
    (r"@slack/bolt", "ext-slack"),
    (r"jsx-email", "ext-jsx-email"),
    (r"drizzle|PlanetScale", "ext-drizzle"),
    (r"effect", "ext-effect"),
    (r"solid-js|SolidJS|SolidStart", "ext-solid"),
    (r"yargs", "ext-yargs"),
    (r"hono", "ext-hono"),
    (r"@opentui", "ext-opentui"),
    (r"vite|Vite", "ext-vite"),
    (r"astro|Astro|Starlight", "ext-astro"),
    (r"electron|Electron", "ext-electron"),
    (r"cloudflare|Cloudflare|Workers", "ext-cloudflare"),
    (r"bun|Bun", "ext-bun"),
    (r"@effect/platform", "ext-effect-platform"),
]

# ============ 包（全词边界，排除易误配短词） ============
# 使用精确包名（含 @opencode-ai/ 前缀 或 独立词边界）
PKG_EXACT = [
    (r"@opencode-ai/opencode", "oc-opencode"),
    (r"@opencode-ai/core", "oc-core"),
    (r"@opencode-ai/schema", "oc-schema"),
    (r"@opencode-ai/llm", "oc-llm"),
    (r"@opencode-ai/plugin", "oc-plugin"),
    (r"@opencode-ai/sdk", "oc-sdk"),
    (r"@opencode-ai/sdk-next", "oc-sdk-next"),
    (r"@opencode-ai/server", "oc-server"),
    (r"@opencode-ai/protocol", "oc-protocol"),
    (r"@opencode-ai/client", "oc-client"),
    (r"@opencode-ai/tui", "oc-tui"),
    (r"@opencode-ai/ui", "oc-ui"),
    (r"@opencode-ai/session-ui", "oc-session-ui"),
    (r"@opencode-ai/app", "oc-app"),
    (r"@opencode-ai/desktop", "oc-desktop"),
    (r"@opencode-ai/cli", "oc-cli"),
    (r"@opencode-ai/web", "oc-web"),
    (r"@opencode-ai/enterprise", "oc-enterprise"),
    (r"@opencode-ai/storybook", "oc-storybook"),
    (r"@opencode-ai/codemode", "oc-codemode"),
    (r"@opencode-ai/function", "oc-function"),
    (r"@opencode-ai/http-recorder", "oc-http-recorder"),
    (r"@opencode-ai/script", "oc-script"),
    (r"@opencode-ai/effect-sqlite-node", "oc-effect-sqlite-node"),
    (r"@opencode-ai/effect-drizzle-sqlite", "oc-effect-drizzle-sqlite"),
    (r"@opencode-ai/console", "oc-console-core"),
    (r"@opencode-ai/stats", "oc-stats-core"),
    (r"@opencode-ai/slack", "oc-slack"),
]
# 裸短词（仅当出现为独立词且无 @opencode-ai/ 前缀时才匹配，避免 "cli" 匹配 CLI 工具描述）
PKG_WORD = [
    (r"\bopencode\b", "oc-opencode"),
    (r"\bcore\b", "oc-core"),
    (r"\bschema\b", "oc-schema"),
    (r"\bllm\b", "oc-llm"),
    (r"\bplugin\b", "oc-plugin"),
    (r"\bsdk\b", "oc-sdk"),
    (r"\bserver\b", "oc-server"),
    (r"\bprotocol\b", "oc-protocol"),
    (r"\bclient\b", "oc-client"),
    (r"\btui\b", "oc-tui"),
    (r"\bsession-ui\b", "oc-session-ui"),
    (r"\bcodemode\b", "oc-codemode"),
    (r"\bhttp-recorder\b", "oc-http-recorder"),
]

asm_info = {}
for cid, c in asm_comp.items():
    deps = c.get("depends_on", [])
    if isinstance(deps, str):
        deps = [deps]
    impl = c.get("implementation", "")
    provides = c.get("provides", "")
    asm_info[cid] = {
        "name": c.get("name", cid),
        "kind": c.get("kind", "skill"),
        "deps": deps,
        "implementation": impl,
        "provides": provides,
        "evidence": c.get("evidence", ""),
    }

# 生成边
new_edges = []
def to_str(x):
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return " ".join(to_str(i) for i in x)
    return str(x)

for cid, info in asm_info.items():
    text = " ".join(to_str(d) for d in info["deps"]) + " " + to_str(info["implementation"]) + " " + to_str(info["provides"])
    # 外部优先（具体短语）
    ext_hits = set()
    for pat, eid in EXT_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            ext_hits.add(eid)
    for eid in ext_hits:
        new_edges.append({"from": eid, "to": cid, "mechanism": "external", "evidence": f"{cid} 关联 {eid}", "dep_raw": text[:80]})
    # 包匹配（精确前缀优先）
    pkg_hits = set()
    for pat, pid in PKG_EXACT:
        if re.search(pat, text):
            pkg_hits.add(pid)
    if not pkg_hits:
        for pat, pid in PKG_WORD:
            if re.search(pat, text):
                pkg_hits.add(pid)
    for pid in pkg_hits:
        new_edges.append({"from": pid, "to": cid, "mechanism": "assembly-to-pkg", "evidence": f"{cid} 关联 {pid}", "dep_raw": text[:80]})

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

pkg_edges = [e for e in mod["edges"] if e.get("mechanism") in ("workspace-dep", "import", "semantic-dep")]
# 保留非自动生成的边（delegate/skill-mandate/hook-mount/instruction-load）
keep_edges = [e for e in mod["edges"] if e.get("mechanism") in ("delegate", "skill-mandate", "hook-mount", "instruction-load")]
# 丢弃旧 assembly-to-pkg / external 自动边，用新 dedup
mod["edges"] = pkg_edges + keep_edges + dedup

# 重算拓扑 + 无环
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
