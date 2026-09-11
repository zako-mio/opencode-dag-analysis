# skill 节点（41）

## skill-agency-agents — agency-agents
- 组: A6a-角色调度 | Layer 1
- 作用: 专业AI角色调度系统。当用户任务较为复杂/专业时激活，根据任务内容自动匹配最合适的AI Agent角色，加载其专业prompt后执行。覆盖工程、设计、营销、安全、测试、GIS、游戏开发等16个部门260+专业Agent。触发关键词：工程师、前端、后端、架构、测试、安全、设计、UX、营销、SEO、数据、数据库、DevOps、CI/CD、移动端、游戏、GIS、地
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-architecture-judgment — architecture-judgment
- 组: A6n-架构判断 | Layer 1
- 作用: >
- 提供: 
- **为什么存在（历史）**: 源自 0910-软件工程架构方法论知识图谱交付（167 节点/360 边/18 组/11 域/三层）；0911 opencode 架构能力扩展实战中由「速查 + 路径路由」升级为 Agent 可执行工作流能力包（workflow/checklist/templates/schemas/gate/openspec 集成）。
- **为什么存在（当前）**: 需求驱动：把一个架构问题变成可解释、可复核、可交付的产物——先判决策类型再路由节点，最后产 ADR（必选）与多维权衡矩阵（选型场景），并过机检门控方可交付；内置离线图谱不联网可用，知识分层引用纪律防止技术层过度推荐。
- **怎么用（触发）**: ①自动路由：任务涉及技术选型/架构风格/模块与服务边界/架构评审/质量属性权衡/技术债治理/演进治理时，主流程自动加载；②显式命令 /arch；③openspec design 工件生成或修改时由行为层 architecture-behavior.md 强制触发。
- **怎么用（工作流）**: ①判类型：归入 routing.md 的 18 个任务场景之一；②读速查：用 cheatsheet.md 对应层条目做首轮判断得到支撑节点 id；③深链接：按 11-node-pages/<ID>.html 或 15-md/nodes/<ID>.md 读节点全文确认；④产出+自检：按 schemas/adr.schema.json 产 ADR（选型加矩阵），边界走 boundary schema，均以 gate_architecture.py --kind adr|boundary 自检，不过不得交付；TEC 节点仅写入 standards_refs。
- **怎么用（协作）**: 由 architect-worker 作为执行载体；受 instr-architecture-behavior 行为层约束；配套 workflow.md / checklist.md / templates / schemas / gate_architecture.py / integrations/openspec-design.md；权威源在 0910 任务仓 20-agent-skill（install-skill.py 派生安装）；与 command-arch、kb-construction（内容交付型/上下文注入型）协作。

