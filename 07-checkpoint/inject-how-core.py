# -*- coding: utf-8 -*-
"""
S4f: 合并 stage-04 how/why 数据到 modified-dag
数据源: stage-04-how-core.json / stage-04-how-ui.json / stage-04-how-console-ext.json
输出: 更新 modified-dag.json（官方包补 how_use/how_scenario/why_modified，外部服务补 why_need/how_integrate/how_usage）
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag"
DATA = os.path.join(BASE, "01-dag-data")
CKPT = os.path.join(BASE, "07-checkpoint")

def load(fp, sig=False):
    with open(fp, encoding="utf-8-sig" if sig else "utf-8") as f:
        return json.load(f)

# 读 3 个 stage-04
how_data = {}
for fn in ("stage-04-how-core.json", "stage-04-how-ui.json", "stage-04-how-console-ext.json"):
    items = load(os.path.join(CKPT, fn), sig=True)
    for item in items:
        iid = item.get("id", "")
        if iid:
            how_data[iid] = item
print(f"stage-04 items: {len(how_data)}")

# stage-04 外部服务 id → modified-dag ext id 映射
EXT_ID_MAP = {
    "ext-deepseek": "ext-deepseek-api",
    "ext-glm": "ext-glm-api",
    "ext-lark-feishu": "ext-lark-api",
    "ext-amap": "ext-amap-api",
    "ext-chrome-cdp": "ext-chrome",
    "ext-drawio": "ext-drawio-service",
    "ext-pdf-reader": "ext-sylphx-pdf",
    "ext-headroom": "ext-headroom-service",  # 可能不存在，检查
}

# 读 modified-dag
with open(os.path.join(DATA, "modified-dag.json"), encoding="utf-8") as f:
    dag = json.load(f)

# 注入
injected = 0
for n in dag["nodes"]:
    nid = n["id"]
    # 查找数据（官方包直接用 id；外部服务用映射）
    h = how_data.get(nid)
    if h is None and n.get("layer_type") == "external":
        # 反向映射：找到 stage-04 id → 本图 id
        for s_id, d_id in EXT_ID_MAP.items():
            if d_id == nid and s_id in how_data:
                h = how_data[s_id]
                break
    if h is None:
        continue
    # 官方包字段
    if n.get("layer_type") == "package":
        n["how_use"] = h.get("how_use", "")
        n["how_scenario"] = h.get("how_scenario", "")
        n["why_design"] = h.get("why_design", n.get("why", ""))
        n["why_modified"] = h.get("why_modified", "")
    # 外部服务字段
    if n.get("layer_type") == "external":
        n["why_need"] = h.get("why_need", "")
        n["why_current"] = h.get("why_current", "")
        n["how_integrate"] = h.get("how_integrate", "")
        n["how_usage"] = h.get("how_usage", "")
    injected += 1
print(f"injected into {injected} nodes")

with open(os.path.join(DATA, "modified-dag.json"), "w", encoding="utf-8") as f:
    json.dump(dag, f, ensure_ascii=False, indent=2)
print("modified-dag.json updated")
