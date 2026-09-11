# mechanism 节点（18）

## mech-agents-protocol — agents-protocol
- 组: AQ-自进化机制 | Layer 0
- 作用: 主Agent 任务调度者→拆解→search-agents 匹配→委派子Agent→聚合；含 MCP 路由规则
- 提供: 
- **为什么存在（历史）**: 为解决单 Agent 上下文爆炸与执行者模式问题，设定'调度者非执行者'分工：主 Agent 只编排(拆解/匹配/委派/聚合)，子 Agent 只执行，角色优先匹配 agency-agents。
- **为什么存在（当前）**: 复杂/多步/联网任务经由 task() 委派子 Agent 并行或接力，主 Agent 上下文不爆；对垂直领域(RL/LLM 推理等)search-agents 命中率低时改走 general 子 Agent+自写角色提示词，保证任意任务都可委派且有正确角色激活。
- **怎么用（触发）**: 收到请求先分类判断：是否需要≥2 个工具/联网/多步推理→ YES 则第一条工具调用必须是 search-agents。
- **怎么用（工作流）**: ①search-agents -Query 关键词 -Top 5 搜角色(只看 JSON 元数据)或自写 2-3 句角色提示词；②拆解任务：独立→并行 Task，有依赖→串行接力(data 传递)，耦合→单 Agent；③组装子 Agent prompt(SUBAGENT 身份+Role Activation+Skills to Load+Task+No Self-Assessment+Return Format)，drawio-worker 须精确写 drawio-reference；④聚合：success→summary|partial→+errors|failed→询问用户；⑤超 3 分钟没发 task→默念失败模式自查(执行者/例外滥用/假并行)。
- **怎么用（协作）**: 依赖 skill/agency-agents/search-agents.py 与 agent-index.json；主 Agent prompt 来自 opencode.jsonc agent.plan/build.prompt 内 Agent Protocol 与 instructions/agent-protocol.md；子 Agent 角色定义在 opencode.jsonc agent(plan/build/pdf-worker/drawio-worker/vision-worker/general/explore/reflection-worker/search-worker)；opencode.jsonc plan.permission 限制 bash 默认 deny。

## mech-architecture — architecture
- 组: AQ-自进化机制 | Layer 0
- 作用: 架构三层栈：skill-architecture-judgment + agent-architect-worker + 行为层强制 + /arch 命令 + gate 门控；ADR/权衡矩阵经 gate_architecture.py PASS 方可交付
- 提供: 
- **为什么存在（历史）**: 源自 0910-软件工程架构方法论知识图谱（167 节点/360 边/18 组/11 域/三层）交付与 0911 opencode 架构能力扩展实战：把「架构判断力」从速查+路径路由升级为 opencode 可执行的架构能力三层栈（能力 Skill + 可见子Agent + 行为层），并补齐显式命令与机检门控。
- **为什么存在（当前）**: 当前由五元组成：skill-architecture-judgment（可执行工作流 + 内置 167 节点离线图谱 + schemas/templates/gate）、agent-architect-worker（可见子Agent，继承父会话模型，产出 ADR/多维权衡矩阵/边界设计说明）、instr-architecture-behavior（行为层全局强制：架构任务必加载 skill + 委派 worker + 门控）、command-arch（/arch 显式入口）、gate_architecture.py（--kind adr|boundary 机检门控，PASS 前不得交付）。知识分层刚性：方法论层 MTH 与本质层 ESS 重召回，技术实践层 TEC 仅作 standards_refs 选型标尺、不得进入 decision/rationale。
- **怎么用（触发）**: 三条触发：①自动路由——任务涉及技术选型/架构风格/模块与服务边界与粒度/架构评审/质量属性权衡/技术债治理/演进治理时，主流程(plan/build)自动加载本 skill 并委派 architect-worker；②显式命令 /arch <任务描述> 或 /arch 选型|评审|边界|技术债 ...；③openspec design 工件生成或修改时由行为层 architecture-behavior.md 强制触发。
- **怎么用（工作流）**: ①判场景：把问题归入 routing.md 的 18 个任务场景之一（先匹配触发问法）；②定产出类型：adr(+矩阵) / boundary 为门控级，review / tech-debt 为模板级；③委派 architect-worker，prompt 含 Skills to Load、对应模板与 schema、TEC 引用约束；④产出后必跑 gate_architecture.py（--kind adr|boundary，schema 与 graph 自动解析），FAIL 回传修正最多 2 轮，不得降级口头通过；⑤交付主产物 + 多维权衡矩阵（涉选型）+ 门控证据 + 命中场景节点；⑥主动询问是否需要 drawio 架构图（是则另委 drawio-worker，prompt 必含 drawio-reference）。
- **怎么用（协作）**: 组成五元 = skill-architecture-judgment + agent-architect-worker + instr-architecture-behavior + command-arch + gate_architecture.py；依赖 opencode.jsonc agent 段（architect-worker 定义）与 config-main（instructions 数组引用 architecture-behavior.md）；与架构图委派链路（drawio-worker + drawio-reference）、kb-construction（内容交付型/上下文注入型）协作；知识图谱为母库离线资产（0910-软件工程架构方法论），不联网即可用。

