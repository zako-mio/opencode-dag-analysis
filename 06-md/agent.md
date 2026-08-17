# agent 节点（7）

## agent-build — build
- 组: A1-Agents | Layer 6
- 作用: 执行者主 Agent，variant=daily，model=deepseek-v4-flash（注释：执行逻辑足够，省成本）。prompt 与 plan 完全一致（replaceAll 同步维护，存在未来不一致风险已记录于 MEMORY），实际按执行者身份运行为主。同时承载 /reflection 原生命令（frontmatter agent=build）。
- 提供: 执行 plan 收敛出的任务、编码安全规则执行（edit 优先/UTF-8 安全）、/reflection 交互式审阅命令宿主、Build 末尾 pending.json 4 层封装写入
- **为什么存在（历史）**: 0801 P0：build prompt 从 1297 chars 精简到 50 chars（消除重复），后因协议合并又扩回为与 plan 完全一致；0802 盘点：plan/build prompt 内容完全相同但独立 JSON 字符串维护（replaceAll 同步，存在未来不一致风险已记录 MEMORY）；0803 改进落地：Return Format 双处同步（files_created 等）；0806 plan/build 双双降级 Flash（model=deepseek-v4-flash，调度逻辑足够）；0807 /reflection 原生命令 frontmatter 固定 agent=build（写权限齐全）；0813 保持 Flash（执行者用 Flash 降本，规划者 Pro 保质量）。
- **为什么存在（当前）**: 执行者用 Flash 降本（注释：执行者，调度逻辑足够）；承载 /reflection 原生命令宿主（frontmatter agent=build，因 build 写权限齐全）；prompt 与 plan 完全一致（replaceAll 同步维护，风险已记录）；variant=daily。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: plan（接收收敛结果与 [COMPLEXITY] 标记）、reflection-worker（处理 pending cycle）、command-reflection（命令宿主）、7 子Agent（执行委派）。

## agent-drawio-worker — drawio-worker
- 组: A1-Agents | Layer 2
- 作用: 图表专家子Agent（mode=subagent, hidden=true），model=deepseek-v4-flash（图表生成无需 Pro 推理）。permission 仅放行 drawio_* 工具。主Agent 委派时必须精确写入 drawio-reference skill（刚性约束，禁止弱化表述），防止子Agent 使用不可靠 CLI 导出产生截断 PNG。
- 提供: draw.io 图表创建与导出验证（流程图/架构图/UML/思维导图/组织图）
- **为什么存在（历史）**: 0801 P0 新增：drawio-worker 配置 Flash 模型；0803 Drawio工具链优化关键转折：曾给 drawio-worker 新增 agent.prompt 字段（强制导出+防越界+VLM 校验规则），但源码级逆向确认 agent.prompt 位于系统提示词位置 0，新增后缓存前缀从 2 变 3，drawio-worker 无法复用其他子Agent 缓存——用户判定'这个代价不值得'→ 回退 prompt 字段；per-agent 行为约束改为经 drawio-reference skill + 主Agent 的 Skills to Load 传递；MCP 路由规则从'必要时加载'改为'必须包含 drawio-reference'（禁止弱化表述）。
- **为什么存在（当前）**: 固定 Flash（图表生成无需 Pro 推理）；permission 仅放行 drawio_*（L3 最小权限）；刻意不设 agent.prompt 字段避免缓存前缀碎片化；委派刚性约束：prompt 必须精确写入'drawio-reference: 图表规范与导出验证'，违者导致不可靠 CLI 导出产生截断 PNG。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: mcp-drawio（工具源）、drawio-reference skill（998 行参考文档+导出验证规范）、plan/build（委派+刚性约束）、VLM 校验（图表内容验证）。

