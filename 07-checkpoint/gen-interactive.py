# -*- coding: utf-8 -*-
"""
S4: 生成三图交互 HTML（cytoscape 单入口三图切换）+ 根入口 index.html
数据源: 01-dag-data/{official,diff,modified}-dag.json
输出: index.html + 04-interactive/{index.html, view-official.html, view-diff.html, view-modified.html}
"""
import json, os, sys, html

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")
INT = os.path.join(BASE, "04-interactive")
os.makedirs(INT, exist_ok=True)

# ============ 读三个 DAG ============
with open(os.path.join(DATA, "official-dag.json"), encoding="utf-8") as f:
    official = json.load(f)
with open(os.path.join(DATA, "diff-dag.json"), encoding="utf-8") as f:
    diff = json.load(f)
with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    modified = json.load(f)

# ============ 组配色（HSL 循环） ============
def group_colors(groups):
    colors = {}
    for i, g in enumerate(groups):
        h = (i * 137) % 360
        colors[g] = f"hsl({h}, 55%, 45%)"
    return colors

ALL_GROUPS = []
for dag in (official, diff, modified):
    for g in dag.get("groups", []):
        if g not in ALL_GROUPS:
            ALL_GROUPS.append(g)
GCOLORS = group_colors(ALL_GROUPS)

