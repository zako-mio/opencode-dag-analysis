# -*- coding: utf-8 -*-
"""
S1b: 合并三个 stage-01 语义分析文件 → 官方包完整语义 + 去重
输出: 07-checkpoint/s1-package-semantics.json
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

out_dir = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\07-checkpoint"
files = [
    "stage-01-core.json",
    "stage-01-ui-app.json",
    "stage-01-console-stats.json",
]

all_pkgs = {}
for fn in files:
    fp = os.path.join(out_dir, fn)
    try:
        with open(fp, encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERR] {fn}: {e}")
        continue
    for p in data:
        pid = p.get("id", "")
        if not pid:
            continue
        if pid in all_pkgs:
            print(f"[WARN] dup id: {pid}")
        all_pkgs[pid] = p

# 汇总依赖边（从 depends_on 收集）
edges = []
for pid, p in all_pkgs.items():
    for dep in p.get("depends_on", []):
        edges.append({"from": dep, "to": pid, "mechanism": "semantic-dep"})

# 统计
with open(os.path.join(out_dir, "s1-package-semantics.json"), "w", encoding="utf-8") as f:
    json.dump(all_pkgs, f, ensure_ascii=False, indent=2)

print(f"total packages: {len(all_pkgs)}")
for pid in sorted(all_pkgs):
    p = all_pkgs[pid]
    print(f"  {pid}: {p.get('implementation','')[:60]}")
print(f"\ntotal semantic edges: {len(edges)}")