## mech-browser-tabs — browser-tabs
- 组: AQ-自进化机制 | Layer 0
- 作用: new_tab 后关闭标签页；任务完成询问是否关闭；批量爬取不逐页关闭
- 提供: 
- **为什么存在（历史）**: 为管理 browser-harness(browser-use)进行网页交互时 Chrome 标签页的生命周期，避免标签页堆积占用资源。
- **为什么存在（当前）**: 当前原则：用完即关(new_tab 打开并提取后关闭标签页)；批量关闭提示(整个任务浏览器读取全部完成后必须用 question 询问关闭所有标签页保留第一个)；批量爬取中途不逐页关闭(影响速度)；WSL2 浏览器自动化统一 agent-browser，browser-harness 降为 Windows 备选。
- **怎么用（触发）**: 使用 browser-harness/browser-use 进行网页交互(new_tab 打开页面、批量爬取、访问多个详情页)时触发。
- **怎么用（工作流）**: ①每次 new_tab() 完成数据提取后关闭该标签页(跑 close-chrome-tabs.ps1 -KeepFirst)；②所有浏览器读取全部完成后用 question 询问用户「是否关闭所有标签页？」；③批量爬取中途不逐页关，等整个任务阶段完成后统一关闭；④标签页参数(-All/-KeepFirst/-KeepUrlPattern/无参列出)。
- **怎么用（协作）**: 指令源 instructions/browser-management.md 与 opencode.jsonc agent.plan/build.prompt 内『浏览器标签页管理』；依赖脚本 close-chrome-tabs.ps1；WSL2 用 agent-browser、Windows 备选 browser-harness(skill/browser-harness)；与代理纪律(mech-proxy)、浏览器自动化 skill 协作。

## mech-cache — cache
- 组: AQ-自进化机制 | Layer 0
- 作用: DeepSeek prefix-cache：前缀字节级稳定，动态内容放末尾，协议不中途修改
- 提供: 
- **为什么存在（历史）**: 本项目 API 调用基于 DeepSeek prefix-cache 机制：缓存命中时 input token 成本降 98%~99%，前缀字节级变化会导致整个缓存失效，故把静态内容稳定置前以最大化命中。
- **为什么存在（当前）**: 作为成本优化核心纪律，要求所有文档/规则/工具定义等静态内容保持在 prompt 前缀且不改，动态内容(用户问题/检索结果/变化参数)始终放末尾；auto-mode.md 全 Agent 作为共享前缀加载，委派协议经 agent.plan/build.prompt 注入(方案 A prompt 隔离)。
- **怎么用（触发）**: 持续作用于每次 API 调用设计：任何静态共享前缀内容必须字节稳定；缓存协议承诺本文档 session 运行期间不修改/不重排/不动态注入。
- **怎么用（工作流）**: ①把共享前缀(如 auto-mode.md/协议)固定在 prompt 最前且冻结；②动态内容追加到尾部；③避免在同一前缀间插入时间戳/会话 ID/动态内容导致缓存失效；④MCP/Skill 工具 schema 首次加载后已被缓存，后续同类任务不做重复 tool discovery。
- **怎么用（协作）**: 作用于所有指令源：instructions/auto-mode.md『Cache Awareness』与『协议稳定性承诺』；与 Parallel & Batching(mech-parallel)及 Variant(mech-variant)协作；配置体现于 opencode.jsonc compaction 段。

