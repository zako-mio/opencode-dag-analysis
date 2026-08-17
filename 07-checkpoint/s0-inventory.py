# -*- coding: utf-8 -*-
"""
S0: 清单解析 — opencode 官方 35 包 + 装配层全量清单
输出: 07-checkpoint/s0-packages.json / s0-assembly.json / s0-summary.txt
"""
import json, os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"D:\Opencode_Download\Mission-file\2026-08\0807-opencode原理分析\opencode-src"
CONFIG = r"C:\Users\15057\.config\opencode"
REF = r"D:\Opencode_Download\Reflection\skills"

out_dir = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\07-checkpoint"
os.makedirs(out_dir, exist_ok=True)

# ============ 1. 官方 35 包 ============
packages = []
pkg_json_files = sorted(glob.glob(os.path.join(SRC, "packages", "*", "package.json")))
pkg_json_files += sorted(glob.glob(os.path.join(SRC, "packages", "console", "*", "package.json")))
pkg_json_files += sorted(glob.glob(os.path.join(SRC, "packages", "stats", "*", "package.json")))
pkg_json_files += sorted(glob.glob(os.path.join(SRC, "packages", "sdk", "js", "package.json")))
pkg_json_files += sorted(glob.glob(os.path.join(SRC, "packages", "slack", "package.json")))

seen = set()
for pf in pkg_json_files:
    try:
        with open(pf, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERR] {pf}: {e}")
        continue
    name = data.get("name", "")
    if not name or not name.startswith("@opencode-ai/"):
        continue
    if name in seen:
        continue
    seen.add(name)
    deps = data.get("dependencies", {})
    # workspace 依赖（官方内部依赖）
    workspace_deps = [k for k in deps if k.startswith("@opencode-ai/")]
    # 主要外部依赖（数量统计）
    external_deps = [k for k in deps if not k.startswith("@opencode-ai/")]
    src_path = os.path.dirname(pf)
    # src 下 ts 文件数量
    ts_count = 0
    for root, dirs, files in os.walk(os.path.join(src_path, "src")):
        if "node_modules" in root or ".git" in root:
            continue
        for fn in files:
            if fn.endswith(".ts") and not fn.endswith(".test.ts") and not fn.endswith(".d.ts"):
                ts_count += 1
    packages.append({
        "id": name.replace("@opencode-ai/", "oc-"),
        "name": name,
        "short": name.replace("@opencode-ai/", ""),
        "version": data.get("version", "?"),
        "path": os.path.relpath(src_path, SRC).replace("\\", "/"),
        "workspace_deps": workspace_deps,
        "external_deps_count": len(external_deps),
        "src_ts_count": ts_count,
        "is_console_stats": "console" in src_path or "stats" in src_path,
    })

packages.sort(key=lambda p: p["id"])

# ============ 2. 装配层 ============
assembly = {"skills": [], "agents": [], "plugins": [], "tools": [], "commands": [], "mcp": [], "instructions": []}

