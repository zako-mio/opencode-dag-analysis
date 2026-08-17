# -*- coding: utf-8 -*-
"""
S4c: 生成组目录 + 差异清单表 + MD 镜像
输出: 03-groups/index.html + 03-groups/{Gxx}.html
     05-diff/diff-list.html
     06-md/00-index.md + 06-md/{kind}.md
"""
import json, os, sys, html

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")
GROUPS = os.path.join(BASE, "03-groups")
DIFFD = os.path.join(BASE, "05-diff")
MDD = os.path.join(BASE, "06-md")
os.makedirs(GROUPS, exist_ok=True)
os.makedirs(DIFFD, exist_ok=True)
os.makedirs(MDD, exist_ok=True)

with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    mod = json.load(f)
with open(os.path.join(DATA, "diff-dag.json"), encoding="utf-8") as f:
    diff = json.load(f)
with open(os.path.join(DATA, "diff-list.json"), encoding="utf-8") as f:
    diff_list = json.load(f)

node_by_id = {n["id"]: n for n in mod["nodes"]}

def esc(s):
    return html.escape(str(s))

# ============ 组目录 ============
groups = {}
for n in mod["nodes"]:
    g = n.get("group", "G-其他")
    groups.setdefault(g, []).append(n)

# 组索引页
group_rows = ""
for g in sorted(groups.keys()):
    gid = g.split("-")[0]
    group_rows += f"<tr><td><a href='{esc(gid)}.html'>{esc(g)}</a></td><td>{len(groups[g])}</td></tr>"

