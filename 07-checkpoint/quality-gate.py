# -*- coding: utf-8 -*-
"""
S5: 质量门控 — opencode DAG 全链验证
检查项:
 1. JSON 合法（三个 DAG + diff-list + 语义数据）
 2. DAG 无环
 3. HTML 断链（节点页/交互图/组/根入口 互相引用）
 4. drawio/png 配套
 5. 节点页覆盖（104 节点全部有页面）
 6. 交互图 DATA 校验（节点数与 DAG 一致）
 7. MD 镜像覆盖
 8. 五段完整性（节点页含 ①②③④）
 9. 统计一致性（index.html 数字 vs 实际）
"""
import json, os, sys, re, glob
from collections import deque

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")
CKPT = os.path.join(BASE, "07-checkpoint")
NODES = os.path.join(BASE, "02-nodes")
INT = os.path.join(BASE, "04-interactive")
GROUPS = os.path.join(BASE, "03-groups")
MD = os.path.join(BASE, "06-md")
DRAWIO = os.path.join(BASE, "05-drawio")

passed = []
failed = []

def check(name, cond, detail=""):
    if cond:
        passed.append(name)
        print(f"  ✅ {name} {detail}")
    else:
        failed.append(name)
        print(f"  ❌ {name} {detail}")

# ============ 1. JSON 合法 ============
print("\n=== 1. JSON 合法性 ===")
json_files = ["official-dag.json", "diff-dag.json", "modified-dag.json", "diff-list.json"]
dags = {}
for fn in json_files:
    fp = os.path.join(DATA, fn)
    try:
        with open(fp, encoding="utf-8-sig") as f:
            dags[fn] = json.load(f)
        check(f"json:{fn}", True)
    except Exception as e:
        check(f"json:{fn}", False, str(e))

# ============ 2. DAG 无环 ============
print("\n=== 2. DAG 无环 ===")
def has_cycle(nodes, edges):
    nids = {n["id"] for n in nodes}
    in_deg = {nid: 0 for nid in nids}
    adj = {nid: [] for nid in nids}
    for e in edges:
        if e["from"] in nids and e["to"] in nids:
            in_deg[e["to"]] += 1
            adj[e["from"]].append(e["to"])
    q = deque([nid for nid, d in in_deg.items() if d == 0])
    visited = 0
    while q:
        n = q.popleft()
        visited += 1
        for to in adj[n]:
            in_deg[to] -= 1
            if in_deg[to] == 0:
                q.append(to)
    return visited != len(nids)

for fn in ("official-dag.json", "diff-dag.json", "modified-dag.json"):
    dag = dags[fn]
    cyc = has_cycle(dag["nodes"], dag["edges"])
    check(f"acyclic:{fn}", not cyc, f"nodes={len(dag['nodes'])} edges={len(dag['edges'])}")

# ============ 3. HTML 断链 ============
print("\n=== 3. HTML 断链 ===")
html_files = glob.glob(os.path.join(BASE, "*.html")) + glob.glob(os.path.join(NODES, "*.html")) + glob.glob(os.path.join(INT, "*.html")) + glob.glob(os.path.join(GROUPS, "*.html")) + glob.glob(os.path.join(BASE, "05-diff", "*.html"))
all_existing = set()
for hf in html_files:
    all_existing.add(os.path.basename(hf))
# 所有节点页
for nid in dags["modified-dag.json"]["nodes"]:
    all_existing.add(f"{nid}.html")

broken = []
for hf in html_files:
    with open(hf, encoding="utf-8", errors="replace") as f:
        content = f.read()
    # 提取本地链接（排除 http/https/#/vendor）
    links = re.findall(r'href=["\']([^"\']+)["\']', content)
    base_dir = os.path.dirname(hf)
    for lk in links:
        if lk.startswith(("http", "#", "mailto:", "javascript:")):
            continue
        if "vendor/" in lk:
            continue
        # 相对路径解析
        lk_clean = lk.split("#")[0].split("?")[0]
        if not lk_clean or lk_clean.endswith(".md"):
            continue
        target = os.path.normpath(os.path.join(base_dir, lk_clean))
        if not os.path.isfile(target):
            broken.append(f"{os.path.relpath(hf, BASE)} -> {lk}")
check("html-no-broken-links", len(broken) == 0, f"broken={len(broken)}")
for b in broken[:15]:
    print(f"    {b}")

