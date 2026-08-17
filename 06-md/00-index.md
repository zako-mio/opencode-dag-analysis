# opencode DAG 分析 — AI 检索镜像

三图：官方包级 / 对比 / 改造双层。共 104 节点。

## 官方包（35）
| 节点 | 名称 | 组 | 层 | 作用 |
|---|---|---|---|---|
| oc-app | app | G10-应用 | 4 | OpenCode 桌面/Web 前端的 SolidJS 主应用。src/app.tsx 组装全部 Provider（Server/SDK/ServerSync/ |
| oc-cli | cli | G10-应用 | 4 | OpenCode 2.0 CLI 入口（bin: lildax）。src/index.ts:10-32 用 Effect 构建命令运行时：Runtime.han |
| oc-client | client | G3-客户端 | 2 | 面向 Web/桌面的客户端库。src/contract.ts:1-17 复用 protocol 的 makeDefaultApi 定义 ClientApi 与  |
| oc-codemode | codemode | G12-沙箱 | 0 | Code Mode 沙箱：基于 schema 描述的受限代码执行（package.json:5 描述）。src/interpreter/runtime.ts:1 |
| oc-console-app | console-app | G16-Console | 2 | Console 主站前端（SolidStart/SSR + Nitro on Cloudflare），包含营销落地页、认证回调、workspace 管理（bil |
| oc-console-core | console-core | G16-Console | 1 | Console 后端领域层：基于 drizzle-orm + PlanetScale 的数据库访问、Actor 权限上下文、以及 Account/User/Wo |
| oc-console-function | console-function | G16-Console | 2 | Cloudflare Workers 端边函数集：auth.ts 是 OpenAuth issuer（GitHub/Google 登录 + Cloudflare |
| oc-console-mail | console-mail | G16-Console | 0 | 邮件模板包：无 src/，全部为 emails/ 下的 jsx-email 模板与共享组件/样式。emails/templates/InviteEmail.ts |
| oc-console-resource | console-resource | G16-Console | 0 | SST 资源访问抽象层，无 src/ 目录（文件在包根）。通过 Proxy 按运行环境暴露 Resource：resource.cloudflare.ts 在  |
| oc-console-support | console-support | G16-Console | 2 | 面向支持/客服的内部工具站（SolidStart SSR）。核心功能是用户数据 lookup：src/lib/lookup.ts 按 wrk_/key_/sk- |
| oc-core | core | G6-核心服务 | 2 | 核心服务层（无根 index.ts，按子路径导出，package.json:18-23 暴露 effect/layer-node、session/runner  |
| oc-desktop | desktop | G10-应用 | 5 | Electron 桌面壳。src/main/index.ts:15-51 聚合应用生命周期：spawnLocalServer 拉起本地 sidecar 服务、r |
| oc-effect-drizzle-sqlite | effect-drizzle-sqlite | G15-存储适配 | 0 | Drizzle ORM 的 Effect 适配层。src/effect-sqlite/driver.ts:15-60 定义 EffectSQLiteDataba |
| oc-effect-sqlite-node | effect-sqlite-node | G15-存储适配 | 0 | 基于 Node 内置 node:sqlite 的 Effect SqlClient 实现。src/index.ts:49-161 make() 用 Databa |
| oc-enterprise | enterprise | G10-应用 | 4 | 基于 SolidStart 的企业版/云端分享服务。src/app.tsx:1-14 用 @opencode-ai/ui 的 Provider（Marked/D |
| oc-function | function | G13-边缘服务 | 0 | Cloudflare Workers 上的会话分享同步服务。src/api.ts:15-114 定义 SyncServer Durable Object：Web |
| oc-http-recorder | http-recorder | G14-工具 | 0 | HTTP 录制/回放工具（package.json:5 描述：Record and replay Effect HTTP client traffic with |
| oc-llm | llm | G5-LLM请求层 | 1 | LLM 请求/协议层。src/index.ts:1-28 导出 LLMClient/Auth/Provider/Tool/ToolRuntime；核心 LLM  |
| oc-opencode | opencode | G19-主入口 | 4 | 主应用/CLI 入口。src/index.ts:45 用 yargs 装配 run/serve/tui/agent/acp 等全部子命令；src/cli/tui |
| oc-plugin | plugin | G7-插件SDK | 1 | 插件 SDK。src/index.ts:20-80 定义 Plugin/PluginInput/Config/Hooks 等公共类型，基于 @opencode- |
| oc-protocol | protocol | G2-通信协议 | 1 | 通信协议层。src/api.ts:26-86 用 effect/unstable/httpapi 定义 OpenCode HttpApi 结构：注册 Healt |
| oc-schema | schema | G1-数据模型 | 0 | 纯类型/数据模型包，仅依赖 effect（package.json:14-16）。以 Effect Schema 定义全部领域类型：Session/Sessio |
| oc-script | script | G14-工具 | 0 | 构建/发布脚本共享工具包。src/index.ts:5-76 读取仓库根 package.json 校验 bun 版本（semver.satisfies 检查， |
| oc-sdk | sdk | G3-客户端 | 0 | 官方 JS 客户端 SDK（packages/sdk/js/）。src/index.ts:1-21 导出 client/server 并通过 createOpe |
| oc-sdk-next | sdk-next | G3-客户端 | 4 | Effect 原生的进程内 OpenCode host SDK（过渡包，替代生成式 @opencode-ai/sdk）。src/opencode.ts 的 cr |
| oc-server | server | G4-服务端 | 3 | HTTP/SSE 服务器实现层。src/api.ts:5-8 用 @opencode-ai/protocol/api 的 makeDefaultApi 装配 H |
| oc-session-ui | session-ui | G9-UI组件 | 3 | 会话级 UI 组件集，介于基础组件库与完整应用之间。src/components/ 提供 SessionTurn、SessionReview、MessagePa |
| oc-slack | slack | G18-集成 | 1 | Slack 机器人集成（@slack/bolt Socket Mode）。src/index.ts 创建 opencode 服务端实例（createOpenco |
| oc-stats-app | stats-app | G17-Stats | 1 | OpenCode Stats 公共数据站点（SolidStart，Cloudflare preset，app.config.ts:1）。首页通过 @openco |
| oc-stats-core | stats-core | G17-Stats | 0 | Stats 后端核心（Effect + drizzle + PlanetScale）。src/athena.ts 封装 AWS Athena 查询服务（Star |
| oc-stats-server | stats-server | G17-Stats | 1 | Stats 后端 Node HTTP 服务（Effect HttpRouter + Bun，Dockerfile 部署）。src/server.ts 用 Nod |
| oc-storybook | storybook | G11-文档站点 | 4 | UI 组件开发文档站。.storybook/main.ts:13-29 用 storybook-solidjs-vite 定义框架并聚合 ui/session- |
| oc-tui | tui | G8-终端UI | 3 | 终端 UI 应用。src/index.tsx:1 导出 run/TuiInput；src/app.tsx:1-50 用 @opentui/solid 渲染整棵组 |
| oc-ui | ui | G9-UI组件 | 0 | SolidJS UI 组件库。src/components/ 含 50+ 基础组件（button/avatar/dialog/context-menu/diff |
| oc-web | web | G11-文档站点 | 0 | 基于 Astro + Starlight 的文档与分享站点。src/pages/s/[id].astro:2-8 渲染会话分享页（Share.tsx 消费 op |