## skill-browser-harness — browser-harness
- 组: A6e-浏览器 | Layer 1
- 作用: "Always use browser-use for any web interaction: automation, scraping, testing, or site/app work."
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-cytoscape-dag-visualization — cytoscape-dag-visualization
- 组: A6c-DAG方法 | Layer 0
- 作用: cytoscape.js 交互 DAG 可视化构建方法论。当任务涉及构建组级+下钻交互 DAG 总览、向页面注入 DATA、环修复、disabled 节点标注、批量 HTML 页插入源码级动态 DAG、染色/排版/幂等防累积、VLM 验证渲染时使用。触发关键词：cytoscape、交互式DAG、DAG总览、下钻、DATA注入、disabled标注、环修复、动
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-dag-tutorial-authoring — dag-tutorial-authoring
- 组: A6c-DAG方法 | Layer 0
- 作用: DAG 教程编写方法论（零基础读者导向）。当任务涉及编写面向初学者的概念/技能 DAG 教程、将可读性规律编码为门控、调研驱动编写、双轨验证(VLM+headless)时使用。触发关键词：DAG教程、教程编写、学习路径、knowledge DAG、可读性门控、调研驱动编写、新手教程。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-drawio-reference — drawio-reference
- 组: A6b-图表 | Layer 1
- 作用: draw.io 图表完整参考文档。包含 XML schema 样式库、Mermaid.js 全语法参考（28种图表类型）、shape 搜索指南、强制导出规范。对 drawio-worker 子Agent 为强制加载项（含防截断规则），不可跳过。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-frontend-design — frontend-design
- 组: A6d-前端设计 | Layer 0
- 作用: 前端设计双引擎系统。先数据驱动 Top K 候选推荐，后设计主管创意裁决。覆盖网页设计、UI 页面、组件、配色、排版、布局、动效、可访问性、交互、表单、响应式、前端开发、landing page、设计系统。适用场景：新建页面/组件、UI 重构、设计审查、配色选型、字体选型。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-github-bulk-upload — github-bulk-upload
- 组: A6o-交付发布 | Layer 0
- 作用: GitHub 大仓库全量上传方法论。当任务涉及将大型交付物/源码克隆(100+MB/数千文件)上传至 GitHub 仓库、处理嵌套.git被识别为gitlink、大文件推送schannel中断、gh CLI代理登录、权限deny转手动push时使用。触发关键词：上传GitHub、GitHub上传、大仓库上传、gh repo create、git push、嵌
- 提供: 
- **为什么存在（历史）**: 源自 DeepSeek Harness 源码解析交付物上传实战（100+MB/8102 文件→公开仓 deepseek-harness-analysis，提交 b22d6bc，远程 tree 9336 条目）；吸收三个开源 skill 方法论（上传预检/敏感扫描/gh CLI 纪律），补足嵌套 .git、断链、postBuffer、代理登录、权限移交等本项目独有场景。
- **为什么存在（当前）**: 需求驱动：需将大型交付物/源码克隆全量上传 GitHub，处理 Windows 下嵌套 .git 被识别为 gitlink、schannel 中断、gh CLI 直连超时走代理设备码登录、push 被权限 deny 转用户手动，以及沙箱禁 push 时改用 Git Data API 整树推送。
- **怎么用（触发）**: 任务涉及将 100+MB/数千文件交付物或源码克隆上传 GitHub、处理嵌套 .git/gitlink、大文件 schannel 中断、gh 代理登录、权限 deny、批量仓库上传时加载。
- **怎么用（工作流）**: 10 步：①准备环境（装 gh CLI/git 身份/敏感扫描）；②代理登录（HTTPS_PROXY + 设备码，非交互须移交用户）；③git 初始化；④断链修复；⑤嵌套 .git 处理（git ls-files -s 查模式 160000→删嵌套 .git）；⑥全量提交；⑦gh repo create + topics；⑧postBuffer 调 500MB/HTTP1.1；⑨推送与协作（deny 转用户手动）；⑩验证（tree 条目/README 大小/branch/visibility/topics 实测，不凭返回 200 推断成功）。沙箱禁 push 时改走 Git Data API（blob→tree→commit→ref）。
- **怎么用（协作）**: 依赖 gh CLI 与 git（定向代理）；凭据按 L1/L2/L3 分层披露；与 single-source-docs-pipeline 分工（Contents API 单文件 vs Git Data API 整树）；依赖 config-main（permission 权限规则）。

