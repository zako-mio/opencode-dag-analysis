# -*- coding: utf-8 -*-
"""
S2b: 合并装配层语义 → 完整装配语义 + 关联历史事件
输出: 07-checkpoint/s2-assembly-semantics.json
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

out_dir = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\07-checkpoint"

# 读 s0 装配清单（数量基准）
with open(os.path.join(out_dir, "s0-assembly.json"), encoding="utf-8") as f:
    s0 = json.load(f)

# 读 4 个 stage-02 文件
files = {
    "core": "stage-02-core-assembly.json",
    "skills-a": "stage-02-skills-a.json",
    "skills-b": "stage-02-skills-b.json",
    "history": "stage-02-history.json",
}
all_comp = {}
history = []
for key, fn in files.items():
    fp = os.path.join(out_dir, fn)
    with open(fp, encoding="utf-8-sig") as f:
        data = json.load(f)
    if key == "history":
        # 兼容 {meta, events} 或纯数组
        history = data.get("events", data) if isinstance(data, dict) else data
        continue
    for c in data:
        cid = c.get("id", "")
        if not cid:
            continue
        if cid in all_comp:
            print(f"[WARN] dup id: {cid} — keep first")
            continue
        all_comp[cid] = c

# 关联历史：按 related_assembly 或 area 匹配
for cid, c in all_comp.items():
    c["history"] = []
    for ev in history:
        if not isinstance(ev, dict):
            continue
        related = ev.get("related_assembly", "")
        area = ev.get("area", "")
        if cid in related or (isinstance(related, list) and any(cid in r for r in related)):
            c["history"].append({"date": ev.get("date"), "change": ev.get("change", "")[:80]})

# 统计装配节点分类
kinds = {}
for c in all_comp.values():
    k = c.get("kind", c.get("source", "unknown"))
    kinds[k] = kinds.get(k, 0) + 1

with open(os.path.join(out_dir, "s2-assembly-semantics.json"), "w", encoding="utf-8") as f:
    json.dump({"components": all_comp, "history": history}, f, ensure_ascii=False, indent=2)

print(f"assembly components total: {len(all_comp)}")
print(f"kinds: {json.dumps(kinds, ensure_ascii=False)}")
print(f"history events: {len(history)}")
# 打印缺失对照：s0 说 43 skills，这里有多少 skill-*
s_comp = [cid for cid in all_comp if cid.startswith("skill-")]
print(f"skill components: {len(s_comp)}")
s0_skills = s0.get("skills", [])
print(f"s0 skills_total: {len(s0_skills)}")
missing = set(s["name"] for s in s0_skills) - set(cid.replace("skill-", "") for cid in s_comp)
print(f"missing skills from s0: {sorted(missing)}")