## agent-explore — explore
- 组: A1-Agents | Layer 1
- 作用: 探索子Agent，model=deepseek-v4-flash，无 description/无专用 permission。用于代码库/知识库快速探索（glob/grep/read），并行产出数据；口径冲突时由主Agent 终裁（MEMORY 记录：包数 237/219 由主Agent 定夺，不重跑）。
- 提供: 快速只读探索、并行调研产出、统一 schema 归一化
- **为什么存在（历史）**: 0801 P0 新增：general/explore Agent（Flash），探索/搜索子Agent 路由；0802 盘点：无 MCP 的探索/搜索子Agent；0803 起大量并行探索委派（0803 对比报告 3 个 explore 并行、0808 MCP 四件套 4 个并行、0817 DAG 3 路并行）；0814 口径冲突裁决（MEMORY：并行 explore 产出包数 237/219 不一致时由主Agent 终裁不重跑）。
- **为什么存在（当前）**: Flash 模型；无 description/无专用 permission（纯只读定位：glob/grep/read）；是并行调研的主力，支撑大规模源码解析方法论（主Agent 只调度/聚合/裁决，explore 并行解析，三源交叉验证）。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: plan/build（委派）、large-scale-source-parse skill（方法论）、general（互补）。

## agent-general — general
- 组: A1-Agents | Layer 0
- 作用: 通用子Agent，model=deepseek-v4-flash，无 description/无专用 permission（继承全局 deny + external_directory 白名单）。无 MCP 工具，省 token。用于通用执行任务，包括 MEMORY 记录的多路并行领域分片联网检索（编码/通用/工具链 3 路并行，代理 127.0.0.1:7890）。
- 提供: 通用执行能力（无专用工具）、领域分片并行检索、异构数据归一化产出
- **为什么存在（历史）**: 0801 P0 新增：general/explore Agent 配置 Flash（L44-49），'通用/探索子Agent 路由'；0802 盘点：无 MCP 工具，省 token（'其他任务 → 委派 general/explore 子Agent（无MCP工具，省token）'）；0803 起成为通用执行主力；0813 记录多路并行领域分片检索模式（3 路并行 general 子Agent 按领域分片联网检索，聚合成本低覆盖全）。
- **为什么存在（当前）**: Flash 模型；无 description/无专用 permission（继承全局 deny + external_directory 白名单）；无 MCP 工具省 token——是 MCP 精兵策略下'通用任务不给专用工具'的直接体现。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: plan/build（委派）、explore（互补：explore 纯探索、general 通用执行）、browser-harness skill（联网）。

## agent-pdf-worker — pdf-worker
- 组: A1-Agents | Layer 0
- 作用: PDF 专家子Agent（mode=subagent, hidden=true），model=deepseek-v4-flash（PDF 提取无需 Pro 推理）。permission 仅放行 pdf-reader_* 工具（L3 最小权限注入），与全局 deny 构成三层纵深。主Agent 的 MCP 路由规则将 PDF/OCR/文档分析任务固定委派给它。
- 提供: PDF 文本提取、OCR、文档分析（经 pdf-reader MCP 的 4 工具）
- **为什么存在（历史）**: 0801 P0 新增：pdf-worker 配置 Flash 模型（L27），子Agent 路由到 Flash；0802 盘点：4 个自定义 subagent 之一，permission 仅放行 pdf-reader_* 工具；MCP 路由规则确立：PDF 读取/OCR/文档分析 → 委派 pdf-worker（必要时加载 pdf-ocr skill）；0813 skill 更新：修正 replaceAll 误加的'0806 临时降级'注释（子Agent 固定 Flash）。
- **为什么存在（当前）**: 固定 Flash（PDF 提取无需 Pro 推理）；mode=subagent + hidden=true；L3 最小权限注入（仅 pdf-reader_* allow），与全局 deny 构成三层纵深防御；描述明确'Use for any task involving PDF files'。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: mcp-pdf-reader（唯一工具源）、pdf-ocr skill（OCR 兜底）、plan/build（MCP 路由规则委派）。