idx = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>组目录 · opencode DAG</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; padding:30px 20px; }}
  .wrap {{ max-width:1000px; margin:0 auto; }}
  h1 {{ font-size:22px; margin-bottom:6px; }}
  .sub {{ color:var(--dim); font-size:13px; margin-bottom:20px; }}
  .nav a {{ color:var(--accent); text-decoration:none; font-size:13px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th, td {{ border:1px solid var(--border); padding:6px 10px; text-align:left; }}
  th {{ background:var(--panel); color:var(--dim); }}
  td a {{ color:var(--accent); text-decoration:none; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="nav"><a href="../index.html">← 根入口</a></div>
  <h1>组目录（{len(groups)} 组）</h1>
  <div class="sub">包级语义组 + 装配层类型组 + 外部服务</div>
  <table>
    <tr><th>组</th><th>节点数</th></tr>
    {group_rows}
  </table>
</div>
</body>
</html>"""
with open(os.path.join(GROUPS, "index.html"), "w", encoding="utf-8") as f:
    f.write(idx)

# 每组页
for g, nodes in groups.items():
    gid = g.split("-")[0]
    rows = "".join(f"<tr><td><a href='../02-nodes/{esc(n['id'])}.html'>{esc(n.get('short', n['id']))}</a></td><td>{esc(n.get('kind',''))}</td><td>Layer {n.get('layer',0)}</td></tr>" for n in sorted(nodes, key=lambda x: x["id"]))
    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(g)} · opencode DAG</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; padding:30px 20px; }}
  .wrap {{ max-width:1000px; margin:0 auto; }}
  h1 {{ font-size:22px; margin-bottom:6px; }}
  .sub {{ color:var(--dim); font-size:13px; margin-bottom:20px; }}
  .nav a {{ color:var(--accent); text-decoration:none; font-size:13px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th, td {{ border:1px solid var(--border); padding:6px 10px; text-align:left; }}
  th {{ background:var(--panel); color:var(--dim); }}
  td a {{ color:var(--accent); text-decoration:none; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="nav"><a href="../index.html">← 根入口</a> · <a href="index.html">组目录</a></div>
  <h1>{esc(g)}（{len(nodes)} 节点）</h1>
  <div class="sub">组内节点列表</div>
  <table>
    <tr><th>节点</th><th>类型</th><th>层</th></tr>
    {rows}
  </table>
</div>
</body>
</html>"""
    with open(os.path.join(GROUPS, f"{gid}.html"), "w", encoding="utf-8") as f:
        f.write(page)
print(f"generated {len(groups)} group pages + index")

# ============ 差异清单表 ============
diff_rows = ""
for d in diff_list:
    diff_rows += f"<tr><td><a href='../02-nodes/{esc(d['node_id'])}.html'>{esc(d['node_name'])}</a></td><td>{esc(d['kind'])}</td><td>{esc(d['group'])}</td><td>{esc(d['change'])}</td><td><small>{esc(d['reason'])}</small></td></tr>"

diff_page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>差异清单 · opencode 改造对比</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; padding:30px 20px; }}
  .wrap {{ max-width:1100px; margin:0 auto; }}
  h1 {{ font-size:22px; margin-bottom:6px; }}
  .sub {{ color:var(--dim); font-size:13px; margin-bottom:20px; }}
  .nav a {{ color:var(--accent); text-decoration:none; font-size:13px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th, td {{ border:1px solid var(--border); padding:6px 10px; text-align:left; }}
  th {{ background:var(--panel); color:var(--dim); }}
  td a {{ color:var(--accent); text-decoration:none; }}
  td small {{ color:var(--dim); }}
</style>
</head>
<body>
<div class="wrap">
  <div class="nav"><a href="../index.html">← 根入口</a> · <a href="../04-interactive/view-diff.html">对比 DAG</a></div>
  <h1>改造差异清单（{len(diff_list)} 项）</h1>
  <div class="sub">官方 v1.18.14 基线 → 本机装配层（~/.config/opencode）的改造点</div>
  <table>
    <tr><th>节点</th><th>类型</th><th>组</th><th>变更</th><th>原因</th></tr>
    {diff_rows}
  </table>
</div>
</body>
</html>"""
with open(os.path.join(DIFFD, "diff-list.html"), "w", encoding="utf-8") as f:
    f.write(diff_page)
print("generated diff-list.html")

# ============ MD 镜像 ============
def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")

md_lines = ["# opencode DAG 分析 — AI 检索镜像", ""]
md_lines.append(f"三图：官方包级 / 对比 / 改造双层。共 {len(mod['nodes'])} 节点。")
md_lines.append("")

# 包节点
md_lines.append("## 官方包（35）")
md_lines.append("| 节点 | 名称 | 组 | 层 | 作用 |")
md_lines.append("|---|---|---|---|---|")
for n in sorted(mod["nodes"], key=lambda x: x["id"]):
    if n.get("layer_type") == "package":
        md_lines.append(f"| {n['id']} | {md_escape(n.get('short',''))} | {md_escape(n.get('group',''))} | {n.get('layer',0)} | {md_escape(n.get('implementation',''))[:80]} |")
md_lines.append("")

# 装配节点
md_lines.append("## 装配层（61）")
md_lines.append("| 节点 | 名称 | 类型 | 组 | 层 | 作用 | why（需求驱动） |")
md_lines.append("|---|---|---|---|---|---|---|")
for n in sorted(mod["nodes"], key=lambda x: x["id"]):
    if n.get("layer_type") == "assembly":
        why_cur = n.get("why_current", "") or n.get("why_history", "") or ""
        md_lines.append(f"| {n['id']} | {md_escape(n.get('short',''))} | {md_escape(n.get('kind',''))} | {md_escape(n.get('group',''))} | {n.get('layer',0)} | {md_escape(n.get('implementation',''))[:60]} | {md_escape(why_cur)[:60]} |")
md_lines.append("")

# 外部服务
md_lines.append("## 外部服务（8）")
md_lines.append("| 节点 | 名称 | 作用 | why（为什么需要） |")
md_lines.append("|---|---|---|---|")
for n in sorted(mod["nodes"], key=lambda x: x["id"]):
    if n.get("layer_type") == "external":
        why_n = n.get("why_need", n.get("implementation", "")) or ""
        md_lines.append(f"| {n['id']} | {md_escape(n.get('short',''))} | {md_escape(n.get('implementation',''))[:60]} | {md_escape(why_n)[:60]} |")
md_lines.append("")

# 差异清单
md_lines.append("## 改造差异清单")
md_lines.append("| 节点 | 类型 | 变更 |")
md_lines.append("|---|---|---|")
for d in diff_list:
    md_lines.append(f"| {d['node_id']} | {d['kind']} | {d['change']} |")
md_lines.append("")

with open(os.path.join(MDD, "00-index.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print("generated 06-md/00-index.md")

# 每个 kind 单独 md
kinds = {}
for n in mod["nodes"]:
    k = n.get("kind", "other")
    kinds.setdefault(k, []).append(n)
for k, nodes in kinds.items():
    lines = [f"# {k} 节点（{len(nodes)}）", ""]
    for n in sorted(nodes, key=lambda x: x["id"]):
        lines.append(f"## {n['id']} — {n.get('short','')}")
        lines.append(f"- 组: {n.get('group','')} | Layer {n.get('layer',0)}")
        lines.append(f"- 作用: {n.get('implementation','')}")
        lines.append(f"- 提供: {n.get('provides','')}")
        lt = n.get("layer_type", "")
        if lt == "assembly":
            lines.append(f"- **为什么存在（历史）**: {n.get('why_history','')}")
            lines.append(f"- **为什么存在（当前）**: {n.get('why_current','')}")
            lines.append(f"- **怎么用（触发）**: {n.get('how_trigger','')}")
            lines.append(f"- **怎么用（工作流）**: {n.get('how_workflow','')}")
            lines.append(f"- **怎么用（协作）**: {n.get('how_collaboration','')}")
        elif lt == "package":
            lines.append(f"- **为什么存在（设计意图）**: {n.get('why_design', n.get('why',''))}")
            lines.append(f"- **改造关联**: {n.get('why_modified','')}")
            lines.append(f"- **怎么用**: {n.get('how_use','')}")
            lines.append(f"- **典型场景与协作**: {n.get('how_scenario','')}")
        elif lt == "external":
            lines.append(f"- **为什么需要**: {n.get('why_need','')}")
            lines.append(f"- **当前状态**: {n.get('why_current','')}")
            lines.append(f"- **怎么接入**: {n.get('how_integrate','')}")
            lines.append(f"- **装配层调用**: {n.get('how_usage','')}")
        lines.append("")
    fn = os.path.join(MDD, f"{k}.md")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
print(f"generated {len(kinds)} kind md files")
