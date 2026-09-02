# -*- coding: utf-8 -*-
"""
S4b-v2: 生成节点详情页（五段：作用/依赖/被依赖/改造原因/内部结构）
数据源: 01-dag-data/modified-dag.json + 08-collect/internal-v1.18.25.json
输出: 02-nodes/{id}.html + 02-nodes/index.html
改造点: 数据源路径 v2；内部结构 DAG 换 new internal；索引副标题改为 36/69/9
"""
import json, os, sys, html

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")
COLLECT = os.path.join(BASE, "08-collect")
NODES = os.path.join(BASE, "02-nodes")
os.makedirs(NODES, exist_ok=True)

# ============ 读入 ============
with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    mod = json.load(f)
with open(os.path.join(DATA, "diff-dag.json"), encoding="utf-8") as f:
    diff = json.load(f)
with open(os.path.join(DATA, "official-dag.json"), encoding="utf-8") as f:
    official = json.load(f)
with open(os.path.join(COLLECT, "internal-v1.18.25.json"), encoding="utf-8") as f:
    internals = json.load(f)
with open(os.path.join(DATA, "diff-list.json"), encoding="utf-8") as f:
    diff_list = json.load(f)

# ============ 索引 ============
node_by_id = {n["id"]: n for n in mod["nodes"]}
edge_out = {}  # node -> [edges]  出边（该节点依赖谁）
edge_in = {}   # node -> [edges]  入边（谁依赖该节点）
for e in mod["edges"]:
    edge_out.setdefault(e["from"], []).append(e)
    edge_in.setdefault(e["to"], []).append(e)

def esc(s):
    return html.escape(str(s))

def list_to_text(x):
    """list 转可读文本（每条带序号）"""
    if isinstance(x, list):
        return "<br>".join(f"· {esc(i)}" for i in x)
    return esc(x)

def deps_list(nid):
    """返回该节点的上游依赖（该节点依赖谁 = 从它出发的边的 to）"""
    outs = edge_out.get(nid, [])
    items = []
    for e in outs:
        to = e["to"]
        if to in node_by_id:
            items.append((to, node_by_id[to].get("short", to), e.get("mechanism", ""), e.get("evidence", "")))
    return items

def deps_by(nid):
    """返回该节点的下游（谁依赖该节点 = 指向它的边的 from）"""
    ins = edge_in.get(nid, [])
    items = []
    for e in ins:
        frm = e["from"]
        if frm in node_by_id:
            items.append((frm, node_by_id[frm].get("short", frm), e.get("mechanism", ""), e.get("evidence", "")))
    return items