# 2.1 skills — 三个路径（递归查找 SKILL.md）
skill_paths = [
    (os.path.join(CONFIG, "skill"), "skill"),
    (os.path.join(CONFIG, "skills"), "skills"),
    (REF, "reflection"),
]
skill_seen = set()
for sp, src_name in skill_paths:
    if not os.path.isdir(sp):
        continue
    for root, dirs, files in os.walk(sp):
        # 跳过 node_modules / .git / __pycache__
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__", "vendor")]
        sk_file = None
        for cand in ("SKILL.md", "_SKILL.md", "skill-card.md"):
            if os.path.isfile(os.path.join(root, cand)):
                sk_file = os.path.join(root, cand)
                break
        if sk_file is None:
            continue
        # skill 目录 = SKILL.md 所在目录
        full = root
        # 名称优先取目录名；若目录名是通用名（如 coding/system 中间层），用 SKILL.md 内 name
        item = os.path.basename(full)
        # 读 SKILL.md 头部描述 + name
        desc = ""
        sname = item
        try:
            with open(sk_file, encoding="utf-8") as f:
                content = f.read(4000)
            m = re.search(r"description[:\s]+(.+?)[\r\n]", content[:2000], re.S)
            if m:
                desc = m.group(1).strip()[:200]
            m2 = re.search(r"(?:^|\n)name[:\s]+([A-Za-z0-9_-]+)[\r\n]", content[:500])
            if m2:
                sname = m2.group(1).strip()
        except Exception:
            pass
        if sname in skill_seen:
            continue
        skill_seen.add(sname)
        # 子文件数（排除 node_modules 等）
        sub_files = 0
        for r2, d2, f2 in os.walk(full):
            d2[:] = [d for d in d2 if d not in ("node_modules", ".git", "__pycache__", "vendor")]
            for fn in f2:
                if not fn.endswith((".pyc", ".png", ".jpg", ".jpeg", ".gif")):
                    sub_files += 1
        assembly["skills"].append({
            "id": "skill-" + sname,
            "name": sname,
            "path": full,
            "source": src_name,
            "desc": desc,
            "sub_files": sub_files,
        })

# 2.2 agents — 从 opencode.jsonc 读（含 plan/build 无 mode 字段）
with open(os.path.join(CONFIG, "opencode.jsonc"), encoding="utf-8") as f:
    cfg_text = f.read()
agents = []
# 先抓所有顶层 agent 键
agent_keys = []
depth = 0
for line in cfg_text.splitlines():
    if '"agent"' in line and '{' in line and depth == 0:
        # 进入 agent 段
        pass
# 简化：用正则匹配 agent 段的键（plan/build/pdf-worker/drawio-worker/general/explore/reflection-worker）
for m in re.finditer(r'"agent"\s*:\s*\{', cfg_text):
    pass
# 直接按已知结构抓：agent 段后的键
agent_section = cfg_text.split('"agent"', 1)[1] if '"agent"' in cfg_text else ""
# 找 agent 段结束（下一级 }），用大括号配对
brace = 0
end = 0
started = False
for i, ch in enumerate(agent_section):
    if ch == "{":
        brace += 1
        started = True
    elif ch == "}":
        brace -= 1
        if started and brace == 0:
            end = i
            break
agent_body = agent_section[:end] if end else ""
for m in re.finditer(r'"(\w[\w-]*)":\s*\{', agent_body):
    name = m.group(1)
    if name in ("permission", "prompt", "model", "description", "mode", "variant", "options"):
        continue
    agents.append({"name": name})
# 补充 mode（子Agent 特有）
for a in agents:
    m = re.search(r'"' + re.escape(a["name"]) + r'"\s*:\s*\{[^{}]*?"mode":\s*"(\w+)"', agent_body)
    a["mode"] = m.group(1) if m else "main"
seen_agents = set()
for a in agents:
    if a["name"] in seen_agents or a["name"] in ("bash", "permission"):
        continue
    seen_agents.add(a["name"])
    assembly["agents"].append({"id": "agent-" + a["name"], "name": a["name"], "mode": a["mode"]})

# 2.3 plugins
plug_dir = os.path.join(CONFIG, "plugins")
if os.path.isdir(plug_dir):
    for fn in sorted(os.listdir(plug_dir)):
        if fn.endswith((".js", ".ts")):
            assembly["plugins"].append({"id": "plugin-" + fn.replace(".", "-"), "name": fn, "path": os.path.join(plug_dir, fn)})

# 2.4 tools
tool_dir = os.path.join(CONFIG, "tools")
if os.path.isdir(tool_dir):
    for fn in sorted(os.listdir(tool_dir)):
        if fn.endswith((".ts", ".js")):
            assembly["tools"].append({"id": "tool-" + fn.replace(".", "-"), "name": fn, "path": os.path.join(tool_dir, fn)})

