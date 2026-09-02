# mechanism 节点（16）

## mech-agents-protocol — agents-protocol
- 组: AQ-自进化机制 | Layer 0
- 作用: 主 Agent 任务调度者→拆解→搜索角色→委派子 Agent→聚合；含 MCP 路由规则。
- 提供: 
- **为什么存在（历史）**: 源于 0801/0802 的 agent-prompt-unification 统一各 Agent 角色，确立「主Agent=调度者、子Agent=执行者」边界。0817 已存在。动机：解决主Agent 亲力亲为导致上下文爆炸、执行面过大。
- **为什么存在（当前）**: 将需≥2工具/联网/多步的任务分解后委派子Agent，仅保留编排+聚合；通过 search-agents 匹配角色、MCP 路由（pdf/drawio/vision）精准指派。
- **怎么用（触发）**: 判断任务是否需多工具/联网/多步推理；是则触发。
- **怎么用（工作流）**: 5 步：分类判断→search-agents 搜角色→拆解任务→组装子Agent prompt→聚合。
- **怎么用（协作）**: agent-plan、agent-build；skill-agency-agents；search-agents(.ps1/.py)；agent-pdf-worker/agent-drawio-worker/agent-vision-worker/agent-general/agent-explore。

## mech-browser-tabs — browser-tabs
- 组: AQ-自进化机制 | Layer 0
- 作用: new_tab 后关闭标签页；任务完成询问是否关闭；批量爬取不逐页关闭。
- 提供: 
- **为什么存在（历史）**: 0817 s2 完全缺失。属 0817 后新增，随 WSL2 浏览器自动化落地。动机：browser-harness 多次爬取会堆积大量标签页。
- **为什么存在（当前）**: 控制 browser-harness 会话的标签页生命周期：单次 new_tab 后即关；任务全完必须询问是否关页；批量中途不逐页关。
- **怎么用（触发）**: 使用 browser-harness 进行爬取/自动化任务时。
- **怎么用（工作流）**: 每次 new_tab() 完成后用 close-chrome-tabs.ps1 -KeepFirst 关闭；全部完成后 question 询问；批量中途不逐页关闭。
- **怎么用（协作）**: agent-plan、agent-build；skill-browser-harness；powershell close-chrome-tabs.ps1。

## mech-cache — cache
- 组: AQ-自进化机制 | Layer 0
- 作用: DeepSeek prefix-cache：前缀字节级稳定，动态内容放末尾，协议不中途修改。
- 提供: 
- **为什么存在（历史）**: 0801 输入缓存优化项目，0817 auto-mode 已含。动机：DeepSeek prefix-cache 命中可降 input 成本 98-99%。
- **为什么存在（当前）**: 严格保证共享前缀（auto-mode.md）session 内字节稳定、不重排不动态注入；静态内容前置、动态内容置末。
- **怎么用（触发）**: 每次 prompt 组装时恒生效。
- **怎么用（工作流）**: 静态规则/工具定义/共享协议放前缀不动；动态内容放末尾；委派协议经 agent.{plan,build}.prompt 注入。
- **怎么用（协作）**: instr-auto-mode；config-main（instructions 顺序 + cost 字段）；provider deepseek。

## mech-coding-discipline — coding-discipline
- 组: AQ-自进化机制 | Layer 0
- 作用: 验证与证据/从磁盘读不依赖对话记忆/路径本地化/元数据不入输出。
- 提供: 
- **为什么存在（历史）**: 0817 auto-mode 已含。动机：约束所有 Agent 形成「先验证再报告」的可靠工程习惯。
- **为什么存在（当前）**: 强制完成前跑测试/lint/构建并展示输出；写新工件前 read 其所有 requires 依赖；路径本地化。
- **怎么用（触发）**: 任何完成声明前；创建/修改文件前；DAG 工件生成前。
- **怎么用（工作流）**: 不报告成功除非有新鲜验证证据；磁盘重读依赖文件；路径仓库本地化；schemas 中 context/rules 为理解约束。
- **怎么用（协作）**: agent-plan、agent-build；各子Agent；instr-auto-mode；DAG 生成脚本。

