# -*- coding: utf-8 -*-
"""
S4c: 补全 oc-opencode 内部结构解析（s0 漏了主包，因 name 无 @opencode-ai/ 前缀）
同时修正 s0-packages.json 加入 oc-opencode
输出: 更新 package-internal-all.json + s0-packages.json
"""
import json, os, sys, re

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"D:\Opencode_Download\Mission-file\2026-08\0807-opencode原理分析\opencode-src"
CKPT = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\07-checkpoint"

# 1. 修正 s0-packages.json：加入 oc-opencode
s0_fp = os.path.join(CKPT, "s0-packages.json")
with open(s0_fp, encoding="utf-8") as f:
    packages = json.load(f)

if not any(p["id"] == "oc-opencode" for p in packages):
    # 扫描 opencode 主包
    pkg_dir = os.path.join(SRC, "packages", "opencode")
    pf = os.path.join(pkg_dir, "package.json")
    with open(pf, encoding="utf-8") as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    workspace_deps = [k for k in deps if k.startswith("@opencode-ai/")]
    src_path = os.path.join(pkg_dir, "src")
    ts_count = 0
    for root, dirs, files in os.walk(src_path):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "generated", "__pycache__")]
        for fn in files:
            if fn.endswith((".ts", ".tsx")) and not fn.endswith((".test.ts", ".test.tsx", ".d.ts")):
                ts_count += 1
    packages.append({
        "id": "oc-opencode",
        "name": "opencode",
        "short": "opencode",
        "version": data.get("version", "?"),
        "path": "packages/opencode",
        "workspace_deps": workspace_deps,
        "external_deps_count": len([k for k in deps if not k.startswith("@opencode-ai/")]),
        "src_ts_count": ts_count,
        "is_console_stats": False,
    })
    packages.sort(key=lambda p: p["id"])
    with open(s0_fp, "w", encoding="utf-8") as f:
        json.dump(packages, f, ensure_ascii=False, indent=2)
    print(f"added oc-opencode to s0-packages.json (ts={ts_count})")

# 2. 解析 opencode 内部结构（复用 parse-internal-all 逻辑）
def resolve_module_path(pkg_src_abs, file_dir, target):
    if target.startswith("."):
        full = os.path.normpath(os.path.join(file_dir, target))
    elif target.startswith("@/"):
        full = os.path.normpath(os.path.join(pkg_src_abs, target[2:]))
    else:
        return None
    cands = []
    for ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"):
        cands.append(full + ext)
        if full.endswith(".js"):
            cands.append(full[:-3] + ".ts")
            cands.append(full[:-3] + ".tsx")
    for cand in cands:
        if os.path.isfile(cand):
            return os.path.relpath(cand, pkg_src_abs).replace("\\", "/")
    for idx in ("index.ts", "index.tsx", "index.js", "index.jsx"):
        cand = os.path.join(full, idx)
        if os.path.isfile(cand):
            return os.path.relpath(cand, pkg_src_abs).replace("\\", "/")
    return None

IMPORT_RE = re.compile(
    r"""import\s+(?:type\s+)?(?:[\w*{}\s,]+\s+from\s+)?['"]([^'"]+)['"]|import\s*\(\s*['"]([^'"]+)['"]\s*\)""",
    re.MULTILINE,
)

# 读现有 internals
int_fp = os.path.join(CKPT, "package-internal-all.json")
with open(int_fp, encoding="utf-8") as f:
    internals = json.load(f)

if "oc-opencode" not in internals:
    pkg_src = os.path.join(SRC, "packages", "opencode", "src")
    modules = {}
    for root, dirs, files in os.walk(pkg_src):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "generated", "__pycache__")]
        for fn in files:
            if not fn.endswith((".ts", ".tsx")):
                continue
            if fn.endswith((".d.ts", ".test.ts", ".test.tsx")):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, pkg_src).replace("\\", "/")
            modules[rel] = {"path": rel, "imports": []}
    edges = []
    for rel, m in modules.items():
        fp = os.path.join(pkg_src, *rel.split("/"))
        file_dir = os.path.dirname(fp)
        try:
            with open(fp, encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue
        for mt in IMPORT_RE.finditer(content):
            target = mt.group(1) or mt.group(2)
            if not target:
                continue
            if target.startswith(".") or target.startswith("@/"):
                resolved = resolve_module_path(pkg_src, file_dir, target)
                if resolved and resolved != rel and resolved in modules:
                    m["imports"].append(resolved)
        m["imports"] = list(dict.fromkeys(m["imports"]))
        for imp in m["imports"]:
            edges.append({"from": imp, "to": rel})
    internals["oc-opencode"] = {
        "package": "oc-opencode", "src": "packages/opencode",
        "modules": modules, "edges": edges,
        "module_count": len(modules), "edge_count": len(edges),
    }
    with open(int_fp, "w", encoding="utf-8") as f:
        json.dump(internals, f, ensure_ascii=False, indent=2)
    print(f"added oc-opencode internals: {len(modules)} modules / {len(edges)} edges")
else:
    r = internals["oc-opencode"]
    print(f"oc-opencode already present: {r['module_count']} modules / {r['edge_count']} edges")