## mech-coding-discipline — coding-discipline
- 组: AQ-自进化机制 | Layer 0
- 作用: 验证与证据/从磁盘读不依赖对话记忆/路径本地化/元数据不入输出
- 提供: 
- **为什么存在（历史）**: 为建立跨 Skill/Workflow 边界的通用编码准则，覆盖所有 Agent，防止依赖对话记忆的旧结果和跨机器绝对路径假设。
- **为什么存在（当前）**: 当前准则：验证与证据(不报告成功除非有新鲜验证证据，完成前跑测试→lint→报告)；从磁盘读取不依赖对话记忆(创建/修改文件前重新读依赖文件)；路径本地化(文件路径保持仓库本地化，子 Agent 返回绝对路径主 Agent 转相对路径)；元数据不入输出(context/rules/project_context 是约束不可复入产出文件)。
- **怎么用（触发）**: 任何 Agent 实施代码/生成 DAG 工件时持续生效：声明完成前、创建/修改文件前必须磁盘重读。
- **怎么用（工作流）**: ①完成声明前运行验证(测试通过→lint 通过→报告结果)并展示输出；②创建/修改文件前从磁盘重新读依赖文件；③DAG 工件生成写新工件前 read 所有 requires 依赖；④文件路径用相对路径或 repoRoot 拼接；⑤不以 context/rules 等约束字段入产出文件。
- **怎么用（协作）**: 指令源 instructions/auto-mode.md『Universal Coding Discipline』；与子 Agent 规则(mech-subagent-rules)、编码安全(mech-coding-safety)协作；影响 DAG 生成流程(proposal/specs/design/tasks requires 依赖读取)。

## mech-coding-safety — coding-safety
- 组: AQ-自进化机制 | Layer 0
- 作用: 优先 edit(UTF-8安全)；禁用 python -c 内联管道；独立.py 文件；修改中文JSON后验证
- 提供: 
- **为什么存在（历史）**: 为防中文 UTF-8 多字节序列被 PowerShell 转义链截断(python -c 经转义会截断中文)，建立文件修改的编码安全优先级。
- **为什么存在（当前）**: 当前规则：优先 edit 工具(全程 UTF-8 安全)；edit 不可用→切 Build 模式修改，绝不降级为 bash 写文件；严禁 bash+Python 内联管道(python -c)；必须脚本写文件时写独立 .py 再执行；改含中文 JSON 后必须 json.load 验证；另有 replaceAll 误伤逐 Agent 复核+旧值零残留检查。
- **怎么用（触发）**: 任何修改文件/写文件/脚本写文件的场景持续生效。
- **怎么用（工作流）**: ①优先 edit(UTF-8 安全)；②edit 不可用→切 Build 模式再改，不用 bash 写；③严禁 python -c + bash 内联管道；④必须脚本写→写独立 .py 再 python 执行；⑤改含中文 JSON 后 json.load 验证；⑥全局替换(replaceAll)后做旧值零残留检查；⑦Python 输出中文优先 sys.stdout.reconfigure(encoding='utf-8')。
- **怎么用（协作）**: 指令源 instructions/auto-mode.md『Universal Coding Discipline』与 opencode.jsonc agent.plan/build.prompt 内『编码安全规则』；MEMORY.md cycle_legacy_coding 记忆；与 Mission 留档路径/Reflection 写入协作。