## mech-coding-safety — coding-safety
- 组: AQ-自进化机制 | Layer 0
- 作用: 优先 edit(UTF-8安全)；禁用 python -c 内联管道；独立.py 文件；修改中文JSON后验证。
- 提供: 
- **为什么存在（历史）**: 0803 编码安全纵深防御项目，0817 已具。动机：bash 内联 python -c 会截断中文 UTF-8。
- **为什么存在（当前）**: 确立 edit 工具为第一优先级，禁止降级为 bash 写文件或内联管道。
- **怎么用（触发）**: 任何修改/写入文件（尤其含中文 JSON）的操作。
- **怎么用（工作流）**: 优先 edit；edit 不可用先切 Build 模式；禁 python -c 管道改用独立 .py；改含中文 JSON 后 json.load 验证。
- **怎么用（协作）**: agent-build、agent-plan；read/edit 工具；instr-auto-mode。

## mech-fault — fault
- 组: AQ-自进化机制 | Layer 0
- 作用: 工具失败重试3次→换方案→记录；MCP 断开降级内置工具；JSON 解析失败正则提取。
- 提供: 
- **为什么存在（历史）**: 0817 auto-mode 已含。动机：子Agent 与工具调用易失败，需设定明确重试上限。
- **为什么存在（当前）**: 为所有 Agent 提供可预测的失败处理阶梯：工具失败 3 次内自尝试至上报。
- **怎么用（触发）**: 工具调用失败、MCP 断连、子Agent 返回非 JSON、bash/网络超时。
- **怎么用（工作流）**: 工具：重试→换替代方案→记录 errors[] 上报；MCP：等 3 秒重连→降级内置工具；JSON：提取最外层 {...}→失败入 errors；超时：延长 timeout→拆分命令。
- **怎么用（协作）**: agent-plan、agent-build；各子Agent；instr-auto-mode。

## mech-gate — gate
- 组: AQ-自进化机制 | Layer 0
- 作用: MANDATORY GATE CHECK：范围/深度/操作/风险四维自评(1-5)输出总分→Daily/Deep。
- 提供: 
- **为什么存在（历史）**: 0817 auto-mode 已含。动机：为推理深度与 token 预算做成本控制基准。
- **为什么存在（当前）**: 作为主Agent 每次操作的强制第一行输出，硬性不可跳过；是 Daily/Deep 决策与 Variant 继承的量化入口。
- **怎么用（触发）**: 主Agent（plan/build）收到任何任务时，第一条助手消息必须先输出；子Agent 不输出。
- **怎么用（工作流）**: 4 维自评（范围/深度/操作/风险各1-5）→总分→对照决策边界→输出 [GATE] 格式。
- **怎么用（协作）**: agent-plan、agent-build；instr-auto-mode；skill-grill-me。

## mech-grill-me — grill-me
- 组: AQ-自进化机制 | Layer 0
- 作用: Plan/默认阶段逐分支拷问用户，直到达成共识；问一答一（question工具），含 Drift 护栏与收敛审计。
- 提供: 
- **为什么存在（历史）**: 源自 skill-grill-me 与 plan prompt 首段。0817 计划书已明示「Plan 阶段 Grill-Me 收敛 13 项决策」。动机：替代主Agent 随性抛多个问题或纯文本提问，强制用 question 工具弹窗逐条收敛设计树。
- **为什么存在（当前）**: Plan 模式唯一入口，保证需求澄清阶段逐分支下钻、依赖互解；防协议漂移要求每条消息必须且只能以一个 question 调用结尾。
- **怎么用（触发）**: 进入 plan/build 角色 prompt 即生效；用户发起计划类任务时。
- **怎么用（工作流）**: 每条消息输出 [GRILL] <ack> 后同消息紧跟一次 question 调用；可自探索的先探索而非问用户；全局收敛后输出 Decision tree resolved + 决策编号清单。
- **怎么用（协作）**: agent-plan、agent-build（prompt 首段注入）；skill-grill-me；内置 question 工具。

