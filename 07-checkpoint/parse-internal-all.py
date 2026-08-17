# -*- coding: utf-8 -*-
"""
S4a: 35 包内部模块级 import 解析
对每个官方包的 src/**/*.ts 解析模块间 import 关系（相对路径 + 别名 + @opencode-ai 内部）
输出: 07-checkpoint/package-internal-all.json
"""
import json, os, sys, re

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"D:\Opencode_Download\Mission-file\2026-08\0807-opencode原理分析\opencode-src"
BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
CKPT = os.path.join(BASE, "07-checkpoint")

with open(os.path.join(CKPT, "s0-packages.json"), encoding="utf-8") as f:
    packages = json.load(f)

def resolve_module_path(pkg_src_abs, file_dir, target, is_tsx=False):
    """把 import target 解析为 src 下相对路径（模块 id）"""
    if target.startswith("."):
        full = os.path.normpath(os.path.join(file_dir, target))
    elif target.startswith("@/"):
        # 包内别名 → 通常指向 src/
        full = os.path.normpath(os.path.join(pkg_src_abs, target[2:]))
    elif target.startswith("#"):
        # bun import map（如 #db / #sqlite / #pty / #fff）→ 尝试映射
        return None
    else:
        return None
    # 尝试扩展名（含 .js → .ts 映射：TS 源码写 .js 实际是 .ts）
    cands = []
    for ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"):
        cands.append(full + ext)
        # .js 后缀可能实际是 .ts
        if full.endswith(".js"):
            cands.append(full[:-3] + ".ts")
            cands.append(full[:-3] + ".tsx")
    for cand in cands:
        if os.path.isfile(cand):
            return os.path.relpath(cand, pkg_src_abs).replace("\\", "/")
    # 目录 → index
    for idx in ("index.ts", "index.tsx", "index.js", "index.jsx"):
        cand = os.path.join(full, idx)
        if os.path.isfile(cand):
            return os.path.relpath(cand, pkg_src_abs).replace("\\", "/")
    return None

# 更健壮的 import 正则：支持 import type / 多行 / 双引号
IMPORT_RE = re.compile(
    r"""import\s+(?:type\s+)?(?:[\w*{}\s,]+\s+from\s+)?['"]([^'"]+)['"]|import\s*\(\s*['"]([^'"]+)['"]\s*\)""",
    re.MULTILINE,
)

result = {}
total_modules = 0
total_edges = 0

for p in packages:
    pid = p["id"]
    pkg_src = os.path.join(SRC, p["path"], "src")
    if not os.path.isdir(pkg_src):
        continue
    modules = {}
    edges = []
    # 第一遍：收集所有模块
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
    # 第二遍：解析 imports
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
            if target.startswith(".") or target.startswith("@/") or target.startswith("#"):
                resolved = resolve_module_path(pkg_src, file_dir, target)
                if resolved and resolved != rel and resolved in modules:
                    m["imports"].append(resolved)
        # 去重
        m["imports"] = list(dict.fromkeys(m["imports"]))
        for imp in m["imports"]:
            edges.append({"from": imp, "to": rel})
    total_modules += len(modules)
    total_edges += len(edges)
    result[pid] = {"package": pid, "src": p["path"], "modules": modules, "edges": edges, "module_count": len(modules), "edge_count": len(edges)}

with open(os.path.join(CKPT, "package-internal-all.json"), "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"packages with internals: {len(result)}")
print(f"total modules: {total_modules}")
print(f"total internal edges: {total_edges}")
for pid, r in sorted(result.items()):
    print(f"  {pid}: {r['module_count']} modules / {r['edge_count']} edges")
