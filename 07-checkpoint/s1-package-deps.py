# -*- coding: utf-8 -*-
"""
S1a: 官方包级依赖解析 — 35 包间 workspace 依赖 + import 级依赖
输出: 07-checkpoint/s1-package-deps.json
"""
import json, os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"D:\Opencode_Download\Mission-file\2026-08\0807-opencode原理分析\opencode-src"
out_dir = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\07-checkpoint"

# 读取 s0 包清单
with open(os.path.join(out_dir, "s0-packages.json"), encoding="utf-8") as f:
    packages = json.load(f)

pkg_by_id = {p["id"]: p for p in packages}
pkg_short_to_id = {p["short"]: p["id"] for p in packages}

# 每个包的 src 绝对路径
def pkg_src_abs(p):
    return os.path.join(SRC, p["path"], "src")

# 1. workspace 依赖边（package.json dependencies 中 @opencode-ai/* 的）
edges = []
edge_keys = set()
for p in packages:
    for wdep in p["workspace_deps"]:
        dep_id = "oc-" + wdep.replace("@opencode-ai/", "")
        if dep_id not in pkg_by_id:
            continue
        key = (dep_id, p["id"])
        if key in edge_keys:
            continue
        edge_keys.add(key)
        edges.append({"from": dep_id, "to": p["id"], "mechanism": "workspace-dep", "evidence": f"{p['name']}/package.json dependencies.{wdep}"})

# 2. import 级依赖（扫描 src 下所有 ts 的 import from '@opencode-ai/xxx'）
# 为控制成本：只统计 每个包的 src 中对其他包的 import 引用次数（有即建边，记录证据行）
import_edges = {}
for p in packages:
    src_abs = pkg_src_abs(p)
    if not os.path.isdir(src_abs):
        continue
    pkg_imports = {}  # dep_short -> count
    evidence_map = {}  # dep_short -> 示例行
    for root, dirs, files in os.walk(src_abs):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "generated", "__pycache__")]
        for fn in files:
            if not fn.endswith((".ts", ".tsx")):
                continue
            fp = os.path.join(root, fn)
            try:
                with open(fp, encoding="utf-8", errors="replace") as f:
                    for ln_no, line in enumerate(f, 1):
                        m = re.search(r"from\s+['\"]@opencode-ai/([\w-]+)['\"]", line)
                        if not m:
                            m = re.search(r"import\s*\(['\"]@opencode-ai/([\w-]+)['\"]\)", line)
                        if not m:
                            continue
                        dep_short = m.group(1)
                        dep_id = "oc-" + dep_short
                        if dep_id == p["id"] or dep_id not in pkg_by_id:
                            continue
                        pkg_imports[dep_id] = pkg_imports.get(dep_id, 0) + 1
                        if dep_id not in evidence_map:
                            rel = os.path.relpath(fp, SRC).replace("\\", "/")
                            evidence_map[dep_id] = f"{rel}:{ln_no}"
            except Exception:
                pass
    for dep_id, cnt in pkg_imports.items():
        key = (dep_id, p["id"])
        if key in edge_keys:
            # 已有 workspace 边，补充 import 信息
            for e in edges:
                if e["from"] == dep_id and e["to"] == p["id"]:
                    e["import_refs"] = cnt
                    e["evidence_example"] = evidence_map.get(dep_id, "")
                    break
            continue
        edge_keys.add(key)
        import_edges[key] = {
            "from": dep_id, "to": p["id"],
            "mechanism": "import",
            "evidence": evidence_map.get(dep_id, ""),
            "import_refs": cnt,
        }

edges.extend(import_edges.values())

# 3. 汇总统计
result = {
    "nodes": packages,
    "edges": edges,
    "stats": {
        "node_count": len(packages),
        "edge_count": len(edges),
        "workspace_edges": sum(1 for e in edges if e["mechanism"] == "workspace-dep"),
        "import_edges": sum(1 for e in edges if e["mechanism"] == "import"),
    },
}

with open(os.path.join(out_dir, "s1-package-deps.json"), "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(json.dumps(result["stats"], ensure_ascii=False, indent=2))
print("\n--- EDGES (from -> to, mechanism, refs) ---")
for e in sorted(edges, key=lambda x: (x["from"], x["to"])):
    print(f"{e['from']} -> {e['to']} [{e['mechanism']}] refs={e.get('import_refs', '-')} ev={e['evidence'][:60]}")