# ============ 内部结构 DAG（cytoscape 内嵌，大包组级+下钻） ============
def internal_dag_html(nid):
    pkg_short = nid.replace("oc-", "")
    int_data = internals.get(nid)
    if not int_data or int_data.get("module_count", 0) < 2:
        return ""
    modules = int_data["modules"]
    edges = int_data["edges"]
    ref_count = {}
    for e in edges:
        ref_count[e["from"]] = ref_count.get(e["from"], 0) + 1
    in_deg = {}
    for e in edges:
        in_deg[e["to"]] = in_deg.get(e["to"], 0) + 1
    nodes = []
    for rel, m in modules.items():
        is_index = rel.endswith("index.ts") or rel == "index.ts"
        cls = []
        if is_index:
            cls.append("entry")
        elif ref_count.get(rel, 0) >= 3:
            cls.append("hot")
        else:
            cls.append("leaf")
        nodes.append({
            "data": {"id": rel, "name": os.path.basename(rel), "path": rel},
            "classes": " ".join(cls),
        })
    seen = set()
    es = []
    for e in edges:
        key = (e["from"], e["to"])
        if key in seen:
            continue
        seen.add(key)
        es.append({"data": {"source": e["to"], "target": e["from"]}})

    # ---- 大包：目录分组组级 + 下钻 ----
    jsid = nid.replace("-", "_")
    # 按顶层目录分组（src 下第一层）
    if len(nodes) > 100:
        group_map = {}
        for n in nodes:
            rel = n["data"]["id"]
            parts = rel.split("/")
            grp = parts[0] if len(parts) > 1 else "(root)"
            group_map.setdefault(grp, []).append(n)
        # 组节点 + 组内边
        group_nodes = []
        grp_ids = {}
        for gi, (grp, members) in enumerate(sorted(group_map.items())):
            gid = f"grp-{gi}"
            grp_ids[grp] = gid
            group_nodes.append({
                "data": {"id": gid, "name": grp, "count": len(members), "kind": "group"},
                "classes": "grp",
            })
        # 组间边：组 A 内模块 import 组 B 内模块 → A -> B
        grp_edges = []
        grp_of = {}
        for n in nodes:
            rel = n["data"]["id"]
            parts = rel.split("/")
            grp_of[rel] = parts[0] if len(parts) > 1 else "(root)"
        for e in es:
            frm_grp = grp_of.get(e["data"]["source"])
            to_grp = grp_of.get(e["data"]["target"])
            if frm_grp and to_grp and frm_grp != to_grp:
                fe = grp_ids.get(frm_grp)
                te = grp_ids.get(to_grp)
                if fe and te:
                    grp_edges.append({"data": {"source": fe, "target": te}})
        # 去重组边
        seen_ge = set()
        dedup_ge = []
        for e in grp_edges:
            key = (e["data"]["source"], e["data"]["target"])
            if key in seen_ge:
                continue
            seen_ge.add(key)
            dedup_ge.append(e)

        data_json = json.dumps({"nodes": group_nodes, "edges": dedup_ge}, ensure_ascii=False)
        # 组内模块映射（下钻用）
        drill_data = {}
        for grp, members in group_map.items():
            m_nodes = []
            m_edges = []
            m_ids = set(m["data"]["id"] for m in members)
            for n in members:
                m_nodes.append(n)
            for e in es:
                if e["data"]["source"] in m_ids and e["data"]["target"] in m_ids:
                    m_edges.append(e)
            drill_data[grp] = {"nodes": m_nodes, "edges": m_edges}
        drill_json = json.dumps(drill_data, ensure_ascii=False)

        return f"""
<h3>模块内部结构 DAG（{int_data['module_count']} 模块 · {int_data['edge_count']} 边 · 组级视图）</h3>
<p style="color:var(--dim);font-size:12px;margin:4px 0;">按目录分组的组级视图：点击组节点下钻查看组内模块依赖；点击模块节点查看完整路径。</p>
<div id="int-nav-{esc(nid)}" style="display:flex;align-items:center;gap:10px;margin:8px 0;">
  <button id="int-back-{esc(nid)}" style="display:none;background:#20324f;color:#7fb0ff;border:1px solid #2a2f3a;border-radius:6px;padding:5px 14px;font-size:12px;cursor:pointer;">← 返回组级视图</button>
  <span id="int-crumb-{esc(nid)}" style="color:var(--dim);font-size:12px;">组级视图</span>
</div>
<div id="int-{esc(nid)}" style="width:100%;height:520px;background:#0b0e14;border:1px solid var(--border);border-radius:8px;"></div>
<script src="vendor/cytoscape.min.js"></script>
<script src="vendor/cytoscape-dagre.min.js"></script>
<script>
const INT{jsid} = {data_json};
const DRILL{jsid} = {drill_json};
const cy{jsid} = cytoscape({{
  container: document.getElementById('int-{esc(nid)}'),
  elements: INT{jsid},
  style: [
    {{ selector: 'node', style: {{
        'label': 'data(name)', 'font-size': '11px', 'color': '#e6e8ee',
        'background-color': '#3a4a6b', 'width': 44, 'height': 30,
        'text-valign': 'center', 'text-halign': 'center', 'shape': 'round-rectangle',
        'border-width': 1, 'border-color': '#2a2f3a',
    }} }},
    {{ selector: 'node.grp', style: {{
        'background-color': '#4f8cff', 'width': 'mapData(count, 1, 80, 50, 110)',
        'height': 36, 'font-weight': 'bold',
    }} }},
    {{ selector: 'edge', style: {{
        'width': 1.2, 'line-color': '#4f8cff', 'target-arrow-shape': 'triangle',
        'arrow-scale': 0.6, 'curve-style': 'bezier', 'target-arrow-color': '#4f8cff',
    }} }},
  ],
  layout: {{ name: 'dagre', rankDir: 'LR', nodeSep: 24, edgeSep: 12, rankSep: 70 }},
  wheelSensitivity: 0.3,
}});
window['cy{jsid}'] = cy{jsid}; // 暴露实例供调试/验证
// 保存组级元素引用（不销毁，下钻后恢复用）
const GROUP_ELEMS{jsid} = cy{jsid}.elements().copy();
let drilled{jsid} = false;
let drillPath{jsid} = '';
// 下钻：点击组节点 → 显示组内模块 DAG
cy{jsid}.on('tap', 'node', (evt) => {{
  const n = evt.target;
  if (n.hasClass('grp')) {{
    const gname = n.data('name');
    const drill = DRILL{jsid}[gname];
    if (drill && drill.nodes.length > 0) {{
      drilled{jsid} = true;
      drillPath{jsid} = gname;
      // 移除组级，添加模块级
      cy{jsid}.elements().remove();
      cy{jsid}.add(drill.nodes);
      cy{jsid}.add(drill.edges);
      cy{jsid}.layout({{ name: 'dagre', rankDir: 'LR', nodeSep: 12, edgeSep: 8, rankSep: 40 }}).run();
      cy{jsid}.fit();
      // 显示返回按钮 + 更新面包屑
      document.getElementById('int-back-{esc(nid)}').style.display = 'inline-block';
      document.getElementById('int-crumb-{esc(nid)}').textContent = '组级视图 / ' + gname;
    }}
  }} else {{
    alert('模块: ' + n.data('path'));
  }}
}});
// 返回组级视图
document.getElementById('int-back-{esc(nid)}').addEventListener('click', () => {{
  if (!drilled{jsid}) return;
  drilled{jsid} = false;
  drillPath{jsid} = '';
  cy{jsid}.elements().remove();
  cy{jsid}.add(GROUP_ELEMS{jsid}.copy());
  cy{jsid}.layout({{ name: 'dagre', rankDir: 'LR', nodeSep: 24, edgeSep: 12, rankSep: 70 }}).run();
  cy{jsid}.fit();
  document.getElementById('int-back-{esc(nid)}').style.display = 'none';
  document.getElementById('int-crumb-{esc(nid)}').textContent = '组级视图';
}});
</script>"""

    # ---- 小包：直接全量模块视图 ----
    jsid = nid.replace("-", "_")
    data_json = json.dumps({"nodes": nodes, "edges": es}, ensure_ascii=False)
    return f"""
<h3>模块内部结构 DAG（{int_data['module_count']} 模块 · {int_data['edge_count']} 边）</h3>
<div id="int-{esc(nid)}" style="width:100%;height:520px;background:#0b0e14;border:1px solid var(--border);border-radius:8px;"></div>
<script src="vendor/cytoscape.min.js"></script>
<script src="vendor/cytoscape-dagre.min.js"></script>
<script>
const INT{jsid} = {data_json};
const cy{jsid} = cytoscape({{
  container: document.getElementById('int-{esc(nid)}'),
  elements: INT{jsid},
  style: [
    {{ selector: 'node', style: {{
        'label': 'data(name)', 'font-size': '9px', 'color': '#9aa3b2',
        'background-color': '#3a4a6b', 'width': 22, 'height': 22,
        'text-valign': 'bottom', 'text-margin-y': 2, 'shape': 'round-rectangle',
    }} }},
    {{ selector: 'node.entry', style: {{ 'background-color': '#4f8cff', 'width': 30, 'height': 30 }} }},
    {{ selector: 'node.hot', style: {{ 'background-color': '#2d6b5f' }} }},
    {{ selector: 'node.leaf', style: {{ 'background-color': '#3a4a6b' }} }},
    {{ selector: 'edge', style: {{ 'width': 1, 'line-color': '#2a2f3a', 'target-arrow-shape': 'triangle', 'arrow-scale': 0.6, 'curve-style': 'bezier' }} }},
  ],
  layout: {{ name: 'dagre', rankDir: 'LR', nodeSep: 12, edgeSep: 8, rankSep: 40 }},
  wheelSensitivity: 0.3,
}});
cy{jsid}.on('tap', 'node', (evt) => {{ alert(evt.target.data('path')); }});
window['cy{jsid}'] = cy{jsid}; // 暴露实例供调试/验证
</script>"""

