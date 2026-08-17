# -*- coding: utf-8 -*-
"""
S3: 三图建模 — 官方包级 DAG / 对比 DAG / 改造双层 DAG
输出: 01-dag-data/official-dag.json / diff-dag.json / modified-dag.json
"""
import json, os, sys, re

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
CKPT = os.path.join(BASE, "07-checkpoint")
DATA = os.path.join(BASE, "01-dag-data")
os.makedirs(DATA, exist_ok=True)

# ============ 读入 ============
with open(os.path.join(CKPT, "s1-package-deps.json"), encoding="utf-8") as f:
    pkg_deps = json.load(f)
with open(os.path.join(CKPT, "s1-package-semantics.json"), encoding="utf-8") as f:
    pkg_sem = json.load(f)
with open(os.path.join(CKPT, "s2-assembly-semantics.json"), encoding="utf-8") as f:
    asm = json.load(f)

asm_comp = asm["components"]
history = asm["history"]

# ============ 1. 官方包节点 ============
# 包语义分组（语义域）
PKG_GROUP = {
    "oc-schema": "G1-数据模型", "oc-protocol": "G2-通信协议", "oc-client": "G3-客户端",
    "oc-sdk": "G3-客户端", "oc-sdk-next": "G3-客户端", "oc-server": "G4-服务端",
    "oc-llm": "G5-LLM请求层", "oc-core": "G6-核心服务", "oc-plugin": "G7-插件SDK",
    "oc-tui": "G8-终端UI", "oc-ui": "G9-UI组件", "oc-session-ui": "G9-UI组件",
    "oc-app": "G10-应用", "oc-desktop": "G10-应用", "oc-cli": "G10-应用",
    "oc-web": "G11-文档站点", "oc-enterprise": "G10-应用", "oc-storybook": "G11-文档站点",
    "oc-codemode": "G12-沙箱", "oc-function": "G13-边缘服务",
    "oc-http-recorder": "G14-工具", "oc-script": "G14-工具",
    "oc-effect-sqlite-node": "G15-存储适配", "oc-effect-drizzle-sqlite": "G15-存储适配",
    "oc-console-app": "G16-Console", "oc-console-core": "G16-Console",
    "oc-console-function": "G16-Console", "oc-console-mail": "G16-Console",
    "oc-console-resource": "G16-Console", "oc-console-support": "G16-Console",
    "oc-stats-app": "G17-Stats", "oc-stats-core": "G17-Stats", "oc-stats-server": "G17-Stats",
    "oc-slack": "G18-集成", "oc-opencode": "G19-主入口",
}

def norm_pkg_id(pid):
    """统一包 id 格式（oc-xxx）"""
    pid = pid.strip()
    if pid.startswith("@opencode-ai/"):
        return "oc-" + pid.replace("@opencode-ai/", "")
    if pid.startswith("oc-"):
        return pid
    return "oc-" + pid

# 官方节点
official_nodes = []
for pid, p in pkg_sem.items():
    nid = norm_pkg_id(pid)
    official_nodes.append({
        "id": nid,
        "name": p.get("name", nid),
        "short": nid.replace("oc-", ""),
        "group": PKG_GROUP.get(nid, "G-其他"),
        "group_name": PKG_GROUP.get(nid, "G-其他"),
        "kind": "package",
        "implementation": p.get("implementation", ""),
        "provides": p.get("provides", ""),
        "key_modules": p.get("key_modules", []),
        "why": p.get("why", ""),
        "layer": 0,
    })

# 官方边（从 workspace 依赖 + 语义 depends_on 合并）
official_edges = []
edge_set = set()
for e in pkg_deps["edges"]:
    f, t = norm_pkg_id(e["from"]), norm_pkg_id(e["to"])
    key = (f, t)
    if key in edge_set:
        continue
    edge_set.add(key)
    official_edges.append({
        "from": f, "to": t,
        "mechanism": e.get("mechanism", "workspace-dep"),
        "evidence": e.get("evidence", ""),
        "evidence_example": e.get("evidence_example", ""),
        "import_refs": e.get("import_refs", 0),
    })