## mech-fault — fault
- 组: AQ-自进化机制 | Layer 0
- 作用: 工具失败重试3次→换方案→记录；MCP 断开降级内置工具；JSON 解析失败正则提取
- 提供: 
- **为什么存在（历史）**: 为应对工具调用失败/MCP 连接断开/JSON 解析失败等运行时故障，建立分级自愈策略，避免无限重试浪费 API 调用与上下文。
- **为什么存在（当前）**: 当前三级自修复与降级：工具调用第1次失败检查参数重试、第2次换替代方案、第3次记录 errors[] 上报；MCP 连接断开等待 3 秒重连、仍失败跳过用内置工具降级；JSON 解析失败用正则提取最外层 {...}；超时先延长后拆分。
- **怎么用（触发）**: 工具调用返回错误、MCP 连接断开、子 Agent 返回非 JSON、bash/网络超时四类故障时触发。
- **怎么用（工作流）**: ①工具失败：格式化重试→换工具/路径/参数→记录 errors[] 上报；②MCP 断开：等 3 秒重连→仍失败跳过降级为内置工具；③JSON 解析：提取最外层 {...}→失败规 errors[]；④超时：先 timeout 延长→失败拆分命令/缓存结果；⑤子 Agent 多次失败后清晰记入 errors 上报，不陷入重试循环。
- **怎么用（协作）**: 指令源 instructions/auto-mode.md『Fault Tolerance』；与 SubAgent Rules('自修复失败 3 次记 errors 上报')和 Agent Protocol 的失败模式自查协作；影响返回 JSON 结构(status/errors 字段)。

## mech-gate — gate
- 组: AQ-自进化机制 | Layer 1
- 作用: MANDATORY GATE CHECK：范围/深度/操作/风险四维自评(1-5)输出总分→Daily/Deep
- 提供: 
- **为什么存在（历史）**: 为解决任务复杂度与推理深度不匹配导致的长任务输出截断/多轮重试成本失控，引入强制自评门控：任务开始前先量化影响范围/逻辑深度/操作数量/风险以决定用哪档推理。
- **为什么存在（当前）**: 作为主 Agent(plan/build)的第一条强制输出，用 4 维各 1-5 分(影响范围/逻辑深度/操作数量/风险精度)求总分定 Variant(≤12→Daily，≥13→Deep)，评分保守宁高估，边界值 12→Daily、13→Deep，为成本与质量作显式权衡。
- **怎么用（触发）**: 主 Agent 收到任务后、任何操作之前，第一条助手消息必须以 [GATE] 范围=X 深度=X 操作=X 风险=X → 总分=XX → Daily|Deep 开头；子 Agent 为纯执行者不输出 GATE。
- **怎么用（工作流）**: ①按 4 维自评表逐一打分并求和；②查决策边界表定 Variant 与 max_tokens/reasoning_effort；③输出 GATE 行后继续任务；④Plan 收敛时把 GATE 自评+COMPLEXITY+决策列表封装进 Reflection Layer A；⑤Build 若检测到 [COMPLEXITY] 标记则继承推理深度不重评。
- **怎么用（协作）**: 指令源 /home/zako-mio/.config/opencode/instructions/auto-mode.md『MANDATORY GATE CHECK』；承接 Variant 控制(mech-variant)与 Reflection Layer A；写入 pending.json；与 Agent 委派协议的'No Self-Assessment'(子 Agent 不重复 GATE)协作。

## mech-grill-me — grill-me
- 组: AQ-自进化机制 | Layer 0
- 作用: Plan 阶段逐分支追问收敛方案，问一答一（question 工具），含 Drift 护栏与收敛审计
- 提供: 
- **为什么存在（历史）**: 源自 RobMitt/grill-me-skill(基于 Matt Pocock 作品 MIT)，用于对用户方案/设计进行压力测试，逐问题拷问直至设计意图完全对齐(Fork 自外部 skill 集成)。
- **为什么存在（当前）**: 作为 Plan 模式的默认协议被内联进 opencode.jsonc agent.plan.prompt/subagent 角色，确保正式编码前决策树所有分支被显式解析，避免模糊需求导致 Build 返工；在长会话中靠三层护栏防协议漂移。
- **怎么用（触发）**: 用户关键词触发('grill me'/'拷问我'/'面试我的方案'/'压力测试这个方案')；或 Plan 模式启动时由 opencode.jsonc agent.plan/build.prompt 内联的 Grill-Me Protocol 自动启用。
- **怎么用（工作流）**: ①收到方案后，每次回答后输出 [GRILL] 简短致谢 → 同一消息内紧接一次 question 工具调用(一次只问一个问题，2-4 个可选答案)；②能靠探索代码库/文件自行回答的分支就先自行探索而非问用户；③沿设计树走遍所有分支直至无决策依赖；④收敛时输出 [GRILL] Decision tree resolved. + 一句话总结 + 决策编号列表。
- **怎么用（协作）**: 依赖 opencode 原生 question 工具；指令源 skill/grill-me/SKILL.md；已内联于 opencode.jsonc agent.plan.prompt 与 agent.build.prompt；与 GATE 门控(Plan 收敛写 GATE+COMPLEXITY)与 Reflection 的 Layer A(GRILL 决策列表)协作。