## skill-grill-me — grill-me
- 组: A6a-角色调度 | Layer 4
- 作用: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when the user wants to stress-test a pla
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-headroom — headroom
- 组: A6h-上下文压缩 | Layer 4
- 作用: Headroom 上下文压缩层（CLI 版）。支持 headroom proxy / audit-reads / savings / inspect / diff / memory 等命令，用于手动压缩超大工具输出、审计 Read-tool 流量、查看压缩节省统计。注意：headroom MCP 服务器已禁用（2026-08-12 量化亏损），CLI 仍可用
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-job-listing-filter — job-listing-filter
- 组: A6i-简历求职 | Layer 0
- 作用: 岗位表批量筛选方法论。当任务涉及从 xlsx/表格按城市/学历/届数/岗位类型/截止日期筛选招聘岗位，或用 openpyxl 解析 WPS 生成表格、设计关键词集与排除词、审计子Agent筛选结果时使用。触发关键词：岗位筛选、校招筛选、招聘表、openpyxl、WPS xlsx、styles.xml、关键词集、排除词、可疑行审计。
- 提供: 
- **为什么存在（历史）**: 源自 2026-08-24 校招岗位筛选实战（25MB 双总表→808 命中），由 reflection-worker 于 09-09 从 cycle_0824_job_filter 提炼，09-11 /reflection 采纳并安装至 skills/。
- **为什么存在（当前）**: 需求驱动：批量筛选 = 表结构定位 + WPS xlsx 格式兼容 + 筛选口径参数化 + 关键词/排除词规则 + 子Agent 审计；筛选结果的正确性不由子Agent 自检保证，而由主Agent 的结果级审计保证。
- **怎么用（触发）**: 任务涉及从 xlsx/表格按城市/学历/届数/岗位类型/截止日期筛选招聘岗位、用 openpyxl 解析 WPS 生成表格、设计岗位类型关键词集与排除词、审计子Agent 筛选结果时加载。
- **怎么用（工作流）**: ①表结构定位（列全 sheet 名、注意表头偏移、字段画像）；②WPS xlsx 解析兼容（复制副本→剥离/替换 styles.xml→重打包读副本）；③筛选口径参数化（截止日期 Excel 序列号 epoch 1899-12-30、学历、城市、届数）；④关键词集与排除词铁律（宽词必配行业硬件排除词，禁裸词跨领域泛词）；⑤算法特赦规则（含「算法」且不含「嵌入式」保留）；⑥委派子Agent（禁私扩关键词）+ 主Agent 结果级审计（可疑行抽样/审计脚本）。
- **怎么用（协作）**: 与 recruit-assist（招聘域）协作；依赖 openpyxl；check_suspect.py 类审计脚本随 skill 复用；依赖 config-main。

## skill-kb-construction — kb-construction
- 组: A6q-知识库构建 | Layer 0
- 作用: 知识库构建全流程主入口。五类分流（内容交付/检索问答/上下文注入/语料资产/数据分析），覆盖建库+扩展+维护全生命周期。触发关键词：建知识库、知识库构建、知识库扩展、知识库维护、知识库升级、建库、知识图谱、RAG建库、知识库迭代、级联更新、知识库门控。
- 提供: 
- **为什么存在（历史）**: 源自 0807/0813/0820/0822/0825/0902/0907/0908 多轮建库与评测实战，0911 收敛为统一主入口——把散落的建库经验（内容交付/检索问答/上下文注入/语料资产/数据分析）整合为五类分流 + 公共主干 + 分层门控。
- **为什么存在（当前）**: 需求驱动：需要一条不默认 RAG 的统一建库路径——先按消费方分流五类谱系，再走共享主干（契约→采集→加工→交付→门控）；契约先行（P0 落盘 contract.md 后才并行生产），门控分层 L1-L7，回放四硬指标。
- **怎么用（触发）**: 触发词（建知识库/知识库构建/知识库扩展/知识库维护/知识库升级/建库/知识图谱/RAG建库/知识库迭代/级联更新/知识库门控）；适用从零建库、既有库增量扩展、多形态知识交付、语料沉淀、数据驱动决策交付。
- **怎么用（工作流）**: ①五类分流判定（Q1 消费方：内容交付/检索问答/上下文注入/数据分析；Q2 是否语料资产；Q3 是否增量级联）；②公共主干 P0 契约→P1 采集→P2 加工→P3 交付→P4 门控；③按类型走各自流水线；④门控 L1-L7 按规模按需启用（生成时自验证/全量审计/结构/视觉/渲染/覆盖度/信源，skipped≠PASS）；⑤级联 12 项 + 回放四硬指标（覆盖度≥90%、门控全过、信源可溯源≥95%、人工抽查无重大语义错误）。
- **怎么用（协作）**: 与 dag-tutorial-authoring、multi-window-dag-delivery、cytoscape-dag-visualization、search-methodology、drawio-worker、pdf-worker、vision-worker、opencode-config 按任务特征路由协作；依赖 scripts/kb_gate.py 分层门控；依赖 config-main。