# 语义补充边（semantic-dep）
for pid, p in pkg_sem.items():
    f = norm_pkg_id(pid)
    for dep in p.get("depends_on", []):
        dep_id = norm_pkg_id(dep) if not isinstance(dep, str) else norm_pkg_id(dep)
        if dep_id == f or dep_id not in {n["id"] for n in official_nodes}:
            continue
        key = (dep_id, f)
        if key in edge_set:
            continue
        edge_set.add(key)
        official_edges.append({"from": dep_id, "to": f, "mechanism": "semantic-dep", "evidence": f"stage-01 {p.get('name','')}", "evidence_example": "", "import_refs": 0})

# ============ 2. 拓扑分层（层次遍历：被依赖方先于依赖方） ============
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
        # 有环：剩余节点放最后一层并标注
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

# ============ 3. 装配层节点（改造版） ============
# 装配分组
ASM_GROUP = {
    "agent": "A1-Agents", "mcp": "A2-MCP", "plugin": "A3-插件工具",
    "tool": "A3-插件工具", "command": "A4-命令指令", "instruction": "A4-命令指令",
    "config": "A5-配置本体", "skills": "A6-Skills", "skill": "A6-Skills", "reflection": "A6-Skills",
}
# skill 领域细分
SKILL_SUBGROUP = {
    "drawio-reference": "A6a-图表", "frontend-design": "A6b-前端设计", "lark-suite": "A6c-办公集成",
    "minimax-docx": "A6c-办公集成", "minimax-xlsx": "A6c-办公集成", "pdf-ocr": "A6d-文档处理",
    "soe-resume": "A6e-简历求职", "resume-builder": "A6e-简历求职", "recruit-assist": "A6e-简历求职",
    "agency-agents": "A6f-角色调度", "grill-me": "A6f-角色调度", "model-switcher": "A6g-模型控制",
    "browser-use": "A6h-浏览器", "browser-harness": "A6h-浏览器", "headroom": "A6i-上下文压缩",
    "opencode-config": "A6j-配置知识", "amap-jsapi-skill": "A6k-地图", "amap-lbs-skill": "A6k-地图",
    "amap-budget-control": "A6k-地图", "superpowers-feature-workflow": "A6l-工作流",
    "superpowers-learning-workflow": "A6l-工作流", "superpowers-openspec-superpowers-workflow": "A6l-工作流",
    "openspec-propose": "A6l-工作流", "openspec-new-change": "A6l-工作流", "openspec-ff-change": "A6l-工作流",
    "openspec-explore": "A6l-工作流", "openspec-apply-change": "A6l-工作流", "openspec-verify-change": "A6l-工作流",
    "openspec-continue-change": "A6l-工作流", "openspec-archive-change": "A6l-工作流", "openspec-bulk-archive-change": "A6l-工作流",
    "openspec-sync-specs": "A6l-工作流", "openspec-update-change": "A6l-工作流", "openspec-onboard": "A6l-工作流",
    "release-openspec": "A6l-工作流", "agent-reflection": "A6m-自进化", "postmortem-failure-review": "A6m-自进化",
    "reusable-asset-inventory": "A6m-自进化", "large-scale-source-parse": "A6m-自进化",
    "multi-window-dag-delivery": "A6m-自进化", "cytoscape-dag-visualization": "A6m-自进化",
    "dag-tutorial-authoring": "A6m-自进化", "github-bulk-upload": "A6m-自进化",
    "cdisk-space-optimization": "A6n-系统优化",
}

asm_nodes = []
for cid, c in asm_comp.items():
    kind = c.get("kind", "skill")
    # 兼容 source 字段（skills-a/b 用 source）
    src = c.get("source", "")
    name = c.get("name", cid)
    if cid.startswith("skill-"):
        kind = "skill"
        name = cid.replace("skill-", "")
    grp = ASM_GROUP.get(kind, "A6-Skills")
    if kind == "skill":
        grp = SKILL_SUBGROUP.get(name, grp)
    # depends_on 可能是字符串或列表
    deps = c.get("depends_on", [])
    if isinstance(deps, str):
        deps = [deps]
    asm_nodes.append({
        "id": cid,
        "name": name,
        "short": cid.split("-", 1)[1] if "-" in cid else cid,
        "group": grp,
        "group_name": grp,
        "kind": kind,
        "implementation": c.get("implementation", c.get("desc", "")),
        "provides": c.get("provides", ""),
        "depends_on_raw": deps,
        "trigger": c.get("trigger", ""),
        "history": c.get("history", []),
        "evidence": c.get("evidence", ""),
        "enabled": c.get("enabled", True),
        "layer": 0,
    })