## mech-memory-gate — memory-gate
- 组: AQ-自进化机制 | Layer 0
- 作用: MEMORY.md 严禁直接修改，走 pending→reflection-worker→/reflection 确认→带[src:]写入
- 提供: 
- **为什么存在（历史）**: 2026-08-19 根因修复：此前直接改 MEMORY.md 导致内容漂移/无溯源，故设硬门禁禁止绕过反射链路直接写入，保证每条记忆带来源签名可回溯。
- **为什么存在（当前）**: 确保记忆写入仅经五步链路(①封装 4 层输入→②追加 pending.json status=waiting→③reflection-worker 处理→④用户 /reflection 逐条 yes/edit 确认→⑤确认后才写入)，写入的每个 § 段必须带 [src: <cycle_id>] 签名，无签名禁止写入，唯一例外是 /reflection 命令本身。
- **怎么用（触发）**: 任何试图写入 MEMORY.md 的编辑/写操作会被拦截；唯一合法触发是 /reflection 用户确认；另子 Agent 若产出记忆条目写入 memory_pending/ 待审。
- **怎么用（工作流）**: ①记忆产出方(主 Agent 封装 4 层或子 Agent 交 memory_pending/)不直接碰 MEMORY.md；②reflection-worker 分析并入 pending.json results(status=done)；③用户 /reflection 三池扫描+统一分析/逐条确认；④确认 yes/edit→主 Agent 写 MEMORY.md(§ 分段，带 [src: cycle_id])；⑤写后校验脚本按 § 切分每段首行为 [src:...]；⑥备份→原子写回→JSON 校验，容量>5000 走分层精简。
- **怎么用（协作）**: 目标文件 MEMORY.md(§-分段格式)；由 opencode.jsonc agent.plan/build.prompt 内 Memo 硬门禁段与 auto-mode.md『Universal SubAgent Rules』身份约束共同强制；依赖 Reflection 链路；子 Agent 记忆写入 ~/opencode/archive/Reflection/memory_pending/。

## mech-mission-archive — mission-archive
- 组: AQ-自进化机制 | Layer 0
- 作用: 任务完成 5 段报告模板 + 询问用户留档 + 路径门控正则校验
- 提供: 
- **为什么存在（历史）**: 为让每次任务产出可复盘可追溯，约定任务完成报告必须含 5 段(当时情况/制定计划/执行情况/完成情况/反思分析建议)，并保存到标准化留档目录。
- **为什么存在（当前）**: 当前双版本留档(AI 友好 report.md + 可读 report.html)，HTML 走质量门控(UTF-8 无替换字符/div 开闭平衡/5 段完整)；三重门控(完整性/询问 question/路径正则)；依赖渲染正确性的交付物(动态 DAG/tap id/组框布局)须用 headless Chromium 实际渲染验证。
- **怎么用（触发）**: 任务完成后触发，必须用 question 工具询问用户「是否留档？」(半自动)。
- **怎么用（工作流）**: ①任务完成后用 question 询问是否留档；②用户确认→按 5 段模板撰写报告；③门控：完整性(5 段齐全)/询问(不得跳过)/路径(校验正则)；④双版本留存：report.md + report.html，HTML 跑质量门控脚本；⑤非项目本地文件存 ~/opencode/archive/Mission-file/{YYYY-MM}/{MMDD-任务名}/，项目文件存工作目录；⑥留档结束后 Build 末尾封装 4 层数据写 pending.json。
- **怎么用（协作）**: 参考 opencode.jsonc agent.plan/build.prompt 内『Mission留档规则』与 instructions/agent-protocol.md；存档目录 /home/zako-mio/opencode/archive/Mission-file/；与 Reflection 的 Layer D(留档产出)协作。

