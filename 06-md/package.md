# package 节点（36）

## oc-app — app
- 组: G10-应用 | Layer 1
- 作用: OpenCode 桌面/Web 前端的 SolidJS 主应用。src/app.tsx 组装全部 Provider（Server/SDK/ServerSync/Settings/Tabs/Command 等约 20 个 context，app.tsx:41-66）并注册 Session/Home/NewSession/Legacy 等路由；src/entry.tsx:5-11 通过 render 挂载 AppInterface 与 PlatformProvider；src/index.ts:1-30 导出 AppBaseProviders、AppInterface 及全部 context hooks（useServer/useSettings/useTabs 等）。桌面专属能力（desktop-menu.ts、updater.ts、wsl/ 目录）以子路径导出供 desktop 包复用。
- 提供: ['AppInterface 与 AppBaseProviders 根组件（SolidJS 应用壳）', 'Server/SDK/ServerSync/Tabs/Settings/Command 等全套全局 context', 'Session 会话页、Home 主页、NewSession 页、布局（新旧两套）页面', 'WSL 服务器探测/管理类型与桌面菜单、更新器（updater.ts）', 'i18n 中英双语词典与 locale 规范化（i18n/、context/language.tsx）', 'draft-store 草稿持久化与 file-picker 常量（utils/draft-store.ts:30）']
- **为什么存在（设计意图）**: 作为 UI 应用壳层，将 session-ui/ui 的无状态组件与 server/core 的业务逻辑粘合为完整应用，同时为 desktop 提供可复用的桌面子模块（菜单/更新/WSL）出口。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-cli — cli
- 组: G10-应用 | Layer 0
- 作用: OpenCode 2.0 CLI 入口（bin: lildax）。src/index.ts:10-32 用 Effect 构建命令运行时：Runtime.handlers 将 Commands 映射到懒加载 handler（api/debug/migrate/service/serve）；commands/commands.ts:6-8 用 effect CLI 声明命令树；framework/runtime.ts:58-59 执行 Command.run；services/daemon.ts 提供后台守护进程服务。命令处理依赖 @opencode-ai/core 的 AppNodeBuilder 与 @opencode-ai/server 路由（serve.ts:2-10）。
- 提供: ['opencode 命令树（api/debug/migrate/service/serve，commands.ts:9-50）', 'Effect 驱动的命令运行时与懒加载 handler（framework/runtime.ts:58）', '后台 daemon 服务管理（services/daemon.ts）', 'TUI 入口（tui.ts 导入 @opencode-ai/tui 运行）', '版本/渠道识别（bin/lildax.cjs 打包）']
- **为什么存在（设计意图）**: 作为 v2 时代的命令行入口，复用 effect CLI 生态以类型安全方式声明命令，并将实际逻辑委托给 core/server/tui 包。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-client — client
- 组: G3-客户端 | Layer 3
- 作用: 面向 Web/桌面的客户端库。src/contract.ts:1-17 复用 protocol 的 makeDefaultApi 定义 ClientApi 与 Location/SessionLocation 中间件，并声明 groupNames/endpointNames 映射（src/contract.ts:19-51）；src/index.ts:1-2 从 generated/ 导出类型化客户端；src/generated/ 与 src/generated-effect/ 由 script/build.ts 依据 contract 生成（普通 + Effect 两版），src/effect.ts:3-25 转出 schema 数据类型并保证不 import core/server（文件头注释 src/effect.ts:1-2）。
- 提供: ['客户端 Api 契约（基于 protocol 默认 Api，packages/client/src/contract.ts:14-17）', '生成的普通客户端（packages/client/src/generated/client.ts）', '生成的 Effect 客户端（packages/client/src/generated-effect/client.ts）', '类型 re-export 与错误类型（packages/client/src/effect.ts:4-25、generated/client-error.ts）', 'group/endpoint 名称映射（packages/client/src/contract.ts:19-51）']
- **为什么存在（设计意图）**: 面向 app/web 前端生成类型安全的 HTTP 客户端，并通过协议层复用服务端同款端点契约；强调不得反向依赖 core/server（src/effect.ts:1-2），保持客户端纯净。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-codemode — codemode
- 组: G12-沙箱 | Layer 1
- 作用: Code Mode 沙箱：基于 schema 描述的受限代码执行（package.json:5 描述）。src/interpreter/runtime.ts:1-3 用 acorn 解析 + typescript transpileModule 在受限解释器中执行 JS 子集，工具调用经 src/tool-runtime.ts 注入 host tools 并受 ExecutionLimits（超时/最大工具调用数/输出字节，src/codemode.ts:10-17）约束。src/openapi/ 提供从 OpenAPI spec 生成工具的运行时（src/openapi/index.ts），src/stdlib/ 提供 JS 子集标准库（string/number/date/collections 等 14 模块）。
- 提供: ['受限 JS 解释器与 AST 执行（packages/codemode/src/interpreter/runtime.ts:1）', '工具调用沙箱运行时（packages/codemode/src/tool-runtime.ts）', '执行资源限制：timeout/maxToolCalls/maxOutputBytes（packages/codemode/src/codemode.ts:10-17）', 'OpenAPI 工具生成器（packages/codemode/src/openapi/index.ts、spec.ts）', 'JS 子集标准库（packages/codemode/src/stdlib/*）', '工具 schema 编解码（packages/codemode/src/tool-schema.ts）']
- **为什么存在（设计意图）**: 为 LLM 提供可审计、受限、确定性的代码执行环境（Effect-native），并支持基于 schema 描述的工具集，避免开放 shell 的安全风险（被 opencode 的 tool/code-mode.ts 桥接使用）。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-console-app — console-app
- 组: G16-Console | Layer 0
- 作用: Console 主站前端（SolidStart/SSR + Nitro on Cloudflare），包含营销落地页、认证回调、workspace 管理（billing/keys/members/settings/usage）、Zen 与 Go 两个 LLM API 网关，以及到 docs/stats/bench 的代理路由。src/app.tsx 挂载路由与 i18n，src/routes/zen/v1/chat/completions.ts 走统一 handler 做鉴权/计费/限流后转发到上游 provider，src/lib/stats-proxy.ts 反向代理 stats.opencode.ai。
- 提供: ['营销/下载/企业页与多语言 i18n（20 语言，src/i18n/）', 'OpenAuth 认证与 session 处理（src/routes/auth/、src/context/auth.ts）', 'workspace 控制台：billing 充值、API key、成员、用量图表（src/routes/workspace/[id]/）', 'Zen 网关：OpenAI/Anthropic/Google 兼容 API + key/IP 限流 + 用量计费（src/routes/zen/）', 'Go 网关（轻量版 zen，src/routes/zen/go/）', 'Stripe webhook、honeycomb webhook、enterprise lead 提交', 'docs/stats/bench 站点反向代理（src/routes/docs/、src/routes/data/）']
- **为什么存在（设计意图）**: Console 是 opencode 的 SaaS 前端：既承担官网/营销/文档分发，也承载用户工作区管理与 Zen/Go 付费 LLM 网关，是 console-core 领域逻辑的界面与入口层。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-console-core — console-core
- 组: G16-Console | Layer 1
- 作用: Console 后端领域层：基于 drizzle-orm + PlanetScale 的数据库访问、Actor 权限上下文、以及 Account/User/Workspace/Key/Billing/Subscription/Model/Provider 等 CRUD 与计费逻辑。src/drizzle/index.ts 封装事务与上下文，src/account.ts 处理账号创建/删除（含级联清理 key、coupon、auth），src/workspace.ts 创建 workspace 并默认生成管理员与 API key，src/billing.ts 对接 Stripe 做 credits 充值。
- 提供: ['Database 封装：PlanetScale drizzle 客户端 + 事务/上下文（src/drizzle/index.ts:36）', 'Actor 权限上下文：请求用户/角色/workspace 断言（src/actor.ts）', '账号生命周期：create/remove/fromID，删除级联清理（src/account.ts:13,27）', 'workspace 创建与成员管理（src/workspace.ts:17）', 'API Key 管理与角色隔离（src/key.ts:11）', 'Stripe 计费：credits 充值/订阅/用量计费（src/billing.ts:22,29）', '模型/Provider 目录与 ZenData 模型成本定义（src/model.ts）', '订阅限额：free/lite/black 阶梯（src/subscription.ts:7）', '全量 drizzle schema SQL（src/schema/*.sql.ts，account/auth/billing/key/model/provider/referral/user/workspace/ip/benchmark）', '邀请邮件渲染（动态 import console-mail，src/user.ts:142）']
- **为什么存在（设计意图）**: 将 Console 的业务领域逻辑从 app（前端/网关）与 function（worker）中独立出来，供 app、support、function 三方复用，避免数据库 schema 与计费逻辑重复实现。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-console-function — console-function
- 组: G16-Console | Layer 0
- 作用: Cloudflare Workers 端边函数集：auth.ts 是 OpenAuth issuer（GitHub/Google 登录 + Cloudflare KV 存储，签发 account/user subject），log-processor.ts 是 tail 处理器，把 Zen/Go 网关的请求日志转发到 Honeycomb 与数据湖，stat.ts 提供 TPS 限流统计查询端点。src/auth.ts:44 用 @openauthjs/openauth 构建 OAuth issuer，src/log-processor.ts:5 解析 _metric: 前缀日志聚合指标。
- 提供: ['OAuth 登录 issuer：GitHub/Google provider + Cloudflare KV 会话存储（src/auth.ts:44）', 'Subjects 定义：account/user 两级认证主体（src/auth.ts:25）', '网关日志采集：tail 事件 → Honeycomb batch + lake ingest（src/log-processor.ts:5）', 'TPS 限流统计查询：按模型 id 聚合 30 分钟窗口 qualify/unqualify（src/stat.ts:7）']
- **为什么存在（设计意图）**: 独立于 app 的 Cloudflare Workers 入口：认证服务与日志/统计边函数需要各自独立的 worker 部署，无法打进 Console 主应用。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-console-mail — console-mail
- 组: G16-Console | Layer 2
- 作用: 邮件模板包：无 src/，全部为 emails/ 下的 jsx-email 模板与共享组件/样式。emails/templates/InviteEmail.tsx 是唯一业务模板（workspace 邀请邮件），被 console-core 的 User 邀请逻辑动态 import 渲染（console/core/src/user.ts:142）。包 exports 映射到 ./emails/templates/*，纯前端渲染无服务逻辑。
- 提供: ['InviteEmail 邀请邮件模板（React/jsx-email，emails/templates/InviteEmail.tsx:26）', '共享邮件组件与内联样式（emails/components.tsx、emails/styles.ts）', '静态邮件资源：字体 woff2/logo/箭头图（emails/templates/static/）', '本地预览命令（email preview emails/templates）']
- **为什么存在（设计意图）**: 将邮件模板与业务代码解耦，供 console-core 按需动态 import（避免 React 依赖进入 core 主包），同时独立可预览开发。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-console-resource — console-resource
- 组: G16-Console | Layer 2
- 作用: SST 资源访问抽象层，无 src/ 目录（文件在包根）。通过 Proxy 按运行环境暴露 Resource：resource.cloudflare.ts 在 Worker 内从 env.SST_RESOURCE_* 读取链接资源，resource.node.ts 在 Node 下回退到 sst 包并对 KV/Bucket 提供客户端实现。src/… 实际为 resource.cloudflare.ts:4 与 resource.node.ts:9 两个入口，按 exports production/import 条件切换。
- 提供: ['统一 Resource 代理：读取 SST 链接的 secrets/KV/数据库配置（resource.cloudflare.ts:4）', 'Node 环境回退：KV get/put/delete/list、Bucket no-op、Cloudflare API 客户端（resource.node.ts:9）', '条件导出：Cloudflare 与 Node 运行时的资源读取差异屏蔽（package.json exports）']
- **为什么存在（设计意图）**: 让 app/core/function 在 Cloudflare Worker 与本地 Node 两种环境共享同一套资源访问代码，隐藏 SST 环境差异。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-console-support — console-support
- 组: G16-Console | Layer 0
- 作用: 面向支持/客服的内部工具站（SolidStart SSR）。核心功能是用户数据 lookup：src/lib/lookup.ts 按 wrk_/key_/sk-/email 标识查询 workspace、billing、usage、订阅与禁用模型等全量数据，src/routes/lookup.tsx 展示查询结果，src/routes/index.tsx 提供查询表单。全部逻辑直接复用 console-core 的 schema 与 domain。
- 提供: ['按 email/workspace id/API key 查询用户全量数据（src/lib/lookup.ts:41）', 'workspace 详情：users/billing/go/payments/usage/disabledModels 分节（src/lib/lookup.ts:30）', '查询表单与结果展示页面（src/routes/index.tsx、src/routes/lookup.tsx）', '复用 console-core 数据库 schema 与 Black/Lite/Subscription 领域逻辑']
- **为什么存在（设计意图）**: 为内部客服提供只读审计工具，复用 console-core 数据层，避免暴露在生产 Console 前端中。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-core — core
- 组: G6-核心服务 | Layer 3
- 作用: 核心服务层（无根 index.ts，按子路径导出，package.json:18-23 暴露 effect/layer-node、session/runner 等）。实现数据库（src/database/sqlite.ts，drizzle ORM）、会话执行（src/session/runner/index.ts:20-28 从已记录历史执行一次续跑）、配置解析（src/config/* 覆盖 agent/command/mcp/lsp/formatter）、权限策略（src/permission.ts）、事件流（src/event.ts，基于 PubSub/Queue）、文件系统与搜索（src/filesystem/*，含 ripgrep 封装 src/ripgrep.ts:5）。Effect 运行时层见 src/effect/layer-node.ts 与 app-node-builder.ts。
- 提供: ['SQLite 持久化：drizzle schema/迁移（packages/core/src/database/sqlite.ts、migration.ts）', 'Session 执行引擎（packages/core/src/session/runner/index.ts:19-28）', '配置系统：agent/command/mcp/lsp/formatter/plugin 解析（packages/core/src/config/*）', '权限与策略引擎（packages/core/src/permission.ts:5、policy.ts）', '事件总线与持久化事件（packages/core/src/event.ts:3）', '文件系统/ripgrep 搜索/文件监听（packages/core/src/filesystem/*、ripgrep.ts）', 'Effect 服务层组装（packages/core/src/effect/layer-node.ts、app-node-builder.ts）', 'Provider/Model/Catalog/集成认证 领域服务（packages/core/src/provider.ts、catalog.ts、integration.ts）']
- **为什么存在（设计意图）**: 把会话/存储/配置/权限等可复用领域逻辑从 CLI 与 HTTP 层抽离为纯 Effect 服务，供 opencode 主程序、server 包及测试直接注入依赖，实现平台无关的核心（bun/node 双实现见 package.json imports 的 #sqlite/#pty/#fff）。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-desktop — desktop
- 组: G10-应用 | Layer 0
- 作用: Electron 桌面壳。src/main/index.ts:15-51 聚合应用生命周期：spawnLocalServer 拉起本地 sidecar 服务、registerIpcHandlers 注册 IPC、createMenu 构建原生菜单、setupAutoUpdater 自动更新、WSL sidecar 管理（wsl/servers.ts）、migrate 数据迁移与 store 清理；src/preload 暴露安全的桥接 API；src/renderer 复用 @opencode-ai/app 渲染 Web UI（renderer/cli.ts:7 通过 window.api.installCli 安装 CLI）。
- 提供: ['Electron 主进程：窗口/菜单/托盘/深链（main/windows.ts、main/menu.ts）', '本地 sidecar server 生命周期管理（main/server.ts spawnLocalServer）', 'IPC 桥与 preload 安全 API（preload/index.ts）', '自动更新（main/updater.ts + electron-updater）', 'WSL 发行版内服务器编排（wsl/）', '背景 CLI 与原生翻译注入（background-cli.ts、native-translations.ts）']
- **为什么存在（设计意图）**: 为 Web UI 提供原生桌面能力（本地服务托管/更新/菜单/WSL），是独立于 @opencode-ai/app 的 Electron 分发层。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-effect-drizzle-sqlite — effect-drizzle-sqlite
- 组: G15-存储适配 | Layer 4
- 作用: Drizzle ORM 的 Effect 适配层。src/effect-sqlite/driver.ts:15-60 定义 EffectSQLiteDatabase 与 make()，通过 drizzle 的 SQLiteAsyncDialect + EffectSQLiteSession 把 Drizzle 查询桥接到任意 Effect SqlClient（注释明示可配 @effect/sql-sqlite-node/bun，driver.ts:30-46）；session.ts:35-49 实现 prepareQuery 与 Effect 化事务会话；sqlite-core/effect/ 提供 select/insert/update/delete/raw/count 全套 Effect 化查询构建器；migrator.ts 提供迁移执行。
- 提供: ['EffectSQLiteDatabase 工厂（make()，driver.ts:49）', 'Drizzle↔Effect 会话桥接（EffectSQLiteSession，session.ts:35）', 'sqlite-core 全套 Effect 查询构建器（sqlite-core/effect/ 10 个文件）', '迁移执行器（effect-sqlite/migrator.ts）', 'EffectCache/EffectLogger 默认 Layer（driver.ts:28）']
- **为什么存在（设计意图）**: 让 Drizzle 类型安全的 schema 查询能在 Effect 生态（SqlClient/Stream/Layer）中运行，供核心存储层使用且依赖可注入、可测试。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-effect-sqlite-node — effect-sqlite-node
- 组: G15-存储适配 | Layer 4
- 作用: 基于 Node 内置 node:sqlite 的 Effect SqlClient 实现。src/index.ts:49-161 make() 用 DatabaseSync 建立同步连接（WAL 模式、外键约束，index.ts:59-70）、实现 execute/executeRaw/executeValues/executeUnprepared 全套 SqlClient 接口并挂载 Semaphore(1) 串行化（index.ts:132-134）；classifySqliteError 做错误归类（index.ts:15,80-82）；layer() 将 client 同时注册为 SqliteClient 与泛型 Client.SqlClient（index.ts:163-168），并注入 Reactivity.layer。
- 提供: ['Effect SqlClient 的 SQLite 实现（node:sqlite DatabaseSync）', 'WAL/外键/只读/扩展加载等连接配置（SqliteClientConfig，index.ts:32-43）', 'Layer 装配（SqliteClient + Client.SqlClient 双注册，index.ts:163）', 'SQL 错误分类与 Effect 化（classifySqliteError）', 'BigInt 安全读取与 stream 占位（setReadBigInts，index.ts:75）']
- **为什么存在（设计意图）**: 为 opencode 核心提供零原生编译依赖的 Effect 化 SQLite 驱动（复用 node 内置 sqlite），与 @effect/sql-sqlite-node 定位一致但归属仓库自有实现。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-enterprise — enterprise
- 组: G10-应用 | Layer 0
- 作用: 基于 SolidStart 的企业版/云端分享服务。src/app.tsx:1-14 用 @opencode-ai/ui 的 Provider（Marked/Dialog/I18n）搭建 SSR 应用根并做 locale 检测；src/routes/api/[...path].ts:1-30 用 Hono + hono-openapi 定义 OpenAPI 文档与 /share 创建端点（zod schema，经 core/share.ts 与 sst Resource 持久化）；routes/share/[shareID].tsx 用 @opencode-ai/session-ui 的 SessionTurn/SessionReview/MessageNav 渲染只读分享会话；core/storage.ts 提供基于 R2 的存储。
- 提供: ['Hono OpenAPI /api 端点（/share 创建、文档，routes/api/[...path].ts:20-27）', '只读分享会话页面（routes/share/[shareID].tsx，复用 session-ui 组件）', 'R2 对象存储封装（core/storage.ts）', 'SSR 应用根与多语言检测（app.tsx:58 detectLocale）', 'cloudflare 部署目标支持（build:cloudflare script）']
- **为什么存在（设计意图）**: 作为云端托管的企业分享服务，复用 ui/session-ui 渲染能力与 core/sdk 数据模型，通过 SolidStart SSR 提供公开只读分享体验。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-function — function
- 组: G13-边缘服务 | Layer 0
- 作用: Cloudflare Workers 上的会话分享同步服务。src/api.ts:15-114 定义 SyncServer Durable Object：WebSocket 订阅连接（fetch 握手 101 + ctx.acceptWebSocket，api.ts:20-37）、publish 将 session/info|message|part 变更写入 R2 Bucket 并广播给订阅者（api.ts:45-66）、share/assertSecret/clear 管理分享密钥与数据清理；Hono 路由提供 /share_create、/share_delete、/share_sync 等端点（api.ts:116-150）。
- 提供: ['Durable Object 实时同步（WebSocket 广播 session 变更）', 'R2 持久化分享数据（publish 写入 Bucket，api.ts:55）', '分享密钥管理（share/assertSecret，api.ts:68-92）', 'Hono HTTP API（share_create/share_delete/share_sync）', 'GitHub App 认证（@octokit/auth-app 依赖）']
- **为什么存在（设计意图）**: 作为云端分享的后端同步服务，利用 Cloudflare Durable Object 的 WebSocket 能力实现跨客户端实时会话同步，与 function 名（FaaS 云端函数）对应。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-http-recorder — http-recorder
- 组: G14-工具 | Layer 4
- 作用: HTTP 录制/回放工具（package.json:5 描述：Record and replay Effect HTTP client traffic with deterministic cassettes）。src/effect.ts:16-25 提供带录制能力的 HttpClient Layer；src/recorder.ts:11-18 resolveAutoMode 决定 record/replay/passthrough 模式（CI 强制 replay）；src/cassette.ts 实现 cassette 文件存储；src/redactor.ts 负责敏感信息脱敏；src/websocket.ts:10-31 支持 WebSocket 录制回放。
- 提供: ['HTTP 客户端录制层（packages/http-recorder/src/effect.ts:16-25）', 'cassette 录制文件格式与存储（packages/http-recorder/src/cassette.ts）', '自动模式：record/replay/passthrough（packages/http-recorder/src/recorder.ts:11-18）', '请求匹配（packages/http-recorder/src/matching.ts）', '敏感信息脱敏（packages/http-recorder/src/redactor.ts）', 'WebSocket 录制回放（packages/http-recorder/src/websocket.ts:10-31）']
- **为什么存在（设计意图）**: 作为测试基础设施：让 LLM 请求与 HTTP 流量可确定性回放（VCR 模式），保证 CI 中测试不依赖网络与真实 token 计费；被 core/llm 的测试与开发流程引用。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-httpapi-codegen — httpapi-codegen
- 组: G14-工具 | Layer 0
- 作用: 构建期源代码生成工具。compile(Api) 反射一个权威 HttpApi 共享契约；emitPromise/emitEffect/emitEffectImported 独立产出客户；write(output,dir) 经 prettier 格式化后落盘。Effect 客户经 effect/unstable/httpapi 解码域值；Promise 客户零 Effect 直接 fetch。
- 提供: 从 HttpApi+Effect Schema 契约生成领域化客户端 TS 源码：类型化输入、解包 {data:A}、void/stream 映射、统一 ClientError、operations 元数据。
- **为什么存在（设计意图）**: 把 HTTP 客户端生成从 OpenCode Core 解耦成私有独立包，测试即规范；契约作为唯一共享源，Promise 与 Effect 双投影解耦；manifest 防重复生成破坏。
- **改造关联**: 
- **怎么用**: 定义 HttpApi 契约→compile 得 Contract→选 emitPromise 或 emitEffect→write 到目录。产物头部注明 Generated by @opencode-ai/httpapi-codegen. Do not edit.
- **典型场景与协作**: @opencode-ai/client 在服务器契约一改时重新生成 src/generated；app/session-ui/sdk-next 消费该 client 做远端与内嵌调用。

## oc-llm — llm
- 组: G5-LLM请求层 | Layer 4
- 作用: LLM 请求/协议层。src/index.ts:1-28 导出 LLMClient/Auth/Provider/Tool/ToolRuntime；核心 LLM 门面 src/llm.ts:45-48 提供 generate/stream 等请求方法。src/route/client.ts:29-49 定义 Route 结构（provider+protocol+endpoint+auth+transport）与 RequestExecutor；src/route/transport/http.ts、websocket.ts 实现 HTTP/WS 传输。内置 8 个 provider（src/providers/：anthropic、openai、google、azure、amazon-bedrock、openrouter 等，package.json:17-28）与 6 个协议适配（src/protocols/：anthropic-messages、openai-chat、openai-responses、gemini、bedrock-converse，package.json:29-35）。
- 提供: ['统一 LLM 客户端门面 generate/stream（packages/llm/src/llm.ts:45）', 'Route 路由抽象：endpoint/auth/transport/body schema（packages/llm/src/route/client.ts:36-48）', 'HTTP 与 WebSocket 传输层（packages/llm/src/route/transport/http.ts、websocket.ts）', '多提供商适配：OpenAI/Anthropic/Google/Azure/Bedrock/OpenRouter/xAI 等（packages/llm/src/providers/）', '多协议编解码：chat/responses/messages/gemini/bedrock（packages/llm/src/protocols/）', 'Tool 定义与执行运行时（packages/llm/src/tool.ts、tool-runtime.ts）', '上下文溢出检测（packages/llm/src/provider-error.ts:4）']
- **为什么存在（设计意图）**: 将多提供商/多协议的请求差异隔离在路由与协议适配层之下，向上提供单一 LLM 门面，支持 HTTP/WS 双通道并可被 http-recorder 录制回放（llm devDependency 依赖 recorder）。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-opencode — opencode
- 组: G19-主入口 | Layer 0
- 作用: 主应用/CLI 入口。src/index.ts:45 用 yargs 装配 run/serve/tui/agent/acp 等全部子命令；src/cli/tui/layer.ts:1 经 @opencode-ai/tui 拉起终端 UI；src/server/server.ts:4-13 组装 Node HTTP/WebSocket 服务器与 HttpApi 路由。会话编排由 src/session/processor.ts:26-27 驱动（回退 LLM、工具调度），工具清单在 src/tool/registry.ts:4-16 注册（read/edit/shell/glob/grep/webfetch 等 20+ 内置工具）。
- 提供: ['CLI 入口：yargs 子命令体系（run/serve/tui/agent/acp/github 等 20+ 命令，packages/opencode/src/index.ts:45）', 'HTTP/SSE/WebSocket 服务器实例（packages/opencode/src/server/server.ts:27-30）', '会话处理器：消息输入→LLM 请求→工具执行的编排循环（packages/opencode/src/session/processor.ts:32）', '内置工具集：read/write/edit/shell/glob/grep/task/webfetch 等（packages/opencode/src/tool/registry.ts:4）', 'Session 状态机、compaction/retry/summary/reminders 生命周期（packages/opencode/src/session/*）', '插件宿主：加载外部 plugin 与 provider 扩展（packages/opencode/src/plugin/index.ts:8）', 'Code Mode 工具桥接（packages/opencode/src/tool/code-mode.ts:4）']
- **为什么存在（设计意图）**: 作为可分发 CLI 二进制（bin/opencode）聚合所有上层能力，把核心服务、LLM、TUI、协议编排成终端可执行产品，同时保持与 server 分离以便 web/desktop 前端复用同一套服务。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-plugin — plugin
- 组: G7-插件SDK | Layer 4
- 作用: 插件 SDK。src/index.ts:20-80 定义 Plugin/PluginInput/Config/Hooks 等公共类型，基于 @opencode-ai/sdk 客户端访问服务；src/tool.ts:3-20 定义 ToolContext/ToolResult。提供 v2 双运行时：effect 版（src/v2/effect/：plugin/context/agent/command/skill/catalog/integration/filesystem/event 等 14 模块）与 promise 版（src/v2/promise/），并含 TUI 插件类型（src/tui.ts:1-40 基于 @opentui）。
- 提供: ['插件公共类型与 Hooks 契约（packages/plugin/src/index.ts:20-80）', '工具 API：ToolContext/ToolDefinition/ToolResult（packages/plugin/src/tool.ts:3-20）', 'Effect 原生 v2 插件 API：agent/command/skill/catalog/integration 注册（packages/plugin/src/v2/effect/plugin.ts）', 'Promise 风格 v2 插件 API（packages/plugin/src/v2/promise/index.ts）', 'TUI 插件接口（基于 @opentui，packages/plugin/src/tui.ts:19-33）', 'shell 工具封装（packages/plugin/src/shell.ts）']
- **为什么存在（设计意图）**: 作为第三方扩展的稳定 SDK 面（发布到 npm，files 只含 dist），把 opencode 对插件的实现细节隔离在 core 内部，对外只暴露类型化、版本化的注册 API。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-protocol — protocol
- 组: G2-通信协议 | Layer 4
- 作用: 通信协议层。src/api.ts:26-86 用 effect/unstable/httpapi 定义 OpenCode HttpApi 结构：注册 Health/Location/Agent/Session/Message/Model/Provider/Integration/Credential/Permission/FS/Command/Skill/Event/Pty/Question/Reference/ProjectCopy 共 18 个 Group（src/api.ts:38-55），并挂 Authorization/SchemaError 中间件（src/api.ts:63-64）。src/errors.ts:3-40 定义带 httpApiStatus 的 TaggedError（400/401/409/503 等）。src/groups/* 按资源定义端点与契约，middleware/authorization.ts:4-6 定义 Authorization 服务。
- 提供: ['OpenCode HttpApi 协议定义（packages/protocol/src/api.ts:37-55）', '18 个资源端点组（packages/protocol/src/groups/*）', '统一错误契约（httpApiStatus 标注，packages/protocol/src/errors.ts:3-40）', 'Authorization/SchemaError 中间件契约（packages/protocol/src/middleware/）', 'OpenAPI 注解（packages/protocol/src/api.ts:56-62）']
- **为什么存在（设计意图）**: 协议与实现分离：protocol 只声明端点/中间件/错误的契约（server 注入具体服务身份，见 src/api.ts:25 注释），使 server、client、cli 对同一协议的不同实现方共享同一类型面。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-schema — schema
- 组: G1-数据模型 | Layer 5
- 作用: 纯类型/数据模型包，仅依赖 effect（package.json:14-16）。以 Effect Schema 定义全部领域类型：Session/SessionInput/SessionMessage（src/session*.ts）、Event 与 Durable 事件清单（src/event.ts、event-manifest.ts、durable-event-manifest.ts）、Provider/Model（src/provider.ts、model.ts）、Permission、Prompt、Agent 等 40+ 模型。src/index.ts:1-28 统一 re-export；src/schema.ts:3-10 提供 AbsolutePath/RelativePath/DateTimeUtc 等基础 branded schema。
- 提供: ['领域数据模型：Session/Message/Event/Permission/Provider/Model 等（packages/schema/src/index.ts:1-28）', 'Effect Schema 编解码与校验基础（packages/schema/src/schema.ts:3-30）', '事件定义清单：Event/EventManifest/Durable（packages/schema/src/event.ts、durable-event-manifest.ts）', 'V1 兼容模型（packages/schema/src/v1/session.ts、question.ts、permission.ts）']
- **为什么存在（设计意图）**: 作为依赖链最底层的单一事实源，所有包共享同一套 Effect Schema 数据契约，保证类型与运行时校验一致，避免跨包重复定义与 drift。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-script — script
- 组: G14-工具 | Layer 1
- 作用: 构建/发布脚本共享工具包。src/index.ts:5-76 读取仓库根 package.json 校验 bun 版本（semver.satisfies 检查，index.ts:16-18）、按环境变量/分支/registry 计算发布 channel（latest/preview）与 version（含 +1 patch 逻辑，index.ts:34-48）、从 .github/TEAM_MEMBERS 加载团队成员名单（index.ts:50-58），最终导出 Script 对象（channel/version/preview/release/team）供发布流水线使用。
- 提供: ['发布版本计算（channel/version/preview，基于 env/分支/npm registry）', 'Bun 版本校验（强制 ^packageManager 版本，index.ts:16）', '团队成员名单加载（.github/TEAM_MEMBERS 解析，index.ts:50）']
- **为什么存在（设计意图）**: 将发布流程共用的版本决策逻辑从 CI 脚本中抽离为可 import 的库，保证多个发布任务（channel 判断、bump 语义）行为一致。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-sdk — sdk
- 组: G3-客户端 | Layer 5
- 作用: 官方 JS 客户端 SDK（packages/sdk/js/）。src/index.ts:1-21 导出 client/server 并通过 createOpencode 同启；src/client.ts:33-50 createOpencodeClient 基于 @hey-api 生成的 gen/sdk.gen.ts（v2 版 src/v2/gen/sdk.gen.ts:7077 class OpencodeClient）并注入 directory header 重写；src/server.ts:22-40 createOpencodeServer 用 cross-spawn 拉起 opencode serve 子进程并等待监听。v2 子目录提供新一代 client/server/data 导出（src/v2/index.ts:1-23）。
- 提供: ['类型化 HTTP 客户端 createOpencodeClient（packages/sdk/js/src/client.ts:33）', '服务端启动助手 createOpencodeServer（spawn opencode serve，packages/sdk/js/src/server.ts:22）', '一体化 createOpencode（packages/sdk/js/src/index.ts:8-21）', 'V2 代客户端/服务端 API（packages/sdk/js/src/v2/client.ts、server.ts）', '从 openapi.json 生成的完整类型与 SDK（packages/sdk/js/src/v2/gen/sdk.gen.ts）']
- **为什么存在（设计意图）**: 对外发布（npm 包）的官方 SDK，将 opencode 内部 server 的 openapi.json 编译为类型安全的客户端，同时提供进程级 server 托管，供第三方应用与 plugin 使用。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-sdk-next — sdk-next
- 组: G3-客户端 | Layer 0
- 作用: Effect 原生的进程内 OpenCode host SDK（过渡包，替代生成式 @opencode-ai/sdk）。src/opencode.ts 的 create() 用 AppNodeBuilder 构建 ApplicationTools/PermissionSaved 上下文，把 server 的 createEmbeddedRoutes 编译成 Web handler 并注入内存 fetch，客户端由此在进程内执行全部路由而无需监听端口/网络 I/O。src/index.ts 聚合 OpenCode 与 Tool 模块并再导出 client 的 Effect 类型。
- 提供: ['进程内 OpenCode host：OpenCode.create()（src/opencode.ts:10）', '内存路由执行：Server router → Web handler → fetch（src/opencode.ts:20-38）', '本地工具注册 tools.register（走 ApplicationTools 服务，src/opencode.ts:41）', 'DI Layer：OpenCode.layer/Service（src/opencode.ts:47,49）', 'Tool 门面：Failure/RegistrationError/make 再导出（src/tool.ts:1）', 'Effect client 类型再导出（ClientError/Session/Model 等，src/index.ts:4）']
- **为什么存在（设计意图）**: README 明示：作为 sdk 的过渡替代，让嵌入式应用无需网络即可获得完整 host 能力，保留 sdk 的注册/工具语义并转为 Effect-native。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-server — server
- 组: G4-服务端 | Layer 1
- 作用: HTTP/SSE 服务器实现层。src/api.ts:5-8 用 @opencode-ai/protocol/api 的 makeDefaultApi 装配 HttpApi，并注入 LocationMiddleware/SessionLocationMiddleware 具体中间件；src/routes.ts:1-13 把 core 的各类服务（SessionV2/SessionExecution/LocationServiceMap/Database/ToolOutputStore 等）装配为 Effect Layer；src/handlers.ts:1-40 合并 19 个 handler（session/message/agent/model/provider/fs/event/pty 等），每个 handler 将 HTTP 请求桥接到 core 领域服务。
- 提供: ['HttpApi 装配与中间件注入（packages/server/src/api.ts:5-8）', '19 个资源 handler（packages/server/src/handlers.ts:21-40）', 'core 服务到 HTTP 层的 Effect Layer 桥接（packages/server/src/routes.ts:1-13）', '授权/会话定位中间件（packages/server/src/middleware/authorization.ts、session-location.ts）', 'CORS 与 auth 基础（packages/server/src/cors.ts、auth.ts）']
- **为什么存在（设计意图）**: 把 Effect HttpApi 与 core 领域服务粘合为可运行的 HTTP 服务（不依赖 CLI），使 opencode 主程序、sdk createOpencodeServer 与其他宿主都能复用同一套服务端装配。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-session-ui — session-ui
- 组: G9-UI组件 | Layer 2
- 作用: 会话级 UI 组件集，介于基础组件库与完整应用之间。src/components/ 提供 SessionTurn、SessionReview、MessagePart、message-file、session-diff、line-comment 等会话渲染组件，并含 markdown 流式渲染整套管线（markdown-stream.ts + markdown-worker.ts + markdown-cache.tsx，用 Worker 实现增量渲染）；src/pierre/ 提供 file-find/file-selection/diff-selection/media 等代码交互原语；src/context/data.tsx 提供会话数据 Provider（被 enterprise share 页复用）。
- 提供: ['SessionTurn/SessionReview 会话轮次与评审组件', 'MessagePart/message-file/session-diff 消息部件与差异展示', 'Markdown 流式渲染管线（worker + stream + cache，markdown-stream.ts:12）', '文件查找/选择/差异选择交互原语（pierre/ 目录）', '会话数据 context（context/data.tsx）', 'PromptInput v2 输入框（v2/components/prompt-input/）']
- **为什么存在（设计意图）**: 把会话级渲染（消息/轮次/评审/markdown 流）从 app 中剥离，使 app 与 enterprise 共享同一套会话表达，避免重复实现。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-slack — slack
- 组: G18-集成 | Layer 0
- 作用: Slack 机器人集成（@slack/bolt Socket Mode）。src/index.ts 创建 opencode 服务端实例（createOpencode）与 Slack App，按 channel+thread 键复用 session：首次消息创建 opencode session 并分享链接，后续消息走 session.prompt；同时订阅 message.part.updated 事件把 tool 完成状态回贴到 thread（src/index.ts:24-51）。
- 提供: ['Slack Socket Mode 机器人（src/index.ts:4）', '每 thread 独立 opencode session 的创建/复用（src/index.ts:22,70-101）', '会话分享链接回帖（src/index.ts:96）', 'tool 执行状态回帖（message.part.updated 订阅，src/index.ts:24-51）', '/test 命令与错误兜底回复（src/index.ts:138）']
- **为什么存在（设计意图）**: 让用户直接在 Slack 线程内驱动 opencode agent，把聊天线程映射为独立 session；作为独立部署的集成入口，复用 @opencode-ai/sdk 而非内嵌实现。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-stats-app — stats-app
- 组: G17-Stats | Layer 0
- 作用: OpenCode Stats 公共数据站点（SolidStart，Cloudflare preset，app.config.ts:1）。首页通过 @opencode-ai/stats-core/domain/home 拉取并渲染使用量排行榜、模型/Provider 对比、geo 分布与市场数据（src/routes/index.tsx:10-41），另有 compare 对比页与 [lab]/[model] 实验页，配合 d3-geo/topojson 世界地图。src/routes/stats-cache.ts 统一设置 CDN 缓存头。
- 提供: ['统计首页：排行榜/用量趋势/Geo 地图/缓存命中率（src/routes/index.tsx）', '模型对比页（src/routes/compare/[firstFamily]/[secondFamily].tsx）', '模型实验室单模型页（src/routes/[lab]/[model].tsx）', 'CDN 缓存控制与 Vary locale 处理（src/routes/stats-cache.ts:5）', 'API：health/newsletter（src/routes/api/）', '多语言 i18n（20 语言）与 sitemap']
- **为什么存在（设计意图）**: 独立的公共数据站（stats.opencode.ai），与 Console 分离部署；展示 opencode 生态模型使用统计，靠 stats-core 提供领域数据。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-stats-core — stats-core
- 组: G17-Stats | Layer 1
- 作用: Stats 后端核心（Effect + drizzle + PlanetScale）。src/athena.ts 封装 AWS Athena 查询服务（StartQuery/轮询/取结果），src/database.ts 提供 Effect 风格 DatabaseConfig/DrizzleClient，src/domain/ 下按 model/provider/geo/home/inference 分域定义聚合类型与查询，src/stat-sync.ts 实现 Athena → 数据库的增量/全量同步管线。src/index.ts 聚合导出全部命名空间。
- 提供: ['Athena 查询服务：执行/轮询/分页取数（src/athena.ts:45）', 'Effect 化数据库层：PlanetScale drizzle + schema + 迁移（src/database.ts:24,40）', '统计领域模型：StatBaseAggregate 聚合结构与 grain day/week（src/domain/stat.ts:6）', 'Model/Provider/Geo 统计仓库与 upsert（src/domain/model.ts 等）', '首页聚合查询（getStatsHomeData，src/domain/home.ts:9）', '统计同步管线：Athena 查询 → 聚合 → 写入（src/stat-sync.ts:23）', 'App 配置（stage/publicUrl）与运行时（src/config.ts、src/runtime.ts）']
- **为什么存在（设计意图）**: 按 stats 独立生态划分：core 承载 Effect 领域服务与数据访问，供 app 查询、server 同步、Lambda 入口三方复用，README 明确 Runtime/DB/domain 全部在 core。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-stats-server — stats-server
- 组: G17-Stats | Layer 0
- 作用: Stats 后端 Node HTTP 服务（Effect HttpRouter + Bun，Dockerfile 部署）。src/server.ts 用 NodeHttpServer 启动 3000 端口服务并注入 Ingest 层，src/router.ts 暴露 GET /health、/ready 与 POST / 数据摄取端点（Bearer 鉴权 + 并发信号量限流），src/ingest.ts 将事件批处理写入 AWS Firehose，src/stat-sync.ts 是每小时 Athena 同步 daemon。
- 提供: ['摄取端点 POST /：事件批收 + Firehose 写入（src/router.ts:25、src/ingest.ts:38）', '健康检查 GET /health 与 /ready（含优雅停机判定，src/router.ts:23-24）', 'Bearer 鉴权（timingSafeEqual，src/router.ts:56）', '每小时统计同步 daemon（src/stat-sync.ts:13）', 'Docker 化部署（Dockerfile:1，turbo prune + bun install）']
- **为什么存在（设计意图）**: 作为摄取网关承接 Console function 的 lake 事件流，并独立承载统计同步 daemon；与 app 站点、core 领域解耦。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-storybook — storybook
- 组: G11-文档站点 | Layer 0
- 作用: UI 组件开发文档站。.storybook/main.ts:13-29 用 storybook-solidjs-vite 定义框架并聚合 ui/session-ui/app 三包的 stories（stories glob 指向 ../../ui、../../session-ui、../../app/src）；同时用 mocks 目录对 app 的 context（local/file/prompt/layout/sdk/sync 等 15+ 个）做 SolidJS router 替换与 context mock（main.ts:36-50），使 app 组件能在 Storybook 中独立渲染；preview.tsx 提供全局预览配置。
- 提供: ['聚合 ui/session-ui/app 三包组件的 Storybook 开发环境', 'app context 全套 mock（main.ts:37-50 别名替换）', 'Playground CSS 与主题工具插件（playground-css-plugin.ts、theme-tool.ts）']
- **为什么存在（设计意图）**: 为组件库提供隔离的开发/审查环境，通过 mock 掉 app 的副作用 context 使跨包组件可以独立预览与回归测试。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-tui — tui
- 组: G8-终端UI | Layer 1
- 作用: 终端 UI 应用。src/index.tsx:1 导出 run/TuiInput；src/app.tsx:1-50 用 @opentui/solid 渲染整棵组件树（SDK/Data/Location/Theme/Clipboard 等 Provider 与 Session 路由），构建在 @opencode-ai/sdk/v2 客户端之上（src/context/sdk.tsx:1）。src/plugin/runtime.tsx 加载 @opencode-ai/plugin/tui 插件，feature-plugins/ 内含 diff-viewer/notifications/which-key/sidebar 等内置插件（src/feature-plugins/builtins.ts:1）。
- 提供: ['终端渲染运行时（src/app.tsx:1，基于 @opentui/solid）', '会话交互 UI：输入/补全/历史/frecency（src/component/prompt/*）', '对话框系统：模型/agent/主题/会话列表等 20+（src/component/dialog-*.tsx）', '内置 TUI 插件：diff-viewer/通知/which-key/侧栏（src/feature-plugins/builtins.ts）', '多 Context Provider：sdk/data/sync/theme/clipboard（src/context/*）', 'V2 SDK 数据层接入（src/context/data.tsx、sdk.tsx）']
- **为什么存在（设计意图）**: 将终端交互封装为独立可复用包，经 opencode 的 cli/tui/layer.ts 加载，同时支持 TUI 插件扩展（@opencode-ai/plugin/tui），使 CLI 与桌面端共用交互逻辑。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-ui — ui
- 组: G9-UI组件 | Layer 3
- 作用: SolidJS UI 组件库。src/components/ 含 50+ 基础组件（button/avatar/dialog/context-menu/diff-changes/icon 等，每个 .tsx 配套 .css 与 .stories.tsx），基于 @kobalte/core 无障碍原语；exports 将 ./components/*.tsx 直接映射为组件子路径（package.json:37）。同时提供 hooks（use-filtered-list）、context（dialog/file/i18n/marked/worker-pool）、theme 主题系统、i18n 词典、v2 新一代组件目录及 storybook 脚手架（src/storybook/scaffold.tsx）。
- 提供: ['50+ 基础 UI 组件（按钮/对话框/下拉/悬浮卡/图标等）', 'Markdown 渲染管线（marked.tsx + worker-pool + shiki 流式高亮）', 'Theme 主题解析与上下文（theme/index.ts、theme/context.tsx）', 'i18n 多语言词典与 plural 规则（i18n/en.ts、context/i18n.tsx）', 'File/Dialog/WorkerPool 等全局 context', '图标集：provider/file/app 三类 sprite（provider-icons/types.ts 等）']
- **为什么存在（设计意图）**: 将跨 app/session-ui/enterprise 复用的无头基础组件与渲染原语独立成库，保证视觉一致性与按需导入（sideEffects 仅 css）。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 

## oc-web — web
- 组: G11-文档站点 | Layer 0
- 作用: 基于 Astro + Starlight 的文档与分享站点。src/pages/s/[id].astro:2-8 渲染会话分享页（Share.tsx 消费 opencode/session 类型，通过 API URL 拉取分享数据）；src/pages/[...slug].md.ts:19-34 提供 docs 内容 API（按 slug 返回 markdown 文档）；src/content/docs/ 含多语言（en/zh/ar/bs/de/...）文档与代码示例（大量引用 @opencode-ai/plugin 与 @opencode-ai/sdk 的用法）。devDependencies 引用 opencode 包（opencode: workspace:*）。
- 提供: ['会话分享查看页（s/[id].astro + components/Share.tsx）', 'docs 文档 API 端点（pages/[...slug].md.ts:19）', 'Starlight 多语言文档站（content.config.ts + i18n/）', '分享 WebSocket 连接状态 UI（Share.tsx:15 status 机）']
- **为什么存在（设计意图）**: 独立部署的文档+分享前端，与桌面 app 完全解耦，仅通过 API URL 消费后端数据，作为云端分享生态的展示层。
- **改造关联**: 
- **怎么用**: 
- **典型场景与协作**: 
