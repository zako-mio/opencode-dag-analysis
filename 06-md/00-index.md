# opencode DAG 分析 — AI 检索镜像

三图：官方包级 / 对比 / 改造双层。共 114 节点。

## 官方包（36）
| 节点 | 名称 | 组 | 层 | 作用 |
|---|---|---|---|---|
| oc-app | app | G10-应用 | 1 | OpenCode 桌面/Web 前端的 SolidJS 主应用。src/app.tsx 组装全部 Provider（Server/SDK/ServerSync/ |
| oc-cli | cli | G10-应用 | 0 | OpenCode 2.0 CLI 入口（bin: lildax）。src/index.ts:10-32 用 Effect 构建命令运行时：Runtime.han |
| oc-client | client | G3-客户端 | 3 | 面向 Web/桌面的客户端库。src/contract.ts:1-17 复用 protocol 的 makeDefaultApi 定义 ClientApi 与  |
| oc-codemode | codemode | G12-沙箱 | 1 | Code Mode 沙箱：基于 schema 描述的受限代码执行（package.json:5 描述）。src/interpreter/runtime.ts:1 |
| oc-console-app | console-app | G16-Console | 0 | Console 主站前端（SolidStart/SSR + Nitro on Cloudflare），包含营销落地页、认证回调、workspace 管理（bil |
| oc-console-core | console-core | G16-Console | 1 | Console 后端领域层：基于 drizzle-orm + PlanetScale 的数据库访问、Actor 权限上下文、以及 Account/User/Wo |
| oc-console-function | console-function | G16-Console | 0 | Cloudflare Workers 端边函数集：auth.ts 是 OpenAuth issuer（GitHub/Google 登录 + Cloudflare |
| oc-console-mail | console-mail | G16-Console | 2 | 邮件模板包：无 src/，全部为 emails/ 下的 jsx-email 模板与共享组件/样式。emails/templates/InviteEmail.ts |
| oc-console-resource | console-resource | G16-Console | 2 | SST 资源访问抽象层，无 src/ 目录（文件在包根）。通过 Proxy 按运行环境暴露 Resource：resource.cloudflare.ts 在  |
| oc-console-support | console-support | G16-Console | 0 | 面向支持/客服的内部工具站（SolidStart SSR）。核心功能是用户数据 lookup：src/lib/lookup.ts 按 wrk_/key_/sk- |
| oc-core | core | G6-核心服务 | 3 | 核心服务层（无根 index.ts，按子路径导出，package.json:18-23 暴露 effect/layer-node、session/runner  |
| oc-desktop | desktop | G10-应用 | 0 | Electron 桌面壳。src/main/index.ts:15-51 聚合应用生命周期：spawnLocalServer 拉起本地 sidecar 服务、r |
| oc-effect-drizzle-sqlite | effect-drizzle-sqlite | G15-存储适配 | 4 | Drizzle ORM 的 Effect 适配层。src/effect-sqlite/driver.ts:15-60 定义 EffectSQLiteDataba |
| oc-effect-sqlite-node | effect-sqlite-node | G15-存储适配 | 4 | 基于 Node 内置 node:sqlite 的 Effect SqlClient 实现。src/index.ts:49-161 make() 用 Databa |
| oc-enterprise | enterprise | G10-应用 | 0 | 基于 SolidStart 的企业版/云端分享服务。src/app.tsx:1-14 用 @opencode-ai/ui 的 Provider（Marked/D |
| oc-function | function | G13-边缘服务 | 0 | Cloudflare Workers 上的会话分享同步服务。src/api.ts:15-114 定义 SyncServer Durable Object：Web |
| oc-http-recorder | http-recorder | G14-工具 | 4 | HTTP 录制/回放工具（package.json:5 描述：Record and replay Effect HTTP client traffic with |
| oc-httpapi-codegen | httpapi-codegen | G14-工具 | 0 | 构建期源代码生成工具。compile(Api) 反射一个权威 HttpApi 共享契约；emitPromise/emitEffect/emitEffectImp |
| oc-llm | llm | G5-LLM请求层 | 4 | LLM 请求/协议层。src/index.ts:1-28 导出 LLMClient/Auth/Provider/Tool/ToolRuntime；核心 LLM  |
| oc-opencode | opencode | G19-主入口 | 0 | 主应用/CLI 入口。src/index.ts:45 用 yargs 装配 run/serve/tui/agent/acp 等全部子命令；src/cli/tui |
| oc-plugin | plugin | G7-插件SDK | 4 | 插件 SDK。src/index.ts:20-80 定义 Plugin/PluginInput/Config/Hooks 等公共类型，基于 @opencode- |
| oc-protocol | protocol | G2-通信协议 | 4 | 通信协议层。src/api.ts:26-86 用 effect/unstable/httpapi 定义 OpenCode HttpApi 结构：注册 Healt |
| oc-schema | schema | G1-数据模型 | 5 | 纯类型/数据模型包，仅依赖 effect（package.json:14-16）。以 Effect Schema 定义全部领域类型：Session/Sessio |
| oc-script | script | G14-工具 | 1 | 构建/发布脚本共享工具包。src/index.ts:5-76 读取仓库根 package.json 校验 bun 版本（semver.satisfies 检查， |
| oc-sdk | sdk | G3-客户端 | 5 | 官方 JS 客户端 SDK（packages/sdk/js/）。src/index.ts:1-21 导出 client/server 并通过 createOpe |
| oc-sdk-next | sdk-next | G3-客户端 | 0 | Effect 原生的进程内 OpenCode host SDK（过渡包，替代生成式 @opencode-ai/sdk）。src/opencode.ts 的 cr |
| oc-server | server | G4-服务端 | 1 | HTTP/SSE 服务器实现层。src/api.ts:5-8 用 @opencode-ai/protocol/api 的 makeDefaultApi 装配 H |
| oc-session-ui | session-ui | G9-UI组件 | 2 | 会话级 UI 组件集，介于基础组件库与完整应用之间。src/components/ 提供 SessionTurn、SessionReview、MessagePa |
| oc-slack | slack | G18-集成 | 0 | Slack 机器人集成（@slack/bolt Socket Mode）。src/index.ts 创建 opencode 服务端实例（createOpenco |
| oc-stats-app | stats-app | G17-Stats | 0 | OpenCode Stats 公共数据站点（SolidStart，Cloudflare preset，app.config.ts:1）。首页通过 @openco |
| oc-stats-core | stats-core | G17-Stats | 1 | Stats 后端核心（Effect + drizzle + PlanetScale）。src/athena.ts 封装 AWS Athena 查询服务（Star |
| oc-stats-server | stats-server | G17-Stats | 0 | Stats 后端 Node HTTP 服务（Effect HttpRouter + Bun，Dockerfile 部署）。src/server.ts 用 Nod |
| oc-storybook | storybook | G11-文档站点 | 0 | UI 组件开发文档站。.storybook/main.ts:13-29 用 storybook-solidjs-vite 定义框架并聚合 ui/session- |
| oc-tui | tui | G8-终端UI | 1 | 终端 UI 应用。src/index.tsx:1 导出 run/TuiInput；src/app.tsx:1-50 用 @opentui/solid 渲染整棵组 |
| oc-ui | ui | G9-UI组件 | 3 | SolidJS UI 组件库。src/components/ 含 50+ 基础组件（button/avatar/dialog/context-menu/diff |
| oc-web | web | G11-文档站点 | 0 | 基于 Astro + Starlight 的文档与分享站点。src/pages/s/[id].astro:2-8 渲染会话分享页（Share.tsx 消费 op |