## skill-lark-suite — lark-suite
- 组: A6f-办公集成 | Layer 1
- 作用: 飞书/Lark 全功能操作入口。通过 lark-cli 操作日历、消息、文档、云盘、多维表格、任务、会议、通讯录、审批、知识库等全部业务域。触发：飞书、lark、lark-cli、feishu、文档、日历、会议、表格、多维表格、任务、审批、知识库。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-login-auth-channel — login-auth-channel
- 组: A6j-联网搜索 | Layer 1
- 作用: 登录态渠道交互式登录 SOP。命中需登录平台（知乎/闲鱼/淘宝/京东/小红书/拼多多/微博）且需登录态拿完整数据时，指导主Agent执行人机交互式登录（可见窗口暂停扫码）+多后端容错降级（agent-browser→Cookie-Editor→MCP/CLI），与子Agent按need_login契约协作。触发：登录态、需要登录才能看、扫码、交互式登录、选品
- 提供: 
- **为什么存在（历史）**: 0906 登录态渠道扩张方案 + 实装内化收尾。0905 架构曾将「社交平台 Cookie 依赖」列为过度工程规避（FactReach 23 渠道只取机制），但用户明确决策：登录态在选品/评价场景是刚需（知乎全文评价/淘宝销量/京东评价/小红书笔记/拼多多详情），须构建而非规避。
- **为什么存在（当前）**: 需求驱动：需在登录态下才能拿到完整数据（知乎/闲鱼/淘宝/京东/小红书/拼多多等 8 渠道），平台风控各异（小红书 x-s/x-t、拼多多 anti_content 强签名），需一套「真能登录并抓取」且能抗风控、有序降级的机制。
- **怎么用（触发）**: 命中 search-methodology 决策树 Path3（电商/选品/评价/口碑意图）且主Agent 判定需要登录态后加载。适用于「登录态/需要登录才能看/扫码/交互式登录/选品评价口碑」场景。
- **怎么用（工作流）**: ①主Agent 命中 Path3 → 先查免登录 API（如 B站 bili-cli/搜索 API，零成本零账号风险，优先采用）→ 有则用免登录；②需登录态 → 三合一检测登录态（URL 跳转 + 页面元素 + 接口探针）；③已登录 → 委派子Agent 已登录态纯抓取，若报风控(403/频控/IP at risk)按多后端降级链降级（不重试同一后端）；④未登录 → 主Agent 开可见窗口 --headed 暂停请用户扫码 → 用户完成 → --restore 持久化登录态（AES-256-GCM 加密落盘）→ 重委派子Agent 纯抓取；⑤降级链走完仍失败 → 返回 {blocked:true, reason} 明确标注不编造。
- **怎么用（协作）**: 路由判定由 search-methodology 决策树 Path3 承担；平台数据/合规矩阵以 source_credibility_map.md 六「需登录域」区块为单一权威源；agent-browser 通用命令（--restore/--headed/auth vault）由 browser-harness skill 承担；登录触发由主Agent、抓取由 search-worker 子Agent，按 need_login 契约（{need_login, platform, reason}）协作；依赖 opencode.env（AGENT_BROWSER_ENCRYPTION_KEY）。

