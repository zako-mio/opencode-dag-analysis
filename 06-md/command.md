# command 节点（1）

## command-reflection — reflection
- 组: A4-命令指令 | Layer 0
- 作用: /reflection 原生命令（frontmatter：description + agent=build），命令体自包含执行不依赖其他文档。流程：读 pending.json（校验 JSON 合法）→ 按 $ARGUMENTS 子动作过滤（无参/all 展示全部 done；memory/skill 按条目类型过滤；status 仅输出 meta 计数；browse 仅列 id/cycle_type/created_at）→ 用 question 工具逐条 yes/no/edit 确认 → yes 写入 MEMORY.md（§ 分段）或 Reflection\skills\{category}\{name}\SKILL.md（含 frontmatter）→ 清理队列并原子写回（先备份 pending.json.bak-YYYYMMDD，同步更新 meta 计数）。门控：逐条审阅不批量跳过；MEMORY.md 超 3500 字符提示手动整理；UTF-8 写后校验中文完整。
- 提供: Memory/Skill pending 条目的交互式审阅与落地（yes 采纳 / no 拒绝 / edit 修改）、meta 计数同步、备份式原子写回
- **为什么存在（历史）**: 0805 Reflection 系统设计时定为'确认命令'（35 项决策 #20-21：/reflection 统一命令 + 交互式对话逐条确认），但当时仅是提示词级约定（'仿真命令'——agent-protocol.md/opencode.jsonc prompt/MEMORY.md 中有章节，opencode 本身未注册斜杠命令，全局 command/ 目录不存在）；0807 用户指出'opencode 并没有 /reflection 指令，这不符合我的预设'→ 经 Grill-Me 收敛 5 项决策创建原生命令 ~/.config/opencode/command/reflection.md（2700 字节）：命令体自包含（完整审阅步骤不依赖提示词）、agent 固定 build（写权限齐全）、统一触发（$ARGUMENTS 区分子动作 memory|skill|status|browse）。
- **为什么存在（当前）**: 命令体自包含（不依赖其他文档）；frontmatter description + agent: build；三处预设文档同步'已注册为原生命令'（agent-protocol.md / opencode.jsonc plan+build prompt / MEMORY.md）；opencode.jsonc 无 command 键（Markdown 命令不支持 variant 字段，command.variant 仅 JSON 命令支持——0813 确认 B4 不改）。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: agent-build（命令宿主）、reflection-worker（产出 memory_entries/skill_proposals）、agent-reflection skill（架构）、MEMORY.md（写入目标）、pending.json（队列状态机）。
