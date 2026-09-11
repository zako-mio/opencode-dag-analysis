# -*- coding: utf-8 -*-
"""S6: 质量门控（JSON 合法 / DAG 无环无悬空 / HTML 断链 / 页数覆盖 / DATA 一致 / 七段完整性）"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE="/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag"
DATA=os.path.join(BASE,"01-dag-data")
results=[]
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    mark = "PASS" if cond else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail else ""))

# 1. JSON 合法性
print("=== 1. JSON 合法性 ===")
dags={}
for f in ["official-dag.json","diff-dag.json","modified-dag.json","diff-list.json"]:
    try:
        dags[f]=json.load(open(os.path.join(DATA,f),encoding="utf-8"))
        check(f"JSON 合法: {f}", True)
    except Exception as e:
        check(f"JSON 合法: {f}", False, str(e))
        dags[f]=None

mod=dags["modified-dag.json"]

# 2. DAG 无环 + 无悬空边
print("=== 2. DAG 无环 / 无悬空边 ===")
def count_cycle_edges(nodes, edges):
    ids={n["id"] for n in nodes}
    dangling=[e for e in edges if e["from"] not in ids or e["to"] not in ids]
    in_deg={n["id"]:0 for n in nodes}; adj={n["id"]:[] for n in nodes}
    for e in edges:
        if e["from"] in ids and e["to"] in ids:
            in_deg[e["to"]]+=1; adj[e["from"]].append(e["to"])
    from collections import deque
    q=deque([x for x,d in in_deg.items() if d==0]); visited=0
    while q:
        x=q.popleft(); visited+=1
        for t in adj[x]:
            in_deg[t]-=1
            if in_deg[t]==0: q.append(t)
    return len(dangling), visited!=len(nodes)
for f in ["official-dag.json","diff-dag.json","modified-dag.json"]:
    d=dags[f]
    if d:
        derr, cyc = count_cycle_edges(d["nodes"], d["edges"])
        check(f"DAG 无悬空边: {f}", derr==0, f"{derr} 条悬空")
        check(f"DAG 无环: {f}", not cyc)
        check(f"DAG 无环(stats一致): {f}", d["stats"].get("has_cycle")==cyc, f"stats={d['stats'].get('has_cycle')} 实际={cyc}")

# 3. 节点页覆盖
print("=== 3. 节点页覆盖 ===")
nodes_dir=os.path.join(BASE,"02-nodes")
node_ids={n["id"] for n in mod["nodes"]}
html_files=set(os.listdir(nodes_dir))
missing_pages=[nid for nid in node_ids if nid+".html" not in html_files]
stale=[f for f in html_files if f.endswith(".html") and f[:-5] not in node_ids and f!="index.html"]
check("节点页全覆盖(129)", len(missing_pages)==0, f"缺 {len(missing_pages)}")
check("无陈旧节点页", len(stale)==0, f"陈旧 {len(stale)}")
check("节点索引存在", "index.html" in html_files)

# 4. 组页覆盖
print("=== 4. 组页覆盖 ===")
groups_dir=os.path.join(BASE,"03-groups")
grp_files=set(os.listdir(groups_dir))
group_names=set(n["group"] for n in mod["nodes"])
# 组页文件名是 gid 或完整组名，采宽松匹配
summary={"gid_need":len(group_names),"files":len(grp_files)-1}
check("组页已生成", len(grp_files)>=len(group_names), f"{len(grp_files)} 文件 vs {len(group_names)} 组")

# 5. 交互图 DATA 一致
print("=== 5. 交互图 DATA 一致 ===")
for view in ["view-official.html","view-diff.html","view-modified.html"]:
    vp=os.path.join(BASE,"04-interactive",view)
    if os.path.exists(vp):
        txt=open(vp,encoding="utf-8").read()
        m=re.search(r"const DATA = (\{.*?\});",txt,re.S)
        if m:
            try:
                data=json.loads(m.group(1))
                # 对 view-modified 应匹配 129 节点
                expected = 129 if view=="view-modified.html" else (36 if view=="view-official.html" else 46)
                check(f"交互图 DATA 节点数: {view}", len(data["nodes"])==expected, f"{len(data['nodes'])} vs {expected}")
            except Exception as e:
                check(f"交互图 DATA 解析: {view}", False, str(e))
        else:
            check(f"交互图 DATA 存在: {view}", False, "未找到 const DATA")
    else:
        check(f"交互图文件存在: {view}", False)

# 6. HTML 无替换字符
print("=== 6. HTML 无替换字符 ===")
bad_files=[]
for sub in ["02-nodes","03-groups","04-interactive"]:
    d=os.path.join(BASE,sub)
    for fn in os.listdir(d):
        if fn.endswith(".html"):
            try:
                t=open(os.path.join(d,fn),encoding="utf-8").read()
                if "\ufffd" in t: bad_files.append(f"{sub}/{fn}")
            except: pass
check("无 U+FFFD 替换字符", len(bad_files)==0, f"{len(bad_files)} 文件")

# 7. 断链检查（相对路径）
print("=== 7. HTML 断链检查 ===")
import html.parser
class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            for k,v in attrs:
                if k=="href": self.hrefs.append(v)
broken=[]
import glob
for htmlf in glob.glob(os.path.join(BASE,"**","*.html"),recursive=True):
    rel=os.path.relpath(htmlf,BASE)
    txt=open(htmlf,encoding="utf-8").read()
    p=LinkParser(); p.feed(txt)
    base_dir=os.path.dirname(htmlf)
    for h in p.hrefs:
        if h.startswith("http") or h.startswith("#") or h.startswith("mailto"): continue
        target=os.path.normpath(os.path.join(base_dir,h.split("#")[0]))
        if h.split("#")[0]=="" : continue
        if not os.path.exists(target): broken.append(f"{rel} -> {h}")
check("HTML 断链 0", len(broken)==0, f"{len(broken)} 断链")

# 8. 统计一致性
print("=== 8. 统计一致性 ===")
check("modified stats.nodes", mod["stats"]["nodes"]==len(mod["nodes"]), f"{mod['stats']['nodes']} vs {len(mod['nodes'])}")
check("modified stats.edges", mod["stats"]["edges"]==len(mod["edges"]), f"{mod['stats']['edges']} vs {len(mod['edges'])}")
off=dags["official-dag.json"]; dif=dags["diff-dag.json"]
check("三图节点数(36/46/129)", (len(off["nodes"]),len(dif["nodes"]),len(mod["nodes"]))==(36,46,129),
      f"{len(off['nodes'])}/{len(dif['nodes'])}/{len(mod['nodes'])}")
check("装配节点 83", mod["stats"].get("asm_nodes")==83, str(mod["stats"].get("asm_nodes")))
check("外部节点 10", mod["stats"].get("ext_nodes")==10, str(mod["stats"].get("ext_nodes")))
check("机制节点 18", mod["stats"].get("mech_nodes")==18, str(mod["stats"].get("mech_nodes")))
check("组数 43", mod["stats"].get("groups")==43, str(mod["stats"].get("groups")))

# 9. 七段完整性（抽 key 类型）
print("=== 9. node 关键字段完整性 ===")
missing_field=[]
for n in mod["nodes"]:
    if n["kind"]=="package" and not n.get("why_design"): missing_field.append(f"{n['id']}.why_design")
    if n["kind"] in ("mechanism","skill") and n.get("layer_type")=="assembly":
        if n["id"].startswith("mech-") and not n.get("why_current"): missing_field.append(f"{n['id']}.why_current")
check("包/机制节点 why 字段完整", len(missing_field)==0, f"缺 {len(missing_field)}")

# 汇总
fail=sum(1 for _,c,_ in results if not c)
if fail==0:
    print(f"\n===== 门控结果: {len(results)}/{len(results)} ALL PASS =====")
    sys.exit(0)
else:
    print(f"\n===== {fail} 项 FAIL =====")
    sys.exit(1)
