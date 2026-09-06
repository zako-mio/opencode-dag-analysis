# -*- coding: utf-8 -*-
"""
S1b: v1.18.29 官方包内部模块级 import 解析
输出: 08-collect/internal-v1.18.29.json
"""
import json, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")

SRC = "/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag/opencode-src-v1.18.29"
BASE = "/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag"
CKPT = os.path.join(BASE, "08-collect")

# 从 s1-package-deps 读包清单（含 path）
with open(os.path.join(CKPT, "s1-package-deps.json"), encoding="utf-8") as f:
    data = json.load(f)
packages = data["packages"]

def norm_pkg_id(name):
    if name == "opencode": return "oc-opencode"
    if name == "@opencode-ai/sdk": return "oc-sdk"
    n = name.replace("@opencode-ai/", "")
    return "oc-" + n

def resolve_module_path(pkg_src_abs, file_dir, target):
    if target.startswith("."):
        full = os.path.normpath(os.path.join(file_dir, target))
    elif target.startswith("@/"):
        full = os.path.normpath(os.path.join(pkg_src_abs, target[2:]))
    elif target.startswith("#"):
        return None
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

result = {}
for p in packages:
    pid = norm_pkg_id(p["name"])
    pkg_src = os.path.join(SRC, p["path"], "src")
    if not os.path.isdir(pkg_src):
        continue
    modules = {}
    edges = []
    for root, dirs, files in os.walk(pkg_src):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "generated", "__pycache__")]
        for fn in files:
            if not fn.endswith((".ts", ".tsx")):
                continue
            if fn.endswith(".d.ts") or fn.endswith(".test.ts") or fn.endswith(".test.tsx"):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, pkg_src).replace("\\", "/")
            modules[rel] = {"path": rel, "imports": []}
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
    result[pid] = {"package": pid, "src": p["path"], "modules": modules, "edges": edges,
                   "module_count": len(modules), "edge_count": len(edges)}

with open(os.path.join(CKPT, "internal-v1.18.29.json"), "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"packages with internals: {len(result)}")
for pid, r in sorted(result.items()):
    print(f"  {pid}: {r['module_count']} modules / {r['edge_count']} edges")