## skill-multi-window-dag-delivery — multi-window-dag-delivery
- 组: A6c-DAG方法 | Layer 0
- 作用: 多层窗口接力 DAG 依赖链分析与交付方法论。当任务涉及将大型源码/插件库拆分为多窗口接力分析 DAG 依赖、每窗口产出 PLAN-layerN.md 接力文件、HTML/MD/drawio/交互图多形态交付、三硬依据溯源时使用。触发关键词：多层窗口DAG、DAG接力、插件依赖分析、层次遍历、拓扑分层、PACKAGE-MAP覆盖度、多窗口交付。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-opencode-capability-extension — opencode-capability-extension
- 组: A6a-配置知识 | Layer 0
- 作用: opencode 自身能力扩展 SOP。当需要为 opencode 新增/补齐一项能力（子Agent+Skill+行为层三层栈），诊断孤儿/半成品能力，统一 skill 双根，做引用普查防迁移断裂，落地契约+门控+冒烟，或用单一真相源+派生对账安装时使用。触发关键词：能力扩展、孤儿能力、三层栈、skill 双根、引用普查、能力注册表、契约先行、install
- 提供: 
- **为什么存在（历史）**: 源自 0911-opencode 架构能力实战（勘察宿主自改造架构→20 项决策计划→阶段 0 前置修复→阶段 1 MVP→三合一冒烟全过，cycles: cycle_20260911_opencode_arch_capability / phase2）。
- **为什么存在（当前）**: 需求驱动：需要一套结构化 SOP 为 opencode 自身新增/补齐能力（子Agent + Skill + 行为层三层栈），诊断孤儿/半成品能力，统一 skill 双根，做引用普查防迁移断裂，落地契约+门控+冒烟，并用单一真相源+派生对账安装。
- **怎么用（触发）**: 需要为 opencode 新增/补齐一项能力（架构/检索/图表/视觉等）、某能力只有单层而成为孤儿/半成品、opencode 自身 skill/agent/instructions/门控需批量治理时加载。
- **怎么用（工作流）**: ①勘察（用五要素三层栈诊断孤儿/半成品）；②计划（分级介入强度，契约先行且 schema 由主Agent 亲写）；③阶段 0 前置修复（skill 双根统一迁移前备份、引用普查 grep 硬编码、stale 归档、能力注册表回填）；④阶段 1 MVP（skill 升级为可执行工作流 + 可见子Agent + 行为层全局强制 + /name 命令 + 独立 gate 脚本）；⑤单一真相源（占位符 + install 派生 + reconcile 逐字节对账，二次 apply 幂等）；⑥门控（字段级白名单判据 + 正负向自检 + 三合一冒烟）；⑦注册表闭环。
- **怎么用（协作）**: 以 architecture-judgment 三层栈为实战样例；与 opencode-config（能力注册表 local/capabilities.md）协作；与 architect-worker / architecture-behavior 同构；依赖 config-main。