## mech-output — output
- 组: AQ-自进化机制 | Layer 0
- 作用: 分段读取/压缩大输出/只读优先，控制 token 规模
- 提供: 
- **为什么存在（历史）**: 为控 token 消耗与上下文占用，避免单次全量返回大文件/大输出撑爆上下文流，建立输出规模控制纪律。
- **为什么存在（当前）**: 当前要求：文件>2000 行用 offset/limit 分段读；grep 命中>50 条用更精确正则缩小；工具返回>3000 字符优先截断关键部分(headroom MCP 已禁用 2026-08-12)；同路径有 read+glob 时优先 glob，内容搜索优先 grep。
- **怎么用（触发）**: 读文件/工具返回/内容搜索时持续生效：大文件分段、大输出压缩、双路径选 lean 者。
- **怎么用（工作流）**: ①大文件分段读取(>2000 行用 offset/limit，先头尾中间按需)；②超大工具输出截断关键部分并留位置标记；③grep 命中>50 时缩范围；④只读优先：同路径 read/glob 选 glob，内容搜索优先 grep 再按需 read；⑤仅在确认需要时才全量展示。
- **怎么用（协作）**: 指令源 instructions/auto-mode.md『Output Discipline』；与 mech-parallel(只读优先)和 mech-session-memory(L1 剪枝裁剪超大工具输出)协作。

## mech-parallel — parallel
- 组: AQ-自进化机制 | Layer 0
- 作用: 独立工具调用并行发出；相邻只读操作合并批次；读优先于写
- 提供: 
- **为什么存在（历史）**: 为降低 API 调用轮次与缓存寿命损耗：互不依赖的独立工具调用必须同一消息并行发出，避免先 glob 再 read 这种浪费一轮的串行。
- **为什么存在（当前）**: 作为缓存性能优化关键，要求探索代码库时先并行 glob(找文件)+grep(搜内容)，结果汇总再决定下一步；相邻同类只读操作合并为批次，不在同一消息混合读写。
- **怎么用（触发）**: 任何含多个互不依赖工具调用/相邻同类只读操作的场景；首次加载 Skill 后不要重复 tool discovery(PDF 任务始终用 pdf-worker 而非重载 pdf-ocr)。
- **怎么用（工作流）**: ①识别互不依赖操作：glob+grep+read 三个独立操作一轮并行发出；②合并相邻同类只读批次；③先并行探索(glob+grep)汇总再定下一步；④写后读等依赖操作必须串行；⑤MCP/Skill 工具 schema 首次加载后缓存，后续同类不重复发现。
- **怎么用（协作）**: 指令源 instructions/auto-mode.md『Parallel & Batching』；与 mech-cache(缓存寿命)和 mech-output(只读优先)协作；子 Agent 多路并行领域分片检索模式见于 MEMORY.md cycle_20260813_parallel_search。

## mech-proxy — proxy
- 组: AQ-自进化机制 | Layer 1
- 作用: 默认直连；境外被墙站点 proxy_on 或 curl -x 172.29.0.1:7890；模型API勿设代理
- 提供: 
- **为什么存在（历史）**: WSL2 内访问宿主机代理网关 172.29.0.1:7890(宿主机 XQNetwork 监听 0.0.0.0:7890，HTTP+SOCKS5 混合端口)，用于访问境外被墙站点。
- **为什么存在（当前）**: 2026-08-22 更新为默认直连：.bashrc 不再自动 export 全局代理 env，仅访问境外被墙站点时手动 proxy_on 开启/proxy_off 关闭；国内流量与模型 API 全部直连；模型 API 调用链(Node fetch/undici)与 webfetch 工具不读代理 env，必须直连；curl/CLI 继承 shell env 默认直连，需境外时 curl -x http://172.29.0.1:7890；git 已配定向代理指向 172.29.0.1:7890。
- **怎么用（触发）**: 默认直连；仅当访问境外被墙站点(Google/X 等)时手动 proxy_on 或显式 curl -x/git 定向代理。
- **怎么用（工作流）**: ①默认 Shell 无代理 env→国内直连；②访问境外被墙内容→proxy_on 或 curl -x http://172.29.0.1:7890 <url>、git、browser-harness；③模型 API(api.deepseek.com/opencode.ai)必须直连禁止设代理；④webfetch 访问境内直接成功，境外会超时需 curl -x；⑤proxy_off 关闭，no_proxy 保证国内流量仍直连；⑥子 Agent 优先国内源直连，境外显式加 curl -x。
- **怎么用（协作）**: 指令源 instructions/auto-mode.md『联网代理纪律（WSL2 环境）』；MEMORY.md cycle_legacy_path/cycle_20260822_network 指针；与 Agent 委派(子 Agent 联网)及浏览器(agent-browser/browser-harness)协作。

