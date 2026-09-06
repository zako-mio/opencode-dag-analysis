# -*- coding: utf-8 -*-
"""S2: 装配层组件清单（id/name/kind/group/enabled/basic desc）——机械提取"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")

CFG = "/home/zako-mio/.config/opencode/opencode.jsonc"
OUT = "/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag/08-collect"
text = open(CFG, encoding="utf-8").read()
text_nc = re.sub(r'//[^\n]*', '', text)

def extract_block(txt, key):
    m = re.search(r'"'+key+r'"\s*:\s*\{', txt)
    if not m: return ""
    start = m.end()-1
    depth=0; end=None
    for i in range(start, len(txt)):
        if txt[i]=='{': depth+=1
        elif txt[i]=='}':
            depth-=1
            if depth==0: end=i; break
    return txt[start:end] if end else ""

components = []

# ---- 1. agents ----
agent_block = extract_block(text_nc, "agent")
if agent_block:
    # 顶层 agent 键
    for mm in re.finditer(r'\n([ \t]{4})"([a-z0-9-]+)"\s*:\s*\{', agent_block):
        akey = mm.group(2)
        # 取该 agent 子块
        sub = extract_block(agent_block, akey)
        if not sub: continue
        desc = re.search(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"', sub)
        model = re.search(r'"model"\s*:\s*"([^"]+)"', sub)
        mode = re.search(r'"mode"\s*:\s*"([^"]+)"', sub)
        components.append({
            "id": "agent-"+akey, "name": akey, "kind": "agent",
            "group": "AG-agents",
            "desc": (desc.group(1) if desc else "")[:200],
            "model": model.group(1) if model else "",
            "mode": mode.group(1) if mode else "",
            "enabled": True,
            "source": "opencode.jsonc agent段",
        })

# ---- 2. mcp ----
mcp_block = extract_block(text_nc, "mcp")
if mcp_block:
    for name in ['vscode-mcp-server','amap','pdf-reader','drawio','drawio-local','headroom']:
        sub = extract_block(mcp_block, name)
        if not sub: continue
        en = re.search(r'"enabled"\s*:\s*(\w+)', sub)
        desc = re.search(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"', sub)
        components.append({
            "id": "mcp-"+name, "name": name, "kind": "mcp",
            "group": "AG-mcp",
            "desc": (desc.group(1) if desc else "")[:200],
            "model": "", "mode": "local",
            "enabled": (en.group(1)=="true") if en else True,
            "source": "opencode.jsonc mcp段",
        })

# ---- 3. instructions（读目录真实文件）----
INSTR_DIR = "/home/zako-mio/.config/opencode/instructions"
for fn in sorted(os.listdir(INSTR_DIR)):
    if fn.endswith(".bak") or ".bak-" in fn: continue
    comp = {
        "id": "instr-"+fn.replace(".md",""), "name": fn.replace(".md",""),
        "kind": "instruction", "group": "AG-instructions",
        "desc": "", "model": "", "mode": "", "enabled": True,
        "source": "instructions/"+fn,
    }
    fp = os.path.join(INSTR_DIR, fn)
    try:
        head = open(fp, encoding="utf-8").read(400)
        comp["desc"] = head.lstrip("# \n").split("\n")[0][:150]
    except Exception: pass
    components.append(comp)

# ---- 4. tools ----
for fn in os.listdir("/home/zako-mio/.config/opencode/tools"):
    if fn.endswith(".bak"): continue
    components.append({
        "id": "tool-"+fn.replace(".ts","").replace(".js",""),
        "name": fn, "kind": "tool", "group": "AG-tools",
        "desc": "自定义工具 "+fn, "model":"", "mode":"", "enabled": True,
        "source": "tools/"+fn,
    })

# ---- 5. command ----
for fn in os.listdir("/home/zako-mio/.config/opencode/command"):
    if fn.endswith(".bak"): continue
    components.append({
        "id": "command-"+fn.replace(".md",""), "name": fn.replace(".md",""),
        "kind": "command", "group": "AG-commands",
        "desc": "自定义命令 "+fn, "model":"", "mode":"", "enabled": True,
        "source": "command/"+fn,
    })

# ---- 6. skills ----
for pfx in ["skill", "skills"]:
    d = os.path.expanduser("~/.config/opencode/"+pfx)
    if not os.path.isdir(d): continue
    for dn in sorted(os.listdir(d)):
        dp = os.path.join(d, dn)
        if not os.path.isfile(os.path.join(dp, "SKILL.md")): continue
        desc = ""
        try:
            head = open(os.path.join(dp,"SKILL.md"), encoding="utf-8").read(600)
            dm = re.search(r'description:\s*(.+)', head)
            if dm: desc = dm.group(1).strip()[:180]
        except Exception: pass
        components.append({
            "id": "skill-"+dn, "name": dn, "kind": "skill",
            "group": "AG-skills",
            "desc": desc, "model":"", "mode":"", "enabled": True,
            "source": pfx+"/"+dn,
        })

with open(os.path.join(OUT, "s2-assembly-inventory.json"), "w", encoding="utf-8") as f:
    json.dump(components, f, ensure_ascii=False, indent=2)
print(f"装配层组件总数: {len(components)}")
from collections import Counter
print("按 kind:", dict(Counter(c["kind"] for c in components)))
print("按 enabled:", dict(Counter(str(c["enabled"]) for c in components)))
