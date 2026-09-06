# -*- coding: utf-8 -*-
"""合并装配层清单为 s2-all-components.json（55 装配 + 17 机制 + 1 config = 73）"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = "/home/zako-mio/opencode/archive/Mission-file/2026-09/0902-opencode-dag/08-collect"

inv = json.load(open(BASE + "/s2-assembly-inventory.json"))
mech = json.load(open(BASE + "/stage-03-mechanisms.json"))
new_asm = json.load(open(BASE + "/stage-03-new-assembly.json"))

components = []
# 1. 装配组件（来自 inventory）
for c in inv:
    components.append(dict(c))

# 2. 机制节点（17 个，从 mechanisms.json 提取 name）
MECH_META = {
    "mech-grill-me": ("Grill-Me 协议", "opencode.jsonc plan/build prompt", "Plan 阶段逐分支追问收敛方案，问一答一（question 工具），含 Drift 护栏与收敛审计"),
    "mech-agents-protocol": ("Agent 委派协议", "opencode.jsonc plan/build prompt", "主Agent 任务调度者→拆解→search-agents 匹配→委派子Agent→聚合；含 MCP 路由规则"),
    "mech-gate": ("GATE 强制门控", "instructions/auto-mode.md", "MANDATORY GATE CHECK：范围/深度/操作/风险四维自评(1-5)输出总分→Daily/Deep"),
    "mech-variant": ("Variant 运行时控制", "auto-mode.md + opencode.jsonc", "Plan 阶段输出[COMPLEXITY]/Build 继承推理深度；Ctrl+T 运行时切换 daily/deep"),
    "mech-reflection-check": ("Reflection 自检系统", "auto-mode.md", "查 pending.json waiting_count→标 processing→委派 reflection-worker→/reflection 逐条确认"),
    "mech-memory-gate": ("MEMORY.md 硬门禁", "auto-mode.md", "MEMORY.md 严禁直接修改，走 pending→reflection-worker→/reflection 确认→带[src:]写入"),
    "mech-cache": ("缓存感知 (Cache Awareness)", "instructions/auto-mode.md", "DeepSeek prefix-cache：前缀字节级稳定，动态内容放末尾，协议不中途修改"),
    "mech-parallel": ("Parallel & Batching", "instructions/auto-mode.md", "独立工具调用并行发出；相邻只读操作合并批次；读优先于写"),
    "mech-output": ("Output Discipline", "instructions/auto-mode.md", "分段读取/压缩大输出/只读优先，控制 token 规模"),
    "mech-fault": ("故障自愈协议", "instructions/auto-mode.md", "工具失败重试3次→换方案→记录；MCP 断开降级内置工具；JSON 解析失败正则提取"),
    "mech-coding-safety": ("编码安全规则", "opencode.jsonc prompt", "优先 edit(UTF-8安全)；禁用 python -c 内联管道；独立.py 文件；修改中文JSON后验证"),
    "mech-mission-archive": ("Mission 留档规则", "opencode.jsonc prompt", "任务完成 5 段报告模板 + 询问用户留档 + 路径门控正则校验"),
    "mech-browser-tabs": ("浏览器标签页管理", "opencode.jsonc prompt", "new_tab 后关闭标签页；任务完成询问是否关闭；批量爬取不逐页关闭"),
    "mech-proxy": ("联网代理纪律 (WSL2)", "instructions/auto-mode.md", "默认直连；境外被墙站点 proxy_on 或 curl -x 172.29.0.1:7890；模型API勿设代理"),
    "mech-subagent-rules": ("Universal SubAgent Rules", "instructions/auto-mode.md", "子Agent 身份约束/工具使用/错误处理/通信规范(JSON)+结构化返回"),
    "mech-coding-discipline": ("Universal Coding Discipline", "instructions/auto-mode.md", "验证与证据/从磁盘读不依赖对话记忆/路径本地化/元数据不入输出"),
    "mech-session-memory": ("Session Memory 结构化压缩", "instructions/auto-mode.md", "compaction 5 段模板(当前状态/关键文件/已做决策/待解决问题/经验教训)+L1剪枝/L2压缩/L3兜底"),
}
for mid, m in mech.items():
    name, source, desc = MECH_META.get(mid, (m.get("name", mid), "auto-mode.md", ""))
    components.append({
        "id": mid, "name": name, "kind": "mechanism",
        "group": "AQ-self-evolution", "desc": desc or m.get("why_current", ""),
        "model": "", "mode": "", "enabled": True, "source": source,
    })

# 3. config 节点（1 个）
components.append({
    "id": "config-main", "name": "opencode.jsonc", "kind": "config",
    "group": "AG-config", "desc": "主配置：agent/provider/mcp/compaction/skills/instructions/permission",
    "model": "", "mode": "", "enabled": True, "source": "~/.config/opencode/opencode.jsonc",
})

with open(BASE + "/s2-all-components.json", "w", encoding="utf-8") as f:
    json.dump({"components": components}, f, ensure_ascii=False, indent=2)

from collections import Counter
print("装配层组件总数:", len(components))
print("按 kind:", dict(Counter(c["kind"] for c in components)))
# 校验新增组件 id 对齐
for cid in new_asm:
    found = any(c["id"] == cid for c in components)
    print(f"  {'✓' if found else '✗'} {cid} (new_asm 匹配)")