# ============ 4. drawio/png 配套 ============
print("\n=== 4. drawio/png 配套 ===")
drawios = glob.glob(os.path.join(DRAWIO, "**", "*.drawio"), recursive=True)
pn_ok = 0
for df in drawios:
    png = df.replace(".drawio", ".png")
    if os.path.isfile(png):
        pn_ok += 1
    else:
        print(f"    missing png: {df}")
check(f"drawio-png-pairs", pn_ok == len(drawios), f"{pn_ok}/{len(drawios)}")

# ============ 5. 节点页覆盖 ============
print("\n=== 5. 节点页覆盖 ===")
mod = dags["modified-dag.json"]
missing_pages = []
for n in mod["nodes"]:
    if not os.path.isfile(os.path.join(NODES, f"{n['id']}.html")):
        missing_pages.append(n["id"])
check("node-pages-coverage", len(missing_pages) == 0, f"missing={len(missing_pages)}")
check("node-pages-count", len(mod["nodes"]) == 104, f"nodes={len(mod['nodes'])}")

# ============ 6. 交互图 DATA 校验 ============
print("\n=== 6. 交互图 DATA ===")
for view in ("view-official.html", "view-diff.html", "view-modified.html"):
    fp = os.path.join(INT, view)
    with open(fp, encoding="utf-8", errors="replace") as f:
        content = f.read()
    m = re.search(r"const DATA = (\{.*?\});\nconst GROUP_COLORS", content, re.S)
    if not m:
        check(f"data:{view}", False, "DATA not found")
        continue
    try:
        data = json.loads(m.group(1))
        n_nodes = len(data["nodes"])
        # 对照 dag
        dag_name = view.replace("view-", "").replace(".html", "")
        dag = dags[f"{dag_name}-dag.json"]
        check(f"data:{view}", n_nodes == len(dag["nodes"]), f"data={n_nodes} dag={len(dag['nodes'])}")
    except Exception as e:
        check(f"data:{view}", False, str(e))

# ============ 7. MD 镜像 ============
print("\n=== 7. MD 镜像 ===")
md_files = glob.glob(os.path.join(MD, "*.md"))
check("md-index-exists", os.path.isfile(os.path.join(MD, "00-index.md")), f"md_files={len(md_files)}")
# MD 应包含全部包 id
idx_content = open(os.path.join(MD, "00-index.md"), encoding="utf-8").read()
missing_md = [n["id"] for n in mod["nodes"] if n["id"] not in idx_content]
check("md-covers-nodes", len(missing_md) == 0, f"missing={len(missing_md)}")

# ============ 8. 节点页段完整性 ============
print("\n=== 8. 节点页段完整性 ===")
five_missing = []
seven_missing = []
for n in mod["nodes"]:
    fp = os.path.join(NODES, f"{n['id']}.html")
    if not os.path.isfile(fp):
        continue
    with open(fp, encoding="utf-8", errors="replace") as f:
        content = f.read()
    # 五段（所有节点）
    for marker in ("① 作用", "② 提供能力", "③ 依赖", "④ 被依赖"):
        if marker not in content:
            five_missing.append(f"{n['id']}:{marker}")
            break
    # 七段（装配层/官方包/外部服务都要有 ⑤⑥）
    if n.get("layer_type") in ("assembly", "package", "external"):
        for marker in ("⑤ 为什么存在", "⑥ 怎么用"):
            if marker not in content:
                seven_missing.append(f"{n['id']}:{marker}")
                break
check("five-section", len(five_missing) == 0, f"missing={len(five_missing)}")
check("seven-section-all", len(seven_missing) == 0, f"missing={len(seven_missing)}")

# ============ 9. 统计一致性 ============
print("\n=== 9. 统计一致性 ===")
idx_html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
# 根入口应包含三图统计（从 DAG stats 动态取）
mod_stats = dags["modified-dag.json"]["stats"]
off_stats = dags["official-dag.json"]["stats"]
diff_stats = dags["diff-dag.json"]["stats"]
need = [
    str(off_stats["nodes"]), str(off_stats["edges"]),
    str(diff_stats["nodes"]),
    str(mod_stats["nodes"]), str(mod_stats["edges"]),
]
ok_stats = all(s in idx_html for s in need)
check("index-stats", ok_stats, f"need={need}")

# ============ 汇总 ============
print(f"\n===== 门控结果: {len(passed)} passed / {len(failed)} failed =====")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
else:
    print("ALL PASS ✅")