## mech-reflection-check — reflection-check
- 组: AQ-自进化机制 | Layer 0
- 作用: 查 pending.json waiting_count→标 processing→委派 reflection-worker→/reflection 逐条确认
- 提供: 
- **为什么存在（历史）**: 自进化子系统：每个 Plan+Build 完整周期结束后异步反思，分析本轮执行经验，把可复用知识写入 Memory 或 Skill 轨道，让 Agent 随任务积累越用越强。
- **为什么存在（当前）**: 重构为状态机 + 三池扫描：pending.json(waiting→processing→done)承载 4 层输入，reflection-worker 只读 Reflection 目录+MEMORY 只写 Reflection 目录；处理前对卡 processing 超时条目回退 waiting 防单点阻塞；/reflection 命令做'whether to keep'(确认)与 worker 做'what to learn'(分析)分工。
- **怎么用（触发）**: 主 Agent 收到用户消息、在任务分类之前，检查 Reflection/pending.json 的 meta.waiting_count>0；或用户输入 /reflection(或 memory|skill|status|browse)。
- **怎么用（工作流）**: ①waiting_count>0→读 pending.json→找最早 waiting cycle→标 processing→写回→委派 reflection-worker 处理反思；②无论成功失败继续正常流程，连续失败 2 次标 expired；③worker 分析 4 层数据→产出 memory/skill 条目→写 pending.json(status=done)；④用户 /reflection→主 Agent 三池扫描→统一分析或逐条 yes/no/edit→确认写入→清理队列(备份→移除→更新 meta→JSON 校验)；⑤处理前超时判定防队列死锁。
- **怎么用（协作）**: 依赖 command/reflection.md、archive/Reflection/pending.json、skills/agent-reflection/SKILL.md、opencode.jsonc agent.reflection-worker；与 MEMORY 硬门禁(mech-memory-gate)、Mission 留档(mech-mission-archive)协作；output 目标 MEMORY.md 与 Reflection/skills/。

## mech-session-memory — session-memory
- 组: AQ-自进化机制 | Layer 0
- 作用: compaction 5 段模板(当前状态/关键文件/已做决策/待解决问题/经验教训)+L1剪枝/L2压缩/L3兜底
- 提供: 
- **为什么存在（历史）**: 0902 后新增：为应对会话上下文膨胀触发 compaction，建立阶梯式压缩决策树(L1 剪枝/L2 结构化压缩/L3 兜底摘要)，避免上下文爆仓与不必要的 compaction 触发。
- **为什么存在（当前）**: 当前压缩模板 5 段(当前状态/关键文件/已做决策/待解决问题/经验教训)，分别服务于恢复会话定位卡点、避免重复探索、不重问已决策项、知道待修问题、不踩两次坑；compaction 后保留 tail_turns=4(preserve_recent_tokens=16384)；模板不重复记录已截断的工具输出；模板语言与会话语言一致。
- **怎么用（触发）**: compaction 触发时；L1 剪枝(标记/截断超大工具输出)仍不足时进入 L2 结构化压缩。
- **怎么用（工作流）**: ①L1 剪枝：截断超大工具输出仅留关键部分+位置标记；②仍不足→L2 按 5 段模板输出结构化记忆；③L2 也不足→L3 通用全量摘要兜底；④compaction 后保留 tail_turns=4；⑤不重复记录已裁剪输出，模板语言跟随会话语言。
- **怎么用（协作）**: 指令源 instructions/auto-mode.md『Session Memory 结构化压缩模板』与 MEMORY.md cycle_0818_v4；配置体现于 opencode.jsonc compaction(auto/prune/tail_turns=4/preserve_recent_tokens=16384/reserved=10000)；与输出控制(mech-output L1 剪枝)和编码纪律(mech-coding-discipline)协作。

