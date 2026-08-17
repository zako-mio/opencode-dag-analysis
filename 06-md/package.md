# package 节点（35）

## oc-app — app
- 组: G10-应用 | Layer 4
- 作用: OpenCode 桌面/Web 前端的 SolidJS 主应用。src/app.tsx 组装全部 Provider（Server/SDK/ServerSync/Settings/Tabs/Command 等约 20 个 context，app.tsx:41-66）并注册 Session/Home/NewSession/Legacy 等路由；src/entry.tsx:5-11 通过 render 挂载 AppInterface 与 PlatformProvider；src/index.ts:1-30 导出 AppBaseProviders、AppInterface 及全部 context hooks（useServer/useSettings/useTabs 等）。桌面专属能力（desktop-menu.ts、updater.ts、wsl/ 目录）以子路径导出供 desktop 包复用。
- 提供: ['AppInterface 与 AppBaseProviders 根组件（SolidJS 应用壳）', 'Server/SDK/ServerSync/Tabs/Settings/Command 等全套全局 context', 'Session 会话页、Home 主页、NewSession 页、布局（新旧两套）页面', 'WSL 服务器探测/管理类型与桌面菜单、更新器（updater.ts）', 'i18n 中英双语词典与 locale 规范化（i18n/、context/language.tsx）', 'draft-store 草稿持久化与 file-picker 常量（utils/draft-store.ts:30）']
- **为什么存在（设计意图）**: 作为 UI 应用壳层，将 session-ui/ui 的无状态组件与 server/core 的业务逻辑粘合为完整应用，同时为 desktop 提供可复用的桌面子模块（菜单/更新/WSL）出口，避免桌面壳重复实现 UI 组装。
- **改造关联**: 属官方底座，本机装配层（opencode.jsonc 的 agent/config/mcp/skill 节点）未引用。仅作为 DAG 中 oc-desktop 的上游被官方依赖链引用（@opencode-ai/desktop 依赖 @opencode-ai/app）。
- **怎么用**: ['浏览器挂载入口：src/entry.tsx:162-176 render(<PlatformProvider><AppBaseProviders><AppInterface/></AppBaseProviders></PlatformProvider>)，桌面 renderer 复用同一组件树（desktop/src/renderer/index.tsx:3-17 直接 import AppBaseProviders/AppInterface/useServer 等）', '公共导出面 src/index.ts:1-30：AppBaseProviders/AppInterface（app.tsx:393/557）、全套 context hooks（useServer/useSettings/useTabs/useCommand/useLanguage）、WSL 类型与 updater/desktop-menu 子路径导出（package.json exports ./desktop-menu、./updater、./wsl/types）', '开发命令：bun start/vite（package.json:18-21）本地起 Vite dev server；desktop 包经 @opencode-ai/app workspace:* 依赖直接复用']
- **典型场景与协作**: 作为桌面端（desktop 渲染进程）与 Web 端（vite serve）共用的 SolidJS 应用壳：desktop/renderer/index.tsx 导入 AppInterface 后只替换 Server/Platform/Updater 等实现（index.tsx:64-321 window.api 桥），实现同一 UI 两套宿主。典型协作链：app 消费 session-ui 的会话渲染组件 + ui 的基础组件 + core 的 ServerConnection，desktop 仅提供原生 IPC/菜单/更新能力。

## oc-cli — cli
- 组: G10-应用 | Layer 4
- 作用: OpenCode 2.0 CLI 入口（bin: lildax）。src/index.ts:10-32 用 Effect 构建命令运行时：Runtime.handlers 将 Commands 映射到懒加载 handler（api/debug/migrate/service/serve）；commands/commands.ts:6-8 用 effect CLI 声明命令树；framework/runtime.ts:58-59 执行 Command.run；services/daemon.ts 提供后台守护进程服务。命令处理依赖 @opencode-ai/core 的 AppNodeBuilder 与 @opencode-ai/server 路由（serve.ts:2-10）。
- 提供: ['opencode 命令树（api/debug/migrate/service/serve，commands.ts:9-50）', 'Effect 驱动的命令运行时与懒加载 handler（framework/runtime.ts:58）', '后台 daemon 服务管理（services/daemon.ts）', 'TUI 入口（tui.ts 导入 @opencode-ai/tui 运行）', '版本/渠道识别（bin/lildax.cjs 打包）']
- **为什么存在（设计意图）**: 作为 v2 时代的命令行入口，复用 effect CLI 生态以类型安全方式声明命令，并将实际逻辑委托给 core/server/tui 包，保证 CLI 层只做装配不做业务实现。
- **改造关联**: 属官方底座，本机装配层未引用（本机不安装 lildax 二进制）。但本机装配层使用 opencode v1 CLI（@opencode-ai/opencode 的 yargs 命令），cli 是 v2 演进方向，改造时需注意双 CLI 并存。
- **怎么用**: ['bin: lildax（package.json:7-9 bin.lildax → ./bin/lildax.cjs），build 产出跨平台二进制（script/build.ts:12 binary=lildax、:80 outfile dist/{name}/bin/lildax、:86 OPENCODE_CLI_NAME）', '命令树：src/commands/commands.ts:6-50 Spec.make 声明 api/debug/migrate/service/serve 子命令，index.ts:10-25 Runtime.handlers 映射懒加载 handler', 'TUI 入口：src/tui.ts:1-18 runTui() 导入 @opencode-ai/tui run + AppNodeBuilder.build(Global.node) 装配完整环境']
- **典型场景与协作**: 作为 v2 时代的命令行入口（OpenCode 2.0 preview）：serve 命令拉起 v2 API 服务器、service 管理后台守护进程、api 命令直接调 OpenAPI、tui 启动终端交互界面。与 web/desktop 互补：cli 是终端用户入口，内部委托 core/server/tui 包实现逻辑而非自己实现。

## oc-client — client
- 组: G3-客户端 | Layer 2
- 作用: 面向 Web/桌面的客户端库。src/contract.ts:1-17 复用 protocol 的 makeDefaultApi 定义 ClientApi 与 Location/SessionLocation 中间件，并声明 groupNames/endpointNames 映射（src/contract.ts:19-51）；src/index.ts:1-2 从 generated/ 导出类型化客户端；src/generated/ 与 src/generated-effect/ 由 script/build.ts 依据 contract 生成（普通 + Effect 两版），src/effect.ts:3-25 转出 schema 数据类型并保证不 import core/server（文件头注释 src/effect.ts:1-2）。
- 提供: ['客户端 Api 契约（基于 protocol 默认 Api，packages/client/src/contract.ts:14-17）', '生成的普通客户端（packages/client/src/generated/client.ts）', '生成的 Effect 客户端（packages/client/src/generated-effect/client.ts）', '类型 re-export 与错误类型（packages/client/src/effect.ts:4-25、generated/client-error.ts）', 'group/endpoint 名称映射（packages/client/src/contract.ts:19-51）']
- **为什么存在（设计意图）**: 面向 app/web 前端生成类型安全的 HTTP 客户端，并通过协议层复用服务端同款端点契约；强调不得反向依赖 core/server（src/effect.ts:1-2），保持客户端纯净。
- **改造关联**: 本机未直接引用 client（本机界面是终端 CLI + 浏览器，不使用 app/web 前端与 client 包），属官方底座；但 client 与 sdk 同源（协议生成），本机若未来走 HTTP 集成可无成本接入同一契约。
- **怎么用**: ["入口：src/index.ts:1-2 re-export generated/index 与 OpenCodeEvent 类型；src/effect.ts 提供 Effect 原生客户端。package.json exports：'.'（Promise 版，src/index.ts）与 './effect'（Effect 版）。", '生成制：由 @opencode-ai/server/api 经 httpapi-codegen 生成 src/generated/*（client.ts/types.ts/client-error.ts/index.ts）；README.md:8-12 要求改契约后 bun run generate + check:generated 防漂移。', "用法示例（client/README.md:29-38）：import { OpenCode } from '@opencode-ai/client/effect'，OpenCode.make({baseUrl}) 后 client.sessions.create/prompt 直接用 canonical 类型（Session.ID/Location.Ref/Prompt）。"]
- **典型场景与协作**: client 面向 app/web/session-ui 前端生成类型安全 HTTP 客户端：零 Effect 依赖的 Promise 根（无 core/server 依赖），/effect 子路径依赖 Effect+Schema+Protocol 且浏览器打包安全。协议层复用服务端同款端点契约，前端因此获得与 server 完全一致的端点类型；sdk-next/app/session-ui 三个官方包依赖它（official-dag reverse）。

## oc-codemode — codemode
- 组: G12-沙箱 | Layer 0
- 作用: Code Mode 沙箱：基于 schema 描述的受限代码执行（package.json:5 描述）。src/interpreter/runtime.ts:1-3 用 acorn 解析 + typescript transpileModule 在受限解释器中执行 JS 子集，工具调用经 src/tool-runtime.ts 注入 host tools 并受 ExecutionLimits（超时/最大工具调用数/输出字节，src/codemode.ts:10-17）约束。src/openapi/ 提供从 OpenAPI spec 生成工具的运行时（src/openapi/index.ts），src/stdlib/ 提供 JS 子集标准库（string/number/date/collections 等 14 模块）。
- 提供: ['受限 JS 解释器与 AST 执行（packages/codemode/src/interpreter/runtime.ts:1）', '工具调用沙箱运行时（packages/codemode/src/tool-runtime.ts）', '执行资源限制：timeout/maxToolCalls/maxOutputBytes（packages/codemode/src/codemode.ts:10-17）', 'OpenAPI 工具生成器（packages/codemode/src/openapi/index.ts、spec.ts）', 'JS 子集标准库（packages/codemode/src/stdlib/*）', '工具 schema 编解码（packages/codemode/src/tool-schema.ts）']
- **为什么存在（设计意图）**: 为 LLM 提供可审计、受限、确定性的代码执行环境（Effect-native），并支持基于 schema 描述的工具集，避免开放 shell 的安全风险（被 opencode 的 tool/code-mode.ts 桥接使用）。
- **改造关联**: 本机未直接引用 codemode（装配层无沙箱类工具依赖，subagent 权限由 permission 层控制而非 codemode 沙箱），属官方底座；但本机权限三层纵深（L1 全局 deny bash 危险命令）与 codemode 的「最小授权」设计哲学同源，可视为同一安全目标在配置层的替代实现。
- **怎么用**: ['入口：src/index.ts:1-4 —— export * as CodeMode / Tool / OpenAPI，export { ToolError, toolError }；core 的 tool/code-mode.ts 桥接使用（official-dag edge evidence）。', 'API（README.md:10-18）：一次性 CodeMode.execute({tools, code}) 与可复用 CodeMode.make({tools, limits}) → runtime.execute(code)；模型写受限 JS 程序，只能调用宿主显式提供的 schema 描述工具。', '实现：src/interpreter/（受限解释器）、src/stdlib/（工具标准库）、src/openapi/（OpenAPI 工具面，含 TODO）；依赖仅 acorn/effect/typescript（Effect-native）。']
- **典型场景与协作**: codemode 为 LLM 提供可审计、受限、确定性的代码执行环境：模型把多步工具调用编排成单个 JS 程序一次执行（省上下文、省 agent 往返），无环境授权（无文件/进程/网络/模块权限）。被 opencode 的 tool/code-mode.ts 桥接为常规工具，报告未深度覆盖但属 G12-沙箱 组的官方能力。