## skill-opencode-config — opencode-config
- 组: A6a-配置知识 | Layer 4
- 作用: OpenCode 配置架构索引 + 路由地图。只承载 模块结构、职责边界、场景/域入口路由、维护约定；不内嵌任何配置具体值（字段全集/模型清单/cost/权限规则等一律在各子文件，需按路由 read 加载）。当用户需要查看、修改、编写、验证 opencode 配置时**必须主动使用**本 skill，并按路由加载对应子文件。触发关键词：opencode配置、
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-apply-change — openspec-apply-change
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 执行 tasks.md 中的实现任务——逐条完成并打勾。tasks.md 就绪后开始编码时使用。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-archive-change — openspec-archive-change
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 归档已完成的变更——合并 delta spec 到主 spec 并移动到 archive。实现完成并验证通过后使用。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-bulk-archive-change — openspec-bulk-archive-change
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 批量归档多个已完成的变更。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-continue-change — openspec-continue-change
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 继续已有的变更——按 DAG 顺序生成下一个未完成的工件。适合恢复中断的工作。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-explore — openspec-explore
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 探索模式——分析代码、理清需求、比较方案。不确定要做什么或需要先思考再动手时使用。不写代码。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-ff-change — openspec-ff-change
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 快速通道——跳过逐步交互，一键生成所有 OpenSpec 工件。适合有经验的用户或简单变更。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-new-change — openspec-new-change
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 逐步创建新变更——比 propose 更细粒度，逐个工件交互式创建。适合复杂或需精细控制的场景。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-onboard — openspec-onboard
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: OpenSpec 引导教程——手把手带领首次使用的用户完成完整流程。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-propose — openspec-propose
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 创建变更提案——一键生成 proposal/design/specs/tasks。明确知道要做什么时使用。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-sync-specs — openspec-sync-specs
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 同步 delta spec 到主 spec（不归档）。仅被 archive-change 或显式召唤时使用。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-update-change — openspec-update-change
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 编辑/协调已有的 OpenSpec 工件。处理手动修改后的重新同步。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-openspec-verify-change — openspec-verify-change
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: 验证实现是否匹配 spec/design。归档前的可选校验步骤。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-pdf-ocr — pdf-ocr
- 组: A6g-文档处理 | Layer 1
- 作用: PDF OCR 识别专项。处理扫描件、图片型 PDF、含水印/印章的文档。支持多语言 OCR（中英）、表格区域提取、印章检测。仅在 PDF 无文本层（扫描件/图片型）时加载。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-recruit-assist — recruit-assist
- 组: A6i-简历求职 | Layer 0
- 作用: 简历投递辅助。支持投简历（打开招聘页+记录跟踪表）、识别简历（扫描表单字段+匹配信息库）、更新信息库、记录投递状态、跟踪企业、上传简历跟踪（本地→飞书增量同步）、下载简历跟踪（飞书→本地全量覆盖）、提取表单（归档表单填写记录）。触发关键词：投简历、识别简历、更新信息库、记录投递、跟踪企业、招聘、简历投递、上传简历跟踪、下载简历跟踪、提取表单。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-release-openspec — release-openspec
- 组: A6l-OpenSpec工作流 | Layer 0
- 作用: OpenSpec 自身发布管理。仅 OpenSpec 维护者使用。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-restricted-corpus-acquisition — restricted-corpus-acquisition
- 组: A6q-知识库构建 | Layer 0
- 作用: 受限/付费语料采集与私有化装配方法论。当任务涉及采集受版权/付费墙限制的书籍、论文、数据集语料，多来源解析与稳定下载，私有语料永不上传公开仓，声明式装配与 fail-closed 门控时使用。触发关键词：受限语料、私有语料、书籍采集、影子库、来源解析、manifest provenance、双仓隔离、git check-ignore、fail-closed 
- 提供: 
- **为什么存在（历史）**: 源自 0910-软件工程架构方法论阶段 2 书籍语料采集实战（30 本 paid/user-copy 经典著作「零购买最大可得」私有语料落地，76 文件/309MB + 官方结构层 11 源 613 文件，全程零进入公开仓，cycle_20260911_se_arch_book_collection）。
- **为什么存在（当前）**: 需求驱动：受限语料的合规边界分层、有状态取用链的可靠性、来源可追溯、私有/公开隔离落机制层、装配默认拒绝（fail-closed）。
- **怎么用（触发）**: 采集受版权/付费墙/机构库限制的语料（书籍/论文/数据集）、目标零购买最大可得、采集结果必须私有保存永不进入公开仓（含公开镜像/Pages）、需多来源解析/稳定下载/来源可追溯/多形态装配交付时加载。
- **怎么用（工作流）**: ①来源分层与合规边界（合法免费/机构库/版权不明三层，仅落私有层）；②来源解析（并行 search-worker，允许替代镜像，版次匹配或标 edition_mismatch）；③直链由 Agent 下、登录/借阅/网盘转用户手动；④有状态取用链（Referer + session cookie + 退避重试 + 镜像轮换）；⑤JS 风控壳改用 GitHub 镜像 + PDF /Title 校验；⑥manifest 逐文件固化 provenance（http_status/source_url/license/sha256 去重）；⑦私有隔离落 git 层（双仓 .gitignore + git check-ignore 实测）；⑧装配 fail-closed（publish-manifest + binary_allowlist 默认拒绝）；⑨可机械派生；⑩主Agent 回盘复验（版次用内容特征判定）。
- **怎么用（协作）**: 依赖 search-worker/search-methodology（来源解析）、github-bulk-upload（公开侧上传与 Git Data API）；关联 kb-construction（语料资产型）；依赖 config-main。