## 装配层（61）
| 节点 | 名称 | 类型 | 组 | 层 | 作用 | why（需求驱动） |
|---|---|---|---|---|---|---|
| agent-build | build | agent | A1-Agents | 6 | 执行者主 Agent，variant=daily，model=deepseek-v4-flash（注释：执行逻辑足够，省 | 执行者用 Flash 降本（注释：执行者，调度逻辑足够）；承载 /reflection 原生命令宿主（frontmatt |
| agent-drawio-worker | drawio-worker | agent | A1-Agents | 2 | 图表专家子Agent（mode=subagent, hidden=true），model=deepseek-v4-fla | 固定 Flash（图表生成无需 Pro 推理）；permission 仅放行 drawio_*（L3 最小权限）；刻意不 |
| agent-explore | explore | agent | A1-Agents | 1 | 探索子Agent，model=deepseek-v4-flash，无 description/无专用 permissio | Flash 模型；无 description/无专用 permission（纯只读定位：glob/grep/read）； |
| agent-general | general | agent | A1-Agents | 0 | 通用子Agent，model=deepseek-v4-flash，无 description/无专用 permissio | Flash 模型；无 description/无专用 permission（继承全局 deny + external_d |
| agent-pdf-worker | pdf-worker | agent | A1-Agents | 0 | PDF 专家子Agent（mode=subagent, hidden=true），model=deepseek-v4-f | 固定 Flash（PDF 提取无需 Pro 推理）；mode=subagent + hidden=true；L3 最小权 |
| agent-plan | plan | agent | A1-Agents | 6 | 主 Agent（调度者角色，非执行者），variant=daily，无显式 model 字段 → 回落顶层 model  | 调度者角色固定：plan=Pro（0813 回滚，规划/委派调度需 Pro 推理质量）、build=Flash（执行者降 |
| agent-reflection-worker | reflection-worker | agent | A1-Agents | 0 | 自我进化系统反思子Agent（mode=subagent, hidden=true），model=deepseek-v4 | 固定 Flash（反思分析无需 Pro 推理）；bash 全 deny（仅文件读写，L3 收紧，工具白名单设计偏保守）； |
| command-reflection | reflection | command | A4-命令指令 | 0 | /reflection 原生命令（frontmatter：description + agent=build），命令体自 | 命令体自包含（不依赖其他文档）；frontmatter description + agent: build；三处预设文 |
| config-main | main | config | A5-配置本体 | 1 | 核心配置本体。①模型路由：model=deepseek/deepseek-v4-pro（attachment+reaso | 三层纵深防御权限（L1 全局 deny：MCP 全 deny + python -c/rm -rf/git push d |
| instr-auto-mode | auto-mode | instruction | A4-命令指令 | 5 | 全局共享前缀协议（Cache-Stable，所有 Agent 加载，session 内字节稳定以维持 DeepSeek  | 所有 Agent（主+子）的共享前缀协议（cache-stable，不可修改前缀字节否则缓存全毁）；GATE 强制门控（ |
| instr-memory | memory | instruction | A4-命令指令 | 5 | 项目记忆索引（§-分段格式，上限 ~3500 字符），作为第二份 instructions 加载。记录的改造决策/经验： | 全局共享版（~/.config/opencode/，workspace 根可建项目版共存）；放在 auto-mode.m |
| mcp-amap | amap | mcp | A2-MCP | 4 | 本地 MCP，经 powershell amap-mcp-wrapper.ps1 启动。已禁用（enabled=fals | enabled=false；description'【已禁用】12 个工具 ~2000 tokens 极低频'（0813 |
| mcp-drawio | drawio | mcp | A2-MCP | 0 | 本地 MCP，命令 node D:\Opencode\drawio-mcp-minimal\package\src\in | enabled=true；description'【启用】draw.io 图表创建（本地精简版 v1.5.0）。仅 dr |
| mcp-drawio-local | drawio-local | mcp | A2-MCP | 0 | 本地 MCP，与主 drawio 同一实例（同 index.js），但注入环境变量 DRAWIO_BASE_URL=ht | enabled=false；description'【禁用·离线兜底】断网时启用，与主 drawio 同一实例'（081 |
| mcp-headroom | headroom | mcp | A2-MCP | 0 | 本地 MCP，经 powershell headroom-mcp-launcher.ps1 启动。已禁用（enabled | enabled=false（2026-08-12 量化亏损：工具开销 > 收益）；CLI 仍可用（headroom pr |
| mcp-pdf-reader | pdf-reader | mcp | A2-MCP | 0 | 本地 MCP，命令 npx -y @sylphx/pdf-reader-mcp@latest。已启用（enabled=t | enabled=true；description'【启用】PDF 文本提取。仅 pdf-worker 子Agent 使用 |
| mcp-vscode-mcp-server | vscode-mcp-server | mcp | A2-MCP | 4 | 本地 MCP，经 powershell -ExecutionPolicy Bypass -File vscode-mcp | enabled=false（0802 审计后禁用）；description 注明'【已禁用】仅 6 个工具(~692 t |
| plugin-vision-interceptor | vision-interceptor | plugin | A3-插件工具 | 6 | opencode 插件，export server(ctx)，挂两个钩子：①chat.message——用户消息到达时把 | 保留双钩子：chat.message（日志 + 首次处理）+ experimental.chat.messages.tr |
| skill-agency-agents | agency-agents | skill | A6f-角色调度 | 5 | 专业 AI 角色调度系统：任务复杂/专业时激活，覆盖工程、设计、营销、安全、测试、GIS、游戏开发等 16 个部门 26 | 专业任务委派前的角色路由入口：判断任务是否需要专家角色、搜索匹配、加载角色 prompt 作为 System Promp |
| skill-agent-reflection | agent-reflection | skill | A6m-自进化 | 6 | Agent 自进化系统：Plan+Build 周期后异步反思，提炼经验写入 Memory（MEMORY.md）或创建新  | 是全部 Reflection skills 的母系统：每个 Plan+Build 周期结束自动触发反思沉淀，维持"系统越 |
| skill-amap-budget-control | amap-budget-control | skill | A6k-地图 | 5 | 高德地图调用预算控制技能：严格管控 API 调用次数，记录用量到 amap-usage.json，接近 5000 次/天 | amap MCP 已禁用（enabled=false，精兵策略：12 工具约 2000 tokens 极低频），本 sk |
| skill-amap-jsapi-skill | amap-jsapi-skill | skill | A6k-地图 | 1 | 高德地图 JSAPI v2.0 (WebGL) 前端开发技能，用于编写/调试地图前端 JS 代码。涵盖地图生命周期、安全 | amap MCP 已禁用后随 _SKILL.md 命名存档/休眠（0815 桥接 opencode-skill-inde |
| skill-amap-lbs-skill | amap-lbs-skill | skill | A6k-地图 | 0 | 高德地图综合服务：POI 搜索、路径规划、旅游规划、周边搜索、热力图数据可视化。生成免费的高德网页链接（不消耗 API  | amap MCP 已禁用后随 _SKILL.md 命名存档/休眠。保留价值：地图场景的零成本入口——简单搜索/导航/周边 |
| skill-browser-harness | browser-harness | skill | A6h-浏览器 | 0 | 统一浏览器交互入口（自动化/爬取/测试/站点应用工作）。通过 CDP 直接控制浏览器：browser-harness d | recruit-assist 投递核心依赖（browser-harness CDP 自动化投递，exec-recruit |
| skill-cdisk-space-optimization | cdisk-space-optimization | skill | A6n-系统优化 | 0 | Windows C 盘空间优化方法论：先实测（注册表/磁盘）再动手，junction 软链接零风险迁移开发缓存，还原点等 | Windows C 盘空间不足的标准处理流程：空间盘点→社交数据实测（注册表）→开发缓存 junction 搬迁→系统清 |
| skill-cytoscape-dag-visualization | cytoscape-dag-visualization | skill | A6m-自进化 | 5 | cytoscape.js 交互 DAG 可视化构建：单页组级+下钻总览与批量 HTML 页源码级动态 DAG 插入。含  | cytoscape.js 交互 DAG 可视化构建的标准方法论：单页交互总览（组级+下钻）+ 批量 HTML 页源码级动 |
| skill-dag-tutorial-authoring | dag-tutorial-authoring | skill | A6m-自进化 | 4 | DAG 教程编写方法论（零基础读者导向）：调研驱动编写（4 路并行交叉验证）、可读性规律编码为门控、统一 schema  | 面向零基础读者的概念/技能 DAG 教程编写标准方法论：调研先行→可读性规律编码为门控→统一 schema 并行写节点→ |
| skill-drawio-reference | drawio-reference | skill | A6a-图表 | 1 | draw.io 图表完整参考文档，包含 XML schema 样式库、Mermaid.js 全语法参考（28 种图表类型 | 主Agent 委派 drawio-worker 生成复杂图表（嵌套容器/泳道/自定义样式/15+ 节点）时仍必须精确写入 |
| skill-frontend-design | frontend-design | skill | A6b-前端设计 | 0 | 前端设计双引擎系统：数据引擎（192 色板/74 字体/84 风格数据库）先推荐 Top K 候选设计系统，再由设计主管 | 所有前端/网页/UI 设计任务的持续入口：新建页面/组件、UI 重构、设计审查、配色/字体选型、landing page |
| skill-github-bulk-upload | github-bulk-upload | skill | A6m-自进化 | 0 | GitHub 大仓库全量上传方法论：处理嵌套 .git 被识别为 gitlink、大文件推送 schannel 中断（p | 大型交付物/源码克隆（100+MB/数千文件）上传 GitHub 的标准流程：预检（README/LICENSE/敏感扫 |
| skill-grill-me | grill-me | skill | A6f-角色调度 | 7 | 对用户的计划/设计进行持续质询直到达成共享理解，逐分支解析决策树。用 question 工具一次一问（2-4 个多选选项 | Plan 模式决策收敛的核心协议：0817-opencode-dag 收敛 13 项决策、0817-github-dag |
| skill-headroom | headroom | skill | A6i-上下文压缩 | 0 | Headroom 上下文压缩层（CLI 版）。支持 proxy/audit-reads/savings/inspect/ | CLI 版持续可用：headroom proxy / audit-reads / savings / inspect / |
| skill-large-scale-source-parse | large-scale-source-parse | skill | A6m-自进化 | 3 | 大规模源码库静态解析方法论：主Agent 只做调度/聚合/裁决，explore 子Agent 并行解析，三源交叉验证，分 | 大型开源项目源码架构解析的标准流程（数百至数万文件）：浅 clone 快照 + 层级骨架先行 + 三源交叉 + 并行解析 |
| skill-lark-suite | lark-suite | skill | A6c-办公集成 | 0 | 飞书/Lark 全功能操作入口，通过已安装的 lark-cli v1.0.76 命令操作飞书全部业务域（日历、消息、文档 | recruit-assist 的飞书网申进度表同步（sync_feishu.py 增量上传/全量下载）依赖 lark-c |
| skill-minimax-docx | minimax-docx | skill | A6c-办公集成 | 0 | 基于 OpenXML SDK (.NET) 的专业 DOCX 文档创建、编辑与格式化技能，三管线：从零创建新文档、填充/ | 所有 Word 文档交付的骨干引擎：0811 英文简历制作（A4/Calibri/17pt 深蓝居中/54 段，busi |
| skill-minimax-xlsx | minimax-xlsx | skill | A6c-办公集成 | 0 | 打开/创建/读取/分析/编辑/验证 Excel 电子表格（.xlsx/.xlsm/.csv/.tsv）。覆盖从零创建 x | 简历投递跟踪表读写（recruit-assist 的 tracker_writer.py 调用其 XML 解包-编辑-打 |
| skill-multi-window-dag-delivery | multi-window-dag-delivery | skill | A6m-自进化 | 6 | 多层窗口接力 DAG 依赖链分析与交付：大型插件库拆窗口接力，每窗口完整执行（采集→建模→注入→生成→门控）并落盘 PL | 大型源码/插件库（数百包）DAG 依赖链分析的标准方法论：单窗口无法完成时拆窗口接力，每窗口可独立执行、交付物同目录累计 |
| skill-opencode-config | opencode-config | skill | A6j-配置知识 | 5 | OpenCode 配置（opencode.jsonc）分级知识库：覆盖官方 Schema v2 全量字段、本项目实际配置 | 任何查看/修改/编写/验证 opencode.jsonc 的操作入口：三阶自检路由按需加载子文件（不一次加载全部）。08 |
| skill-openspec-apply-change | openspec-apply-change | skill | A6l-工作流 | 1 | 执行 OpenSpec 变更中 tasks.md 的实现任务，逐条完成并打勾。通过 openspec status 与  | 所有 OpenSpec 变更的实施环节（specs 锁定后进入编码）；与 propose/ff 配对构成完整闭环；本地装 |
| skill-openspec-archive-change | openspec-archive-change | skill | A6l-工作流 | 1 | 归档已完成的变更：将 delta spec 合并到主 spec 并移动到 archive。先加载 archive 指令上 | 每个 OpenSpec 变更生命周期的收尾；归档时智能合并 delta 到主 spec（agent 驱动读 delta  |
| skill-openspec-bulk-archive-change | openspec-bulk-archive-change | skill | A6l-工作流 | 1 | 单次批量归档多个已完成变更，智能处理 spec 冲突——通过检查代码库判断实际实现。逐变更收集工件状态、任务完成度与 d | 累积多个已完成变更需要批量收尾时；本地多线程/多窗口任务（如 DAG 多窗口交付）产生多个并行变更，批量归档是配套收尾能 |
| skill-openspec-continue-change | openspec-continue-change | skill | A6l-工作流 | 0 | 继续已有变更，按 DAG 依赖顺序生成下一个未完成工件。解析状态判断 ready/blocked，获取 instruct | 本地任务跨会话/被中断频繁（如多阶段 DAG 交付、长任务 checkpoint），continue-change 是恢 |
| skill-openspec-explore | openspec-explore | skill | A6l-工作流 | 0 | 探索模式立场：分析代码、理清需求、比较方案，不写代码。自由提问与 ASCII 可视化，可创建 proposal/desi | 所有 OpenSpec 变更的思考前置：分析代码、理清需求、比较方案、可视化权衡。当前 DAG 化改造（0817-ope |
| skill-openspec-ff-change | openspec-ff-change | skill | A6l-工作流 | 2 | 快速通道一键生成所有 OpenSpec 工件，跳过逐步交互。按 requires 依赖边传递闭包确定必建工件集合（app | 简单变更或用户有经验时的默认快速路径；本地 DAG 化任务中作为快速建模入口，减少交互轮次。 |
| skill-openspec-new-change | openspec-new-change | skill | A6l-工作流 | 1 | 逐步交互式创建新变更，比 propose 更细粒度。仅创建变更目录并展示第一个工件模板后停止，等待用户方向，适合复杂或需 | 复杂变更需要逐步确认每个工件时使用；本地改造强调 Grill-Me 逐项决策，new-change 与之同构（一步一确认 |
| skill-openspec-onboard | openspec-onboard | skill | A6l-工作流 | 2 | 引导首次用户完成完整 OpenSpec 流程的教学技能，边做边讲。预检 CLI 安装后走 welcome→选任务→建变更 | 新成员/新项目引入 OpenSpec 工作流时；教学式引导保证首次使用者理解工件 DAG 全流程（与本地"培训/教学"类 |
| skill-openspec-propose | openspec-propose | skill | A6l-工作流 | 2 | 一键生成变更提案：创建 change 并生成全部工件（proposal/specs/design/tasks）。明确知道 | 当前用于本地装配层改造（如 openspec 系列技能自身维护、DAG 交付物生成）等明确变更的提案创建；与 apply |
| skill-openspec-sync-specs | openspec-sync-specs | skill | A6l-工作流 | 0 | 将 delta spec 同步到主 spec（不归档），agent 驱动读取 delta 并智能编辑主 spec，处理  | 归档流程内部依赖（archive-change 调用）；需要独立合并 delta 不归档时显式使用；是主 spec 知识 |
| skill-openspec-update-change | openspec-update-change | skill | A6l-工作流 | 2 | 编辑/协调已有 OpenSpec 工件并保持一致性，处理手动修改后的重新同步。按请求做定向修改或一致性审查，逐工件确认后 | 工件被手动修改或需求变更需要跨工件协调时；本地改造中 SKILL.md/规格文档被人工编辑后的一致性校验，与"修改安全链 |
| skill-openspec-verify-change | openspec-verify-change | skill | A6l-工作流 | 0 | 归档前可选校验：验证实现是否匹配 spec/design/tasks。从完整性/正确性/一致性三维度生成 CRITICA | 归档前的质量闸门：验证实现与工件一致后才允许归档；当前 DAG 交付与装配层改造中的规格实现均以此为一致性校验参照。 |
| skill-pdf-ocr | pdf-ocr | skill | A6d-文档处理 | 1 | PDF OCR 识别专项，处理扫描件、图片型 PDF、含水印/印章的文档。支持中英多语言 OCR、表格区域提取、印章检测 | 扫描件/图片型 PDF/含水印印章文档的持续需求（简历评审、offer 拒绝决策、证件扫描件等）。pdf-worker  |
| skill-postmortem-failure-review | postmortem-failure-review | skill | A6m-自进化 | 1 | 失败项目复盘方法论：先区分路线错误与执行错误，五因框架分类失败，双 explore 并行探索（失败项目+参考项目），A/ | 失败/部分失败项目的系统性复盘入口：先区分路线错误与执行错误（路线错误代价高且无法修补），五因框架分类，产出 5 段式复 |
| skill-recruit-assist | recruit-assist | skill | A6e-简历求职 | 1 | 简历投递辅助：投简历（浏览器打开招聘页+记录跟踪表）、识别简历（扫描表单字段匹配信息库）、维护信息库、记录投递状态、跟踪 | 求职季投递主场景：投简历、跟踪企业、飞书同步持续使用；browser-harness（CDP 浏览器自动化）与 trac |
| skill-release-openspec | release-openspec | skill | A6l-工作流 | 0 | OpenSpec 自身发布管理技能，以可恢复状态机运行发布工作流：每次调用检查 GitHub 实时状态，只执行下一步安全 | 本机作为 OpenSpec 维护者的发布操作入口（Fission-AI/OpenSpec 仓库维护场景）；0815 桥接 |
| skill-resume-builder | resume-builder | skill | A6e-简历求职 | 0 | 简历制作助手：从零创建、ATS 优化、岗位定制（JD 关键词提取）、求职信、面试准备（STAR）与简历评分修改建议，基于 | 求职季简历创作主工具：从零创建、ATS 优化、JD 关键词定制、cover letter、STAR 面试演练持续使用（0 |
| skill-reusable-asset-inventory | reusable-asset-inventory | skill | A6m-自进化 | 0 | 从失败/遗留项目提炼可复用资产：A/B/C 三级分类（直接复用/需修改/仅思路）+优先级排序公式+参考项目对标，gap  | 项目失败或重写 v2 前抢救可复用资产的标准流程；客观评估哪些代码值得保留、哪些该丢弃；与 postmortem 配对构 |
| skill-soe-resume | soe-resume | skill | A6e-简历求职 | 0 | 央国企/体制内简历制作、评审与优化助手。三大功能：简历评审（8 维度评分 + 红黄绿灯）、简历修改（先评审确认后改写）、 | 央国企求职持续场景（国家电网/中石化等网申前必经评审）。0815 起收入 exec-recruit preset（简历投 |
| skill-superpowers-feature-workflow | superpowers-feature-workflow | skill | A6l-工作流 | 1 | 规范开发流程：需求澄清→方案设计→TDD 实现→验证。不依赖 OpenSpec CLI 的轻量级规范编程工作流。显式 o | 显式 opt-in 的规范开发流程：当用户要求纪律化功能交付（且不想要 OpenSpec 工件生成）时提供 10 步工作 |
| skill-superpowers-learning-workflow | superpowers-learning-workflow | skill | A6l-工作流 | 0 | 会话后知识沉淀工作流，回写项目记忆、决策记录与可复用教训。将学习成果分类为持久事实、当前状态、会话结果、可复用教训四类， | 显式召唤的知识沉淀工作流：项目结束/里程碑后主动回写记忆、决策记录、可复用教训，解决 AI 是金鱼（跨会话记忆缺失）的痛 |
| skill-superpowers-openspec-superpowers-workflow | superpowers-openspec-superpowers-workflow | skill | A6l-工作流 | 3 | 完整交付流程编排器：Superpowers 探索→OpenSpec 锁定→TDD 实施→验证→归档，全程门控。作为路由控 | 复杂功能交付的全流程编排器：路由控制者，防止误路由到 OpenSpec proposal skill（Guardrail |
| tool-read | read | tool | A3-插件工具 | 5 | 自定义 read 工具（TypeScript，zod 定义参数），覆盖 opencode 内置 read：①目录→列出条 | 保留图片自动分析能力（IMAGE_EXTS 9 种格式）→ GLM-4V 描述；GLM_MODELS = ['glm-4 |

## 外部服务（8）
| 节点 | 名称 | 作用 | why（为什么需要） |
|---|---|---|---|
| ext-amap-api |  | 地图 POI/路径规划服务 | 地理/LBS 能力：POI 搜索、周边搜索、路径规划、地理编码、旅游规划。解决 Agent 处理地点/路线/导航类查询需 |
| ext-chrome |  | browser-harness 自动化浏览器 | 网页交互/抓取/测试的唯一通道：browser-harness skill 要求 Always use browser- |
| ext-deepseek-api |  | deepseek-v4-pro/flash 模型 API | 主模型供给：plan=deepseek-v4-pro（规划/委派推理）、build 与全部 7 个子Agent=deep |
| ext-drawio-service |  | draw.io 在线/本地图表渲染 | 图表交付能力：流程图/架构图/UML/思维导图/组织图批量生成与 4x PNG 导出（0816-0817 三个 DAG  |
| ext-glm-api |  | VLM 图片转文字服务（glm-4.6v / glm-4.6v-flash） | 补 DeepSeek-flash 无视觉能力的短板：read.ts 工具把图片文件经 GLM-4V 转文字描述（Deep |
| ext-lark-api |  | lark-cli 调用的飞书开放平台 | 协同办公主通道：recruit-assist 的飞书网申进度表同步（sync_feishu.py 增量上传/全量下载）、 |
| ext-opencode-plugin |  | 插件 SDK（node_modules 1.18.9） | vision-interceptor.js 插件依赖 @opencode-ai/plugin SDK（node_modu |
| ext-sylphx-pdf |  | PDF 文本提取 npm 包 | PDF 文档读取能力：简历解析、财报读取、论文提取。解决 Agent 无法直接读 PDF 二进制需求；无它则所有 PDF |

## 改造差异清单
| 节点 | 类型 | 变更 |
|---|---|---|
| agent-plan | agent | 新增装配 |
| agent-build | agent | 新增装配 |
| agent-pdf-worker | agent | 新增装配 |
| agent-drawio-worker | agent | 新增装配 |
| agent-general | agent | 新增装配 |
| agent-explore | agent | 新增装配 |
| agent-reflection-worker | agent | 新增装配 |
| mcp-vscode-mcp-server | mcp | 新增装配 |
| mcp-amap | mcp | 新增装配 |
| mcp-pdf-reader | mcp | 新增装配 |
| mcp-drawio | mcp | 新增装配 |
| mcp-drawio-local | mcp | 新增装配 |
| mcp-headroom | mcp | 新增装配 |
| plugin-vision-interceptor | plugin | 新增装配 |
| tool-read | tool | 新增装配 |
| command-reflection | command | 新增装配 |
| instr-auto-mode | instruction | 新增装配 |
| instr-memory | instruction | 新增装配 |
| config-main | config | 新增装配 |
| skill-drawio-reference | skill | 新增装配 |
| skill-frontend-design | skill | 新增装配 |
| skill-lark-suite | skill | 新增装配 |
| skill-minimax-docx | skill | 新增装配 |
| skill-minimax-xlsx | skill | 新增装配 |
| skill-pdf-ocr | skill | 新增装配 |
| skill-soe-resume | skill | 新增装配 |
| skill-superpowers-feature-workflow | skill | 新增装配 |
| skill-superpowers-learning-workflow | skill | 新增装配 |
| skill-superpowers-openspec-superpowers-workflow | skill | 新增装配 |
| skill-release-openspec | skill | 新增装配 |
| skill-agency-agents | skill | 新增装配 |
| skill-amap-budget-control | skill | 新增装配 |
| skill-amap-jsapi-skill | skill | 新增装配 |
| skill-amap-lbs-skill | skill | 新增装配 |
| skill-browser-harness | skill | 新增装配 |
| skill-grill-me | skill | 新增装配 |
| skill-headroom | skill | 新增装配 |
| skill-opencode-config | skill | 新增装配 |
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
| skill-recruit-assist | skill | 新增装配 |
| skill-resume-builder | skill | 新增装配 |
| skill-agent-reflection | skill | 新增装配 |
| skill-cdisk-space-optimization | skill | 新增装配 |
| skill-cytoscape-dag-visualization | skill | 新增装配 |
| skill-dag-tutorial-authoring | skill | 新增装配 |
| skill-github-bulk-upload | skill | 新增装配 |
| skill-large-scale-source-parse | skill | 新增装配 |
| skill-multi-window-dag-delivery | skill | 新增装配 |
| skill-postmortem-failure-review | skill | 新增装配 |
| skill-reusable-asset-inventory | skill | 新增装配 |
| oc-schema | package | 被装配层引用（配置修改） |
| oc-script | package | 被装配层引用（配置修改） |
| oc-opencode | package | 被装配层引用（配置修改） |
| oc-core | package | 被装配层引用（配置修改） |