## agent-plan — plan
- 组: A1-Agents | Layer 6
- 作用: 主 Agent（调度者角色，非执行者），variant=daily，无显式 model 字段 → 回落顶层 model deepseek-v4-pro（注释明确：只动顶层一处省维护）。prompt 由两部分组成：Grill-Me 协议（用 question 工具逐条追问收敛设计树，含 drift guardrails 防协议漂移）与 Agent 调度协议（分类判断→search-agents.ps1 搜索角色→拆解子任务→并行/接力委派→聚合精简 JSON）。permission 对 bash 全 deny，仅放行 git status/git diff/Get-ChildItem 只读命令（L2 层收紧执行面）。
- 提供: 需求澄清与设计树收敛（Grill-Me）、任务拆解与子Agent 委派、MCP 路由决策（PDF→pdf-worker / 图表→drawio-worker / 其他→general/explore）、Mission 留档 5 段报告触发、Build 末尾 Reflection 4 层写入、Variant 继承 [COMPLEXITY] 标记
- **为什么存在（历史）**: 0801 P0 输入缓存优化引入：grill-me 协议固化到 plan prompt 开头（+500 tokens，缓存命中后免费）；0802 Mission留档系统：注入 Mission留档规则（5段报告+三重门控）；0803 改进落地：Return Format 升级为 8 字段 + MEMORY.md 同步询问；0803 Drawio 缓存修正：确认 agent.prompt 位于系统提示词位置 0，仅用于结构性协议替换；0805 Reflection 系统：新增 Build 末尾 pending.json 4 层封装写入 + Reflection 自检规则；0806 plan/build 双双降级 Flash（临时）；0807 /reflection 原生命令 prompt 同步；0813 plan 回滚 Pro（删除 plan.model 字段回落顶层 model，只动顶层一处省维护）。permission 对 bash 全 deny，仅放行 git status/git diff/Get-ChildItem 只读命令（L2 收紧执行面）。
- **为什么存在（当前）**: 调度者角色固定：plan=Pro（0813 回滚，规划/委派调度需 Pro 推理质量）、build=Flash（执行者降本）——分工清晰的模型策略；删 model 字段回落顶层实现单点维护；prompt 同时承载 Grill-Me + Agent 调度协议 + 编码安全 + 留档 + Variant 继承 + Reflection 规则，是全配置最大的定制项。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: build（执行收敛结果）、7 子Agent（委派）、agency-agents skill（search-agents.ps1 角色搜索）、reflection-worker（异步反思）、command-reflection（/reflection）。

## agent-reflection-worker — reflection-worker
- 组: A1-Agents | Layer 0
- 作用: 自我进化系统反思子Agent（mode=subagent, hidden=true），model=deepseek-v4-flash（反思分析无需 Pro 推理）。permission bash 全 deny（仅文件读写，L3 收紧）。处理 Plan+Build 周期后的异步反思：读取 pending.json 中 status=processing 的 cycle（含 4 层输入数据）→ 生成 memory_entries/skill_proposals。
- 提供: 异步反思分析、Memory/Skill 条目生成、pending.json 状态流转（waiting→processing）
- **为什么存在（历史）**: 0805 Reflection 系统新增：基于 Hermes Agent 自进化架构 + 35 项 Plan 决策收敛（核心动机：持续自我改进 > 减少重复错误 > 提升 Plan 质量）；opencode.jsonc 新增 reflection-worker（hidden subagent, Flash 模型, bash 全 deny）+ skills.paths 加 Reflection/skills + external_directory 加 D:\Opencode_Download\Reflection\**；设计为'Skill (agent-reflection) + 子Agent (reflection-worker) 组合'，Fork 工具仅文件读写最小集。
- **为什么存在（当前）**: 固定 Flash（反思分析无需 Pro 推理）；bash 全 deny（仅文件读写，L3 收紧，工具白名单设计偏保守）；hidden subagent；描述明确'Use ONLY for asynchronous post-cycle reflection tasks'。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: plan/build（4 层输入来源）、agent-reflection skill（方法论）、command-reflection（/reflection 交互确认写入）、pending.json 状态机。