## oc-console-app — console-app
- 组: G16-Console | Layer 2
- 作用: Console 主站前端（SolidStart/SSR + Nitro on Cloudflare），包含营销落地页、认证回调、workspace 管理（billing/keys/members/settings/usage）、Zen 与 Go 两个 LLM API 网关，以及到 docs/stats/bench 的代理路由。src/app.tsx 挂载路由与 i18n，src/routes/zen/v1/chat/completions.ts 走统一 handler 做鉴权/计费/限流后转发到上游 provider，src/lib/stats-proxy.ts 反向代理 stats.opencode.ai。
- 提供: ['营销/下载/企业页与多语言 i18n（20 语言，src/i18n/）', 'OpenAuth 认证与 session 处理（src/routes/auth/、src/context/auth.ts）', 'workspace 控制台：billing 充值、API key、成员、用量图表（src/routes/workspace/[id]/）', 'Zen 网关：OpenAI/Anthropic/Google 兼容 API + key/IP 限流 + 用量计费（src/routes/zen/）', 'Go 网关（轻量版 zen，src/routes/zen/go/）', 'Stripe webhook、honeycomb webhook、enterprise lead 提交', 'docs/stats/bench 站点反向代理（src/routes/docs/、src/routes/data/）']
- **为什么存在（设计意图）**: 控制台全部业务状态（workspace/billing/usage/limits）以 SSR + SolidStart 文件路由承载，前端不直接读写 DB，而是 import @opencode-ai/console-core 的 fn 函数（drizzle 查询 + Actor 上下文）在 server 端执行——单一业务逻辑源，前端只是视图层。zen 网关（OpenAI/Anthropic/Google 兼容端点 + IP/Key 限流 + sticky provider + usage batching）也以 routes 形式内嵌在 app 中，与 UI 同仓库部署。
- **改造关联**: 本机未修改该包（v1.18.14 原样）；但它是装配层认知的官方对标物：本机 deepseek-v4-pro/flash 模型配置、opencode.jsonc provider 结构（modalities/variants/cost 字段）即是对 console 的 ZenData ModelSchema/ProviderSchema 的本地简化仿写。
- **怎么用**: SolidStart (SolidJS) 前端 SPA：bun dev 启动 vite dev 服务器（--host 0.0.0.0）；bun run build 先跑 script/generate-sitemap.ts 生成 sitemap，再 vite build 产出 .output，随后调 ../../opencode/script/schema.ts 把 opencode 的 config.json/tui.json schema 注入 .output/public/。生产形态是 SST/Cloudflare 部署的 SSR 站点（entry-server.tsx 用 createHandler 做 locale/dir 服务端渲染，routes/ 下同时存在 API 路由如 openapi.json.ts、honeycomb/webhook.ts、feishu.ts 重定向）。
- **典型场景与协作**: opencode 官方商业控制台前端（https://opencode.ai）：落地页、登录/授权（auth/）、workspace 管理、账单/订阅/Key/用量仪表盘、Black/Lite 订阅计划页、zen API 网关路由（routes/zen/v1 与 zen/go/v1）、honeycomb 告警 webhook 入口。