## mech-subagent-rules — subagent-rules
- 组: AQ-自进化机制 | Layer 0
- 作用: 子Agent 身份约束/工具使用/错误处理/通信规范(JSON)+结构化返回
- 提供: 
- **为什么存在（历史）**: 为统一所有 task() 创建的子 Agent 行为，消除身份冲突(子 Agent 不再收调度者角色指令)，并规范输出为可聚合的结构化 JSON。
- **为什么存在（当前）**: 当前约束：子 Agent 仅执行分配任务不委派/不调度/不调用其他 Agent，不使用 search-agents 等搜索机制，严禁直接改 MEMORY.md 或 pending.json 之外记忆文件(记忆条目写 memory_pending/ 待审)；所有输出必须返回结构化 JSON；工具使用优先已加载专用工具、结果超长截断、读优先于写；错误处理自修复 3 次后记 errors 上报；通信用 JSON，summary≤200 字。
- **怎么用（触发）**: 任何通过 task() 创建的子 Agent(plan/build/pdf-worker/drawio-worker/vision-worker/general/explore/reflection-worker/search-worker)被委派时作为共享前缀规则生效。
- **怎么用（工作流）**: ①身份约束：执行者身份不委派不搜 Agent，记忆产出入 memory_pending/；②工具：优先专用工具/结果超长截断/读优先于写；③错误：自修复失败 3 次记 errors 上报不无限重试；④通信：输出结构化 JSON，summary≤200 字，files_created/modified 绝对路径，data 仅核心结果，decisions/warnings/errors 分级。
- **怎么用（协作）**: 指令源 instructions/auto-mode.md『Universal SubAgent Rules』；子 Agent 定义于 opencode.jsonc agent；与故障自愈(mech-fault)、输出控制(mech-output)、编码纪律(mech-coding-discipline)、MEMORY 硬门禁(mech-memory-gate)共同作用于子 Agent。

## mech-variant — variant
- 组: AQ-自进化机制 | Layer 0
- 作用: Plan 阶段输出[COMPLEXITY]/Build 继承推理深度；Ctrl+T 运行时切换 daily/deep
- 提供: 
- **为什么存在（历史）**: 为在一次会话内按任务轻重动态调整推理强度，用 daily/deep 双 variant 映射不同 max_tokens 与 reasoning_effort，避免固定深度对简单任务浪费、对复杂任务截断。
- **为什么存在（当前）**: 提供运行时切换(Ctrl+T 循环)免改文件重启，并新增 [COMPLEXITY: X/20] 继承规则：Plan 收敛摘要打标记，Build 启动检测到即用匹配推理深度不重评，保证 DAG 上下游(Plan→Build)推理一致，成本可控且质量稳定。
- **怎么用（触发）**: 运行时按 Ctrl+T 循环切换(daily↔deep)；或 tui.json 绑定 variant_list 键位；或编辑 opencode.jsonc agent.plan/build.variant 手动切换；或 Build 启动检测到前置 plan 消息含 [COMPLEXITY] 标记时自动继承。
- **怎么用（工作流）**: ①GATE 门控评分定启动 variant(≤12 Daily/≥13 Deep)；②运行时按 Ctrl+T 免重启切换；③Plan 收敛写 [COMPLEXITY: X/20]；④Build 检测标记→用匹配深度→否则按 auto-mode 正常评估；⑤不改 opencode.jsonc agent.plan/build variant 配置。
- **怎么用（协作）**: 配置源 opencode.jsonc provider(variants 映射 daily/deep 的 max_tokens/reasoning_effort)与 compaction 段；承接 GATE 门控(mech-gate)；变体定义在 opencode.jsonc agent.plan/build.variant；与 mech-cache 协作(固定前缀稳定)。
