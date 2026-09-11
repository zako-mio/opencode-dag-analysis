# -*- coding: utf-8 -*-
"""S4: 重建三图 DAG（official / diff / modified），含 mechanism 节点与全边丰富化"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = "/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag"
CKPT = os.path.join(BASE, "08-collect")
DATA = os.path.join(BASE, "01-dag-data")
os.makedirs(DATA, exist_ok=True)

def load(p):
    with open(os.path.join(CKPT,p),encoding="utf-8") as f: return json.load(f)

pkg_deps = load("s1-package-deps.json")
asm_inv = load("s2-all-components.json")["components"]
mech = load("stage-03-mechanisms.json")
new_asm = load("stage-03-new-assembly.json")
pkg_updates = load("stage-03-package-updates.json")["package_updates"]
httpapi = load("stage-03-httpapi-codegen.json")
opencode_go = load("stage-03-opencode-go.json")

# ============ 官方包节点（36） ============
# 0817 官方包语义（保留）+ httpapi-codegen 新增
PKG_GROUP = {
    "oc-schema":"G1-数据模型","oc-protocol":"G2-通信协议","oc-client":"G3-客户端",
    "oc-sdk":"G3-客户端","oc-sdk-next":"G3-客户端","oc-server":"G4-服务端",
    "oc-llm":"G5-LLM请求层","oc-core":"G6-核心服务","oc-plugin":"G7-插件SDK",
    "oc-tui":"G8-终端UI","oc-ui":"G9-UI组件","oc-session-ui":"G9-UI组件",
    "oc-app":"G10-应用","oc-desktop":"G10-应用","oc-cli":"G10-应用",
    "oc-web":"G11-文档站点","oc-enterprise":"G10-应用","oc-storybook":"G11-文档站点",
    "oc-codemode":"G12-沙箱","oc-function":"G13-边缘服务",
    "oc-http-recorder":"G14-工具","oc-script":"G14-工具","oc-httpapi-codegen":"G14-工具",
    "oc-effect-sqlite-node":"G15-存储适配","oc-effect-drizzle-sqlite":"G15-存储适配",
    "oc-console-app":"G16-Console","oc-console-core":"G16-Console","oc-console-function":"G16-Console",
    "oc-console-mail":"G16-Console","oc-console-resource":"G16-Console","oc-console-support":"G16-Console",
    "oc-stats-app":"G17-Stats","oc-stats-core":"G17-Stats","oc-stats-server":"G17-Stats",
    "oc-slack":"G18-集成","oc-opencode":"G19-主入口",
}
SHORT_ORDER = ["opencode","core","schema","llm","plugin","sdk","server","protocol","client","tui","codemode","http-recorder","app","ui","session-ui","desktop","cli","web","enterprise","function","storybook","script","effect-sqlite-node","effect-drizzle-sqlite","console-app","console-core","console-function","console-mail","console-resource","console-support","stats-app","stats-core","stats-server","sdk-next","slack","httpapi-codegen"]

# 官方包基本节点（从 s1-package-deps 重建）
pkg_by_id = {}
for p in pkg_deps["packages"]:
    n = p["name"]
    if n=="opencode": pid="oc-opencode"
    elif n=="@opencode-ai/sdk": pid="oc-sdk"
    elif n=="@opencode-ai/sdk-next": pid="oc-sdk-next"
    else: pid="oc-"+n.replace("@opencode-ai/","")
    pkg_by_id[pid] = {"id":pid,"name":n,"short":pid.replace("oc-",""),"group":PKG_GROUP.get(pid,"G-其他"),"group_name":PKG_GROUP.get(pid,"G-其他"),"kind":"package","layer":0,"layer_type":"package"}
# httpapi-codegen
pkg_by_id["oc-httpapi-codegen"]["name"]="@opencode-ai/httpapi-codegen"
pkg_by_id["oc-httpapi-codegen"]["short"]="httpapi-codegen"

# 0817 官方包语义（implementation/provides/why）—— 复用
try:
    old_official = load("../01-dag-data/official-dag.json") if False else None
except: old_official=None
old_official = None
old_official_path = os.path.join(DATA,"official-dag.json")
if os.path.exists(old_official_path):
    old_official = json.load(open(old_official_path,encoding="utf-8"))
old_sem = {n["id"]:n for n in (old_official["nodes"] if old_official else [])}

# 官方节点语义补全（保留 0817 语义 + 补版本变化 + httpapi）
for pid, node in pkg_by_id.items():
    old = old_sem.get(pid,{})
    node["implementation"]=old.get("implementation","")
    node["provides"]=old.get("provides","")
    node["key_modules"]=old.get("key_modules",[])
    node["why_design"]=old.get("why_design",old.get("why",""))
    node["why_modified"]=old.get("why_modified","")
    node["how_use"]=old.get("how_use","")
    node["how_scenario"]=old.get("how_scenario","")
    up = pkg_updates.get(pid,{})
    node["version_delta"]=up.get("version_delta","v1.18.14 → v1.18.30")
    node["what_changed"]=up.get("what_changed","")
# httpapi-codegen 专用
pkg_by_id["oc-httpapi-codegen"]["implementation"]=httpapi["implementation"]
pkg_by_id["oc-httpapi-codegen"]["provides"]=httpapi["provides"]
pkg_by_id["oc-httpapi-codegen"]["why_design"]=httpapi["why_design"]
pkg_by_id["oc-httpapi-codegen"]["how_use"]=httpapi["how_use"]
pkg_by_id["oc-httpapi-codegen"]["how_scenario"]=httpapi["how_scenario"]

official_nodes = list(pkg_by_id.values())
# 官方边（沿用 0817 基线的 workspace + import + semantic，并补 httpapi→client）
official_edges_std = []
# 采用 0817 边作为权威基线，若旧数据存在则读
old_edges = []
if old_official:
    old_edges = old_official["edges"]
for e in old_edges:
    official_edges_std.append({"from":e["from"],"to":e["to"],"mechanism":e.get("mechanism","workspace-dep"),"evidence":e.get("evidence",""),"evidence_example":e.get("evidence_example",""),"import_refs":e.get("import_refs",0)})
# workspace 提取边（56 条，从 s1 规范化）
seen = set()
for e in pkg_deps["edges"]:
    key=(e["from"],e["to"])
    if key in seen: continue
    seen.add(key)
    if all(k in pkg_by_id for k in key):
        official_edges_std.append({"from":e["from"],"to":e["to"],"mechanism":"workspace-dep","evidence":"v1.18.30 workspace dep","evidence_example":"","import_refs":0})
# httpapi-codegen → oc-client（被 client 依赖）
official_edges_std.append({"from":"oc-httpapi-codegen","to":"oc-client","mechanism":"workspace-dep","evidence":"client depends on httpapi-codegen","evidence_example":"","import_refs":0})
# 去重
se=set(); dedup=[]
for e in official_edges_std:
    key=(e["from"],e["to"])
    if key in se: continue
    se.add(key); dedup.append(e)
official_edges = dedup
print("官方包节点:",len(official_nodes),"官方边:",len(official_edges))

with open(os.path.join(DATA,"official-dag.json"),"w",encoding="utf-8") as f:
    json.dump({"name":"official","title":"官方原版 opencode 包级 DAG (v1.18.30)","version_note":"基于官方源码 v1.18.30，36 workspace 包","nodes":official_nodes,"edges":official_edges,"groups":list(dict.fromkeys(n["group"] for n in official_nodes)),
     "stats":{"nodes":len(official_nodes),"edges":len(official_edges),"layers":0,"groups":len(set(n["group"] for n in official_nodes)),"has_cycle":False,"modified_pkgs":0,"external_nodes":0}},f,ensure_ascii=False,indent=2)
print("official 已写入")

# ============ 工具函数：拓扑分层 + 无环 ============
def topo_layer(nodes, edges):
    in_deg={n["id"]:0 for n in nodes}; adj={n["id"]:[] for n in nodes}
    for e in edges:
        if e["from"] in in_deg and e["to"] in in_deg:
            in_deg[e["to"]]+=1; adj[e["from"]].append(e["to"])
    from collections import deque
    q=deque([nid for nid,d in in_deg.items() if d==0]); layer={}; l=0
    while q:
        for nid in q: layer[nid]=l
        nxt=[]
        for nid in q:
            for to in adj[nid]:
                in_deg[to]-=1
                if in_deg[to]==0: nxt.append(to)
        q=nxt; l+=1
    for n in nodes:
        if n["id"] not in layer: layer[n["id"]]=l
    return layer
def has_cycle(nodes, edges):
    in_deg={n["id"]:0 for n in nodes}; adj={n["id"]:[] for n in nodes}
    for e in edges:
        if e["from"] in in_deg and e["to"] in in_deg:
            in_deg[e["to"]]+=1; adj[e["from"]].append(e["to"])
    from collections import deque
    q=deque([nid for nid,d in in_deg.items() if d==0]); visited=0
    while q:
        n=q.popleft(); visited+=1
        for to in adj[n]:
            in_deg[to]-=1
            if in_deg[to]==0: q.append(to)
    return visited!=len(nodes)

# ============ diff 图（官方 + 改造点染色 + 外部服务）============
# 先确定被装配层引用的官方包
pkg_used_by_asm = set()
# 装配层→官方包 边规则（基于已知关系）
asm_to_pkg = []
for c in asm_inv:
    cid=c["id"]; name=c.get("name","")
    if c["kind"]=="agent":
        # agent 依赖核心包（plan/build 主 Agent 用全部包；子Agent 用特定）
        if cid in ("agent-plan","agent-build"):
            for pid in ["oc-opencode","oc-core","oc-schema","oc-llm","oc-plugin","oc-sdk","oc-server"]:
                asm_to_pkg.append((pid,cid,"agent-core"))
        elif cid=="agent-vision-worker": asm_to_pkg.append(("oc-core","agent-vision-worker","agent-dep"))
        elif cid in ("agent-pdf-worker","agent-drawio-worker","agent-reflection-worker","agent-architect-worker"):
            asm_to_pkg.append(("oc-core",cid,"agent-dep"))
        elif cid in ("agent-general","agent-explore"): asm_to_pkg.append(("oc-schema",cid,"agent-dep"))
        elif cid=="agent-search-worker": asm_to_pkg.append(("oc-schema",cid,"agent-dep"))
    elif c["kind"]=="skill":
        # skill 依赖外部服务/包的按描述推断（简化：核心 skill 依赖 oc-core）
        if name in ("opencode-config","grill-me","headroom"): asm_to_pkg.append(("oc-core",cid,"skill-dep"))
    elif c["kind"]=="instruction":
        asm_to_pkg.append(("oc-opencode",cid,"instruction-load"))
    elif c["kind"]=="mcp":
        if cid=="mcp-pdf-reader": asm_to_pkg.append(("oc-schema",cid,"mcp-dep"))
        elif cid=="mcp-drawio": asm_to_pkg.append(("oc-plugin",cid,"mcp-dep"))
    elif c["kind"]=="tool": asm_to_pkg.append(("oc-opencode",cid,"tool-dep"))
    elif c["kind"]=="command": asm_to_pkg.append(("oc-opencode",cid,"command-dep"))
    elif c["kind"]=="config": asm_to_pkg.append(("oc-opencode",cid,"config-dep"))
for pid,_cid,_m in asm_to_pkg: pkg_used_by_asm.add(pid)

ext_nodes = [
 {"id":"ext-glm-api","name":"GLM API（智谱）","kind":"external","group":"X-外部服务","implementation":"VLM 图片转文字服务（glm-4.6v / glm-5.3-flash）","provides":"图片描述 + 编码模型","why_need":"VLM 双链路首选（read.ts），响应快、限流额度高","how_integrate":"env ZHIPU_API_KEY → open.bigmodel.cn/api/paas/v4","why_current":"GLM-4.6v 视觉 / GLM-5.3-flash 编码","layer":0},
 {"id":"ext-amap-api","name":"高德地图 API","kind":"external","group":"X-外部服务","implementation":"地图 POI/路径规划服务","provides":"地图能力","why_need":"地图类任务（amap skill 引用）","how_integrate":"amap-mcp-wrapper.ps1","why_current":"已禁用 mcp-amap","layer":0},
 {"id":"ext-lark-api","name":"飞书/Lark API","kind":"external","group":"X-外部服务","implementation":"lark-cli 调用的飞书开放平台","provides":"日历/文档/多维表格等","why_need":"lark-suite skill 依赖","how_integrate":"lark-cli","why_current":"启用 lark-suite skill","layer":0},
 {"id":"ext-chrome","name":"Chrome 浏览器","kind":"external","group":"X-外部服务","implementation":"browser-harness 自动化浏览器","provides":"网页自动化","why_need":"browser-harness skill 依赖","how_integrate":"PowerShell CDP + close-chrome-tabs.ps1","why_current":"WSL2 用 agent-browser","layer":0},
 {"id":"ext-deepseek-api","name":"DeepSeek API（官方直连）","kind":"external","group":"X-外部服务","implementation":"deepseek-v4-pro/flash/flash-vision-exp 模型 API","provides":"LLM 推理 + 视觉","why_need":"官方直连兜底 Pro 与视觉；主 Agent 默认模型","how_integrate":"env DEEPSEEK_API_KEY → api.deepseek.com/v1","why_current":"承载 deepseek-v4-pro(仅官方) + vision-exp","layer":0},
 {"id":"ext-drawio-service","name":"draw.io 服务","kind":"external","group":"X-外部服务","implementation":"draw.io 在线/本地图表渲染","provides":"图表导出","why_need":"drawio-worker 子Agent 依赖","how_integrate":"drawio-mcp-minimal + DRAWIO_BASE_URL","why_current":"启用 mcp-drawio","layer":0},
 {"id":"ext-sylphx-pdf","name":"@sylphx/pdf-reader-mcp","kind":"external","group":"X-外部服务","implementation":"PDF 文本提取 npm 包","provides":"PDF 提取","why_need":"pdf-worker 子Agent 依赖","how_integrate":"npx @sylphx/pdf-reader-mcp","why_current":"启用 mcp-pdf-reader","layer":0},
 {"id":"ext-opencode-plugin","name":"@opencode-ai/plugin SDK","kind":"external","group":"X-外部服务","implementation":"插件 SDK（node_modules 1.18.x）","provides":"插件钩子类型","why_need":"plugin 开发（已无插件但 SDK 保留）","how_integrate":"node_modules @opencode-ai/plugin","why_current":"插件目录已空","layer":0},
  {"id":"ext-opencode-go","name":"OpenCode Go 套餐","kind":"external","group":"X-外部服务","implementation":"OpenAI 兼容协议（@ai-sdk/openai-compatible），baseURL=opencode.ai/zen/go/v1。订阅套餐 $10/月($60 额度)，DeepSeek Flash 包月 3x","provides":"deepseek-v4-flash(go) / glm-5.2 / kimi-k2.7-code / qwen3.7-plus / muse-spark-1.3-contributor / hy4-preview / omen-alpha(stealth) 模型","why_need":"覆盖高性价比编码模型（Flash 包月 3x 额度）+ 新增 Muse Spark 1.3/Hy4/Omen Alpha","how_integrate":"env OPENCODE_GO_API_KEY","why_current":"blacklist deepseek-v4-pro（仅官方直连）","layer":0},
  {"id":"ext-tavily-api","name":"Tavily Search API","kind":"external","group":"X-外部服务","implementation":"外部搜索 API（web search，1 credit/次），search-methodology/skill 的发现层外部搜索降级链首选","provides":"外部事实搜索/网页检索","why_need":"search-methodology skill 依赖外部搜索后端做发现层；search-worker 子Agent 证据包构建","how_integrate":"env TAVILY_API_KEY → api.tavily.com/search","why_current":"0905 联网搜索能力架构新增；search-methodology/skill 依赖","layer":0},
]
print("外部服务:",len(ext_nodes))
for en in ext_nodes: en["layer_type"]="external"

# ---- diff 图 ----
diff_nodes=[]
for n in official_nodes:
    nn=dict(n)
    nn["status"]="modified" if n["id"] in pkg_used_by_asm else "official"
    diff_nodes.append(nn)
ext_id_set=set()
for en in ext_nodes:
    en2=dict(en); en2["status"]="external"; diff_nodes.append(en2); ext_id_set.add(en["id"])

diff_edges=[dict(e) for e in official_edges]
# 注：diff 图只画官方包依赖边（68），装配层→官方包引用仅作 status 染色标记，不画成边（避免悬空，同 0902 设计）

layer2=topo_layer(diff_nodes,diff_edges)
for n in diff_nodes: n["layer"]=layer2.get(n["id"],0)
diff_dag={"name":"diff","title":"官方 + 改造对比 DAG (v1.18.30 基线 + 装配层引用染色)","version_note":"官方 v1.18.30 基线；改造点=装配层引用（红）+ 外部服务（绿）","nodes":diff_nodes,"edges":diff_edges,"groups":list(dict.fromkeys(n["group"] for n in diff_nodes)),
 "stats":{"nodes":len(diff_nodes),"edges":len(diff_edges),"layers":max(layer2.values())+1 if layer2 else 0,"groups":len(set(n["group"] for n in diff_nodes)),"has_cycle":has_cycle(diff_nodes,diff_edges),"modified_pkgs":len(pkg_used_by_asm),"external_nodes":sum(1 for n in diff_nodes if n.get("status")=="external")}}
with open(os.path.join(DATA,"diff-dag.json"),"w",encoding="utf-8") as f: json.dump(diff_dag,f,ensure_ascii=False,indent=2)
print(f"diff: {diff_dag['stats']}")

# ============ modified 图（包级 + 装配层双层 + mechanism）============
# skill 功能域子分组
SKILL_GROUP={
 "agency-agents":"A6a-角色调度","grill-me":"A6a-角色调度","opencode-config":"A6a-配置知识",
 "drawio-reference":"A6b-图表","cytoscape-dag-visualization":"A6c-DAG方法","multi-window-dag-delivery":"A6c-DAG方法","dag-tutorial-authoring":"A6c-DAG方法",
 "frontend-design":"A6d-前端设计","browser-harness":"A6e-浏览器","lark-suite":"A6f-办公集成",
 "pdf-ocr":"A6g-文档处理","headroom":"A6h-上下文压缩","recruit-assist":"A6i-简历求职","resume-builder":"A6i-简历求职","soe-resume":"A6i-简历求职","search-methodology":"A6j-联网搜索","login-auth-channel":"A6j-联网搜索",
 "openspec-propose":"A6l-OpenSpec工作流","openspec-new-change":"A6l-OpenSpec工作流","openspec-ff-change":"A6l-OpenSpec工作流","openspec-explore":"A6l-OpenSpec工作流",
 "openspec-apply-change":"A6l-OpenSpec工作流","openspec-verify-change":"A6l-OpenSpec工作流","openspec-continue-change":"A6l-OpenSpec工作流",
 "openspec-archive-change":"A6l-OpenSpec工作流","openspec-bulk-archive-change":"A6l-OpenSpec工作流","openspec-sync-specs":"A6l-OpenSpec工作流",
 "openspec-update-change":"A6l-OpenSpec工作流","openspec-onboard":"A6l-OpenSpec工作流","release-openspec":"A6l-OpenSpec工作流",
 "superpowers-feature-workflow":"A6m-Superpowers","superpowers-learning-workflow":"A6m-Superpowers","superpowers-openspec-superpowers-workflow":"A6m-Superpowers",
 "architecture-judgment":"A6n-架构判断",
 "github-bulk-upload":"A6o-交付发布","single-source-docs-pipeline":"A6o-交付发布",
 "job-listing-filter":"A6i-简历求职",
 "kb-construction":"A6q-知识库构建","restricted-corpus-acquisition":"A6q-知识库构建","resumable-content-pipeline":"A6q-知识库构建",
 "opencode-capability-extension":"A6a-配置知识",
}
AGENT_GROUP={"agent-plan":"AG1-主Agent","agent-build":"AG1-主Agent"}
# 装配分组
def asm_group(c):
    kind=c["kind"]; name=c.get("name","")
    if kind=="agent":
        return "AG1-主Agent" if c["id"] in ("agent-plan","agent-build") else "AG2-子Agent"
    if kind=="mcp": return "AG3-MCP"
    if kind=="instruction": return "AG4-指令"
    if kind=="tool": return "AG5-工具插件"
    if kind=="command": return "AG5-工具插件"
    if kind=="config": return "AG6-配置本体"
    if kind=="skill": return SKILL_GROUP.get(name,"A6k-其他技能")
    if kind=="mechanism": return "AQ-自进化机制"
    return "AG-其他"

asm_nodes=[]
for c in asm_inv:
    cid=c["id"]; kind=c["kind"]; name=c.get("name","")
    grp=asm_group(c)
    node={"id":cid,"name":name if kind!="skill" else name,"short":cid.split("-",1)[1] if "-" in cid else cid,
      "group":grp,"group_name":grp,"kind":kind,"layer_type":"assembly",
      "implementation":c.get("desc",""),"provides":"","layer":0,"enabled":c.get("enabled",True),
      "source":c.get("source","")}
    # 语义补全（机制、新增组件）
    if kind=="mechanism":
        m=mech.get(cid,{})
        node["why_history"]=m.get("why_history",""); node["why_current"]=m.get("why_current","")
        node["how_trigger"]=m.get("how_trigger",""); node["how_workflow"]=m.get("how_workflow","")
        node["how_collaboration"]=m.get("how_collaboration","")
    elif cid in new_asm:
        m=new_asm[cid]
        node["implementation"]=c.get("desc","") or node.get("implementation","")
        node["why_history"]=m.get("why_history",""); node["why_current"]=m.get("why_current","")
        node["how_trigger"]=m.get("how_trigger",""); node["how_workflow"]=m.get("how_workflow","")
        node["how_collaboration"]=m.get("how_collaboration","")
        node["dependencies"]=m.get("dependencies",[])
    asm_nodes.append(node)
print("装配层节点:",len(asm_nodes))

# ---- modified 边（全边丰富化）----
mod_edges=[dict(e) for e in official_edges]
# 1. 装配 → 官方包
for pid,cid,m in asm_to_pkg:
    mod_edges.append({"from":pid,"to":cid,"mechanism":m,"evidence":"装配层→官方包","evidence_example":"","import_refs":0})
# 2. 装配 → 外部服务（组件依赖外部）
asm_ext_rules=[
 # (组件, 外部服务, 依赖理由)
 ("agent-vision-worker","ext-deepseek-api","vision 模型依赖官方 DeepSeek"),
 ("config-main","ext-opencode-go","provider Go 套餐"),
 ("config-main","ext-deepseek-api","provider DeepSeek 官方"),
 ("config-main","ext-glm-api","provider 智谱 GLM"),
 ("skill-lark-suite","ext-lark-api","lark-cli 调用飞书"),
 ("skill-browser-harness","ext-chrome","浏览器自动化"),
 ("skill-drawio-reference","ext-drawio-service","draw.io 导出"),
 ("skill-pdf-ocr","ext-sylphx-pdf","PDF 提取"),
 ("mcp-pdf-reader","ext-sylphx-pdf","PDF MCP 服务"),
 ("mcp-drawio","ext-drawio-service","drawio MCP"),
  ("mcp-amap","ext-amap-api","地图 MCP"),
  ("mech-proxy","ext-opencode-go","境外访问"),
  ("agent-search-worker","ext-tavily-api","搜索管线依赖 Tavily 外部搜索"),
  ("skill-search-methodology","ext-tavily-api","搜索方法论依赖 Tavily 后端"),
  ("skill-search-methodology","ext-chrome","外部搜索降级链 agent-browser"),
  ("skill-login-auth-channel","ext-chrome","登录态渠道浏览器自动化"),
]
for comp,ext,reason in asm_ext_rules:
    mod_edges.append({"from":ext,"to":comp,"mechanism":"external","evidence":reason,"evidence_example":"","import_refs":0})
# 3. 装配 ↔ 装配 边
# agent-plan/build 委派子Agent
for sub in ["agent-pdf-worker","agent-drawio-worker","agent-general","agent-explore","agent-reflection-worker","agent-vision-worker","agent-search-worker","agent-architect-worker"]:
    mod_edges.append({"from":"agent-plan","to":sub,"mechanism":"delegate","evidence":"plan 委派协议"})
    mod_edges.append({"from":"agent-build","to":sub,"mechanism":"delegate","evidence":"build 委派协议"})
# drawio-worker → drawio-reference skill（强制加载）
mod_edges.append({"from":"skill-drawio-reference","to":"agent-drawio-worker","mechanism":"skill-mandate","evidence":"drawio-reference 强制加载"})
# pdf-worker → pdf-ocr skill
mod_edges.append({"from":"skill-pdf-ocr","to":"agent-pdf-worker","mechanism":"skill-mandate","evidence":"pdf-ocr OCR 支持"})
# search-worker → search-methodology skill（强制加载）
mod_edges.append({"from":"skill-search-methodology","to":"agent-search-worker","mechanism":"skill-mandate","evidence":"search-methodology 强制加载"})
# vision-worker → auto-mode（视觉路由）
mod_edges.append({"from":"instr-auto-mode","to":"agent-vision-worker","mechanism":"hook-mount","evidence":"vision-worker 路由规则"})
# instruction → agent（auto-mode, architecture-behavior, search-behavior 被 agent 使用）
for ag in ["agent-plan","agent-build"]:
    mod_edges.append({"from":"instr-auto-mode","to":ag,"mechanism":"instruction-load","evidence":"auto-mode.md 作为 agent 指令"})
    mod_edges.append({"from":"instr-architecture-behavior","to":ag,"mechanism":"instruction-load","evidence":"architecture-behavior 作为 agent 指令"})
    mod_edges.append({"from":"instr-search-behavior","to":ag,"mechanism":"instruction-load","evidence":"search-behavior 作为 agent 指令"})
    mod_edges.append({"from":"instr-browser-management","to":ag,"mechanism":"instruction-load","evidence":"browser-management 作为 agent 指令"})
    mod_edges.append({"from":"instr-downloads","to":ag,"mechanism":"instruction-load","evidence":"downloads 作为 agent 指令"})
# 行为层路由子Agent
mod_edges.append({"from":"instr-search-behavior","to":"agent-search-worker","mechanism":"route","evidence":"搜索行为路由 search-worker"})
mod_edges.append({"from":"instr-architecture-behavior","to":"agent-architect-worker","mechanism":"route","evidence":"架构行为层路由 architect-worker"})
# command-reflection → reflection-worker
mod_edges.append({"from":"command-reflection","to":"agent-reflection-worker","mechanism":"command-use","evidence":"/reflection 调反射 worker"})
# 4. 机制 → 受影响组件（全边丰富化）
mech_edges=[
 ("mech-grill-me","agent-plan","机制驱动"),("mech-grill-me","agent-build","机制驱动"),("mech-grill-me","skill-grill-me","机制源头"),
 ("mech-agents-protocol","agent-plan","驱动"),("mech-agents-protocol","agent-build","驱动"),("mech-agents-protocol","skill-agency-agents","角色匹配"),
 ("mech-gate","agent-plan","门控"),("mech-gate","agent-build","门控"),
 ("mech-variant","config-main","配置变体"),
 ("mech-reflection-check","agent-reflection-worker","驱动"),("mech-reflection-check","command-reflection","驱动"),("mech-reflection-check","agent-plan","周期末"),
 ("mech-memory-gate","config-main","守护（MEMORY 硬门禁指向 config）"),("mech-memory-gate","command-reflection","审阅"),
 ("mech-cache","instr-auto-mode","共享前缀"),
 ("mech-parallel","agent-explore","并行"),("mech-parallel","agent-general","并行"),
 ("mech-output","skill-headroom","压缩"),
 ("mech-fault","agent-general","容错"),
 ("mech-coding-safety","agent-build","安全编码"),
 ("mech-mission-archive","agent-plan","留档"),("mech-mission-archive","config-main","路径"),
 ("mech-browser-tabs","skill-browser-harness","标签管理"),
 ("mech-proxy","config-main","联网"),("mech-proxy","agent-general","子Agent联网"),
 ("mech-subagent-rules","agent-pdf-worker","子Agent规范"),("mech-subagent-rules","agent-drawio-worker","子Agent规范"),
 ("mech-subagent-rules","agent-search-worker","子Agent规范"),
 ("mech-coding-discipline","agent-build","编码纪律"),("mech-coding-discipline","agent-plan","编码纪律"),
 ("mech-session-memory","config-main","compaction 压缩配置"),("mech-session-memory","instr-auto-mode","压缩模板源"),
 ("mech-grill-me","skill-grill-me","机制源头"),
 ("mech-agents-protocol","skill-agency-agents","角色匹配"),
 ("mech-architecture","skill-architecture-judgment","机制源头"),
 ("mech-architecture","agent-architect-worker","驱动"),
 ("mech-architecture","instr-architecture-behavior","行为层"),
 ("mech-architecture","command-arch","命令入口"),
 ("mech-architecture","config-main","配置"),
 ("mech-architecture","mech-gate","门控"),
]
for comp,target,reason in mech_edges:
    mod_edges.append({"from":comp,"to":target,"mechanism":"mechanism","evidence":reason,"evidence_example":"","import_refs":0})
print("modified 边基础:",len(mod_edges))

# ---- 去重边 ----
seen_e=set(); dedup_mod=[]
for e in mod_edges:
    key=(e["from"],e["to"],e.get("mechanism",""))
    if key in seen_e: continue
    seen_e.add(key); dedup_mod.append(e)
# 悬空边清洗：只保留两端都在节点集的边
mod_nodes_all = official_nodes + asm_nodes + ext_nodes
mod_ids = {n["id"] for n in mod_nodes_all}
clean_edges=[]
for e in dedup_mod:
    if e["from"] in mod_ids and e["to"] in mod_ids: clean_edges.append(e)
print(f"modified 去重后边: {len(dedup_mod)} → 悬空清洗后: {len(clean_edges)}")

layer3=topo_layer(mod_nodes_all, clean_edges)
for n in mod_nodes_all: n["layer"]=layer3.get(n["id"],0)
mod_dag={"name":"modified","title":"改造版 opencode 包级 + 装配层双层 DAG (v1.18.30 + 自进化)","version_note":"官方 36 包（v1.18.30）+ 装配层 83 组件 + 外部服务 10","nodes":mod_nodes_all,"edges":clean_edges,"groups":list(dict.fromkeys(n["group"] for n in mod_nodes_all)),
 "stats":{"nodes":len(mod_nodes_all),"edges":len(clean_edges),"layers":max(layer3.values())+1 if layer3 else 0,"groups":len(set(n["group"] for n in mod_nodes_all)),"has_cycle":has_cycle(mod_nodes_all,clean_edges),
  "pkg_nodes":sum(1 for n in mod_nodes_all if n.get("layer_type")=="package"),"asm_nodes":sum(1 for n in mod_nodes_all if n.get("layer_type")=="assembly"),"ext_nodes":sum(1 for n in mod_nodes_all if n.get("layer_type")=="external"),
  "mech_nodes":sum(1 for n in mod_nodes_all if n.get("kind")=="mechanism")}}
with open(os.path.join(DATA,"modified-dag.json"),"w",encoding="utf-8") as f: json.dump(mod_dag,f,ensure_ascii=False,indent=2)
print(f"modified: {mod_dag['stats']}")

# ---- diff-list（差异清单）----
diff_list=[]
for n in asm_nodes:
    diff_list.append({"node_id":n["id"],"node_name":n["name"],"kind":n["kind"],"group":n["group"],"change":"新增装配" if n.get("enabled",True) else "新增（禁用）","reason":"改造需求（见历史）","enabled":n.get("enabled",True)})
for pid in pkg_used_by_asm:
    diff_list.append({"node_id":pid,"node_name":pid.replace("oc-",""),"kind":"package","group":PKG_GROUP.get(pid,""),"change":"被装配层引用（配置修改）","reason":"官方包被本机配置引用","enabled":True})
with open(os.path.join(DATA,"diff-list.json"),"w",encoding="utf-8") as f: json.dump(diff_list,f,ensure_ascii=False,indent=2)
print(f"diff-list 条目: {len(diff_list)}")
print("\n====== 建模完成 ======")