# 2.5 commands
cmd_dir = os.path.join(CONFIG, "command")
if os.path.isdir(cmd_dir):
    for fn in sorted(os.listdir(cmd_dir)):
        if fn.endswith(".md"):
            assembly["commands"].append({"id": "command-" + fn.replace(".", "-"), "name": fn, "path": os.path.join(cmd_dir, fn)})

# 2.6 mcp — 从 config 提取 enabled 状态
mcps = []
for m in re.finditer(r'"(\w[\w-]*)":\s*\{[^{}]*?"enabled":\s*(true|false)', cfg_text):
    mcps.append({"name": m.group(1), "enabled": m.group(2) == "true"})
seen_mcp = set()
for x in mcps:
    if x["name"] in seen_mcp:
        continue
    seen_mcp.add(x["name"])
    assembly["mcp"].append({"id": "mcp-" + x["name"], "name": x["name"], "enabled": x["enabled"]})

# 2.7 instructions
instr = []
for m in re.finditer(r'"([~A-Za-z_\\/.:-]*auto-mode\.md|~[^"]*MEMORY\.md)"', cfg_text):
    instr.append({"path": m.group(1)})
seen_i = set()
for i in instr:
    if i["path"] in seen_i:
        continue
    seen_i.add(i["path"])
    assembly["instructions"].append({"id": "instr-" + os.path.basename(i["path"]).replace(".", "-"), "name": os.path.basename(i["path"]), "path": i["path"]})

# ============ 3. 汇总 ============
summary = {
    "packages_total": len(packages),
    "packages_console_stats": sum(1 for p in packages if p["is_console_stats"]),
    "packages_main": len(packages) - sum(1 for p in packages if p["is_console_stats"]),
    "skills_total": len(assembly["skills"]),
    "skills_by_source": {},
    "agents_total": len(assembly["agents"]),
    "plugins_total": len(assembly["plugins"]),
    "tools_total": len(assembly["tools"]),
    "commands_total": len(assembly["commands"]),
    "mcp_total": len(assembly["mcp"]),
    "mcp_enabled": sum(1 for m in assembly["mcp"] if m["enabled"]),
    "instructions_total": len(assembly["instructions"]),
    "assembly_total": sum(len(v) for v in assembly.values()),
}
for sp in set(s["source"] for s in assembly["skills"]):
    summary["skills_by_source"][sp] = sum(1 for s in assembly["skills"] if s["source"] == sp)

with open(os.path.join(out_dir, "s0-packages.json"), "w", encoding="utf-8") as f:
    json.dump(packages, f, ensure_ascii=False, indent=2)
with open(os.path.join(out_dir, "s0-assembly.json"), "w", encoding="utf-8") as f:
    json.dump(assembly, f, ensure_ascii=False, indent=2)
with open(os.path.join(out_dir, "s0-summary.txt"), "w", encoding="utf-8") as f:
    for k, v in summary.items():
        f.write(f"{k}: {v}\n")
    f.write("\n--- PACKAGES ---\n")
    for p in packages:
        f.write(f"{p['short']} ({p['version']}) deps={p['workspace_deps']} ext={p['external_deps_count']} ts={p['src_ts_count']} path={p['path']}\n")
    f.write("\n--- SKILLS ---\n")
    for s in assembly["skills"]:
        f.write(f"[{s['source']}] {s['name']} (files={s['sub_files']}): {s['desc'][:80]}\n")
    f.write("\n--- AGENTS ---\n")
    for a in assembly["agents"]:
        f.write(f"{a['name']} ({a['mode']})\n")
    f.write("\n--- MCP ---\n")
    for m in assembly["mcp"]:
        f.write(f"{m['name']} enabled={m['enabled']}\n")
    f.write("\n--- PLUGINS/TOOLS/COMMANDS/INSTRUCTIONS ---\n")
    for k in ("plugins", "tools", "commands", "instructions"):
        for x in assembly[k]:
            f.write(f"[{k}] {x['name']}\n")

print(json.dumps(summary, ensure_ascii=False, indent=2))