## oc-console-core — console-core
- 组: G16-Console | Layer 1
- 作用: Console 后端领域层：基于 drizzle-orm + PlanetScale 的数据库访问、Actor 权限上下文、以及 Account/User/Workspace/Key/Billing/Subscription/Model/Provider 等 CRUD 与计费逻辑。src/drizzle/index.ts 封装事务与上下文，src/account.ts 处理账号创建/删除（含级联清理 key、coupon、auth），src/workspace.ts 创建 workspace 并默认生成管理员与 API key，src/billing.ts 对接 Stripe 做 credits 充值。
- 提供: ['Database 封装：PlanetScale drizzle 客户端 + 事务/上下文（src/drizzle/index.ts:36）', 'Actor 权限上下文：请求用户/角色/workspace 断言（src/actor.ts）', '账号生命周期：create/remove/fromID，删除级联清理（src/account.ts:13,27）', 'workspace 创建与成员管理（src/workspace.ts:17）', 'API Key 管理与角色隔离（src/key.ts:11）', 'Stripe 计费：credits 充值/订阅/用量计费（src/billing.ts:22,29）', '模型/Provider 目录与 ZenData 模型成本定义（src/model.ts）', '订阅限额：free/lite/black 阶梯（src/subscription.ts:7）', '全量 drizzle schema SQL（src/schema/*.sql.ts，account/auth/billing/key/model/provider/referral/user/workspace/ip/benchmark）', '邀请邮件渲染（动态 import console-mail，src/user.ts:142）']
- **为什么存在（设计意图）**: 用 namespace + fn(zod, impl) 模式把参数校验(zod) + Actor 权限上下文 + DB 事务统一封装，业务函数即 API 边界——console-function/app 直接 import 复用，避免三处重复实现；Actor（account/public/user/system 四型）贯穿所有查询做租户隔离（workspaceID 过滤），是控制台多租户安全的核心机制。
- **改造关联**: 本机未改该包；装配层对它的借用体现在方法论：本地自定义工具 read.ts 的 zod args schema、子Agent 的 JSON 返回合约、以及 mission-archiving 的 5 段报告，都沿用了 zod 定义契约 + 结构化输出这一 console-core 模式。
- **怎么用**: 被 console-app / console-function / console-support 以 workspace:* 依赖引用（exports 映射 ./src/*.ts 直读 TS 源码）。业务入口均为 fn(zodSchema, impl) 封装的函数：Actor.provide 提供 account/user/system 上下文（AsyncLocalStorage），Database.use/transaction 执行 drizzle 查询（PlanetScale/MySQL + postgres 双驱动），Key/Workspace/User/Provider/Subscription/Billing/BlackData/LiteData/Referral 等 namespace 各司其职。DB 操作经 bun sst shell drizzle-kit（script/db）迁移。
- **典型场景与协作**: console 全栈业务逻辑层：workspace 创建（含默认 API Key 与 billing 记录）、Key 生成（sk- + 64 随机字符）、model/provider 目录（ZenData 的 Format: anthropic|google|openai|oa-compat 与 cost/cacheRead/byok/sticky/trial 字段）、订阅限额（free/lite/black 三档 rolling/weekly/monthly 窗口）、Stripe 计费（billing.ts 的 Stripe client + 4.4% 处理费公式）、AWS SES 邮件（aws.ts）。

## oc-console-function — console-function
- 组: G16-Console | Layer 2
- 作用: Cloudflare Workers 端边函数集：auth.ts 是 OpenAuth issuer（GitHub/Google 登录 + Cloudflare KV 存储，签发 account/user subject），log-processor.ts 是 tail 处理器，把 Zen/Go 网关的请求日志转发到 Honeycomb 与数据湖，stat.ts 提供 TPS 限流统计查询端点。src/auth.ts:44 用 @openauthjs/openauth 构建 OAuth issuer，src/log-processor.ts:5 解析 _metric: 前缀日志聚合指标。
- 提供: ['OAuth 登录 issuer：GitHub/Google provider + Cloudflare KV 会话存储（src/auth.ts:44）', 'Subjects 定义：account/user 两级认证主体（src/auth.ts:25）', '网关日志采集：tail 事件 → Honeycomb batch + lake ingest（src/log-processor.ts:5）', 'TPS 限流统计查询：按模型 id 聚合 30 分钟窗口 qualify/unqualify（src/stat.ts:7）']
- **为什么存在（设计意图）**: 把认证签发、限流计数查询、日志遥测拆成独立 Worker，与 app 的 SSR 路由解耦——auth 需要 KV 会话存储与 OAuth provider 配置，log-processor 需要 Trace API，放在 function 层可独立部署/独立扩缩容；console-core 的业务函数（Account/Workspace/Actor/Database）被直接 import 复用，保持单一业务源。
- **改造关联**: 本机未改；装配层没有直接复用 function 包，但其独立 Worker 做限流/遥测的架构与本地 headroom proxy（8787 端口压缩代理）、browser-harness daemon 的独立进程承载横切能力是同一设计思路。
- **怎么用**: Cloudflare Worker/Lambda 入口包：src/auth.ts 导出 fetch handler（@openauthjs/openauth issuer，GitHub/Google OAuth provider + CloudflareStorage KV 会话）；src/stat.ts 导出 POST / 查询 ModelTpsRateLimitTable 近 30 个 1 分钟 interval 的 qualify/unqualify 计数；src/log-processor.ts 导出 tail()（Cloudflare Workers Trace 日志处理：解析 _metric: 前缀日志 → 转发 Honeycomb https://api.honeycomb.io/1/batch/zen + 数据湖 ingest）。依赖 ai / @ai-sdk/anthropic|openai|openai-compatible（LLM 代理链）。
- **典型场景与协作**: 控制台的 Serverless 边缘函数：openauth 认证签发（account/user subjects）、TPS 限流计数聚合查询（配合 app 侧 modelTpsLimiter）、Zen 网关的 observability 数据管线（honeycomb 批量写入 + lake ingest，含 llm.error 事件）。

## oc-console-mail — console-mail
- 组: G16-Console | Layer 0
- 作用: 邮件模板包：无 src/，全部为 emails/ 下的 jsx-email 模板与共享组件/样式。emails/templates/InviteEmail.tsx 是唯一业务模板（workspace 邀请邮件），被 console-core 的 User 邀请逻辑动态 import 渲染（console/core/src/user.ts:142）。包 exports 映射到 ./emails/templates/*，纯前端渲染无服务逻辑。
- 提供: ['InviteEmail 邀请邮件模板（React/jsx-email，emails/templates/InviteEmail.tsx:26）', '共享邮件组件与内联样式（emails/components.tsx、emails/styles.ts）', '静态邮件资源：字体 woff2/logo/箭头图（emails/templates/static/）', '本地预览命令（email preview emails/templates）']
- **为什么存在（设计意图）**: 邮件模板独立成包并用 JSX 组件化渲染（@jsx-email），原因：1) 与业务逻辑隔离，纯展示层可单独预览迭代；2) JSX 类型安全 + 复用组件（styles.ts）；3) console-core 的 AWS SES 只负责发送，模板与发送解耦，模板可被 app/core 两处引用。
- **改造关联**: 本机未改。装配层的邮件能力另起炉灶（recruit-assist 用 lark-cli/飞书或 minimax-docx），未采用 SES 邮件链路。
- **怎么用**: 纯模板包：exports 映射 ./emails/templates/*（InviteEmail.tsx 等），用 @jsx-email（render/cli/all）把 React/TSX 组件渲染为 HTML 邮件；bun dev = email preview emails/templates 本地预览。被 console-core/console-app 以 workspace:* 依赖，配合 AWS SES（aws.ts 的 SendEmail）发送。
- **典型场景与协作**: 控制台的邀请/通知邮件模板（InviteEmail），与 billing/subscription 流程联动（付费邀请、黑金计划等场景）。

## oc-console-resource — console-resource
- 组: G16-Console | Layer 0
- 作用: SST 资源访问抽象层，无 src/ 目录（文件在包根）。通过 Proxy 按运行环境暴露 Resource：resource.cloudflare.ts 在 Worker 内从 env.SST_RESOURCE_* 读取链接资源，resource.node.ts 在 Node 下回退到 sst 包并对 KV/Bucket 提供客户端实现。src/… 实际为 resource.cloudflare.ts:4 与 resource.node.ts:9 两个入口，按 exports production/import 条件切换。
- 提供: ['统一 Resource 代理：读取 SST 链接的 secrets/KV/数据库配置（resource.cloudflare.ts:4）', 'Node 环境回退：KV get/put/delete/list、Bucket no-op、Cloudflare API 客户端（resource.node.ts:9）', '条件导出：Cloudflare 与 Node 运行时的资源读取差异屏蔽（package.json exports）']
- **为什么存在（设计意图）**: 用 Proxy 把环境差异隐藏在统一 Resource 门面后：node 侧走 sst 资源绑定 + Cloudflare API 直连，cloudflare 侧走 env 注入，消费方零改动；类型由 sst-env.d.ts 提供。这是运行时可移植性的典型设计——同一套业务代码在本地调试与线上部署共享同一读取接口。
- **改造关联**: 本机未改该包。装配层借鉴了同样的 Proxy 门面思想：amap-lbs-skill 的 config.json 读写封装、vision-interceptor 的 GLM_KEY 环境变量回退（process.env.ZHIPU_API_KEY || 硬编码），都是密钥统一入口 + 环境回退的本地变体。
- **怎么用**: 两文件双环境实现，均导出 Resource Proxy：resource.node.ts 用 sst 的 Resource + cloudflare 官方 SDK（apiToken=CLOUDFLARE_API_TOKEN）提供 KV get/put/delete/list、Bucket put（no-op）；resource.cloudflare.ts 从 cloudflare:workers env（SST_RESOURCE_*）解析同一批资源。消费方统一 import { Resource }，按属性名读取（Resource.STRIPE_SECRET_KEY.value、Resource.UpstashRedisRestUrl.value、Resource.ZEN_LIMITS.value、Resource.AWS_SES_ACCESS_KEY_ID.value 等）。
- **典型场景与协作**: console 全包的配置/密钥注入面：Stripe secret、AWS SES key、Cloudflare token/account、Upstash Redis、GitHub/Google OAuth client、Zen 限额 JSON、Black/Lite 价格表——node（本地/sst shell）与 cloudflare（线上 Worker）两套运行时共用同一属性接口。

## oc-console-support — console-support
- 组: G16-Console | Layer 2
- 作用: 面向支持/客服的内部工具站（SolidStart SSR）。核心功能是用户数据 lookup：src/lib/lookup.ts 按 wrk_/key_/sk-/email 标识查询 workspace、billing、usage、订阅与禁用模型等全量数据，src/routes/lookup.tsx 展示查询结果，src/routes/index.tsx 提供查询表单。全部逻辑直接复用 console-core 的 schema 与 domain。
- 提供: ['按 email/workspace id/API key 查询用户全量数据（src/lib/lookup.ts:41）', 'workspace 详情：users/billing/go/payments/usage/disabledModels 分节（src/lib/lookup.ts:30）', '查询表单与结果展示页面（src/routes/index.tsx、src/routes/lookup.tsx）', '复用 console-core 数据库 schema 与 Black/Lite/Subscription 领域逻辑']
- **为什么存在（设计意图）**: 支持后台与用户前台（console-app）同构（同 SolidStart + console-core），但只暴露 lookup 只读查询——刻意最小化支持工具面；use server + console-core 复用保证查询与前台一致（同一 drizzle schema、同一 Actor 隔离），支持人员无法直接改库。
- **改造关联**: 本机未改。装配层无对应物（客服功能未自建），仅作官方架构参考：最小只读支持后台 + 复用业务 core。
- **怎么用**: SolidStart 客服/后台站点：bun dev = sst shell --stage production -- vite dev（直连生产环境跑本地 dev）；routes/ 仅 index.tsx 与 lookup.tsx 两个页面，src/lib/lookup.ts 用 use server 直接调 console-core 的 drizzle 查询（Auth/User/Workspace/Billing/Payment/Usage/Key/Model 表联查）按 identifier 反查用户/workspace 全量快照。
- **典型场景与协作**: 支持人员用的用户/工作区查找后台：输入邮箱或标识符 → 返回该账号下所有 workspaces（auth、用户、billing、go 计划、支付、用量、禁用模型）。

## oc-core — core
- 组: G6-核心服务 | Layer 2
- 作用: 核心服务层（无根 index.ts，按子路径导出，package.json:18-23 暴露 effect/layer-node、session/runner 等）。实现数据库（src/database/sqlite.ts，drizzle ORM）、会话执行（src/session/runner/index.ts:20-28 从已记录历史执行一次续跑）、配置解析（src/config/* 覆盖 agent/command/mcp/lsp/formatter）、权限策略（src/permission.ts）、事件流（src/event.ts，基于 PubSub/Queue）、文件系统与搜索（src/filesystem/*，含 ripgrep 封装 src/ripgrep.ts:5）。Effect 运行时层见 src/effect/layer-node.ts 与 app-node-builder.ts。
- 提供: ['SQLite 持久化：drizzle schema/迁移（packages/core/src/database/sqlite.ts、migration.ts）', 'Session 执行引擎（packages/core/src/session/runner/index.ts:19-28）', '配置系统：agent/command/mcp/lsp/formatter/plugin 解析（packages/core/src/config/*）', '权限与策略引擎（packages/core/src/permission.ts:5、policy.ts）', '事件总线与持久化事件（packages/core/src/event.ts:3）', '文件系统/ripgrep 搜索/文件监听（packages/core/src/filesystem/*、ripgrep.ts）', 'Effect 服务层组装（packages/core/src/effect/layer-node.ts、app-node-builder.ts）', 'Provider/Model/Catalog/集成认证 领域服务（packages/core/src/provider.ts、catalog.ts、integration.ts）']
- **为什么存在（设计意图）**: 把会话/存储/配置/权限等可复用领域逻辑从 CLI 与 HTTP 层抽离为纯 Effect 服务，供 opencode 主程序、server 包及测试直接注入依赖，实现平台无关的核心（bun/node 双实现见 package.json imports 的 #sqlite/#pty/#fff）。
- **改造关联**: 本机装配层经 config-main 深度改造 core 的运行行为：provider 走 @ai-sdk/deepseek 直连（core/provider 路由）、permission 三层纵深（core/permission 服务）、compaction 参数（core/session 的 compaction）、Reflection 系统的 pending.json 与指令加载；plan/build/explore/general 等 7 个 agent 全部依赖 provider/deepseek 经 core 的模型路由与权限服务。即 core 是被引用最多的官方底座（modified-dag 中 8 个节点依赖它）。
- **怎么用**: ['入口/导出：package.json exports 提供 ./effect/layer-node、./effect/app-node、./session/runner、./system-context 与 ./src/*.ts 通配；src/ 下 90+ 模块（session.ts/event.ts/config.ts/permission.ts/provider.ts/tool-output-store.ts/agent.ts 等）按路径导入。', '关键服务装配：src/effect/layer-node.ts 提供 LayerNode（类型化依赖节点/group 装配），src/effect/app-node.ts 提供 GlobalNode/LocationNode 分类标签；src/session/runner/index.ts:25-33 导出 SessionRunner.Service（run: 从已记录 Session history 续跑一次）。', '无 bin（bin 字段实为顶层 opencode 的声明）；被 opencode/server/tui/sdk-next/app/enterprise 等以 workspace 依赖方式直接 import 服务（如 server/src/routes.ts:3-11 批量 import LayerNode/Database/EventV2/SessionV2 等 10+ 服务）。']
- **典型场景与协作**: core 是产品的能力底座：server 包把它粘成 HTTP 服务（routes.ts 的 applicationServices = LayerNode.group([Database.node, EventV2.node, ...]）），opencode 主程序用它做会话/存储/权限/工具调度，tui 用它做全局状态与安装版本。与 llm 协作（tool-output-store.ts:11 import llm 类型）完成请求-工具循环，与 plugin 协作承载插件运行时，是报告-02 所述会话生命周期与消息处理的实际执行者。

## oc-desktop — desktop
- 组: G10-应用 | Layer 5
- 作用: Electron 桌面壳。src/main/index.ts:15-51 聚合应用生命周期：spawnLocalServer 拉起本地 sidecar 服务、registerIpcHandlers 注册 IPC、createMenu 构建原生菜单、setupAutoUpdater 自动更新、WSL sidecar 管理（wsl/servers.ts）、migrate 数据迁移与 store 清理；src/preload 暴露安全的桥接 API；src/renderer 复用 @opencode-ai/app 渲染 Web UI（renderer/cli.ts:7 通过 window.api.installCli 安装 CLI）。
- 提供: ['Electron 主进程：窗口/菜单/托盘/深链（main/windows.ts、main/menu.ts）', '本地 sidecar server 生命周期管理（main/server.ts spawnLocalServer）', 'IPC 桥与 preload 安全 API（preload/index.ts）', '自动更新（main/updater.ts + electron-updater）', 'WSL 发行版内服务器编排（wsl/）', '背景 CLI 与原生翻译注入（background-cli.ts、native-translations.ts）']
- **为什么存在（设计意图）**: 为 Web UI 提供原生桌面能力（本地服务托管/更新/菜单/WSL），是独立于 @opencode-ai/app 的 Electron 分发层，将浏览器版应用无损提升为桌面应用而不污染 app 包。
- **改造关联**: 属官方底座，本机装配层未引用。官方依赖链：desktop 依赖 @opencode-ai/app + @opencode-ai/ui（package.json:39-40），是 app 包的唯一 Electron 宿主。
- **怎么用**: ['开发/构建：bun predev→electron-vite dev（package.json:14-18）；打包 electron-builder --config（package.json:19-23，main 指向 ./out/main/index.js）', '主进程装配 src/main/index.ts:15-51：spawnLocalServer 拉起 sidecar、registerIpcHandlers、createMenu、setupAutoUpdater、WSL 控制器、migrate 与 store 清理', '渲染进程 src/renderer/index.tsx 复用 @opencode-ai/app（index.tsx:3-17），经 preload 的 window.api 桥（index.tsx:64-321）访问原生能力']
- **典型场景与协作**: 作为独立于 @opencode-ai/app 的 Electron 分发层：主进程管理本地 sidecar server 生命周期（main/server.ts）、原生菜单/深链/更新；渲染进程复用 app 的 AppInterface 只替换平台实现（onboarding.tsx:1-41 用 window.api 判断首次启动）。与 cli 形成双入口：desktop 面向图形用户、cli 面向终端用户，共享同一 server/core 后端。

## oc-effect-drizzle-sqlite — effect-drizzle-sqlite
- 组: G15-存储适配 | Layer 0
- 作用: Drizzle ORM 的 Effect 适配层。src/effect-sqlite/driver.ts:15-60 定义 EffectSQLiteDatabase 与 make()，通过 drizzle 的 SQLiteAsyncDialect + EffectSQLiteSession 把 Drizzle 查询桥接到任意 Effect SqlClient（注释明示可配 @effect/sql-sqlite-node/bun，driver.ts:30-46）；session.ts:35-49 实现 prepareQuery 与 Effect 化事务会话；sqlite-core/effect/ 提供 select/insert/update/delete/raw/count 全套 Effect 化查询构建器；migrator.ts 提供迁移执行。
- 提供: ['EffectSQLiteDatabase 工厂（make()，driver.ts:49）', 'Drizzle↔Effect 会话桥接（EffectSQLiteSession，session.ts:35）', 'sqlite-core 全套 Effect 查询构建器（sqlite-core/effect/ 10 个文件）', '迁移执行器（effect-sqlite/migrator.ts）', 'EffectCache/EffectLogger 默认 Layer（driver.ts:28）']
- **为什么存在（设计意图）**: 让 Drizzle 类型安全的 schema 查询能在 Effect 生态（SqlClient/Stream/Layer）中运行，供核心存储层使用且依赖可注入、可测试，是 core 数据库层的类型安全 + 效果系统双重要求的产物。
- **改造关联**: 属官方底座，本机装配层未引用。官方依赖链：core 的 database/sqlite.ts 使用 drizzle ORM（drizzle-orm 依赖），本包提供其 Effect 化接入面；effect-sqlite-node 是其底层驱动实现。
- **怎么用**: ['exports："."（index.ts 汇总）、./effect-sqlite（driver）、./effect-sqlite/migrator、./sqlite-core/effect（package.json:12-17）；index.ts:1-7 导出 EffectLogger、driver/session 全量与 migrate', '工厂：make()（driver.ts:49-52，Effect.fn 返回 EffectSQLiteDatabase）、makeWithDefaults（driver.ts:75）；会话：EffectSQLiteSession（session.ts:35，prepareQuery + Effect 化事务）、EffectSQLiteTransaction（session.ts:206）', 'migrate（sqlite-core/effect/session.ts:426）执行迁移；查询构建器 sqlite-core/effect/ 提供 select/insert/update/delete/raw/count 全套 Effect 化 API']
- **典型场景与协作**: 作为 Drizzle ORM 与 Effect 生态的桥接层：core 存储层定义 drizzle schema 后，经 make() 桥接到任意 Effect SqlClient（driver.ts:30-46 注释明示可配 @effect/sql-sqlite-node/bun 或本仓库 effect-sqlite-node），使查询以 Effect Effect/Stream/Layer 形式参与依赖注入与测试。

## oc-effect-sqlite-node — effect-sqlite-node
- 组: G15-存储适配 | Layer 0
- 作用: 基于 Node 内置 node:sqlite 的 Effect SqlClient 实现。src/index.ts:49-161 make() 用 DatabaseSync 建立同步连接（WAL 模式、外键约束，index.ts:59-70）、实现 execute/executeRaw/executeValues/executeUnprepared 全套 SqlClient 接口并挂载 Semaphore(1) 串行化（index.ts:132-134）；classifySqliteError 做错误归类（index.ts:15,80-82）；layer() 将 client 同时注册为 SqliteClient 与泛型 Client.SqlClient（index.ts:163-168），并注入 Reactivity.layer。
- 提供: ['Effect SqlClient 的 SQLite 实现（node:sqlite DatabaseSync）', 'WAL/外键/只读/扩展加载等连接配置（SqliteClientConfig，index.ts:32-43）', 'Layer 装配（SqliteClient + Client.SqlClient 双注册，index.ts:163）', 'SQL 错误分类与 Effect 化（classifySqliteError）', 'BigInt 安全读取与 stream 占位（setReadBigInts，index.ts:75）']
- **为什么存在（设计意图）**: 为 opencode 核心提供零原生编译依赖的 Effect 化 SQLite 驱动（复用 node 内置 sqlite），与 @effect/sql-sqlite-node 定位一致但归属仓库自有实现，避免引入外部原生模块、保证跨平台可移植。
- **改造关联**: 属官方底座，本机装配层未引用（本机 opencode 数据走 server 侧 SQLite，未直接 import 此包）。官方依赖链：core 存储层经 drizzle 消费（见 effect-drizzle-sqlite 说明），本包是其底层驱动候选。
- **怎么用**: ['exports "." → ./src/index.ts（package.json:11-13）；核心 API：make(config)（index.ts:49-52，Effect<SqliteClient>，含 filename/readonly/WAL/allowExtension 等配置 index.ts:32-43）与 layer(config)（index.ts:163-168，同时注册 SqliteClient + 泛型 Client.SqlClient 并注入 Reactivity.layer）', 'TypeId 标记 "@opencode-ai/effect-sqlite-node/NodeSqliteClient"（index.ts:20-21）区分服务身份；loadExtension 支持扩展加载（index.ts:26）', '基于 node:sqlite DatabaseSync（index.ts:59-70 WAL/外键），Semaphore(1) 串行化执行（index.ts:132-134），classifySqliteError 做 Effect 错误分类（index.ts:15）']
- **典型场景与协作**: 作为核心存储层的 Effect SQLite 驱动底座：core 的数据库层经 layer() 注入 SqliteClient 服务后，上层只需 Effect.provide 即可获得类型安全 SQL 能力。与 effect-drizzle-sqlite 配合：后者把 Drizzle 查询桥接到任意 Effect SqlClient（含本包实现）。

## oc-enterprise — enterprise
- 组: G10-应用 | Layer 4
- 作用: 基于 SolidStart 的企业版/云端分享服务。src/app.tsx:1-14 用 @opencode-ai/ui 的 Provider（Marked/Dialog/I18n）搭建 SSR 应用根并做 locale 检测；src/routes/api/[...path].ts:1-30 用 Hono + hono-openapi 定义 OpenAPI 文档与 /share 创建端点（zod schema，经 core/share.ts 与 sst Resource 持久化）；routes/share/[shareID].tsx 用 @opencode-ai/session-ui 的 SessionTurn/SessionReview/MessageNav 渲染只读分享会话；core/storage.ts 提供基于 R2 的存储。
- 提供: ['Hono OpenAPI /api 端点（/share 创建、文档，routes/api/[...path].ts:20-27）', '只读分享会话页面（routes/share/[shareID].tsx，复用 session-ui 组件）', 'R2 对象存储封装（core/storage.ts）', 'SSR 应用根与多语言检测（app.tsx:58 detectLocale）', 'cloudflare 部署目标支持（build:cloudflare script）']
- **为什么存在（设计意图）**: 作为云端托管的企业分享服务，复用 ui/session-ui 渲染能力与 core/sdk 数据模型，通过 SolidStart SSR 提供公开只读分享体验；build:cloudflare 目标使同一代码可部署到 CF Workers 边缘。
- **改造关联**: 属官方底座，本机装配层未引用。官方依赖链：enterprise 依赖 ui/session-ui/core/sdk（package.json:16-19），与 app 共享会话渲染层。
- **怎么用**: ['SolidStart 应用：bun dev/build/start（package.json:9-13），build:cloudflare 设 OPENCODE_DEPLOYMENT_TARGET=cloudflare 部署到 CF；shell-prod 经 sst 推生产', '应用根 src/app.tsx:1-14：用 ui 的 I18nProvider/DialogProvider/MarkedProvider/Font 组装 SSR 根并 detectLocaleFromHeader（app.tsx:25-30）；API 路由 routes/api/[...path].ts:1-30 用 Hono + hono-openapi 定义 OpenAPI 与 /share 创建端点', '分享页 routes/share/[shareID].tsx 复用 @opencode-ai/session-ui 的 SessionTurn/SessionReview/MessageNav 渲染只读会话；存储走 core/storage.ts（R2）']
- **典型场景与协作**: 作为云端托管的企业分享服务：SSR 渲染只读分享会话 + Hono OpenAPI 端点创建分享，经 function 包（Durable Object WebSocket 同步）与 web 包（分享页展示）形成完整分享生态。典型链路：app 内点分享→enterprise /api 创建→function 同步→web /s/[id] 展示。

## oc-function — function
- 组: G13-边缘服务 | Layer 0
- 作用: Cloudflare Workers 上的会话分享同步服务。src/api.ts:15-114 定义 SyncServer Durable Object：WebSocket 订阅连接（fetch 握手 101 + ctx.acceptWebSocket，api.ts:20-37）、publish 将 session/info|message|part 变更写入 R2 Bucket 并广播给订阅者（api.ts:45-66）、share/assertSecret/clear 管理分享密钥与数据清理；Hono 路由提供 /share_create、/share_delete、/share_sync 等端点（api.ts:116-150）。
- 提供: ['Durable Object 实时同步（WebSocket 广播 session 变更）', 'R2 持久化分享数据（publish 写入 Bucket，api.ts:55）', '分享密钥管理（share/assertSecret，api.ts:68-92）', 'Hono HTTP API（share_create/share_delete/share_sync）', 'GitHub App 认证（@octokit/auth-app 依赖）']
- **为什么存在（设计意图）**: 作为云端分享的后端同步服务，利用 Cloudflare Durable Object 的 WebSocket 能力实现跨客户端实时会话同步，与 function 名（FaaS 云端函数）对应；R2 做持久化、secret 做访问控制。
- **改造关联**: 属官方底座，本机装配层未引用（本机无 Cloudflare 环境）。与 oc-enterprise、oc-web 组成官方云端分享三件套，本机离线部署不需要。
- **怎么用**: ['Cloudflare Workers 部署（sst 管理，src/api.ts:1-7 import sst Resource + cloudflare:workers）；Hono 入口 src/api.ts:116-150 暴露 POST /share_create、/share_delete、/share_delete_admin、/share_sync 与 GET /share_poll（WebSocket 升级）、/share_data', 'SyncServer Durable Object（api.ts:15-114）：fetch 握手 101 + acceptWebSocket 订阅（api.ts:20-37）、publish 校验 session 前缀后写 R2 Bucket 并广播（api.ts:45-66）、share/assertSecret/clear 管理密钥与清理（api.ts:68-109）', '环境变量注入：Env 类型要求 SYNC_SERVER（DO namespace）、Bucket（R2）、WEB_DOMAIN（api.ts:9-13）']
- **典型场景与协作**: 作为云端分享的后端同步服务：enterprise 的 /share 创建端点调用 function 的 share_create 生成密钥，分享页订阅 WebSocket 经 share_poll 实时接收 session 变更广播，数据落 R2 供 web 分享页拉取。与 web/enterprise 构成完整云端分享闭环。

## oc-http-recorder — http-recorder
- 组: G14-工具 | Layer 0
- 作用: HTTP 录制/回放工具（package.json:5 描述：Record and replay Effect HTTP client traffic with deterministic cassettes）。src/effect.ts:16-25 提供带录制能力的 HttpClient Layer；src/recorder.ts:11-18 resolveAutoMode 决定 record/replay/passthrough 模式（CI 强制 replay）；src/cassette.ts 实现 cassette 文件存储；src/redactor.ts 负责敏感信息脱敏；src/websocket.ts:10-31 支持 WebSocket 录制回放。
- 提供: ['HTTP 客户端录制层（packages/http-recorder/src/effect.ts:16-25）', 'cassette 录制文件格式与存储（packages/http-recorder/src/cassette.ts）', '自动模式：record/replay/passthrough（packages/http-recorder/src/recorder.ts:11-18）', '请求匹配（packages/http-recorder/src/matching.ts）', '敏感信息脱敏（packages/http-recorder/src/redactor.ts）', 'WebSocket 录制回放（packages/http-recorder/src/websocket.ts:10-31）']
- **为什么存在（设计意图）**: 作为测试基础设施：让 LLM 请求与 HTTP 流量可确定性回放（VCR 模式），保证 CI 中测试不依赖网络与真实 token 计费；被 core/llm 的测试与开发流程引用。
- **改造关联**: 本机未直接引用 http-recorder（装配层不做 LLM 请求录制，成本优化走 DeepSeek prefix-cache 而非 VCR 回放），属官方底座；本机在测试/复现需求上以 config 级缓存（cache_read 0.003625）替代录制方案，二者是同一「降本/确定性」目标的不同路径。
- **怎么用**: ['入口：src/index.ts:1-11 —— export const HttpRecorder = { http, socket }（HTTP + WebSocket 双通道录制）；namespace 导出 CassetteMetadata/RecorderOptions/RedactOptions/RequestMatcher/RequestSnapshot 类型。', '用法（README.md:8-21）：@effect/vitest 测试中把 HttpClientRequest 挂上 recorder 录制成 JSON cassette，测试时确定性回放（VCR 模式）；redaction.ts/redactor.ts 提供密钥/头脱敏。', '依赖仅 @effect/platform-node(-shared)，Node 22+/Bun；核心文件 cassette.ts（cassette 读写）、matching.ts（请求匹配）、recorder.ts、socket.ts/websocket.ts。']
- **典型场景与协作**: http-recorder 是测试基础设施：llm 的 devDependency 引它（llm/package.json），使 LLM provider 请求（HTTP/WS 双通道）可录制回放，CI 中测试不依赖网络、不产生真实 token 计费；redact 机制保证录制文件不含密钥。core/llm 的开发与测试流程（报告-03 的请求链路分析依赖可复现请求）均受益。

## oc-llm — llm
- 组: G5-LLM请求层 | Layer 1
- 作用: LLM 请求/协议层。src/index.ts:1-28 导出 LLMClient/Auth/Provider/Tool/ToolRuntime；核心 LLM 门面 src/llm.ts:45-48 提供 generate/stream 等请求方法。src/route/client.ts:29-49 定义 Route 结构（provider+protocol+endpoint+auth+transport）与 RequestExecutor；src/route/transport/http.ts、websocket.ts 实现 HTTP/WS 传输。内置 8 个 provider（src/providers/：anthropic、openai、google、azure、amazon-bedrock、openrouter 等，package.json:17-28）与 6 个协议适配（src/protocols/：anthropic-messages、openai-chat、openai-responses、gemini、bedrock-converse，package.json:29-35）。
- 提供: ['统一 LLM 客户端门面 generate/stream（packages/llm/src/llm.ts:45）', 'Route 路由抽象：endpoint/auth/transport/body schema（packages/llm/src/route/client.ts:36-48）', 'HTTP 与 WebSocket 传输层（packages/llm/src/route/transport/http.ts、websocket.ts）', '多提供商适配：OpenAI/Anthropic/Google/Azure/Bedrock/OpenRouter/xAI 等（packages/llm/src/providers/）', '多协议编解码：chat/responses/messages/gemini/bedrock（packages/llm/src/protocols/）', 'Tool 定义与执行运行时（packages/llm/src/tool.ts、tool-runtime.ts）', '上下文溢出检测（packages/llm/src/provider-error.ts:4）']
- **为什么存在（设计意图）**: 将多提供商/多协议的请求差异隔离在路由与协议适配层之下，向上提供单一 LLM 门面，支持 HTTP/WS 双通道并可被 http-recorder 录制回放（llm devDependency 依赖 recorder）。
- **改造关联**: 本机经 config-main 深度改造 llm 的 provider 侧：provider.deepseek 用 @ai-sdk/deepseek（baseURL https://api.deepseek.com/v1、超时 300/120/60s、daily/deep 双 variant + 成本表 cache_read 0.003625），plan/build 与 5 子 agent 全部经此路由；即本机不是改 llm 源码，而是通过配置层为 llm 提供 DeepSeek provider 与模型路由策略（modified-dag 中 agent-plan/agent-build 的 depends_on provider/deepseek）。
- **怎么用**: ['入口：src/index.ts 导出 LLMClient、Auth、Provider、Tool/ToolRuntime、LLM 命名空间与 schema 全量；核心 API 是 LLM.generate / LLM.stream（src/llm.ts:88-89 直通 LLMClient.generate/stream）。', '子路径导出（package.json exports 21 项）：./route（Route/LLMClient/Transport/Protocol/Framing/Endpoint）、./provider（ProviderDefinition）、./providers/*（Anthropic/OpenAI/Google/Bedrock/OpenRouter/XAI 等 14 家）、./protocols/*（openai-chat/openai-responses/anthropic-messages/gemini/bedrock-converse 等）。', '典型调用：llm.ts:31-37 定义 RequestInput（system/prompt/messages/tools/toolChoice/generation/providerOptions），generate/stream 以它发起一次请求；tool.ts 与 tool-runtime.ts 提供工具定义与派发（toDefinitions/ToolRuntime）。']
- **典型场景与协作**: llm 是模型接入的统一门面：core 的会话执行（session/llm.ts）经它向 DeepSeek/Anthropic/OpenAI 等发请求，opencode 主程序在 providers 命令中用它枚举模型（src/cli/cmd/providers.ts）。报告-03 的完整请求链路（route 选择→protocol 适配→framing→transport HTTP/WS）与缓存策略（cache-policy.ts）即本包的核心机制；devDependency 引 http-recorder 使请求可录制回放。

## oc-opencode — opencode
- 组: G19-主入口 | Layer 4
- 作用: 主应用/CLI 入口。src/index.ts:45 用 yargs 装配 run/serve/tui/agent/acp 等全部子命令；src/cli/tui/layer.ts:1 经 @opencode-ai/tui 拉起终端 UI；src/server/server.ts:4-13 组装 Node HTTP/WebSocket 服务器与 HttpApi 路由。会话编排由 src/session/processor.ts:26-27 驱动（回退 LLM、工具调度），工具清单在 src/tool/registry.ts:4-16 注册（read/edit/shell/glob/grep/webfetch 等 20+ 内置工具）。
- 提供: ['CLI 入口：yargs 子命令体系（run/serve/tui/agent/acp/github 等 20+ 命令，packages/opencode/src/index.ts:45）', 'HTTP/SSE/WebSocket 服务器实例（packages/opencode/src/server/server.ts:27-30）', '会话处理器：消息输入→LLM 请求→工具执行的编排循环（packages/opencode/src/session/processor.ts:32）', '内置工具集：read/write/edit/shell/glob/grep/task/webfetch 等（packages/opencode/src/tool/registry.ts:4）', 'Session 状态机、compaction/retry/summary/reminders 生命周期（packages/opencode/src/session/*）', '插件宿主：加载外部 plugin 与 provider 扩展（packages/opencode/src/plugin/index.ts:8）', 'Code Mode 工具桥接（packages/opencode/src/tool/code-mode.ts:4）']
- **为什么存在（设计意图）**: 作为可分发 CLI 二进制（bin/opencode）聚合所有上层能力，把核心服务、LLM、TUI、协议编排成终端可执行产品，同时保持与 server 分离以便 web/desktop 前端复用同一套服务。
- **改造关联**: 本机装配层未直接引用 opencode 包本体，但 config-main（opencode.jsonc）正是 opencode 的运行时配置（provider/@ai-sdk/deepseek 直连、permission 三层纵深、compaction、skills.paths、7 agent 装配），plan/build 及其 prompt 通过 opencode 的 instructions 段注入 auto-mode.md 与 MEMORY.md；即本机以「配置 + 插件 + 指令」方式改造 opencode 行为而非改源码。
- **怎么用**: ['入口：bin/opencode（packages/opencode/bin/opencode:1-30）——spawn 真实入口子进程并转发信号；源码入口 src/index.ts:44-126 用 yargs 组装命令树，注册 run/generate/serve/agent/mcp/tui/attach/session/db/plugin/export/import/github/pr/models/stats 等 20+ 子命令（src/index.ts:81-103），.strict() 强制精确命令。', '导出 API：package.json bin: {opencode: ./bin/opencode}，exports 映射 ./src/*.ts；dev 模式 bun run --conditions=browser ./src/index.ts。主要子命令入口在 src/cli/cmd/（serve.ts/run.ts/agent.ts/tui.ts 等 25 个）。', '核心聚合：src/index.ts:11-27 import InstallationVersion 与全部 Command 类，把 core（会话/存储）、llm（LLM 门面）、tui（终端 UI）、server（HTTP 服务）、plugin/codemode/sdk/protocol/schema 全部编排进 CLI 进程。']
- **典型场景与协作**: opencode 是产品的总装线：用户敲 opencode serve 拉起 HTTP 服务（src/cli/cmd/serve.ts），敲 opencode run 进入会话执行（src/session/ 目录的 session.ts/processor.ts/llm.ts/compaction.ts 驱动完整 agent 循环）；TUI 由 cli/ui.ts 或 tui 命令加载 @opencode-ai/tui（src/cli/cmd/tui.ts）。与 core 协作提供领域服务、与 llm 协作做模型请求、与 server 协作暴露 HTTP/SSE、与 protocol/schema 共享契约。

## oc-plugin — plugin
- 组: G7-插件SDK | Layer 1
- 作用: 插件 SDK。src/index.ts:20-80 定义 Plugin/PluginInput/Config/Hooks 等公共类型，基于 @opencode-ai/sdk 客户端访问服务；src/tool.ts:3-20 定义 ToolContext/ToolResult。提供 v2 双运行时：effect 版（src/v2/effect/：plugin/context/agent/command/skill/catalog/integration/filesystem/event 等 14 模块）与 promise 版（src/v2/promise/），并含 TUI 插件类型（src/tui.ts:1-40 基于 @opentui）。
- 提供: ['插件公共类型与 Hooks 契约（packages/plugin/src/index.ts:20-80）', '工具 API：ToolContext/ToolDefinition/ToolResult（packages/plugin/src/tool.ts:3-20）', 'Effect 原生 v2 插件 API：agent/command/skill/catalog/integration 注册（packages/plugin/src/v2/effect/plugin.ts）', 'Promise 风格 v2 插件 API（packages/plugin/src/v2/promise/index.ts）', 'TUI 插件接口（基于 @opentui，packages/plugin/src/tui.ts:19-33）', 'shell 工具封装（packages/plugin/src/shell.ts）']
- **为什么存在（设计意图）**: 作为第三方扩展的稳定 SDK 面（发布到 npm，files 只含 dist），把 opencode 对插件的实现细节隔离在 core 内部，对外只暴露类型化、版本化的注册 API。
- **改造关联**: 本机直接引用：plugin-vision-interceptor 依赖 @opencode-ai/plugin 的 server export 接口，通过 chat.message + experimental.chat.messages.transform 双钩子实现 VLM 双通道（付费 glm-4.6v 优先 + 429 降级免费 glm-4.6v-flash + processedImages 内存缓存防重复扣费）；这是本机唯一一个以官方插件 SDK 编写并挂载进装配层的组件，是官方包「接口化改造」的典型。
- **怎么用**: ['入口：src/index.ts 定义插件类型面（ProviderContext/WorkspaceAdapter/ToolDefinition/TUI 类型等）并 re-export tool.js；导出路径 ./tool、./tui、./v2/effect（v2/effect/plugin、v2/effect/integration）、./v2/promise。', '插件写法：export server(ctx) 挂钩子（如 plugin-vision-interceptor 的 chat.message 与 experimental.chat.messages.transform）；ToolContext（src/tool.ts:1-24）提供 sessionID/messageID/agent/directory/worktree/abort/metadata/ask；tui.ts 提供 TUI 渲染插槽类型（@opentui/core 的 Renderable/SlotMode）。', 'v2 面：src/v2/effect/plugin.ts + registration.ts 提供 Effect 原生插件注册与生命周期（agent/command/event/fs/location/reference/skill 等子模块），发布到 npm（files 只含 dist）。']
- **典型场景与协作**: plugin 是第三方扩展面：core 内部承载插件运行时，tui 经 ./tui 暴露 UI 插槽，opencode 主程序加载插件配置。本机正是它的直接使用者——plugin-vision-interceptor（modified-dag 中 depends_on_raw: '@opencode-ai/plugin（server export 接口）'）用双钩子把图片转 VLM 文字再送 LLM，是报告-01 分析的 VLM 双通道的核心实现。

## oc-protocol — protocol
- 组: G2-通信协议 | Layer 1
- 作用: 通信协议层。src/api.ts:26-86 用 effect/unstable/httpapi 定义 OpenCode HttpApi 结构：注册 Health/Location/Agent/Session/Message/Model/Provider/Integration/Credential/Permission/FS/Command/Skill/Event/Pty/Question/Reference/ProjectCopy 共 18 个 Group（src/api.ts:38-55），并挂 Authorization/SchemaError 中间件（src/api.ts:63-64）。src/errors.ts:3-40 定义带 httpApiStatus 的 TaggedError（400/401/409/503 等）。src/groups/* 按资源定义端点与契约，middleware/authorization.ts:4-6 定义 Authorization 服务。
- 提供: ['OpenCode HttpApi 协议定义（packages/protocol/src/api.ts:37-55）', '18 个资源端点组（packages/protocol/src/groups/*）', '统一错误契约（httpApiStatus 标注，packages/protocol/src/errors.ts:3-40）', 'Authorization/SchemaError 中间件契约（packages/protocol/src/middleware/）', 'OpenAPI 注解（packages/protocol/src/api.ts:56-62）']
- **为什么存在（设计意图）**: 协议与实现分离：protocol 只声明端点/中间件/错误的契约（server 注入具体服务身份，见 src/api.ts:25 注释），使 server、client、cli 对同一协议的不同实现方共享同一类型面。
- **改造关联**: 本机未直接引用 protocol（vision 插件与 agent 都不触碰协议层），属官方底座；本机改造全部发生在协议「之上」的配置/插件层，协议契约保持不变，从而 server/client/sdk 三端自动同步。
- **怎么用**: ['入口：src/api.ts:1-38 —— 用 Effect HttpApi 声明完整端点树：makeApiFromGroup 聚合 HealthGroup/LocationGroup/AgentGroup/SessionGroup/MessageGroup/ModelGroup/ProviderGroup/PermissionGroup/EventGroup/PtyGroup/QuestionGroup/ReferenceGroup/IntegrationGroup/CredentialGroup/ProjectCopyGroup 等 19 个 group；src/api.ts:25 注释明示「Protocol 拥有中间件位置，Server 注入具体 key」。', '导出：package.json exports ./src/*.ts；src/errors.ts 定义协议级错误类型；依赖仅 @opencode-ai/schema + effect（纯契约层）。', '消费方：server/src/api.ts:1-3 makeDefaultApi 绑定中间件；client 的生成器读 server/api 编译出客户端（client/README.md:14-15）。']
- **典型场景与协作**: protocol 是协议契约的单一所有权者：server 注入中间件/服务实现，client 从同一份协议编译客户端，cli 也消费同一类型面——三方对同一协议的不同实现共享同一契约，避免端点 drift。报告-02 所述消息/事件的 HTTP+SSE 传输模型即由 EventGroup/SessionGroup 等声明。

## oc-schema — schema
- 组: G1-数据模型 | Layer 0
- 作用: 纯类型/数据模型包，仅依赖 effect（package.json:14-16）。以 Effect Schema 定义全部领域类型：Session/SessionInput/SessionMessage（src/session*.ts）、Event 与 Durable 事件清单（src/event.ts、event-manifest.ts、durable-event-manifest.ts）、Provider/Model（src/provider.ts、model.ts）、Permission、Prompt、Agent 等 40+ 模型。src/index.ts:1-28 统一 re-export；src/schema.ts:3-10 提供 AbsolutePath/RelativePath/DateTimeUtc 等基础 branded schema。
- 提供: ['领域数据模型：Session/Message/Event/Permission/Provider/Model 等（packages/schema/src/index.ts:1-28）', 'Effect Schema 编解码与校验基础（packages/schema/src/schema.ts:3-30）', '事件定义清单：Event/EventManifest/Durable（packages/schema/src/event.ts、durable-event-manifest.ts）', 'V1 兼容模型（packages/schema/src/v1/session.ts、question.ts、permission.ts）']
- **为什么存在（设计意图）**: 作为依赖链最底层的单一事实源，所有包共享同一套 Effect Schema 数据契约，保证类型与运行时校验一致，避免跨包重复定义与 drift。
- **改造关联**: 本机装配层未直接引用 schema（plugin-vision-interceptor 用的是 @opencode-ai/plugin 的 server export，经插件 SDK 间接消费 schema 的 Event/Part 类型），属官方底座；但 vision 插件把图片 part 转文字的核心修复（experimental.chat.messages.transform）正是作用于 schema 定义的 message part 结构——改造发生在数据契约之上而非之内。
- **怎么用**: ['入口：src/index.ts:1-28 统一 re-export 40+ 模型（Agent/Command/Event/Session/SessionMessage/Provider/Model/Permission/Prompt/Skill/Question 等）；src/schema.ts:3-10 提供 AbsolutePath/RelativePath/DateTimeUtc 等基础 branded schema。', "导出：package.json exports {'.': ./src/index.ts, './*': ./src/*.ts}，仅依赖 effect。所有领域类型都是 Effect Schema（运行时校验 + 类型推导二合一），可被任意包按路径导入单个模型（如 @opencode-ai/schema/event）。"]
- **典型场景与协作**: schema 是依赖链最底层的单一事实源：llm/protocol/core/client/app 全部以它为数据契约（official-dag 中 6 个节点直接依赖）。协议端点的请求/响应类型、事件清单、session 消息模型都由它定义，报告-02 对 SessionMessage/Part 的逐字段分析即基于该包；改契约只需改 schema 一处，各包类型与运行时校验自动对齐。

## oc-script — script
- 组: G14-工具 | Layer 0
- 作用: 构建/发布脚本共享工具包。src/index.ts:5-76 读取仓库根 package.json 校验 bun 版本（semver.satisfies 检查，index.ts:16-18）、按环境变量/分支/registry 计算发布 channel（latest/preview）与 version（含 +1 patch 逻辑，index.ts:34-48）、从 .github/TEAM_MEMBERS 加载团队成员名单（index.ts:50-58），最终导出 Script 对象（channel/version/preview/release/team）供发布流水线使用。
- 提供: ['发布版本计算（channel/version/preview，基于 env/分支/npm registry）', 'Bun 版本校验（强制 ^packageManager 版本，index.ts:16）', '团队成员名单加载（.github/TEAM_MEMBERS 解析，index.ts:50）']
- **为什么存在（设计意图）**: 将发布流程共用的版本决策逻辑从 CI 脚本中抽离为可 import 的库，保证多个发布任务（channel 判断、bump 语义）行为一致，是官方发布流水线的单一事实源。
- **改造关联**: 属官方底座，本机装配层未引用（本机不跑官方发布流水线）。官方依赖链：cli 的 devDependencies 引用 @opencode-ai/script（package.json:31）。
- **怎么用**: ['exports "." → ./src/index.ts（package.json:12-14），作为发布脚本库被 cli 的 script/build.ts:3 import 使用（$ 从 bun、Script.version/channel 参与构建）', 'src/index.ts:5-76 读取仓库根 package.json 校验 bun 版本（:16-18 semver.satisfies）、按 env/分支/registry 计算 channel（latest/preview，:26-32）与 version（含 +1 patch 逻辑，:34-48）、加载 .github/TEAM_MEMBERS 团队成员（:50-58）', 'env 控制：OPENCODE_CHANNEL/OPENCODE_BUMP/OPENCODE_VERSION/OPENCODE_RELEASE（:20-25）']
- **典型场景与协作**: 作为构建/发布共享工具库：cli 构建时用它算 channel/version 决定产物命名（script/build.ts:81 execArgv --user-agent lildax/{Script.version}），CI 流水线用它做 bump 语义与发布渠道决策。任何发布相关任务先经它统一版本决策，避免各脚本口径不一致。

## oc-sdk — sdk
- 组: G3-客户端 | Layer 0
- 作用: 官方 JS 客户端 SDK（packages/sdk/js/）。src/index.ts:1-21 导出 client/server 并通过 createOpencode 同启；src/client.ts:33-50 createOpencodeClient 基于 @hey-api 生成的 gen/sdk.gen.ts（v2 版 src/v2/gen/sdk.gen.ts:7077 class OpencodeClient）并注入 directory header 重写；src/server.ts:22-40 createOpencodeServer 用 cross-spawn 拉起 opencode serve 子进程并等待监听。v2 子目录提供新一代 client/server/data 导出（src/v2/index.ts:1-23）。
- 提供: ['类型化 HTTP 客户端 createOpencodeClient（packages/sdk/js/src/client.ts:33）', '服务端启动助手 createOpencodeServer（spawn opencode serve，packages/sdk/js/src/server.ts:22）', '一体化 createOpencode（packages/sdk/js/src/index.ts:8-21）', 'V2 代客户端/服务端 API（packages/sdk/js/src/v2/client.ts、server.ts）', '从 openapi.json 生成的完整类型与 SDK（packages/sdk/js/src/v2/gen/sdk.gen.ts）']
- **为什么存在（设计意图）**: 对外发布（npm 包）的官方 SDK，将 opencode 内部 server 的 openapi.json 编译为类型安全的客户端，同时提供进程级 server 托管，供第三方应用与 plugin 使用。
- **改造关联**: 本机未直接引用 sdk（vision 插件经 @opencode-ai/plugin 消费类型，agent 经 CLI/HTTP 而非 SDK 连接），属官方底座；本机的改造接口是配置层（opencode.jsonc）与插件层（plugin-vision-interceptor），不触及 SDK 客户端面。
- **怎么用**: ['入口：sdk/js/src/index.ts；核心 client 工厂 createOpencodeClient(config)（src/client.ts:55-76，把 directory 注入 x-opencode-directory 头并 wrap 错误）；类型面 re-export 自 src/gen/（openapi.json 编译产物）。', '导出（package.json exports）：./client、./server、./v2、./v2/client、./v2/gen/client、./v2/server、./v2/types；server.ts:17-40 createOpencodeServer(options) 用 cross-spawn 拉起 opencode serve 子进程（hostname/port/signal 托管），process.ts 提供 stop/bindAbort（win32 下 taskkill 树杀）。', 'v2：src/v2/client.ts、src/v2/server.ts、src/v2/data.ts、src/v2/index.ts 提供 Effect 原生类型面（plugin/tui/enterprise/slack 均消费 @opencode-ai/sdk/v2）。']
- **典型场景与协作**: sdk 是官方对外发布（npm）的客户端：第三方应用用 createOpencodeClient 连远程 server、用 createOpencodeServer 进程内托管本地服务；plugin 包 import 它做 SDK 类型（plugin/src/index.ts:1-12），tui/enterprise/slack 均依赖（official-dag 中 8 个反向引用）。报告-03 对请求链路/缓存的分析中 SDK 出现 40 次，是协议端到端消费的关键路径。

## oc-sdk-next — sdk-next
- 组: G3-客户端 | Layer 4
- 作用: Effect 原生的进程内 OpenCode host SDK（过渡包，替代生成式 @opencode-ai/sdk）。src/opencode.ts 的 create() 用 AppNodeBuilder 构建 ApplicationTools/PermissionSaved 上下文，把 server 的 createEmbeddedRoutes 编译成 Web handler 并注入内存 fetch，客户端由此在进程内执行全部路由而无需监听端口/网络 I/O。src/index.ts 聚合 OpenCode 与 Tool 模块并再导出 client 的 Effect 类型。
- 提供: ['进程内 OpenCode host：OpenCode.create()（src/opencode.ts:10）', '内存路由执行：Server router → Web handler → fetch（src/opencode.ts:20-38）', '本地工具注册 tools.register（走 ApplicationTools 服务，src/opencode.ts:41）', 'DI Layer：OpenCode.layer/Service（src/opencode.ts:47,49）', 'Tool 门面：Failure/RegistrationError/make 再导出（src/tool.ts:1）', 'Effect client 类型再导出（ClientError/Session/Model 等，src/index.ts:4）']
- **为什么存在（设计意图）**: 把 HTTP 服务抽象成可内存执行的 fetch handler，是 Effect 生态服务即组合的体现：客户端与服务器共享同一路由定义，测试无需起端口；ApplicationTools/PermissionSaved 以 Layer 注入，宿主可注册自定义工具并随 Scope 关闭释放资源。
- **改造关联**: 本机未改。装配层没用 sdk-next，但本机自定义工具/插件机制（plugins/vision-interceptor.js 的 chat.message + experimental.chat.messages.transform 钩子）与 host 内嵌、挂载钩子的宿主模式同源。
- **怎么用**: import { OpenCode } 后 OpenCode.create() 在进程内把 @opencode-ai/server 的 HttpRouter（createEmbeddedRoutes）经 HttpRouter.toWebHandler 转成 fetch 处理器，再用 @opencode-ai/client/effect 的 OpenCode.make({baseUrl:http://opencode.local}) + FetchHttpClient.layer 把请求打到内存 handler——零监听端口零网络 IO，完整保留路由/中间件/handler/codec/error。同时导出 Tool 命名空间（tools.register 走 Core 的 ApplicationTools 服务）与 ClientError/AbsolutePath/Model/Provider 等 Effect 类型；提供 OpenCode.layer 供依赖注入。
- **典型场景与协作**: 进程内嵌式 opencode 宿主：单元测试（sessions.get/prompt/interrupt/events 重放）、桌面端/插件宿主把 opencode 作为库而非服务调用；README 明示 transitional package，将替代生成的 @opencode-ai/sdk。

## oc-server — server
- 组: G4-服务端 | Layer 3
- 作用: HTTP/SSE 服务器实现层。src/api.ts:5-8 用 @opencode-ai/protocol/api 的 makeDefaultApi 装配 HttpApi，并注入 LocationMiddleware/SessionLocationMiddleware 具体中间件；src/routes.ts:1-13 把 core 的各类服务（SessionV2/SessionExecution/LocationServiceMap/Database/ToolOutputStore 等）装配为 Effect Layer；src/handlers.ts:1-40 合并 19 个 handler（session/message/agent/model/provider/fs/event/pty 等），每个 handler 将 HTTP 请求桥接到 core 领域服务。
- 提供: ['HttpApi 装配与中间件注入（packages/server/src/api.ts:5-8）', '19 个资源 handler（packages/server/src/handlers.ts:21-40）', 'core 服务到 HTTP 层的 Effect Layer 桥接（packages/server/src/routes.ts:1-13）', '授权/会话定位中间件（packages/server/src/middleware/authorization.ts、session-location.ts）', 'CORS 与 auth 基础（packages/server/src/cors.ts、auth.ts）']
- **为什么存在（设计意图）**: 把 Effect HttpApi 与 core 领域服务粘合为可运行的 HTTP 服务（不依赖 CLI），使 opencode 主程序、sdk createOpencodeServer 与其他宿主都能复用同一套服务端装配。
- **改造关联**: 本机未直接修改/引用 server 源码，但运行时通过它承载装配层：config-main 的 model 路由（provider/deepseek）与权限配置最终经 server 的 HTTP 层暴露给所有 agent 调用；本机对服务端的影响是「配置注入」（OPENCODE_CONFIG_CONTENT 式的 config 覆盖 + 权限 deny/allow），而非替换服务实现。
- **怎么用**: ['入口：src/api.ts:1-6 —— Api = makeDefaultApi({locationMiddleware, sessionLocationMiddleware})，把 @opencode-ai/protocol/api 声明的协议绑定上具体中间件；src/routes.ts:1-16 组装 applicationServices = LayerNode.group([...10+ 服务]) 并 createRoutes/createEmbeddedRoutes 两个工厂（带/不带 password 认证）。', '导出：package.json exports ./src/*.ts；依赖仅 @opencode-ai/core、@opencode-ai/protocol、drizzle-orm、effect（不依赖 CLI）。被 opencode serve 命令、sdk createOpencodeServer、sdk-next 的 createEmbeddedRoutes（进程内内存路由）三方复用。', '服务端实现：src/handlers.ts、src/auth.ts、src/cors.ts、src/pty-environment.ts 提供具体 handler/认证/CORS/PTY 环境。']
- **典型场景与协作**: server 把 core 领域服务粘合成可运行的 HTTP 服务：routes.ts 里 LayerNode.group 注入 Database/EventV2/SessionV2/PermissionSaved/PtyTicket 等 10+ 服务，协议中间件（authorization/schema-error/session-location）在此装配。opencode 主程序经 serve 子命令启动它，sdk/sdk-next 进程内复用它（createEmbeddedRoutes 无端口跑内存 fetch）；报告-02 所述 HTTP/SSE 通信骨架即本包 + protocol 的组合。

## oc-session-ui — session-ui
- 组: G9-UI组件 | Layer 3
- 作用: 会话级 UI 组件集，介于基础组件库与完整应用之间。src/components/ 提供 SessionTurn、SessionReview、MessagePart、message-file、session-diff、line-comment 等会话渲染组件，并含 markdown 流式渲染整套管线（markdown-stream.ts + markdown-worker.ts + markdown-cache.tsx，用 Worker 实现增量渲染）；src/pierre/ 提供 file-find/file-selection/diff-selection/media 等代码交互原语；src/context/data.tsx 提供会话数据 Provider（被 enterprise share 页复用）。
- 提供: ['SessionTurn/SessionReview 会话轮次与评审组件', 'MessagePart/message-file/session-diff 消息部件与差异展示', 'Markdown 流式渲染管线（worker + stream + cache，markdown-stream.ts:12）', '文件查找/选择/差异选择交互原语（pierre/ 目录）', '会话数据 context（context/data.tsx）', 'PromptInput v2 输入框（v2/components/prompt-input/）']
- **为什么存在（设计意图）**: 把会话级渲染（消息/轮次/评审/markdown 流）从 app 中剥离，使 app 与 enterprise 共享同一套会话表达，避免重复实现；pierre/ 目录进一步抽象代码交互原语供应用层装配。
- **改造关联**: 属官方底座，本机装配层未引用。官方依赖链中同时被 oc-app 与 oc-enterprise 依赖（package.json 均列 @opencode-ai/session-ui workspace:*），是分享场景的公共渲染源。
- **怎么用**: ['会话级组件子路径导入：package.json:7-25 exports 提供 ./session-diff、./message-file、./message-part-text、./markdown-stream、./markdown-cache、./line-comment-styles、./pierre/*、./context/* 等，app 与 enterprise 直接复用（app/src/app.tsx:6 import File from @opencode-ai/session-ui/file）', 'markdown 流式渲染管线：markdown-stream.ts + markdown-worker.ts + markdown-cache.tsx 组合（Worker 增量渲染），app 的会话页经 context/data.tsx Provider 消费', 'PromptInput v2：./v2/prompt-input（index/interaction/store/types）新一代输入框子路径导出']
- **典型场景与协作**: 作为 app（桌面/Web 会话页）与 enterprise（只读分享页 routes/share/[shareID].tsx 复用 SessionTurn/SessionReview/MessageNav）共同依赖的会话表达层：app 渲染完整可交互会话，enterprise 用同一套组件渲染只读分享，避免两处重复实现会话 UI。

## oc-slack — slack
- 组: G18-集成 | Layer 1
- 作用: Slack 机器人集成（@slack/bolt Socket Mode）。src/index.ts 创建 opencode 服务端实例（createOpencode）与 Slack App，按 channel+thread 键复用 session：首次消息创建 opencode session 并分享链接，后续消息走 session.prompt；同时订阅 message.part.updated 事件把 tool 完成状态回贴到 thread（src/index.ts:24-51）。
- 提供: ['Slack Socket Mode 机器人（src/index.ts:4）', '每 thread 独立 opencode session 的创建/复用（src/index.ts:22,70-101）', '会话分享链接回帖（src/index.ts:96）', 'tool 执行状态回帖（message.part.updated 订阅，src/index.ts:24-51）', '/test 命令与错误兜底回复（src/index.ts:138）']
- **为什么存在（设计意图）**: 用 Socket Mode（无需公网回调）降低自托管门槛；一线程一会话的隔离保证多用户并发互不干扰；SDK（@opencode-ai/sdk）直连 server 复用完整会话/工具/分享协议，bot 只做 Slack 协议↔opencode 协议的翻译层。
- **改造关联**: 本机未改，且本机装配层刻意绕开 Slack（MEMORY 中飞书为协同入口，lark-suite skill 覆盖消息/日历/文档）。slack 包是官方 IM 接入参考：本机 lark-suite + lark-cli 即同类聊天平台↔AI 会话桥的飞书版。
- **怎么用**: bun dev（bun run src/index.ts）启动 Slack Bolt 机器人：env 需 SLACK_BOT_TOKEN / SLACK_SIGNING_SECRET / SLACK_APP_TOKEN（.env.example 提供）；App({socketMode:true}) 建立 Socket Mode 长连接；内部 createOpencode({port:0}) 起一个临时 opencode server，把每个 Slack 线程(channel-thread_ts)映射为独立 opencode session：收到消息 → client.session.create + session.share 分享链接 → session.prompt 发提示 → say() 回帖；订阅 message.part.updated 事件把 tool 完成状态实时回帖（app.client.chat.postMessage）。
- **典型场景与协作**: 把 opencode 接入 Slack 工作区：@机器人或在频道内对话即开启独立 AI 会话，工具调用进度与最终回答以线程化消息呈现，会话可分享（share URL）。

## oc-stats-app — stats-app
- 组: G17-Stats | Layer 1
- 作用: OpenCode Stats 公共数据站点（SolidStart，Cloudflare preset，app.config.ts:1）。首页通过 @opencode-ai/stats-core/domain/home 拉取并渲染使用量排行榜、模型/Provider 对比、geo 分布与市场数据（src/routes/index.tsx:10-41），另有 compare 对比页与 [lab]/[model] 实验页，配合 d3-geo/topojson 世界地图。src/routes/stats-cache.ts 统一设置 CDN 缓存头。
- 提供: ['统计首页：排行榜/用量趋势/Geo 地图/缓存命中率（src/routes/index.tsx）', '模型对比页（src/routes/compare/[firstFamily]/[secondFamily].tsx）', '模型实验室单模型页（src/routes/[lab]/[model].tsx）', 'CDN 缓存控制与 Vary locale 处理（src/routes/stats-cache.ts:5）', 'API：health/newsletter（src/routes/api/）', '多语言 i18n（20 语言）与 sitemap']
- **为什么存在（设计意图）**: 与 console 同构（SolidStart + ui 包）但独立部署，因为受众不同（公开数据 vs 私有控制台）且数据来自完全不同的管线（Athena 数仓 vs 业务 DB）；i18n 20 语言 + d3 地图可视化为纯前端展示层，无写路径。
- **改造关联**: 本机未改。装配层的 dashboard/报表能力未自建（用 excel/markdown 报告替代），stats-app 是官方数据可视化站的参照物。
- **怎么用**: SolidStart 统计站前端：bun run dev:stats（仓库根）或 bun run --cwd packages/stats/app typecheck；routes/ 有首页 index.tsx（d3-geo/topojson world map + i18n 20 语言）、model-catalog（模型目录页）、compare/[model]（模型对比）、[lab]/[model] 实验页、stats/api/health|newsletter API、sitemap.xml.ts。数据源：@opencode-ai/stats-core 的 domain 查询（runStatsEffect 执行 Effect）。
- **典型场景与协作**: 公开统计站点（与 console 分离的独立站点）：按模型/供应商/国家展示 token 成本、耗时、TPS、缓存命中率等排行榜与地理分布；模型目录、两两对比、实验室页。

## oc-stats-core — stats-core
- 组: G17-Stats | Layer 0
- 作用: Stats 后端核心（Effect + drizzle + PlanetScale）。src/athena.ts 封装 AWS Athena 查询服务（StartQuery/轮询/取结果），src/database.ts 提供 Effect 风格 DatabaseConfig/DrizzleClient，src/domain/ 下按 model/provider/geo/home/inference 分域定义聚合类型与查询，src/stat-sync.ts 实现 Athena → 数据库的增量/全量同步管线。src/index.ts 聚合导出全部命名空间。
- 提供: ['Athena 查询服务：执行/轮询/分页取数（src/athena.ts:45）', 'Effect 化数据库层：PlanetScale drizzle + schema + 迁移（src/database.ts:24,40）', '统计领域模型：StatBaseAggregate 聚合结构与 grain day/week（src/domain/stat.ts:6）', 'Model/Provider/Geo 统计仓库与 upsert（src/domain/model.ts 等）', '首页聚合查询（getStatsHomeData，src/domain/home.ts:9）', '统计同步管线：Athena 查询 → 聚合 → 写入（src/stat-sync.ts:23）', 'App 配置（stage/publicUrl）与运行时（src/config.ts、src/runtime.ts）']
- **为什么存在（设计意图）**: 用 Effect 服务（Context.Service + Layer）组织全部依赖（Athena/Database/Config），运行时以 Layer 注入——与 console-core 的 fn 风格不同，stats 选择了纯函数式依赖注入，便于 Lambda/Server 两种宿主复用同一套查询/同步逻辑；Athena 只扫一次源表的 GROUPING SETS 设计明确为降成本优化。
- **改造关联**: 本机未改。装配层在多源数据归一化统计（如 0817 DAG 的包统计、github-dag 的 commit 统计）上复用了其思路：统一 schema 归一化 + 增量锚点窗口，但用 Python 而非 Effect。
- **怎么用**: Effect 生态服务包：Athena service（@aws-sdk/client-athena，StartQueryExecution→GetQueryExecution→GetQueryResults 轮询 300 次，WorkGroup/Catalog/Database 来自 Resource.InferenceEvent）；Database service（@planetscale/database + drizzle-orm/planetscale-serverless，DATABASE_URL 或 Resource.StatsDatabase.url）；domain/ 下 inference/model/provider/geo/stat（buildStatsQuery 用 GROUPING SETS 一次扫描聚合 sessions/requests/tokens/cost/duration/TPS 等指标）；stat-sync.ts 增量/全量同步（锚定 ISO 周、5 分钟摄取滞后、56 天展示窗口）。scripts: db:migrate / db:push / honeycomb:backfill / ensure-unique-users。
- **典型场景与协作**: 统计数据的采集-聚合-落库核心：Lambda（stats/function→core）与 stats-server 共用；honeycomb-backfill 把历史遥测灌入 Athena；migrate/ensure-unique-users 维护 PlanetScale 统计表。

## oc-stats-server — stats-server
- 组: G17-Stats | Layer 1
- 作用: Stats 后端 Node HTTP 服务（Effect HttpRouter + Bun，Dockerfile 部署）。src/server.ts 用 NodeHttpServer 启动 3000 端口服务并注入 Ingest 层，src/router.ts 暴露 GET /health、/ready 与 POST / 数据摄取端点（Bearer 鉴权 + 并发信号量限流），src/ingest.ts 将事件批处理写入 AWS Firehose，src/stat-sync.ts 是每小时 Athena 同步 daemon。
- 提供: ['摄取端点 POST /：事件批收 + Firehose 写入（src/router.ts:25、src/ingest.ts:38）', '健康检查 GET /health 与 /ready（含优雅停机判定，src/router.ts:23-24）', 'Bearer 鉴权（timingSafeEqual，src/router.ts:56）', '每小时统计同步 daemon（src/stat-sync.ts:13）', 'Docker 化部署（Dockerfile:1，turbo prune + bun install）']
- **为什么存在（设计意图）**: 独立常驻 Node 服务承担 HTTP 接收 + Firehose 写湖，因为：1) Worker 直连 Firehose 的批处理/重试逻辑需要长驻进程承载；2) 与 console-function 的 honeycomb 直写并行，形成 honeycomb（实时观测）+ lake（数仓）双通道；3) 用 Effect Layer 组合 Ingest/Routes/Server，测试性高。
- **改造关联**: 本机未改。装配层无对应物；但本地 agent 采集→HTTP 上报→批量入湖链路与 headroom CLI 的 savings 统计（本地记录压缩收益）是同类 telemetry 思路。
- **怎么用**: bun src/server.ts 启动（package.json start）：NodeHttpServer（PORT 默认 3000 / HOST 0.0.0.0）承载 Effect HttpRouter；router.ts 挂 GET /health、GET /ready（关停时 503）、POST /（带 Bearer 鉴权 isAuthorized + 8 并发 Semaphore 的 ingest 端点）；ingest.ts 用 @aws-sdk/client-firehose 把事件按 database.table 路由批量写 Kinesis Firehose（500 条/批、3 次重试、退出信号优雅关停）。
- **典型场景与协作**: Zen 网关日志的接收-转发服务：console-function 的 log-processor（Worker）把 lake ingest 事件 POST 到 stats-server，stats-server 校验鉴权后写入 Firehose → 数据湖 → Athena 供 stats-core 查询。

## oc-storybook — storybook
- 组: G11-文档站点 | Layer 4
- 作用: UI 组件开发文档站。.storybook/main.ts:13-29 用 storybook-solidjs-vite 定义框架并聚合 ui/session-ui/app 三包的 stories（stories glob 指向 ../../ui、../../session-ui、../../app/src）；同时用 mocks 目录对 app 的 context（local/file/prompt/layout/sdk/sync 等 15+ 个）做 SolidJS router 替换与 context mock（main.ts:36-50），使 app 组件能在 Storybook 中独立渲染；preview.tsx 提供全局预览配置。
- 提供: ['聚合 ui/session-ui/app 三包组件的 Storybook 开发环境', 'app context 全套 mock（main.ts:37-50 别名替换）', 'Playground CSS 与主题工具插件（playground-css-plugin.ts、theme-tool.ts）']
- **为什么存在（设计意图）**: 为组件库提供隔离的开发/审查环境，通过 mock 掉 app 的副作用 context 使跨包组件可以独立预览与回归测试，是 UI 开发流程的质量基础设施而非运行时依赖。
- **改造关联**: 属官方底座，本机装配层未引用（本机未启用 Storybook 工作流）。devDependencies 依赖 ui/session-ui（package.json:12-13），纯开发期工具不影响运行时。
- **怎么用**: ['bun storybook（package.json:7 storybook dev -p 6006）本地组件浏览；bun build（:8 storybook build）产出静态组件文档', '配置 .storybook/main.ts:13-29：storybook-solidjs-vite 框架 + addon（docs/a11y/vitest），stories glob 聚合 ../../ui、../../session-ui、../../app/src 三包 stories（main.ts:25-29）', 'app context mock：main.ts:36-60 用 alias 将 @solidjs/router 与 15+ app context（local/file/prompt/layout/sdk/sync/command 等）替换为 mocks 目录实现，使 app 组件可独立渲染']
- **典型场景与协作**: 作为组件开发与审查环境：ui/session-ui 的组件在隔离环境下预览回归，app 的页面级组件通过 mock 掉副作用 context（router/server/language）后在 Storybook 中独立渲染。典型协作：开发 ui 新组件→写 stories→storybook 预览→a11y/vitest addon 做可访问性与行为测试。

## oc-tui — tui
- 组: G8-终端UI | Layer 3
- 作用: 终端 UI 应用。src/index.tsx:1 导出 run/TuiInput；src/app.tsx:1-50 用 @opentui/solid 渲染整棵组件树（SDK/Data/Location/Theme/Clipboard 等 Provider 与 Session 路由），构建在 @opencode-ai/sdk/v2 客户端之上（src/context/sdk.tsx:1）。src/plugin/runtime.tsx 加载 @opencode-ai/plugin/tui 插件，feature-plugins/ 内含 diff-viewer/notifications/which-key/sidebar 等内置插件（src/feature-plugins/builtins.ts:1）。
- 提供: ['终端渲染运行时（src/app.tsx:1，基于 @opentui/solid）', '会话交互 UI：输入/补全/历史/frecency（src/component/prompt/*）', '对话框系统：模型/agent/主题/会话列表等 20+（src/component/dialog-*.tsx）', '内置 TUI 插件：diff-viewer/通知/which-key/侧栏（src/feature-plugins/builtins.ts）', '多 Context Provider：sdk/data/sync/theme/clipboard（src/context/*）', 'V2 SDK 数据层接入（src/context/data.tsx、sdk.tsx）']
- **为什么存在（设计意图）**: 将终端交互封装为独立可复用包，经 opencode 的 cli/tui/layer.ts 加载，同时支持 TUI 插件扩展（@opencode-ai/plugin/tui），使 CLI 与桌面端共用交互逻辑。
- **改造关联**: 本机未直接修改 tui（本机主 Agent 以 CLI 非交互/自动化方式运行，未挂载自定义 TUI 插件），属官方底座；vision 插件只处理 chat.messages.transform，不涉及 TUI 渲染面，装配层没有对 tui 的引用点。
- **怎么用**: ["入口：src/index.tsx:1 —— export { run, type TuiInput } from './app'；src/app.tsx:1-15 用 @opentui/solid 的 render/useRenderer + @opentui/keymap 构建终端渲染循环，import @opencode-ai/core 的 Global/Flag/InstallationVersion 做运行状态。", '36 个深路径导出（package.json exports）：./builtins、./config（keybind）、./context/*（args/epilogue/exit/kv/project/runtime/sdk/sync/theme/editor/clipboard）、./attention、./editor、./plugin/runtime、./plugin/slots、./ui/dialog、./ui/spinner、./ui/toast、./keymap 等，供宿主与 TUI 插件按需加载。', '加载方式：被 opencode 的 cli/tui 命令（src/cli/cmd/tui.ts）与 cli/tui/layer.ts 动态加载；TUI 插件经 @opencode-ai/plugin/tui 的类型面挂 UI 插槽（plugin/src/tui.ts 的 Renderable/SlotMode）。']
- **典型场景与协作**: tui 是终端交互层：opencode 主程序加载它渲染会话/输入/工具状态 UI，TUI 插件经 plugin/tui 暴露的 slot 注入自定义组件（报告-01 插件钩子的一部分）；与 core 协作读全局状态（Global/Flag），与 sdk 协作连后端。claude-code 式交互、桌面端复用同一交互逻辑（cli 与 desktop 共用）。

## oc-ui — ui
- 组: G9-UI组件 | Layer 0
- 作用: SolidJS UI 组件库。src/components/ 含 50+ 基础组件（button/avatar/dialog/context-menu/diff-changes/icon 等，每个 .tsx 配套 .css 与 .stories.tsx），基于 @kobalte/core 无障碍原语；exports 将 ./components/*.tsx 直接映射为组件子路径（package.json:37）。同时提供 hooks（use-filtered-list）、context（dialog/file/i18n/marked/worker-pool）、theme 主题系统、i18n 词典、v2 新一代组件目录及 storybook 脚手架（src/storybook/scaffold.tsx）。
- 提供: ['50+ 基础 UI 组件（按钮/对话框/下拉/悬浮卡/图标等）', 'Markdown 渲染管线（marked.tsx + worker-pool + shiki 流式高亮）', 'Theme 主题解析与上下文（theme/index.ts、theme/context.tsx）', 'i18n 多语言词典与 plural 规则（i18n/en.ts、context/i18n.tsx）', 'File/Dialog/WorkerPool 等全局 context', '图标集：provider/file/app 三类 sprite（provider-icons/types.ts 等）']
- **为什么存在（设计意图）**: 将跨 app/session-ui/enterprise 复用的无头基础组件与渲染原语独立成库，保证视觉一致性与按需导入（sideEffects 仅 css，package.json:14-16），同时承载 v2 新一代组件迁移（src/v2/）避免破坏旧接口。
- **改造关联**: 属官方底座，本机装配层未引用（无 agent/mcp/skill 依赖它）。但它是 DAG 中被依赖最多的 UI 节点之一（app/session-ui/enterprise/storybook/tui 均依赖），改造上游 UI 时是唯一公共修改点。
- **怎么用**: ['按组件子路径导入：package.json:35-57 exports 将 ./components/*.tsx、./context/*、./theme/*、./hooks、./v2/* 直接映射（如 @opencode-ai/ui/context/marked、@opencode-ai/ui/theme/context），app/enterprise/session-ui 均以该方式消费（enterprise/src/app.tsx:3-10 import Font/MarkedProvider/DialogProvider/I18nProvider/ui i18n dict）', '主题与样式：@opencode-ai/ui/styles（tailwind 入口）、@opencode-ai/ui/theme（theme/index.ts:1 resolve/loader）、i18n 词典（i18n/en.ts:1 dict 导出，enterprise 用它做 SSR locale 检测 app.tsx:25-30）', 'storybook 脚手架：./storybook/scaffold 与 ./storybook/fixtures 供组件开发预览（storybook/scaffold.tsx:30 create）']
- **典型场景与协作**: 作为跨 app/session-ui/enterprise/storybook 复用的无头组件与渲染原语层：app 用 MarkedProvider+ThemeProvider 组装会话页；enterprise 用 ui 的 i18n/Font/对话框搭 SolidStart SSR 根；session-ui 用 ui 的 marked/worker-pool 实现流式 markdown。改一个基础组件（如 button）会同时影响所有上层包，是 UI 层最底层的公共依赖（G9-UI组件 Layer 0）。

## oc-web — web
- 组: G11-文档站点 | Layer 0
- 作用: 基于 Astro + Starlight 的文档与分享站点。src/pages/s/[id].astro:2-8 渲染会话分享页（Share.tsx 消费 opencode/session 类型，通过 API URL 拉取分享数据）；src/pages/[...slug].md.ts:19-34 提供 docs 内容 API（按 slug 返回 markdown 文档）；src/content/docs/ 含多语言（en/zh/ar/bs/de/...）文档与代码示例（大量引用 @opencode-ai/plugin 与 @opencode-ai/sdk 的用法）。devDependencies 引用 opencode 包（opencode: workspace:*）。
- 提供: ['会话分享查看页（s/[id].astro + components/Share.tsx）', 'docs 文档 API 端点（pages/[...slug].md.ts:19）', 'Starlight 多语言文档站（content.config.ts + i18n/）', '分享 WebSocket 连接状态 UI（Share.tsx:15 status 机）']
- **为什么存在（设计意图）**: 独立部署的文档+分享前端，与桌面 app 完全解耦，仅通过 API URL 消费后端数据，作为云端分享生态的展示层；Starlight 承载多语言文档站与代码示例。
- **改造关联**: 属官方底座，本机装配层未引用。devDependencies 引用 opencode 包（package.json:39 opencode workspace:*）仅用于类型导入 Session 模型（s/[id].astro:4），无运行时耦合。
- **怎么用**: ['astro 命令：bun dev/start（package.json:7-12）本地文档站，dev:remote 指向线上 API（VITE_API_URL=https://api.opencode.ai）；build→astro build 产出静态站，preview 本地预览', '分享页：src/pages/s/[id].astro:1-8 按短 ID 渲染分享会话（Share.tsx 经 VITE_API_URL 拉取分享数据）；docs API：pages/[...slug].md.ts:19-34 按 slug 返回 markdown', '内容集：src/content.config.ts:8-16 defineCollection（docs + i18n）驱动 Starlight 多语言文档']
- **典型场景与协作**: 作为独立部署的文档+分享前端：与桌面 app 完全解耦，仅通过 API URL 消费后端数据。典型协作：web 的分享页 s/[id] 展示 enterprise 创建 + function 同步的分享会话，docs API 供第三方以 markdown 拉取文档，是云端分享生态的展示层。