# ============ 每节点页 ============
def gen_node_page(nid):
    n = node_by_id.get(nid)
    if not n:
        return None
    short = n.get("short", nid)
    kind = n.get("kind", "package")
    grp = n.get("group", "")
    impl = n.get("implementation", "")
    provides = n.get("provides", "")
    why = n.get("why", "")
    hist = n.get("history", [])
    status = n.get("status", "")
    layer = n.get("layer", 0)
    enabled = n.get("enabled", True)
    # 依赖 / 被依赖
    outs = deps_list(nid)
    ins = deps_by(nid)
    # 改造原因（装配层专用：历史事件）
    hist_html = ""
    if hist:
        rows = "".join(f"<tr><td>{esc(h.get('date',''))}</td><td>{esc(h.get('change',''))}</td></tr>" for h in hist)
        hist_html = f"""<h3>改造历史</h3>
        <table><tr><th>日期</th><th>变更</th></tr>{rows}</table>"""
    elif status == "modified":
        hist_html = "<p style='color:var(--dim)'>该官方包被本机装配层引用（配置改造点）。</p>"
    # 内部结构
    int_html = internal_dag_html(nid) if kind == "package" else ""
    # 详情页状态
    status_badge = {
        "official": '<span class="tag">官方原生</span>',
        "modified": '<span class="tag yellow">被改造引用</span>',
        "external": '<span class="tag green">外部服务</span>',
    }.get(status, "")
    if n.get("layer_type") == "assembly":
        status_badge += '<span class="tag">装配层</span>'
    if enabled is False:
        status_badge += '<span class="tag red">已禁用</span>'

    dep_rows = "".join(f"<tr><td><a href='{esc(frm)}.html'>{esc(frm_name)}</a></td><td>{esc(mech)}</td><td><small>{esc(ev[:100])}</small></td></tr>" for frm, frm_name, mech, ev in outs)
    depby_rows = "".join(f"<tr><td><a href='{esc(to)}.html'>{esc(to_name)}</a></td><td>{esc(mech)}</td><td><small>{esc(ev[:100])}</small></td></tr>" for to, to_name, mech, ev in ins)

    # ---- 七段增强：⑤为什么存在（why） ⑥怎么用（how） ----
    whyhow_html = ""
    lt = n.get("layer_type", "")
    if lt == "assembly" and (n.get("why_history") or n.get("why_current")):
        why_hist = n.get("why_history", "") or ""
        why_cur = n.get("why_current", "") or ""
        how_trig = n.get("how_trigger", "") or ""
        how_wf = n.get("how_workflow", "") or ""
        how_collab = n.get("how_collaboration", "") or ""
        whyhow_html = f"""
  <h2>⑤ 为什么存在（why）</h2>
  <div class="why-block">
    <div class="why-item"><span class="why-label">历史引入动机</span><p>{list_to_text(why_hist)}</p></div>
    <div class="why-item"><span class="why-label">当前需求驱动</span><p>{list_to_text(why_cur)}</p></div>
  </div>

  <h2>⑥ 怎么用（how）</h2>
  <div class="how-block">
    <div class="how-item"><span class="how-label">触发方式</span><p>{list_to_text(how_trig)}</p></div>
    <div class="how-item"><span class="how-label">工作流/用法</span><p>{list_to_text(how_wf)}</p></div>
    <div class="how-item"><span class="how-label">协作关系</span><p>{list_to_text(how_collab)}</p></div>
  </div>
"""
    elif lt == "package" and (n.get("why_design") or n.get("why_modified") or n.get("how_use") or n.get("how_scenario")):
        why_design = n.get("why_design", "") or n.get("why", "") or ""
        why_mod = n.get("why_modified", "") or ""
        how_use = n.get("how_use", "") or ""
        how_scen = n.get("how_scenario", "") or ""
        whyhow_html = f"""
  <h2>⑤ 为什么存在（why）</h2>
  <div class="why-block">
    <div class="why-item"><span class="why-label">设计意图（官方）</span><p>{list_to_text(why_design)}</p></div>
    <div class="why-item"><span class="why-label">改造关联</span><p>{list_to_text(why_mod) or '<span class="empty">官方底座，未被本机装配层直接引用</span>'}</p></div>
  </div>

  <h2>⑥ 怎么用（how）</h2>
  <div class="how-block">
    <div class="how-item"><span class="how-label">怎么用</span><p>{list_to_text(how_use)}</p></div>
    <div class="how-item"><span class="how-label">典型场景与协作</span><p>{list_to_text(how_scen)}</p></div>
  </div>
"""
    elif lt == "external" and (n.get("why_need") or n.get("how_integrate")):
        why_need = n.get("why_need", "") or ""
        why_cur = n.get("why_current", "") or ""
        how_int = n.get("how_integrate", "") or ""
        how_usage = n.get("how_usage", "") or ""
        whyhow_html = f"""
  <h2>⑤ 为什么存在（why）</h2>
  <div class="why-block">
    <div class="why-item"><span class="why-label">为什么需要</span><p>{list_to_text(why_need)}</p></div>
    <div class="why-item"><span class="why-label">当前状态</span><p>{list_to_text(why_cur) or '<span class="empty">—</span>'}</p></div>
  </div>

  <h2>⑥ 怎么用（how）</h2>
  <div class="how-block">
    <div class="how-item"><span class="how-label">怎么接入</span><p>{list_to_text(how_int)}</p></div>
    <div class="how-item"><span class="how-label">装配层调用</span><p>{list_to_text(how_usage)}</p></div>
  </div>
"""

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(short)} · opencode DAG</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; padding:30px 20px 60px; }}
  .wrap {{ max-width:1100px; margin:0 auto; }}
  h1 {{ font-size:22px; margin-bottom:6px; display:flex; align-items:center; gap:12px; flex-wrap:wrap; }}
  .sub {{ color:var(--dim); font-size:13px; margin-bottom:20px; }}
  .tag {{ background:#20324f; color:#7fb0ff; padding:2px 10px; border-radius:20px; font-size:12px; }}
  .tag.yellow {{ background:#3a2f1a; color:#e0b25e; }}
  .tag.green {{ background:#1f3a2a; color:#5fd08a; }}
  .tag.red {{ background:#3a1f1f; color:#e06b6b; }}
  .nav {{ margin-bottom:20px; display:flex; gap:12px; align-items:center; }}
  .nav a {{ color:var(--accent); text-decoration:none; font-size:13px; }}
  .nav a:hover {{ text-decoration:underline; }}
  h2, h3 {{ margin:22px 0 10px; color:var(--dim); font-size:15px; border-bottom:1px solid var(--border); padding-bottom:6px; }}
  h3 {{ margin-top:30px; }}
  p {{ font-size:14px; line-height:1.8; color:var(--text); }}
  ul {{ font-size:14px; line-height:1.8; padding-left:22px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; margin-top:8px; }}
  th, td {{ border:1px solid var(--border); padding:6px 10px; text-align:left; }}
  th {{ background:var(--panel); color:var(--dim); }}
  td a {{ color:var(--accent); text-decoration:none; }}
  td small {{ color:var(--dim); }}
  .empty {{ color:var(--dim); font-size:13px; font-style:italic; }}
  .why-block, .how-block {{ display:flex; flex-direction:column; gap:10px; }}
  .why-item, .how-item {{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:12px 14px; }}
  .why-label, .how-label {{ display:inline-block; background:#1f3a2a; color:#5fd08a; padding:2px 10px; border-radius:20px; font-size:12px; margin-bottom:6px; }}
  .how-label {{ background:#3a2f1a; color:#e0b25e; }}
  .why-item p, .how-item p {{ margin-top:4px; font-size:13.5px; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="nav">
    <a href="../index.html">← 根入口</a>
    <a href="../04-interactive/view-modified.html">改造 DAG</a>
    <a href="index.html">节点索引</a>
  </div>
  <h1>{esc(short)} {status_badge}</h1>
  <div class="sub">{esc(nid)} · {esc(kind)} · {esc(grp)} · Layer {layer}</div>

  <h2>① 作用</h2>
  <p>{esc(impl) or '<span class="empty">暂无</span>'}</p>

  <h2>② 提供能力</h2>
  <p>{list_to_text(provides) or '<span class="empty">暂无</span>'}</p>

  <h2>③ 依赖（上游）</h2>
  {('<table><tr><th>节点</th><th>机制</th><th>证据</th></tr>' + dep_rows + '</table>') if outs else '<p class="empty">无内部依赖（或为叶子/外部）</p>'}

  <h2>④ 被依赖（下游）</h2>
  {('<table><tr><th>节点</th><th>机制</th><th>证据</th></tr>' + depby_rows + '</table>') if ins else '<p class="empty">无下游依赖</p>'}

  {whyhow_html}

  {hist_html}

  {int_html}
</div>
</body>
</html>"""
    return doc

# ============ 批量生成 ============
pages = []
for nid in sorted(node_by_id.keys()):
    doc = gen_node_page(nid)
    if doc is None:
        continue
    with open(os.path.join(NODES, f"{nid}.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    pages.append(nid)
print(f"generated {len(pages)} node pages")

# ============ 节点索引 ============
def node_rows():
    rows = []
    for nid in sorted(node_by_id.keys()):
        n = node_by_id[nid]
        rows.append(f"<tr><td><a href='{esc(nid)}.html'>{esc(n.get('short', nid))}</a></td><td>{esc(n.get('kind',''))}</td><td>{esc(n.get('group',''))}</td><td>Layer {n.get('layer',0)}</td></tr>")
    return "".join(rows)

idx = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>节点页索引 · opencode DAG</title>
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
</style>
</head>
<body>
<div class="wrap">
  <div class="nav"><a href="../index.html">← 根入口</a></div>
  <h1>节点页索引（{len(node_by_id)} 节点）</h1>
  <div class="sub">36 官方包 + 69 装配组件 + 9 外部服务</div>
  <table>
    <tr><th>节点</th><th>类型</th><th>组</th><th>层</th></tr>
    {node_rows()}
  </table>
</div>
</body>
</html>"""
with open(os.path.join(NODES, "index.html"), "w", encoding="utf-8") as f:
    f.write(idx)
print("generated nodes index")
