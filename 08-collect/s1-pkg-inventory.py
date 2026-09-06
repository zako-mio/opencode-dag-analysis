# -*- coding: utf-8 -*-
"""S1: 从 v1.18.29 源码提取包级清单与 workspace 依赖边（修复norm）"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")

SRC = "/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag/opencode-src-v1.18.29"
OUT = "/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag/08-collect"

pkgs = {}
for root, dirs, files in os.walk(os.path.join(SRC, "packages")):
    if "node_modules" in root: continue
    if "package.json" in files:
        p = os.path.join(root, "package.json")
        try:
            with open(p, encoding="utf-8") as f:
                j = json.load(f)
        except Exception:
            continue
        name = j.get("name")
        if not name: continue
        rel = os.path.relpath(p, SRC).replace(os.sep, "/")
        rel_dir = os.path.dirname(rel)
        pkgs[name] = {"name": name, "path": rel_dir, "version": j.get("version", "")}

def norm_pkg_id(name):
    """统一包 id 格式（oc-xxx）"""
    if name == "opencode":
        return "oc-opencode"
    if name == "@opencode-ai/sdk":
        return "oc-sdk"
    if name == "@opencode-ai/sdk-next":
        return "oc-sdk-next"
    n = name.replace("@opencode-ai/", "")
    return "oc-" + n

def norm_name(name):
    """边 from 侧：包目录名 → 包 id（用于匹配 packages 值）"""
    # 直接用包的 name 字段匹配会最准；这里用 path 反查
    for pk, info in pkgs.items():
        if info["path"].split("/")[-1] == name and pk.startswith("@opencode-ai"):
            return norm_pkg_id(pk)
    if name == "opencode":
        return "oc-opencode"
    return norm_pkg_id(name)

# workspace 依赖边（from=source包路径短名, to=依赖包name）
workspace_deps = []
for name, info in pkgs.items():
    p = os.path.join(SRC, info["path"], "package.json")
    with open(p, encoding="utf-8") as f:
        j = json.load(f)
    deps = j.get("dependencies", {})
    from_id = norm_pkg_id(name)
    for dep_name, ver in deps.items():
        if dep_name in pkgs:
            to_id = norm_pkg_id(dep_name)
            if from_id == to_id: continue
            workspace_deps.append({"from": from_id, "to": to_id, "mechanism": "workspace-dep", "evidence": dep_name})

# 去重
seen = set()
norm_deps = []
for e in workspace_deps:
    key = (e["from"], e["to"])
    if key in seen: continue
    seen.add(key)
    norm_deps.append(e)

with open(os.path.join(OUT, "s1-package-deps.json"), "w", encoding="utf-8") as f:
    json.dump({"packages": list(pkgs.values()), "edges": norm_deps}, f, ensure_ascii=False, indent=2)
print(f"包数: {len(pkgs)}")
print(f"规范化边: {len(norm_deps)}")
for e in sorted(norm_deps, key=lambda x:(x['from'],x['to'])):
    print(f"  {e['from']} -> {e['to']}")