## mech-memory-gate — memory-gate
- 组: AQ-自进化机制 | Layer 0
- 作用: MEMORY.md 严禁直接修改，走 pending→reflection-worker→/reflection 确认→带[src:]写入。
- 提供: 
- **为什么存在（历史）**: 2026-08-19 根因修复引入，0817 版本缺失。动机：此前存在直接 edit/write MEMORY.md 导致记忆条目失序、来源不明的隐患。
- **为什么存在（当前）**: 杜绝任何绕过通道，所有记忆写入必须经 pending→reflection-worker→/reflection 逐条确认；且每个 § 段必须带 [src: <cycle_id>] 签名。
- **怎么用（触发）**: 任何试图写入 MEMORY.md 的行为（除 /reflection 审阅执行者外）。
- **怎么用（工作流）**: ①封装 4 层→②pending.json(waiting)→③reflection-worker 处理→④用户 /reflection yes/edit 确认→⑤确认后才写入并可带 [src:] 签名。
- **怎么用（协作）**: instr-memory（MEMORY.md）；command-reflection；agent-reflection-worker；instr-auto-mode。

## mech-mission-archive — mission-archive
- 组: AQ-自进化机制 | Layer 0
- 作用: 任务完成 5 段报告模板 + 询问用户留档 + 路径门控正则校验。
- 提供: 
- **为什么存在（历史）**: 0802 Mission留档系统创立，0817 已具。0819 增强为双版本留档。动机：把每次任务产出与复盘报告按规范路径持久化。
- **为什么存在（当前）**: 半自动触发（question 询问是否留档），报告强制 5 段，三重门控确保留档规范。
- **怎么用（触发）**: 任务完成后（含留档询问确认）。
- **怎么用（工作流）**: question 询问「是否留档」→验证路径正则→保存 5 段报告→用户确认。
- **怎么用（协作）**: agent-plan、agent-build；question 工具；config-main；MEMORY legacy_archive §。

## mech-output — output
- 组: AQ-自进化机制 | Layer 0
- 作用: 分段读取/压缩大输出/只读优先，控制 token 规模。
- 提供: 
- **为什么存在（历史）**: 0812 headroom MCP 量化亏损被禁用，0817 auto-mode 已含。动机：工具返回过大时全量灌入会撑爆上下文。
- **为什么存在（当前）**: 大文件分段读取、超长输出截断保留位置标记、优先 glob/grep 而非全量 read。
- **怎么用（触发）**: 文件>2000 行、工具返回>3000 字符、或同路径可选 read/glob 时。
- **怎么用（工作流）**: offset/limit 分段读；截断关键部分并留位置标记；优先 glob；内容搜索用 grep。
- **怎么用（协作）**: agent-plan、agent-build；skill-headroom（CLI）；instr-auto-mode；mcp-headroom（已禁用）。

## mech-parallel — parallel
- 组: AQ-自进化机制 | Layer 0
- 作用: 独立工具调用并行发出；相邻只读操作合并批次；读优先于写。
- 提供: 
- **为什么存在（历史）**: 0813 多路并行领域分片检索模式，0817 auto-mode 已含。动机：互不依赖的独立工具调用串行发出会浪费多轮 API 调用。
- **为什么存在（当前）**: 要求同一消息并行发出多个 read/glob/grep 等独立操作；相邻同类只读合并批次。
- **怎么用（触发）**: 存在多个互不依赖的读/查询操作、或探索库需并行 glob+grep。
- **怎么用（工作流）**: 同一消息并行多工具；相邻同类合并批次；先并行 glob 找文件+grep 搜内容再决定下一步；不在同消息混读写。
- **怎么用（协作）**: agent-plan、agent-build；agent-explore/agent-general；instr-auto-mode。