# 装配层 → 包 边（从 depends_on_raw 匹配包 id 或字符串含包名）
asm_to_pkg_edges = []
for n in asm_nodes:
    for dep in n["depends_on_raw"]:
        dep_str = dep if isinstance(dep, str) else json.dumps(dep, ensure_ascii=False)
        # 匹配包
        for pid, p in pkg_sem.items():
            pnid = norm_pkg_id(pid)
            pname = p.get("name", "")
            if pnid in dep_str or pname in dep_str or (pname.split("/")[-1] in dep_str and len(pname.split("/")[-1]) > 3):
                asm_to_pkg_edges.append({"from": pnid, "to": n["id"], "mechanism": "assembly-to-pkg", "evidence": f"{n['id']} depends_on 含 {pname}", "dep_raw": dep_str[:80]})
                break

# 外部服务节点（GLM API、高德 API、飞书、Chrome、npm 包等）
ext_nodes = [
    {"id": "ext-glm-api", "name": "GLM API（智谱）", "kind": "external", "group": "X-外部服务", "implementation": "VLM 图片转文字服务（glm-4.6v / glm-4.6v-flash）", "provides": "图片描述", "layer": 0},
    {"id": "ext-amap-api", "name": "高德地图 API", "kind": "external", "group": "X-外部服务", "implementation": "地图 POI/路径规划服务", "provides": "地图能力", "layer": 0},
    {"id": "ext-lark-api", "name": "飞书/Lark API", "kind": "external", "group": "X-外部服务", "implementation": "lark-cli 调用的飞书开放平台", "provides": "日历/文档/多维表格等", "layer": 0},
    {"id": "ext-chrome", "name": "Chrome 浏览器", "kind": "external", "group": "X-外部服务", "implementation": "browser-harness 自动化浏览器", "provides": "网页自动化", "layer": 0},
    {"id": "ext-deepseek-api", "name": "DeepSeek API", "kind": "external", "group": "X-外部服务", "implementation": "deepseek-v4-pro/flash 模型 API", "provides": "LLM 推理", "layer": 0},
    {"id": "ext-drawio-service", "name": "draw.io 服务", "kind": "external", "group": "X-外部服务", "implementation": "draw.io 在线/本地图表渲染", "provides": "图表导出", "layer": 0},
    {"id": "ext-sylphx-pdf", "name": "@sylphx/pdf-reader-mcp", "kind": "external", "group": "X-外部服务", "implementation": "PDF 文本提取 npm 包", "provides": "PDF 提取", "layer": 0},
    {"id": "ext-opencode-plugin", "name": "@opencode-ai/plugin SDK", "kind": "external", "group": "X-外部服务", "implementation": "插件 SDK（node_modules 1.18.9）", "provides": "插件钩子类型", "layer": 0},
]

# ============ 4. 图1: official-dag ============
layer_map = topo_layer(official_nodes, official_edges)
for n in official_nodes:
    n["layer"] = layer_map.get(n["id"], 0)

official_dag = {
    "name": "official",
    "title": "官方原版 opencode 包级 DAG",
    "version_note": "基于官方源码 v1.18.14（0807-opencode原理分析 clone），35 workspace 包",
    "nodes": official_nodes,
    "edges": official_edges,
    "groups": list(dict.fromkeys(n["group"] for n in official_nodes)),
    "stats": {
        "nodes": len(official_nodes),
        "edges": len(official_edges),
        "layers": max(layer_map.values()) + 1,
        "groups": len(set(n["group"] for n in official_nodes)),
        "has_cycle": has_cycle(official_nodes, official_edges),
    },
}

with open(os.path.join(DATA, "official-dag.json"), "w", encoding="utf-8") as f:
    json.dump(official_dag, f, ensure_ascii=False, indent=2)
print("official:", json.dumps(official_dag["stats"], ensure_ascii=False))

# ============ 5. 图2: diff-dag（官方 + 改造点染色 + 装配层浅标注） ============
# 改造点：装配层新增节点（相对官方）全部视为"新增"；官方包被配置引用的标"modified"
pkg_used_by_asm = set()
for e in asm_to_pkg_edges:
    pkg_used_by_asm.add(e["from"])

diff_nodes = []
for n in official_nodes:
    nn = dict(n)
    nn["status"] = "modified" if n["id"] in pkg_used_by_asm else "official"
    diff_nodes.append(nn)
# 外部服务
for en in ext_nodes:
    en2 = dict(en)
    en2["status"] = "external"
    diff_nodes.append(en2)

