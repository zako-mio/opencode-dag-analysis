# -*- coding: utf-8 -*-
"""
S4e: 主页面全面升级 — 简介 + 三图卡片(含对比) + 核心结论 + 历史时间线 + 装配体系导航 + 统计面板
输出: index.html（覆盖 gen-interactive.py 生成的简易版）
"""
import json, os, sys, html

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")
CKPT = os.path.join(BASE, "07-checkpoint")

with open(os.path.join(DATA, "official-dag.json"), encoding="utf-8") as f:
    official = json.load(f)
with open(os.path.join(DATA, "diff-dag.json"), encoding="utf-8") as f:
    diff = json.load(f)
with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    modified = json.load(f)
with open(os.path.join(CKPT, "s2-assembly-semantics.json"), encoding="utf-8") as f:
    asm = json.load(f)
history = asm["history"]

def esc(s):
    return html.escape(str(s))

# 历史时间线 HTML
timeline_rows = ""
for ev in sorted(history, key=lambda x: x.get("date", "")):
    date = ev.get("date", "")
    area = ev.get("area", "")
    change = ev.get("change", "")
    reason = ev.get("reason", "")[:120]
    timeline_rows += f"""
    <div class="tl-item">
      <div class="tl-date">{esc(date)}</div>
      <div class="tl-body">
        <div class="tl-area">{esc(area)}</div>
        <div class="tl-change">{esc(change)}</div>
        <div class="tl-reason">{esc(reason)}</div>
      </div>
    </div>"""

# 装配体系分类统计
asm_kinds = {}
for n in modified["nodes"]:
    if n.get("layer_type") == "assembly":
        k = n.get("kind", "other")
        asm_kinds[k] = asm_kinds.get(k, 0) + 1

kind_zh = {
    "skill": "Skills 技能", "agent": "Agents 代理", "mcp": "MCP 服务",
    "plugin": "插件", "tool": "工具", "command": "命令", "instruction": "指令", "config": "配置本体",
}
asm_nav = ""
for k, cnt in sorted(asm_kinds.items()):
    zh = kind_zh.get(k, k)
    # 生成该类索引锚点（在节点页索引里按 kind 过滤）
    asm_nav += f"<a class='chip' href='02-nodes/index.html'><b>{esc(zh)}</b><small>{cnt}</small></a>"

# 核心结论
conclusions = [
    ("改造深度", "仅 6 个官方包（opencode/core/schema/plugin/sdk/server）被装配层直接引用。opencode 的扩展点是 <b>配置装配层</b>（~/.config/opencode），而非源码 fork。"),
    ("装配体系", "61 个装配组件：43 skills + 7 agents + 6 mcp + 1 plugin + 1 tool + 1 command + 2 instructions + 1 config。真正触核心包的只有配置层，skills 大多挂外部服务。"),
    ("skill 协作网络", "33 条 skill 间作用关系：OpenSpec 12-skill 工作流闭环、superpowers 家族、DAG 三 skill 上下游链、amap 协作路由、recruit↔browser。装配层是一个有内部协作网络的体系。"),
    ("历史脉络", "18 个改造事件（2026-08-01~17）：输入缓存优化 → MCP 精兵策略 → 编码安全三层防御 → Reflection 自进化 → VLM 双通道修复 → 降本（Flash）→ 部分回滚 Pro。每次改造都需求驱动、有据可查。"),
]

concl_html = ""
for title, text in conclusions:
    concl_html += f"""
    <div class="concl-item">
      <h4>{esc(title)}</h4>
      <p>{text}</p>
    </div>"""

# 外部服务
ext_names = [n.get("short", n["id"]) for n in modified["nodes"] if n.get("layer_type") == "external"]

doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>opencode DAG 依赖分析 · 改造结果与官方对比</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --panel2:#1c2230; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; --green:#5fd08a; --yellow:#e0b25e; --red:#e06b6b; --purple:#b48ae0; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; padding:40px 20px 80px; }}
  .wrap {{ max-width:1200px; margin:0 auto; }}
  h1 {{ font-size:28px; margin-bottom:8px; }}
  .sub {{ color:var(--dim); font-size:14px; margin-bottom:30px; line-height:1.8; }}
  .section {{ margin-top:44px; }}
  .section h2 {{ font-size:20px; margin-bottom:16px; color:var(--text); border-bottom:1px solid var(--border); padding-bottom:10px; }}
  .section h2 .tag {{ font-size:12px; background:#20324f; color:#7fb0ff; padding:2px 10px; border-radius:20px; margin-left:10px; vertical-align:middle; }}

  /* 三图卡片 */
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:16px; }}
  .card {{ background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:22px; text-decoration:none; color:var(--text); display:block; transition:all .2s; position:relative; overflow:hidden; }}
  .card:hover {{ border-color:var(--accent); transform:translateY(-2px); box-shadow:0 4px 20px rgba(0,0,0,.3); }}
  .card .tag {{ display:inline-block; padding:3px 12px; border-radius:20px; font-size:12px; margin-bottom:12px; }}
  .card .tag.t1 {{ background:#20324f; color:#7fb0ff; }}
  .card .tag.t2 {{ background:#3a2f1a; color:var(--yellow); }}
  .card .tag.t3 {{ background:#1f3a2a; color:var(--green); }}
  .card h3 {{ font-size:17px; margin-bottom:10px; }}
  .card .meta {{ color:var(--dim); font-size:13px; line-height:1.8; }}
  .card .stat {{ display:flex; gap:16px; margin-top:14px; padding-top:12px; border-top:1px solid var(--border); font-size:12px; color:var(--dim); }}
  .card .stat b {{ color:var(--accent); font-size:15px; display:block; }}

  /* 核心结论 */
  .concl-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }}
  .concl-item {{ background:var(--panel); border:1px solid var(--border); border-left:4px solid var(--accent); border-radius:10px; padding:16px 18px; }}
  .concl-item h4 {{ font-size:15px; color:var(--accent); margin-bottom:8px; }}
  .concl-item p {{ font-size:13.5px; line-height:1.8; color:var(--dim); }}

  /* 时间线 */
  .timeline {{ position:relative; padding-left:24px; }}
  .timeline::before {{ content:''; position:absolute; left:8px; top:0; bottom:0; width:2px; background:var(--border); }}
  .tl-item {{ position:relative; margin-bottom:20px; }}
  .tl-item::before {{ content:''; position:absolute; left:-22px; top:6px; width:10px; height:10px; border-radius:50%; background:var(--accent); }}
  .tl-date {{ font-size:13px; color:var(--accent); font-weight:600; margin-bottom:4px; }}
  .tl-body {{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:12px 14px; }}
  .tl-area {{ display:inline-block; background:#20324f; color:#7fb0ff; padding:1px 8px; border-radius:12px; font-size:11px; margin-bottom:6px; }}
  .tl-change {{ font-size:13px; line-height:1.7; }}
  .tl-reason {{ font-size:12px; color:var(--dim); margin-top:4px; font-style:italic; }}

  /* 装配导航 */
  .chips {{ display:flex; flex-wrap:wrap; gap:10px; }}
  .chip {{ display:inline-flex; align-items:center; gap:8px; background:var(--panel); border:1px solid var(--border); border-radius:24px; padding:8px 16px; text-decoration:none; color:var(--text); font-size:13px; transition:border-color .2s; }}
  .chip:hover {{ border-color:var(--accent); }}
  .chip b {{ font-weight:600; }}
  .chip small {{ background:var(--panel2); color:var(--dim); padding:1px 8px; border-radius:12px; font-size:11px; }}

  /* 快速入口 */
  .links {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:10px; }}
  .links a {{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:10px 14px; color:var(--text); text-decoration:none; font-size:13px; transition:border-color .2s; }}
  .links a:hover {{ border-color:var(--accent); }}
  .links a small {{ color:var(--dim); display:block; font-size:11px; margin-top:2px; }}

  .ext-line {{ color:var(--dim); font-size:13px; margin-top:12px; }}
  .ext-line b {{ color:var(--green); }}
</style>
</head>
<body>
<div class="wrap">
  <h1>opencode DAG 依赖分析</h1>
  <div class="sub">
    以 DAG 结构化展开 <b>opencode 改造结果</b> 与 <b>官方 opencode</b> 的对比。<br>
    三图渐进式：<b>官方原版</b>（基线）→ <b>对比</b>（改造点）→ <b>改造版双层</b>（包级 + 装配层）。<br>
    数据源：官方 v1.18.14 源码（35 workspace 包）+ 本机 ~/.config/opencode 装配层（61 组件）。
  </div>

  <!-- 三图卡片 -->
  <div class="section">
    <h2>三图总览 <span class="tag">渐进式理解</span></h2>
    <div class="cards">
      <a class="card" href="04-interactive/view-official.html">
        <span class="tag t1">图1 · 基线</span>
        <h3>官方原版包级 DAG</h3>
        <div class="meta">opencode 官方 monorepo 的 35 个 workspace 包依赖关系，未改造基线。看官方架构：schema 数据模型 → llm/protocol 层 → core 服务 → app/cli/tui 应用。</div>
        <div class="stat">
          <div><b>{official['stats']['nodes']}</b>包</div>
          <div><b>{official['stats']['edges']}</b>边</div>
          <div><b>{official['stats']['layers']}</b>层</div>
          <div><b>{official['stats']['groups']}</b>组</div>
        </div>
      </a>
      <a class="card" href="04-interactive/view-diff.html">
        <span class="tag t2">图2 · 对比</span>
        <h3>官方 + 改造对比 DAG</h3>
        <div class="meta">官方包为基线，标注哪些包被改造引用（黄边）、外部服务（绿）。改造不深：仅 6 包被引用，扩展点是配置层。</div>
        <div class="stat">
          <div><b>{diff['stats']['nodes']}</b>节点</div>
          <div><b>{diff['stats'].get('modified_pkgs', 6)}</b>被改造</div>
          <div><b>{diff['stats'].get('external_nodes', 8)}</b>外部</div>
        </div>
      </a>
      <a class="card" href="04-interactive/view-modified.html">
        <span class="tag t3">图3 · 改造版</span>
        <h3>改造版双层 DAG</h3>
        <div class="meta">包级 + 装配层双层：35 官方包（下）+ 61 装配组件（skills/agents/mcp/tools）+ 外部服务。装配层内部有 33 条 skill 协作关系。</div>
        <div class="stat">
          <div><b>{modified['stats']['nodes']}</b>节点</div>
          <div><b>{modified['stats']['edges']}</b>边</div>
          <div><b>{modified['stats']['groups']}</b>组</div>
        </div>
      </a>
    </div>
    <div class="ext-line">外部服务：{' / '.join(f'<b>{esc(n)}</b>' for n in ext_names)}</div>
  </div>

  <!-- 核心结论 -->
  <div class="section">
    <h2>核心结论 <span class="tag">本项目的洞察</span></h2>
    <div class="concl-grid">{concl_html}</div>
  </div>

  <!-- 历史变迁时间线 -->
  <div class="section">
    <h2>改造历史时间线 <span class="tag">{len(history)} 事件</span></h2>
    <div class="timeline">{timeline_rows}</div>
  </div>

  <!-- 装配体系导航 -->
  <div class="section">
    <h2>装配体系 <span class="tag">{sum(asm_kinds.values())} 组件</span></h2>
    <div class="chips">{asm_nav}</div>
    <div class="ext-line">每个装配组件有完整 <b>why（历史引入动机 + 当前需求驱动）- how（触发/工作流/协作）</b> 说明，见节点页 ⑤⑥ 段。</div>
  </div>

  <!-- 快速入口 -->
  <div class="section">
    <h2>快速入口</h2>
    <div class="links">
      <a href="04-interactive/view-official.html">图1 官方 DAG<small>35 包 · {official['stats']['edges']} 边 · {official['stats']['groups']} 组</small></a>
      <a href="04-interactive/view-diff.html">图2 对比 DAG<small>{diff['stats']['nodes']} 节点 · {diff['stats']['edges']} 边</small></a>
      <a href="04-interactive/view-modified.html">图3 改造双层 DAG<small>{modified['stats']['nodes']} 节点 · {modified['stats']['groups']} 组</small></a>
      <a href="03-groups/index.html">组目录<small>{modified['stats']['groups']} 组索引</small></a>
      <a href="02-nodes/index.html">节点页索引<small>{len(modified['nodes'])} 节点全页</small></a>
      <a href="05-diff/diff-list.html">改造差异清单<small>改造点明细</small></a>
      <a href="05-drawio/main/modified.png">改造双层静态图<small>drawio PNG</small></a>
      <a href="06-md/00-index.md">MD 镜像（AI 检索）<small>全节点文本</small></a>
      <a href="01-dag-data/modified-dag.json">改造 DAG JSON<small>含 why/how 数据</small></a>
      <a href="README.md">README<small>项目说明</small></a>
    </div>
  </div>
</div>
</body>
</html>"""

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(doc)
print(f"index.html upgraded: {len(doc)} bytes")