## mech-proxy — proxy
- 组: AQ-自进化机制 | Layer 1
- 作用: 默认直连；境外被墙站点 proxy_on 或 curl -x 172.29.0.1:7890；模型API勿设代理。
- 提供: 
- **为什么存在（历史）**: WSL2 代理网关 172.29.0.1:7890。0813 时子Agent 联网给代理；0822 策略改为默认直连。动机：区分国内直连与境外被墙访问。
- **为什么存在（当前）**: 模型 API 链不读代理 env 必须直连；境外被墙站点需显式 curl -x；国内源全直连。
- **怎么用（触发）**: 按访问目标分域：模型 API/国内源直连；境外被墙站点用 -x 代理；git 固定定向代理。
- **怎么用（工作流）**: 默认直连（proxy_off 无全局 env）；境外需求手动 curl -x 或依赖 git 定向代理；proxy_on 后 no_proxy 保国内直连。
- **怎么用（协作）**: config-main；instr-auto-mode；agent-general/agent-explore；git 全局代理。

## mech-reflection-check — reflection-check
- 组: AQ-自进化机制 | Layer 0
- 作用: 查 pending.json waiting_count→标 processing→委派 reflection-worker→/reflection 逐条确认。
- 提供: 
- **为什么存在（历史）**: Reflection 系统创立于 0805，0817 已有 agent-plan「Build 末尾 Reflection 4 层写入」。动机：把每个 Plan+Build 周期的决策与数据异步沉淀为记忆/技能。
- **为什么存在（当前）**: 在消息接收即刻检查 pending.json 的 meta.waiting_count>0，存在即标记 processing 并委派 reflection-worker；每周期结束封装 4 层写入。
- **怎么用（触发）**: 收到用户消息且 pending.json waiting 待处理；以及每周期末尾。
- **怎么用（工作流）**: ①封装 4 层输入→②追加 pending.json(status=waiting)→③下轮消息检查 waiting_count→④标 processing 委派 reflection-worker→⑤反思产出→⑥/reflection 审阅确认。
- **怎么用（协作）**: agent-plan、agent-build；agent-reflection-worker；command-reflection；skill-agent-reflection；pending.json。

## mech-subagent-rules — subagent-rules
- 组: AQ-自进化机制 | Layer 0
- 作用: 子Agent 身份约束/工具使用/错误处理/通信规范(JSON)+结构化返回。
- 提供: 
- **为什么存在（历史）**: 0817 auto-mode 已含。动机：统一所有 task() 子Agent 的身份约束与返回契约。
- **为什么存在（当前）**: 子Agent 纯执行不委派/不调用 search；禁止改 MEMORY.md；以固定结构化 JSON 返回。
- **怎么用（触发）**: 主Agent 通过 task() 创建任何子Agent 时。
- **怎么用（工作流）**: 身份约束→结构化 JSON 返回→读优先于写→3 次自修复上限后记录 errors[] 上报。
- **怎么用（协作）**: agent-* 子Agent；agent-plan、agent-build；instr-auto-mode；skill-agency-agents。

## mech-variant — variant
- 组: AQ-自进化机制 | Layer 0
- 作用: Plan 阶段输出[COMPLEXITY]/Build 继承推理深度；Ctrl+T 运行时切换 daily/deep。
- 提供: 
- **为什么存在（历史）**: 0817 配置已为各模型定义 daily/deep variants。动机：同一模型按任务复杂度分配推理预算。
- **为什么存在（当前）**: 提供运行时切换（Ctrl+T）与跨阶段继承：Plan 收敛摘要携带 [COMPLEXITY: X/20]，Build 阶段检测到即用匹配推理深度。
- **怎么用（触发）**: 会话中需升降推理强度时按 Ctrl+T；或 Build 检测到上一条 plan 含 [COMPLEXITY] 标记。
- **怎么用（工作流）**: 查阅 variant 列表切换；或改 opencode.jsonc agent.variant；Plan 输出 [COMPLEXITY]，Build 启动时匹配。
- **怎么用（协作）**: config-main（provider variants + agent.variant）；instr-auto-mode；agent-plan、agent-build。