## 装配层（69）
| 节点 | 名称 | 类型 | 组 | 层 | 作用 | why（需求驱动） |
|---|---|---|---|---|---|---|
| agent-build | build | agent | AG1-主Agent | 6 |  |  |
| agent-drawio-worker | drawio-worker | agent | AG2-子Agent | 7 | Diagram creation specialist using draw.io. Use for flowchart |  |
| agent-explore | explore | agent | AG2-子Agent | 7 | Fast agent specialized for exploring codebases. Inherits par |  |
| agent-general | general | agent | AG2-子Agent | 7 | General-purpose agent for researching complex questions and  |  |
| agent-pdf-worker | pdf-worker | agent | AG2-子Agent | 7 | PDF reader, OCR, and document analysis specialist. Use for a |  |
| agent-plan | plan | agent | AG1-主Agent | 6 |  |  |
| agent-reflection-worker | reflection-worker | agent | AG2-子Agent | 7 | Reflection specialist for the self-evolution system. Analyze |  |
| agent-vision-worker | vision-worker | agent | AG2-子Agent | 7 | Vision analysis specialist using DeepSeek vision model. Use  | 需要图片理解/截图分析/UI对照还原能力，且主Agent已换用 vision-exp 具备看图，委派链路上需要一个明确可 |
| command-reflection | reflection | command | AG5-工具插件 | 1 | 自定义命令 reflection.md |  |
| config-main | main | config | AG6-配置本体 | 2 | 主配置：agent/provider/mcp/compaction/skills/instructions/permis | 用 Go 订阅的包月额度覆盖高性价比编码；用 DeepSeek 官方直连兜底 Pro 与视觉；用智谱官方补 GLM-5. |
| instr-agent-protocol | agent-protocol | instruction | AG4-指令 | 1 | Agent Protocol (Cache-Stable Prefix) | 当前配置自动化后主Agent需在发起工具前先做任务分类，并规范子Agent prompt 结构。 |
| instr-auto-mode | auto-mode | instruction | AG4-指令 | 1 | Agent Universal Protocol (Cache-Stable Prefix — Do NOT modif |  |
| instr-browser-management | browser-management | instruction | AG4-指令 | 1 | 浏览器标签页管理 | 约束每次 new_tab 用完即关、整批任务完成后经 question 询问是否批量关闭、批量爬取中途不逐页关以免拖慢速 |
| instr-downloads | downloads | instruction | AG4-指令 | 1 | 文件导出与下载默认路径 | 当用户未指定路径且文件非项目本地文件时，强制保存到 D:\Opencode_Download，避免污染工作目录。 |
| instr-memory | memory | instruction | AG4-指令 | 1 | 项目记忆索引（§分段格式，上限~5000字符，含[src:]签名） |  |
| mcp-amap | amap | mcp | AG3-MCP | 1 | 【已禁用】12 个工具 ~2000 tokens 极低频 |  |
| mcp-drawio | drawio | mcp | AG3-MCP | 5 | 【启用】draw.io 图表创建（本地精简版 v1.5.0）。仅 drawio-worker 子Agent 使用 |  |
| mcp-drawio-local | drawio-local | mcp | AG3-MCP | 0 | 【禁用·离线兜底】断网时启用，与主 drawio 同一实例 |  |
| mcp-headroom | headroom | mcp | AG3-MCP | 0 | 【已禁用 2026-08-12】量化亏损（工具开销 > 收益）。切 Claude Code/Codex 走 proxy  |  |
| mcp-pdf-reader | pdf-reader | mcp | AG3-MCP | 6 | 【启用】PDF 文本提取。仅 pdf-worker 子Agent 使用（4 工具） |  |
| mcp-vscode-mcp-server | vscode-mcp-server | mcp | AG3-MCP | 0 | 【已禁用】仅 6 个工具(~692 tokens) 极少使用。审计报告见 Mission-file\\2026-08\\ |  |
| mech-agents-protocol | agents-protocol | mechanism | AQ-自进化机制 | 0 | 主 Agent 任务调度者→拆解→搜索角色→委派子 Agent→聚合；含 MCP 路由规则。 | 将需≥2工具/联网/多步的任务分解后委派子Agent，仅保留编排+聚合；通过 search-agents 匹配角色、MC |
| mech-browser-tabs | browser-tabs | mechanism | AQ-自进化机制 | 0 | new_tab 后关闭标签页；任务完成询问是否关闭；批量爬取不逐页关闭。 | 控制 browser-harness 会话的标签页生命周期：单次 new_tab 后即关；任务全完必须询问是否关页；批量 |
| mech-cache | cache | mechanism | AQ-自进化机制 | 0 | DeepSeek prefix-cache：前缀字节级稳定，动态内容放末尾，协议不中途修改。 | 严格保证共享前缀（auto-mode.md）session 内字节稳定、不重排不动态注入；静态内容前置、动态内容置末。 |
| mech-coding-discipline | coding-discipline | mechanism | AQ-自进化机制 | 0 | 验证与证据/从磁盘读不依赖对话记忆/路径本地化/元数据不入输出。 | 强制完成前跑测试/lint/构建并展示输出；写新工件前 read 其所有 requires 依赖；路径本地化。 |
| mech-coding-safety | coding-safety | mechanism | AQ-自进化机制 | 0 | 优先 edit(UTF-8安全)；禁用 python -c 内联管道；独立.py 文件；修改中文JSON后验证。 | 确立 edit 工具为第一优先级，禁止降级为 bash 写文件或内联管道。 |
| mech-fault | fault | mechanism | AQ-自进化机制 | 0 | 工具失败重试3次→换方案→记录；MCP 断开降级内置工具；JSON 解析失败正则提取。 | 为所有 Agent 提供可预测的失败处理阶梯：工具失败 3 次内自尝试至上报。 |
| mech-gate | gate | mechanism | AQ-自进化机制 | 0 | MANDATORY GATE CHECK：范围/深度/操作/风险四维自评(1-5)输出总分→Daily/Deep。 | 作为主Agent 每次操作的强制第一行输出，硬性不可跳过；是 Daily/Deep 决策与 Variant 继承的量化入 |
| mech-grill-me | grill-me | mechanism | AQ-自进化机制 | 0 | Plan/默认阶段逐分支拷问用户，直到达成共识；问一答一（question工具），含 Drift 护栏与收敛审计。 | Plan 模式唯一入口，保证需求澄清阶段逐分支下钻、依赖互解；防协议漂移要求每条消息必须且只能以一个 question  |
| mech-memory-gate | memory-gate | mechanism | AQ-自进化机制 | 0 | MEMORY.md 严禁直接修改，走 pending→reflection-worker→/reflection 确认→ | 杜绝任何绕过通道，所有记忆写入必须经 pending→reflection-worker→/reflection 逐条确 |
| mech-mission-archive | mission-archive | mechanism | AQ-自进化机制 | 0 | 任务完成 5 段报告模板 + 询问用户留档 + 路径门控正则校验。 | 半自动触发（question 询问是否留档），报告强制 5 段，三重门控确保留档规范。 |
| mech-output | output | mechanism | AQ-自进化机制 | 0 | 分段读取/压缩大输出/只读优先，控制 token 规模。 | 大文件分段读取、超长输出截断保留位置标记、优先 glob/grep 而非全量 read。 |
| mech-parallel | parallel | mechanism | AQ-自进化机制 | 0 | 独立工具调用并行发出；相邻只读操作合并批次；读优先于写。 | 要求同一消息并行发出多个 read/glob/grep 等独立操作；相邻同类只读合并批次。 |
| mech-proxy | proxy | mechanism | AQ-自进化机制 | 1 | 默认直连；境外被墙站点 proxy_on 或 curl -x 172.29.0.1:7890；模型API勿设代理。 | 模型 API 链不读代理 env 必须直连；境外被墙站点需显式 curl -x；国内源全直连。 |
| mech-reflection-check | reflection-check | mechanism | AQ-自进化机制 | 0 | 查 pending.json waiting_count→标 processing→委派 reflection-work | 在消息接收即刻检查 pending.json 的 meta.waiting_count>0，存在即标记 processi |
| mech-subagent-rules | subagent-rules | mechanism | AQ-自进化机制 | 0 | 子Agent 身份约束/工具使用/错误处理/通信规范(JSON)+结构化返回。 | 子Agent 纯执行不委派/不调用 search；禁止改 MEMORY.md；以固定结构化 JSON 返回。 |
| mech-variant | variant | mechanism | AQ-自进化机制 | 0 | Plan 阶段输出[COMPLEXITY]/Build 继承推理深度；Ctrl+T 运行时切换 daily/deep。 | 提供运行时切换（Ctrl+T）与跨阶段继承：Plan 收敛摘要携带 [COMPLEXITY: X/20]，Build 阶 |
| skill-agency-agents | agency-agents | skill | A6a-角色调度 | 1 | 专业AI角色调度系统。当用户任务较为复杂/专业时激活，根据任务内容自动匹配最合适的AI Agent角色，加载其专业pro |  |
| skill-browser-harness | browser-harness | skill | A6e-浏览器 | 1 | "Always use browser-use for any web interaction: automation, |  |
| skill-cytoscape-dag-visualization | cytoscape-dag-visualization | skill | A6c-DAG方法 | 0 | cytoscape.js 交互 DAG 可视化构建方法论。当任务涉及构建组级+下钻交互 DAG 总览、向页面注入 DAT |  |
| skill-dag-tutorial-authoring | dag-tutorial-authoring | skill | A6c-DAG方法 | 0 | DAG 教程编写方法论（零基础读者导向）。当任务涉及编写面向初学者的概念/技能 DAG 教程、将可读性规律编码为门控、调 |  |
| skill-drawio-reference | drawio-reference | skill | A6b-图表 | 1 | draw.io 图表完整参考文档。包含 XML schema 样式库、Mermaid.js 全语法参考（28种图表类型） |  |
| skill-frontend-design | frontend-design | skill | A6d-前端设计 | 0 | 前端设计双引擎系统。先数据驱动 Top K 候选推荐，后设计主管创意裁决。覆盖网页设计、UI 页面、组件、配色、排版、布 |  |
| skill-grill-me | grill-me | skill | A6a-角色调度 | 4 | Interview the user relentlessly about a plan or design until |  |
| skill-headroom | headroom | skill | A6h-上下文压缩 | 4 | Headroom 上下文压缩层（CLI 版）。支持 headroom proxy / audit-reads / sav |  |
| skill-lark-suite | lark-suite | skill | A6f-办公集成 | 1 | 飞书/Lark 全功能操作入口。通过 lark-cli 命令操作飞书资源，覆盖日历、消息、文档、云盘、多维表格、电子表格 |  |
| skill-multi-window-dag-delivery | multi-window-dag-delivery | skill | A6c-DAG方法 | 0 | 多层窗口接力 DAG 依赖链分析与交付方法论。当任务涉及将大型源码/插件库拆分为多窗口接力分析 DAG 依赖、每窗口产出 |  |
| skill-opencode-config | opencode-config | skill | A6b-配置知识 | 4 | OpenCode 配置（opencode.jsonc）分级知识库。覆盖官方 Schema v2 全部字段、本项目实际配置 |  |
| skill-openspec-apply-change | openspec-apply-change | skill | A6l-OpenSpec工作流 | 0 | 执行 tasks.md 中的实现任务——逐条完成并打勾。tasks.md 就绪后开始编码时使用。 |  |
| skill-openspec-archive-change | openspec-archive-change | skill | A6l-OpenSpec工作流 | 0 | 归档已完成的变更——合并 delta spec 到主 spec 并移动到 archive。实现完成并验证通过后使用。 |  |
| skill-openspec-bulk-archive-change | openspec-bulk-archive-change | skill | A6l-OpenSpec工作流 | 0 | 批量归档多个已完成的变更。 |  |
| skill-openspec-continue-change | openspec-continue-change | skill | A6l-OpenSpec工作流 | 0 | 继续已有的变更——按 DAG 顺序生成下一个未完成的工件。适合恢复中断的工作。 |  |
| skill-openspec-explore | openspec-explore | skill | A6l-OpenSpec工作流 | 0 | 探索模式——分析代码、理清需求、比较方案。不确定要做什么或需要先思考再动手时使用。不写代码。 |  |
| skill-openspec-ff-change | openspec-ff-change | skill | A6l-OpenSpec工作流 | 0 | 快速通道——跳过逐步交互，一键生成所有 OpenSpec 工件。适合有经验的用户或简单变更。 |  |
| skill-openspec-new-change | openspec-new-change | skill | A6l-OpenSpec工作流 | 0 | 逐步创建新变更——比 propose 更细粒度，逐个工件交互式创建。适合复杂或需精细控制的场景。 |  |
| skill-openspec-onboard | openspec-onboard | skill | A6l-OpenSpec工作流 | 0 | OpenSpec 引导教程——手把手带领首次使用的用户完成完整流程。 |  |
| skill-openspec-propose | openspec-propose | skill | A6l-OpenSpec工作流 | 0 | 创建变更提案——一键生成 proposal/design/specs/tasks。明确知道要做什么时使用。 |  |
| skill-openspec-sync-specs | openspec-sync-specs | skill | A6l-OpenSpec工作流 | 0 | 同步 delta spec 到主 spec（不归档）。仅被 archive-change 或显式召唤时使用。 |  |
| skill-openspec-update-change | openspec-update-change | skill | A6l-OpenSpec工作流 | 0 | 编辑/协调已有的 OpenSpec 工件。处理手动修改后的重新同步。 |  |
| skill-openspec-verify-change | openspec-verify-change | skill | A6l-OpenSpec工作流 | 0 | 验证实现是否匹配 spec/design。归档前的可选校验步骤。 |  |
| skill-pdf-ocr | pdf-ocr | skill | A6g-文档处理 | 1 | PDF OCR 识别专项。处理扫描件、图片型 PDF、含水印/印章的文档。支持多语言 OCR（中英）、表格区域提取、印章 |  |
| skill-recruit-assist | recruit-assist | skill | A6i-简历求职 | 0 | 简历投递辅助。支持投简历（打开招聘页+记录跟踪表）、识别简历（扫描表单字段+匹配信息库）、更新信息库、记录投递状态、跟踪 |  |
| skill-release-openspec | release-openspec | skill | A6l-OpenSpec工作流 | 0 | OpenSpec 自身发布管理。仅 OpenSpec 维护者使用。 |  |
| skill-resume-builder | resume-builder | skill | A6i-简历求职 | 0 | 当用户请求制作简历、修改简历、优化简历、写CV、写求职信、准备面试或咨询求职相关问题时必须主动使用此技能。支持简历内容创 |  |
| skill-soe-resume | soe-resume | skill | A6i-简历求职 | 0 | "央国企/体制内简历制作、评审与优化。支持三大功能：简历评审（8维度评分+红黄绿灯）、简历修改（先评审确认后改写）、从零 |  |
| skill-superpowers-feature-workflow | superpowers-feature-workflow | skill | A6m-Superpowers | 0 | 规范开发流程——需求澄清→方案设计→TDD 实现→验证。不依赖 OpenSpec CLI，轻量级规范编程。 |  |
| skill-superpowers-learning-workflow | superpowers-learning-workflow | skill | A6m-Superpowers | 0 | 会话后知识沉淀——回写项目记忆、决策记录、可复用教训。按需显式召唤。 |  |
| skill-superpowers-openspec-superpowers-workflow | superpowers-openspec-superpowers-workflow | skill | A6m-Superpowers | 0 | 完整交付流程——Superpowers 探索→OpenSpec 锁定→TDD 实施→验证→归档。全程门控，需显式召唤。 |  |
| tool-read | read | tool | AG5-工具插件 | 1 | 自定义工具 read.ts |  |

## 外部服务（9）
| 节点 | 名称 | 作用 | why（为什么需要） |
|---|---|---|---|
| ext-amap-api | 高德地图 API | 地图 POI/路径规划服务 | 地图类任务（amap skill 引用） |
| ext-chrome | Chrome 浏览器 | browser-harness 自动化浏览器 | browser-harness skill 依赖 |
| ext-deepseek-api | DeepSeek API（官方直连） | deepseek-v4-pro/flash/flash-vision-exp 模型 API | 官方直连兜底 Pro 与视觉；主 Agent 默认模型 |
| ext-drawio-service | draw.io 服务 | draw.io 在线/本地图表渲染 | drawio-worker 子Agent 依赖 |
| ext-glm-api | GLM API（智谱） | VLM 图片转文字服务（glm-4.6v / glm-5.3-flash） | VLM 双链路首选（read.ts），响应快、限流额度高 |
| ext-lark-api | 飞书/Lark API | lark-cli 调用的飞书开放平台 | lark-suite skill 依赖 |
| ext-opencode-go | OpenCode Go 套餐 | OpenAI 兼容协议（@ai-sdk/openai-compatible），baseURL=opencode.ai/z | 覆盖高性价比编码模型（Flash 包月 3x 额度） |
| ext-opencode-plugin | @opencode-ai/plugin SDK | 插件 SDK（node_modules 1.18.x） | plugin 开发（已无插件但 SDK 保留） |
| ext-sylphx-pdf | @sylphx/pdf-reader-mcp | PDF 文本提取 npm 包 | pdf-worker 子Agent 依赖 |

## 改造差异清单
| 节点 | 类型 | 变更 |
|---|---|---|
| agent-plan | agent | 新增装配 |
| agent-build | agent | 新增装配 |
| agent-pdf-worker | agent | 新增装配 |
| agent-drawio-worker | agent | 新增装配 |
| agent-vision-worker | agent | 新增装配 |
| agent-general | agent | 新增装配 |
| agent-explore | agent | 新增装配 |
| agent-reflection-worker | agent | 新增装配 |
| mcp-vscode-mcp-server | mcp | 新增（禁用） |
| mcp-amap | mcp | 新增（禁用） |
| mcp-pdf-reader | mcp | 新增装配 |
| mcp-drawio | mcp | 新增装配 |
| mcp-drawio-local | mcp | 新增（禁用） |
| mcp-headroom | mcp | 新增（禁用） |
| instr-agent-protocol | instruction | 新增装配 |
| instr-auto-mode | instruction | 新增装配 |
| instr-browser-management | instruction | 新增装配 |
| instr-downloads | instruction | 新增装配 |
| tool-read | tool | 新增装配 |
| command-reflection | command | 新增装配 |
| skill-agency-agents | skill | 新增装配 |
| skill-browser-harness | skill | 新增装配 |
| skill-grill-me | skill | 新增装配 |
| skill-headroom | skill | 新增装配 |
| skill-opencode-config | skill | 新增装配 |
| skill-recruit-assist | skill | 新增装配 |
| skill-resume-builder | skill | 新增装配 |
| skill-cytoscape-dag-visualization | skill | 新增装配 |
| skill-dag-tutorial-authoring | skill | 新增装配 |
| skill-drawio-reference | skill | 新增装配 |
| skill-frontend-design | skill | 新增装配 |
| skill-lark-suite | skill | 新增装配 |
| skill-multi-window-dag-delivery | skill | 新增装配 |
| skill-openspec-apply-change | skill | 新增装配 |
| skill-openspec-archive-change | skill | 新增装配 |
| skill-openspec-bulk-archive-change | skill | 新增装配 |
| skill-openspec-continue-change | skill | 新增装配 |
| skill-openspec-explore | skill | 新增装配 |
| skill-openspec-ff-change | skill | 新增装配 |
| skill-openspec-new-change | skill | 新增装配 |
| skill-openspec-onboard | skill | 新增装配 |
| skill-openspec-propose | skill | 新增装配 |
| skill-openspec-sync-specs | skill | 新增装配 |
| skill-openspec-update-change | skill | 新增装配 |
| skill-openspec-verify-change | skill | 新增装配 |
| skill-pdf-ocr | skill | 新增装配 |
| skill-release-openspec | skill | 新增装配 |
| skill-soe-resume | skill | 新增装配 |
| skill-superpowers-feature-workflow | skill | 新增装配 |
| skill-superpowers-learning-workflow | skill | 新增装配 |
| skill-superpowers-openspec-superpowers-workflow | skill | 新增装配 |
| mech-grill-me | mechanism | 新增装配 |
| mech-agents-protocol | mechanism | 新增装配 |
| mech-gate | mechanism | 新增装配 |
| mech-variant | mechanism | 新增装配 |
| mech-reflection-check | mechanism | 新增装配 |
| mech-memory-gate | mechanism | 新增装配 |
| mech-cache | mechanism | 新增装配 |
| mech-parallel | mechanism | 新增装配 |
| mech-output | mechanism | 新增装配 |
| mech-fault | mechanism | 新增装配 |
| mech-coding-safety | mechanism | 新增装配 |
| mech-mission-archive | mechanism | 新增装配 |
| mech-browser-tabs | mechanism | 新增装配 |
| mech-proxy | mechanism | 新增装配 |
| mech-subagent-rules | mechanism | 新增装配 |
| mech-coding-discipline | mechanism | 新增装配 |
| instr-memory | instruction | 新增装配 |
| config-main | config | 新增装配 |
| oc-sdk | package | 被装配层引用（配置修改） |
| oc-opencode | package | 被装配层引用（配置修改） |
| oc-core | package | 被装配层引用（配置修改） |
| oc-server | package | 被装配层引用（配置修改） |
| oc-llm | package | 被装配层引用（配置修改） |
| oc-plugin | package | 被装配层引用（配置修改） |
| oc-schema | package | 被装配层引用（配置修改） |