## skill-resumable-content-pipeline — resumable-content-pipeline
- 组: A6q-知识库构建 | Layer 0
- 作用: 大型内容/知识生产可续跑流水线。当任务涉及从零构建论文全集、课程知识库、方法论图谱等需多子Agent分片、数小时级、可中断续跑的内容生产时使用。触发关键词：知识库构建、论文全集、课程知识库、分片并行、可续跑、幂等生成脚本、超时治理、聚合终裁、多层门控。
- 提供: 
- **为什么存在（历史）**: 源自 2026-08-25 LLM 论文全集采集/全量分析、09-10 软件工程架构知识库、09-09 课程知识库等多轮大型内容生产实战，经合并批 batch_20260911 提炼。
- **为什么存在（当前）**: 需求驱动：目标产物由 ≥50 个同构节点组成、单会话无法一次完成、需多路并行子Agent 分片产出且超时/中断后零浪费恢复，多形态交付并通过多层门控。
- **怎么用（触发）**: 任务涉及从零构建论文全集/课程知识库/方法论图谱等需多子Agent 分片、数小时级、可中断续跑的内容生产时加载；适用节点数多、耗时数小时、允许分阶段暂停续跑；不适用 <20 节点小任务或每节点需强交互确认场景。
- **怎么用（工作流）**: ①契约先行落盘（contract.md：路径/命名/schema/信源分级/版权红线，长 prompt 委派引用短路径防 JSON 截断）；②骨架先行门控（先数据 JSON 层完成节点清单 + DAG 校验再并行写作）；③分片并行（按领域/主题/年代分片，子Agent 只写各自唯一文件域，预算约 20 token/s、单轮 <10min）；④幂等脚本先落盘（每节点独立目录，超时复跑不重复不丢）；⑤聚合终裁（主Agent 去重、统一口径，不取平均不重跑，双路补漏）；⑥独立门控（主Agent 不信生产者自检，查数据完整性/结构/HTML/链接可达性/内容有无，CI 不可用层显式 SKIPPED）；⑦发布与 git diff 漂移检测。
- **怎么用（协作）**: 与 kb-construction（内容交付型）、single-source-docs-pipeline（多产物一致）、search-methodology（信源）、drawio-worker（图表）协作；契约先行原则对齐 mech-coding-discipline；依赖 config-main。