diff_edges = [dict(e) for e in official_edges]
# 外部服务到包的边（providers → 配置引用）
for n in asm_nodes:
    for dep in n["depends_on_raw"]:
        dep_str = dep if isinstance(dep, str) else json.dumps(dep, ensure_ascii=False)
        if "deepseek" in dep_str.lower():
            diff_edges.append({"from": "ext-deepseek-api", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → deepseek"})
        if "GLM" in dep_str or "glm" in dep_str:
            diff_edges.append({"from": "ext-glm-api", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → GLM"})

layer_map2 = topo_layer(diff_nodes, diff_edges)
for n in diff_nodes:
    n["layer"] = layer_map2.get(n["id"], 0)

diff_dag = {
    "name": "diff",
    "title": "官方 + 改造对比 DAG（改造点染色）",
    "version_note": "官方 v1.18.14 基线；改造点 = ~/.config/opencode 装配层引用（新增红/修改黄/外部绿）",
    "nodes": diff_nodes,
    "edges": diff_edges,
    "groups": list(dict.fromkeys(n["group"] for n in diff_nodes)),
    "stats": {
        "nodes": len(diff_nodes),
        "edges": len(diff_edges),
        "layers": max(layer_map2.values()) + 1,
        "groups": len(set(n["group"] for n in diff_nodes)),
        "has_cycle": has_cycle(diff_nodes, diff_edges),
        "modified_pkgs": len(pkg_used_by_asm),
        "external_nodes": sum(1 for n in diff_nodes if n["status"] == "external"),
    },
}

with open(os.path.join(DATA, "diff-dag.json"), "w", encoding="utf-8") as f:
    json.dump(diff_dag, f, ensure_ascii=False, indent=2)
print("diff:", json.dumps(diff_dag["stats"], ensure_ascii=False))

# ============ 6. 图3: modified-dag（包级 + 装配层双层） ============
mod_nodes = []
for n in official_nodes:
    nn = dict(n)
    nn["layer_type"] = "package"
    mod_nodes.append(nn)
for n in asm_nodes:
    nn = dict(n)
    nn["layer_type"] = "assembly"
    mod_nodes.append(nn)
for en in ext_nodes:
    en2 = dict(en)
    en2["layer_type"] = "external"
    mod_nodes.append(en2)

mod_edges = [dict(e) for e in official_edges]
# 装配 → 包
for e in asm_to_pkg_edges:
    mod_edges.append(e)
# 装配 → 外部服务
for n in asm_nodes:
    for dep in n["depends_on_raw"]:
        dep_str = dep if isinstance(dep, str) else json.dumps(dep, ensure_ascii=False)
        if "deepseek" in dep_str.lower():
            mod_edges.append({"from": "ext-deepseek-api", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → deepseek"})
        if "GLM" in dep_str or "glm" in dep_str:
            mod_edges.append({"from": "ext-glm-api", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → GLM"})
        if "高德" in dep_str or "amap" in dep_str.lower():
            mod_edges.append({"from": "ext-amap-api", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → 高德"})
        if "飞书" in dep_str or "lark" in dep_str.lower():
            mod_edges.append({"from": "ext-lark-api", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → 飞书"})
        if "Chrome" in dep_str or "浏览器" in dep_str:
            mod_edges.append({"from": "ext-chrome", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → Chrome"})
        if "drawio" in dep_str.lower() or "draw.io" in dep_str:
            mod_edges.append({"from": "ext-drawio-service", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → draw.io"})
        if "pdf-reader" in dep_str.lower() or "sylphx" in dep_str.lower():
            mod_edges.append({"from": "ext-sylphx-pdf", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → pdf-reader"})
        if "@opencode-ai/plugin" in dep_str:
            mod_edges.append({"from": "ext-opencode-plugin", "to": n["id"], "mechanism": "external", "evidence": f"{n['id']} → plugin SDK"})

# 装配↔装配 边（agent 委派关系 + skill 引用）
asm_by_id = {n["id"]: n for n in asm_nodes}
# agent-plan/build → 各子Agent（委派）
for sub in ["agent-pdf-worker", "agent-drawio-worker", "agent-general", "agent-explore", "agent-reflection-worker"]:
    if sub in asm_by_id:
        mod_edges.append({"from": "agent-plan", "to": sub, "mechanism": "delegate", "evidence": "plan 委派协议"})
        mod_edges.append({"from": "agent-build", "to": sub, "mechanism": "delegate", "evidence": "build 委派协议"})
# drawio-worker → drawio-reference skill
if "agent-drawio-worker" in asm_by_id and "skill-drawio-reference" in asm_by_id:
    mod_edges.append({"from": "skill-drawio-reference", "to": "agent-drawio-worker", "mechanism": "skill-mandate", "evidence": "drawio-reference 强制加载"})
# vision-interceptor → auto-mode（挂载于 messages.transform）
if "plugin-vision-interceptor" in asm_by_id and "instr-auto-mode" in asm_by_id:
    mod_edges.append({"from": "instr-auto-mode", "to": "plugin-vision-interceptor", "mechanism": "hook-mount", "evidence": "插件挂载于消息管线"})
# instruction → agent（auto-mode 被 plan/build 使用）
for ag in ["agent-plan", "agent-build"]:
    if ag in asm_by_id:
        mod_edges.append({"from": "instr-auto-mode", "to": ag, "mechanism": "instruction-load", "evidence": "auto-mode.md 作为 agent 指令"})
        mod_edges.append({"from": "instr-memory", "to": ag, "mechanism": "instruction-load", "evidence": "MEMORY.md 作为 agent 指令"})

# 去重边
seen_edges = set()
dedup_mod_edges = []
for e in mod_edges:
    key = (e["from"], e["to"], e.get("mechanism", ""))
    if key in seen_edges:
        continue
    seen_edges.add(key)
    dedup_mod_edges.append(e)

layer_map3 = topo_layer(mod_nodes, dedup_mod_edges)
for n in mod_nodes:
    n["layer"] = layer_map3.get(n["id"], 0)

mod_dag = {
    "name": "modified",
    "title": "改造版 opencode 包级 + 装配层双层 DAG",
    "version_note": "官方 35 包（v1.18.14）+ 装配层 61 组件（~/.config/opencode）+ 外部服务 8",
    "nodes": mod_nodes,
    "edges": dedup_mod_edges,
    "groups": list(dict.fromkeys(n["group"] for n in mod_nodes)),
    "stats": {
        "nodes": len(mod_nodes),
        "edges": len(dedup_mod_edges),
        "layers": max(layer_map3.values()) + 1,
        "groups": len(set(n["group"] for n in mod_nodes)),
        "has_cycle": has_cycle(mod_nodes, dedup_mod_edges),
        "pkg_nodes": sum(1 for n in mod_nodes if n["layer_type"] == "package"),
        "asm_nodes": sum(1 for n in mod_nodes if n["layer_type"] == "assembly"),
        "ext_nodes": sum(1 for n in mod_nodes if n["layer_type"] == "external"),
        "pkg_edges": sum(1 for e in dedup_mod_edges if e.get("mechanism") in ("workspace-dep", "import", "semantic-dep")),
        "asm_edges": sum(1 for e in dedup_mod_edges if e.get("mechanism") in ("assembly-to-pkg", "delegate", "skill-mandate", "hook-mount", "instruction-load")),
        "ext_edges": sum(1 for e in dedup_mod_edges if e.get("mechanism") == "external"),
    },
}

with open(os.path.join(DATA, "modified-dag.json"), "w", encoding="utf-8") as f:
    json.dump(mod_dag, f, ensure_ascii=False, indent=2)
print("modified:", json.dumps(mod_dag["stats"], ensure_ascii=False))

# ============ 7. 差异清单（供对比表） ============
diff_list = []
for n in asm_nodes:
    diff_list.append({
        "node_id": n["id"],
        "node_name": n["name"],
        "kind": n["kind"],
        "group": n["group"],
        "change": "新增装配" if n.get("enabled", True) else "新增（禁用）",
        "reason": "改造需求（历史事件见 history 字段）",
        "enabled": n.get("enabled", True),
    })
for pid in pkg_used_by_asm:
    diff_list.append({
        "node_id": pid,
        "node_name": pid.replace("oc-", ""),
        "kind": "package",
        "group": PKG_GROUP.get(pid, ""),
        "change": "被装配层引用（配置修改）",
        "reason": "官方包被本机配置引用",
        "enabled": True,
    })

with open(os.path.join(DATA, "diff-list.json"), "w", encoding="utf-8") as f:
    json.dump(diff_list, f, ensure_ascii=False, indent=2)
print(f"diff-list entries: {len(diff_list)}")