# ============ 生成单图视图 HTML（cytoscape） ============
def gen_view_html(dag, view_name, view_title, legend_extra=""):
    # 节点 DATA 预处理：kind 染色
    nodes = []
    for n in dag["nodes"]:
        nid = n["id"]
        grp = n.get("group", "G-其他")
        nkind = n.get("kind", "package")
        status = n.get("status", "")
        # 节点样式类
        cls = []
        if nkind == "package":
            cls.append("pkg")
        elif nkind == "external":
            cls.append("ext")
        elif nkind == "skill":
            cls.append("skill")
        elif nkind in ("agent", "mcp", "plugin", "tool", "command", "instruction", "config"):
            cls.append("asm")
        if status == "modified":
            cls.append("mod")
        if status == "external":
            cls.append("ext")
        if n.get("enabled") is False:
            cls.append("disabled")
        nodes.append({
            "data": {
                "id": nid,
                "name": n.get("short", nid),
                "group": grp,
                "kind": nkind,
                "layer": n.get("layer", 0),
                "status": status,
                "color": GCOLORS.get(grp, "#666"),
                "url": f"../02-nodes/{nid}.html",
            },
            "classes": " ".join(cls),
        })
    edges = []
    for e in dag["edges"]:
        edges.append({
            "data": {"id": f"e{len(edges)}", "source": e["from"], "target": e["to"], "mechanism": e.get("mechanism", "")},
        })

    data_json = json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False)

    legend = f"""
    <b>节点</b>：包(灰蓝)/装配(青)/skill(紫)/外部服务(绿)<br>
    <b>边</b>：A→B 表示 A 依赖 B<br>
    {legend_extra}<br>
    交互：点击节点跳转详情页；拖拽平移；滚轮缩放；shift+点击多选。
    """

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{view_title}</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; height:100vh; overflow:hidden; }}
  header {{ position:fixed; top:0; left:0; right:0; z-index:10; background:var(--panel); border-bottom:1px solid var(--border); padding:10px 20px; display:flex; align-items:center; gap:16px; flex-wrap:wrap; }}
  header h1 {{ font-size:16px; font-weight:600; }}
  .badge {{ background:#20324f; color:#7fb0ff; padding:2px 10px; border-radius:20px; font-size:12px; }}
  .badge.ext {{ background:#1f3a2a; color:#5fd08a; }}
  header a {{ color:var(--accent); text-decoration:none; font-size:13px; }}
  header a:hover {{ text-decoration:underline; }}
  .hint {{ color:var(--dim); font-size:12px; }}
  #graph {{ position:fixed; top:54px; left:0; right:0; bottom:0; min-height:600px; }}
  #side {{ position:fixed; right:0; top:54px; bottom:0; width:300px; background:var(--panel); border-left:1px solid var(--border); padding:16px; overflow:auto; z-index:9; }}
  #side h2 {{ font-size:14px; margin-bottom:10px; color:var(--dim); }}
  #side .legend {{ font-size:12px; color:var(--dim); line-height:1.8; }}
  #side .legend b {{ color:var(--text); }}
  #zoominfo {{ position:fixed; bottom:14px; left:20px; background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:8px 14px; font-size:12px; color:var(--dim); z-index:9; }}
  #zoominfo b {{ color:var(--text); }}
  .node-pkg {{ background:#3a4a6b; }}
  .node-asm {{ background:#2d6b5f; }}
  .node-skill {{ background:#6b4a7a; }}
  .node-ext {{ background:#4a6b3a; }}
  .node-mod {{ border:2px solid #e0b25e; }}
  .node-disabled {{ opacity:0.4; }}
</style>
</head>
<body>
<header>
  <h1>{view_title} <span class="badge">opencode DAG</span></h1>
  <a href="../index.html">← 根入口</a>
  <span class="hint">节点 {len(nodes)} · 边 {len(edges)} · 组 {len(dag.get('groups', []))} · 层 {dag['stats'].get('layers', 0)}</span>
</header>
<div id="side">
  <h2>图例</h2>
  <div class="legend">{legend}</div>
  <h2 style="margin-top:14px;">组配色</h2>
  <div id="glegend"></div>
</div>
<div id="zoominfo">缩放 <b id="zval">1.00</b> · 节点 <b id="zcount">0</b></div>
<div id="graph"></div>
<script src="vendor/cytoscape.min.js"></script>
<script src="vendor/cytoscape-dagre.min.js"></script>
<script>
const DATA = {data_json};
const GROUP_COLORS = {json.dumps(GCOLORS, ensure_ascii=False)};
const cy = cytoscape({{
  container: document.getElementById('graph'),
  elements: DATA,
  style: [
    {{ selector: 'node', style: {{
        'background-color': 'data(color)', 'label': 'data(name)', 'color': '#e6e8ee',
        'font-size': '11px', 'text-valign': 'bottom', 'text-margin-y': 2,
        'width': 'mapData(layer, 0, 8, 36, 48)', 'height': 'mapData(layer, 0, 8, 36, 48)',
        'shape': 'round-rectangle', 'border-width': 1, 'border-color': '#2a2f3a',
    }} }},
    {{ selector: 'node.pkg', style: {{ 'border-color': '#4f8cff' }} }},
    {{ selector: 'node.asm', style: {{ 'border-color': '#5fd08a' }} }},
    {{ selector: 'node.skill', style: {{ 'border-color': '#b48ae0' }} }},
    {{ selector: 'node.ext', style: {{ 'border-color': '#5fd08a', 'shape': 'ellipse' }} }},
    {{ selector: 'node.mod', style: {{ 'border-color': '#e0b25e', 'border-width': 3 }} }},
    {{ selector: 'node.disabled', style: {{ 'opacity': 0.4 }} }},
    {{ selector: 'edge', style: {{
        'width': 1.5, 'line-color': '#3a4a6b', 'target-arrow-color': '#3a4a6b',
        'target-arrow-shape': 'triangle', 'curve-style': 'bezier', 'arrow-scale': 0.8,
    }} }},
    {{ selector: 'edge[mechanism = "external"]', style: {{ 'line-color': '#5fd08a', 'target-arrow-color': '#5fd08a', 'line-style': 'dashed' }} }},
    {{ selector: 'edge[mechanism = "delegate"]', style: {{ 'line-color': '#b48ae0', 'target-arrow-color': '#b48ae0', 'line-style': 'dashed' }} }},
    {{ selector: 'edge[mechanism = "assembly-to-pkg"]', style: {{ 'line-color': '#e0b25e', 'target-arrow-color': '#e0b25e' }} }},
  ],
  layout: {{ name: 'dagre', rankDir: 'LR', nodeSep: 24, edgeSep: 12, rankSep: 90 }},
  wheelSensitivity: 0.2,
}});
// 图例组配色
const gl = document.getElementById('glegend');
for (const [g, c] of Object.entries(GROUP_COLORS)) {{
  const d = document.createElement('div');
  d.style.cssText = 'display:flex;align-items:center;gap:8px;margin:3px 0;font-size:11px;color:var(--dim);';
  d.innerHTML = `<span style="width:12px;height:12px;border-radius:3px;background:${{c}};display:inline-block;"></span> ${{g}}`;
  gl.appendChild(d);
}}
// 缩放信息
cy.on('zoom', () => {{ document.getElementById('zval').textContent = cy.zoom().toFixed(2); }});
cy.on('layoutstop', () => {{ document.getElementById('zcount').textContent = cy.nodes().length; }});
// 兜底：layout 完成后延迟更新 zcount（防止事件时序错过）
setTimeout(() => {{
  const zc = document.getElementById('zcount');
  if (zc && cy) zc.textContent = cy.nodes().length;
}}, 500);
setTimeout(() => {{
  const zc = document.getElementById('zcount');
  if (zc && cy) zc.textContent = cy.nodes().length;
}}, 3000);
// 点击节点跳详情
cy.on('tap', 'node', (evt) => {{
  const n = evt.target;
  const url = n.data('url');
  if (url) window.open(url, '_blank');
}});
// 颜色双击还原
cy.on('dbltap', 'node', (evt) => {{
  const n = evt.target;
  const grp = n.data('group');
  n.style('background-color', GROUP_COLORS[grp] || '#666');
}});
</script>
</body>
</html>"""
    return html_doc

# ============ 生成三个视图 ============
views = [
    ("view-official.html", official, "图1 · 官方原版包级 DAG", "<b>官方基线</b>：35 workspace 包，workspace/import 依赖（v1.18.14 源码）"),
    ("view-diff.html", diff, "图2 · 官方 + 改造对比 DAG", "<b>染色</b>：黄边=被改造引用的包；绿=外部服务"),
    ("view-modified.html", modified, "图3 · 改造版双层 DAG", "<b>双层</b>：包级（上）+ 装配层（下）+ 外部服务（绿）；改造点=黄边"),
]
for fname, dag, title, extra in views:
    doc = gen_view_html(dag, fname, title, extra)
    with open(os.path.join(INT, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"generated {fname}: {len(doc)} bytes")

# ============ 根入口 index.html ============
def dag_summary(dag):
    return f"节点 {dag['stats']['nodes']} · 边 {dag['stats']['edges']} · 层 {dag['stats']['layers']} · 组 {dag['stats']['groups']}"

# 快速入口统计（动态）
off_s = official["stats"]
diff_s = diff["stats"]
mod_s = modified["stats"]

idx = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>opencode DAG 依赖分析总览</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; padding:40px 20px; }}
  .wrap {{ max-width:1200px; margin:0 auto; }}
  h1 {{ font-size:26px; margin-bottom:6px; }}
  .sub {{ color:var(--dim); font-size:14px; margin-bottom:30px; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:16px; }}
  .card {{ background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:20px; text-decoration:none; color:var(--text); display:block; transition:border-color .2s; }}
  .card:hover {{ border-color:var(--accent); }}
  .card h2 {{ font-size:18px; margin-bottom:8px; }}
  .card .meta {{ color:var(--dim); font-size:13px; line-height:1.7; }}
  .card .tag {{ display:inline-block; background:#20324f; color:#7fb0ff; padding:2px 10px; border-radius:20px; font-size:12px; margin-bottom:10px; }}
  .card .tag.green {{ background:#1f3a2a; color:#5fd08a; }}
  .card .tag.yellow {{ background:#3a2f1a; color:#e0b25e; }}
  .section {{ margin-top:36px; }}
  .section h3 {{ font-size:16px; margin-bottom:12px; color:var(--dim); border-bottom:1px solid var(--border); padding-bottom:6px; }}
  .links {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:10px; }}
  .links a {{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:10px 14px; color:var(--text); text-decoration:none; font-size:13px; }}
  .links a:hover {{ border-color:var(--accent); }}
  .links a small {{ color:var(--dim); display:block; font-size:11px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>opencode DAG 依赖分析</h1>
  <div class="sub">三图渐进式：官方原版 → 对比 → 改造版双层。数据源：官方 v1.18.14 源码 + 本机 ~/.config/opencode 装配层</div>

  <div class="cards">
    <a class="card" href="04-interactive/view-official.html">
      <span class="tag">图1 · 基线</span>
      <h2>官方原版包级 DAG</h2>
      <div class="meta">{dag_summary(official)}<br>35 workspace 包依赖关系（workspace:* + import），未改造基线</div>
    </a>
    <a class="card" href="04-interactive/view-diff.html">
      <span class="tag yellow">图2 · 对比</span>
      <h2>官方 + 改造对比 DAG</h2>
      <div class="meta">{dag_summary(diff)}<br>黄边=被改造引用的包，绿=外部服务，附差异清单表</div>
    </a>
    <a class="card" href="04-interactive/view-modified.html">
      <span class="tag green">图3 · 改造版</span>
      <h2>改造版双层 DAG</h2>
      <div class="meta">{dag_summary(modified)}<br>包级 + 装配层（skills/agents/mcp/tools/commands）+ 外部服务</div>
    </a>
  </div>

  <div class="section">
    <h3>快速入口</h3>
    <div class="links">
      <a href="04-interactive/view-official.html">图1 官方 DAG<small>{off_s['nodes']} 包 · {off_s['edges']} 边 · {off_s['groups']} 组</small></a>
      <a href="04-interactive/view-diff.html">图2 对比 DAG<small>{diff_s['nodes']} 节点 · {diff_s['edges']} 边</small></a>
      <a href="04-interactive/view-modified.html">图3 改造双层 DAG<small>{mod_s['nodes']} 节点 · {mod_s['groups']} 组</small></a>
      <a href="03-groups/index.html">组目录<small>38 组索引</small></a>
      <a href="02-nodes/index.html">节点页索引<small>35 包 + 61 装配 + 8 外部</small></a>
      <a href="06-md/00-index.md">MD 镜像（AI 检索）<small>全节点文本</small></a>
      <a href="01-dag-data/official-dag.json">官方 DAG JSON<small>数据</small></a>
      <a href="01-dag-data/diff-dag.json">对比 DAG JSON<small>数据</small></a>
      <a href="01-dag-data/modified-dag.json">改造 DAG JSON<small>数据</small></a>
      <a href="01-dag-data/diff-list.json">差异清单 JSON<small>改造点</small></a>
    </div>
  </div>
</div>
</body>
</html>"""
with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(idx)
print("generated index.html:", len(idx), "bytes")