## skill-resume-builder — resume-builder
- 组: A6i-简历求职 | Layer 0
- 作用: 当用户请求制作简历、修改简历、优化简历、写CV、写求职信、准备面试或咨询求职相关问题时必须主动使用此技能。支持简历内容创作、ATS优化、岗位定制、成就公式指导、求职信撰写、面试准备、简历评分与修改建议。触发关键词：简历、resume、CV、求职、面试、cover letter、求职信、改简历、写简历、优化简历、简历模板、简历格式、STAR、实习申请、找实习、
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-search-methodology — search-methodology
- 组: A6j-联网搜索 | Layer 1
- 作用: 联网搜索方法论。需求工程层的搜索执行引擎——发现层三层(LLM初发现/信息源信用地图/外部搜索降级)+Query转译(实体消歧/学名+科名/排除运算符)+时效分流(稳定知识LLM/实时信息外部搜索)。触发:任何需要外部事实核查、多源交叉验证、实体消歧、搜索执行或证据包构建的查询。
- 提供: 
- **为什么存在（历史）**: 0905 联网搜索能力架构缺口清单——「无搜索方法论 Skill」，方法论此前散落 MEMORY 跨会话不稳。复用 anysearch Skill 编码范式 + goose frontmatter 懒加载，将搜索 SOP 沉淀为可加载的细粒度 skill。
- **为什么存在（当前）**: 需求驱动：需要一套结构化的搜索执行引擎（决策树路由 + 发现层三层 + Query 转译 + 证据包契约），把「搜索」从主Agent 的临时行为升级为可复用、可内化、可自扩展的能力。
- **怎么用（触发）**: search-worker 或主Agent 加载（Skills to Load 中指定）。前端 name/description 常驻，全量内容按需注入；命中 Trigger 条件（依赖外部事实/需交叉验证/实体歧义/时效超截止/用户要求搜索）即触发。
- **怎么用（工作流）**: ①决策树路由判定 Path1/Path2/HYBRID/Path3；②发现层：LLM初发现（仅稳定知识）→ 信息源信用地图（渐进披露 domains/<域>.md）→ 外部搜索降级链（Tavily 首筛→必应/DDG/Wiki 零成本→agent-browser 动态兜底，带 Tavily 预算状态机与降级策略）；③Query 转译（实体消歧：中文词→拉丁学名+科名+排除运算符）；④回源与交叉验证（curl→agent-browser→API，≥2 独立源）；⑤输出证据包契约并按 validate_evpack.py 自检提交。
- **怎么用（协作）**: 由 search-worker 作为执行载体；受 search-behavior instruction 约束（信源分级/实证规则）；Path3 时联动 login-auth-channel skill（登录态）；依赖 source_credibility_map.md + domains/*.md（信源导航）、validate_evpack.py（证据包校验）、Tavily API + agent-browser + browser-harness（获取后端）、opencode.env（key 注入）、代理纪律。

## skill-single-source-docs-pipeline — single-source-docs-pipeline
- 组: A6o-交付发布 | Layer 0
- 作用: 单一真相源文档交付流水线。当任务需同时交付 MD（真相源）+ HTML（可读版）+ 公开部署，且多产物必须保持一致时使用。触发关键词：MD/HTML 双轨、单一真相源、派生脚本、对账脚本、文档一致性、GitHub Pages 发布、自包含 HTML、链接可达性。
- 提供: 
- **为什么存在（历史）**: 源自 09-07 offshore_reflect_v3、09-11 stage6 内容排版发布、08-25 GitHub Pages 上传与 changelog 系统等实战，经合并批 batch_20260911 与 0911 架构能力实战提炼。
- **为什么存在（当前）**: 需求驱动：同一内容需交付 MD（真相源）+ HTML（可读版）+ 公开部署且多产物必须数据一致，杜绝「MD 改了 HTML 忘改」与「归档复制后相对路径 404」类漂移。
- **怎么用（触发）**: 需同时交付 MD + HTML（或再加 PDF/站点）且两者必须数据一致、曾出现多产物漂移、需将文档发布为 GitHub Pages 静态站点时加载；不适用一次性交互页面或不发布不归档的单机内容。
- **怎么用（工作流）**: ①选单一真相源（MD/数据 JSON 为唯一权威，HTML 一律脚本派生，禁双写）；②派生脚本（build_report.py / gen-changelog.py，占位符 replace 避开 format 的 CSS 大括号冲突）；③对账脚本（跨文档核对目录数/组数/模型名/路径/网关，不一致即报错退出）；④可机检门控（逐句标记词布尔校验 + 链接可达性 + div 开闭平衡 + UTF-8 无替换字符）；⑤可移植化（归档 HTML 内联 CSS 自包含或校正导航前缀）；⑥发布（GitHub Actions Pages，push 被拦用 gh api PUT contents + workflow_dispatch，LFS 用 media.githubusercontent.com 直链）；⑦发布前回盘复验（Pages 200 + 关键入口 200 实测）。
- **怎么用（协作）**: 与 kb-construction（内容交付型门控）、github-bulk-upload（push 被 deny 时 Contents/Git Data API）、resumable-content-pipeline（多产物交付）协作；单一真相源原则对齐 mech-coding-discipline；依赖 config-main。

## skill-soe-resume — soe-resume
- 组: A6i-简历求职 | Layer 0
- 作用: "央国企/体制内简历制作、评审与优化。支持三大功能：简历评审（8维度评分+红黄绿灯）、简历修改（先评审确认后改写）、从零生成（读取个人信息+交互问答）。内置CV4SOE的4维度转换方法论（动词行政化升级/视角宏观化包装/关键词安全合规/软实力组织化呈现）。触发关键词：央国企简历、央企简历、国企简历、SOE简历、体制内简历、央企求职、国企求职、国家电网简历、中
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-superpowers-feature-workflow — superpowers-feature-workflow
- 组: A6m-Superpowers | Layer 0
- 作用: 规范开发流程——需求澄清→方案设计→TDD 实现→验证。不依赖 OpenSpec CLI，轻量级规范编程。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-superpowers-learning-workflow — superpowers-learning-workflow
- 组: A6m-Superpowers | Layer 0
- 作用: 会话后知识沉淀——回写项目记忆、决策记录、可复用教训。按需显式召唤。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## skill-superpowers-openspec-superpowers-workflow — superpowers-openspec-superpowers-workflow
- 组: A6m-Superpowers | Layer 0
- 作用: 完整交付流程——Superpowers 探索→OpenSpec 锁定→TDD 实施→验证→归档。全程门控，需显式召唤。
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 
