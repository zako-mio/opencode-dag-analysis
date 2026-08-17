# instruction 节点（2）

## instr-auto-mode — auto-mode
- 组: A4-命令指令 | Layer 5
- 作用: 全局共享前缀协议（Cache-Stable，所有 Agent 加载，session 内字节稳定以维持 DeepSeek prefix-cache）。核心内容：①强制 GATE 门控（范围/深度/操作/风险 4 维 1-5 分自评→总分→Daily≤12/Deep≥13，主Agent 强制输出）；②Variant 运行时控制（Ctrl+T 切换、DeepSeek 思考模式有效参数表、被忽略参数说明）；③Universal SubAgent Rules（结构化 JSON 返回、身份约束、工具/错误处理/通信规范）；④通用编码纪律（验证证据、从磁盘读取、路径本地化、元数据不入输出）；⑤缓存感知原则（静态前缀/动态末尾）；⑥并行批处理规范；⑦输出规模控制；⑧故障自愈协议（3 次重试上限）；⑨Session Memory 阶梯式压缩模板（L1 剪枝→L2 结构化→L3 摘要）。
- 提供: 全 Agent 统一行为协议（门控/委派/编码/缓存/容错/压缩）、成本控制基准（Daily 8192/Deep 16384 tokens）
- **为什么存在（历史）**: 0801 P0 输入缓存优化核心产物：扩充 auto-mode.md（620→2000+ chars，共享前缀 3x 增长）；实测确认 auto-mode.md 是 DeepSeek prefix-cache 共享前缀（两不同 role 子Agent 请求命中率 53.3%）→ 确立'静态协议前缀，字节稳定性承诺'；0803 改进落地：Return Format 升级 8 字段（去 next_step）+ 通信规范 6 条 + Session Memory 结构化压缩模板（Claude Code 对比 P0 差距，5 阶压缩→3 层阶梯 L1 剪枝/L2 结构化/L3 兜底）；0803 Drawio 缓存修正：per-agent 行为约束禁止经 agent.prompt 注入（位置 0 破坏前缀）→ 统一写入对应 skill 经 Skills to Load 传递；0813 skill 更新：移除 6 处 headroom MCP 引用（改为通用截断做法，因 headroom 已禁用）。
- **为什么存在（当前）**: 所有 Agent（主+子）的共享前缀协议（cache-stable，不可修改前缀字节否则缓存全毁）；GATE 强制门控（4 维度自评 1-5 分 → 总分 Daily≤12/Deep≥13 → variant 决策边界）；Universal SubAgent Rules（身份约束/工具使用/错误处理/结构化 JSON 通信）；Cache Awareness（静态前缀+动态末尾，缓存命中降本 98-99%）；Parallel & Batching（并行发出/合并批次/MCP 发现缓存）；Output Discipline（分段读取/压缩大输出/只读优先）；Fault Tolerance（3 级自愈）；Session Memory 压缩模板（5 段）。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: config-main（instructions 引用）、instr-memory（动态内容置后）、agent-plan/build prompt（互补：prompt 内嵌委派细节，auto-mode 管通用协议）、skill 体系（per-agent 约束经 skill 传递）。

## instr-memory — memory
- 组: A4-命令指令 | Layer 5
- 作用: 项目记忆索引（§-分段格式，上限 ~3500 字符），作为第二份 instructions 加载。记录的改造决策/经验：Reflection 系统与 /reflection 命令、模型分配（plan=Pro 回落顶层 / build=Flash / 子Agent 全 Flash）、MCP 精兵策略（6 台启用 2 台 pdf-reader/drawio，headroom 2026-08-12 量化亏损禁用）、三层权限纵深防御、compaction 参数、prefix-cache 优化（静态前缀 auto-mode.md / 动态末尾 MEMORY.md）、编码安全（edit 优先 / 禁 python -c 管道 / replaceAll 零残留检查）、多路并行领域分片检索、HTML 双交付质量门控、多维权衡矩阵选型、子Agent 口径冲突裁决、排障两原则、双轨交付一致性三原则、经验跨项目迁移方法论。
- 提供: 跨会话记忆持久化、历史决策回溯、经验教训复用、config 修改安全链（备份→改→验证→哈希→零残留）
- **为什么存在（历史）**: 0803 改进落地 P1（Claude Code 对比报告识别记忆系统差距）：当前会话结束后上下文丢失，无持久化记忆机制 → 创建 MEMORY.md（4 类分类 × 15 条预填充：中文偏好/安全规则/配置路径等）；Grill-Me 决策：路径 ~/.config/opencode/MEMORY.md（全局共享）、去掉子Agent next_step 字段、instructions 顺序 auto-mode.md 在前（保缓存）MEMORY.md 在后（动态内容）；0805 Reflection 系统：格式迁移 §-分段 Hermes 格式（保留 4 段分类作标签）+ 自引用规则（waiting_count 检查）+ /reflection 命令定义 + 容量上限 3500 提醒；0813 skill 更新：同步修正精兵策略口径（7→6 台 MCP、headroom MCP 禁用但 CLI 保留、压缩阶梯修正）。
- **为什么存在（当前）**: 全局共享版（~/.config/opencode/，workspace 根可建项目版共存）；放在 auto-mode.md 之后（动态内容不破坏静态前缀缓存断点）；§-分段格式上限 ~3500 字符（超限提示手动整理）；每次收到用户消息先查 meta.waiting_count>0 → 有 waiting 则标 processing 委派 reflection-worker（无论成败继续正常流程）。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: command-reflection（审阅写入）、agent-reflection/reflection-worker（产出条目）、config-main（instructions 引用）、instr-auto-mode（缓存序位）。
