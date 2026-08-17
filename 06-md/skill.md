# skill 节点（42）

## skill-agency-agents — agency-agents
- 组: A6f-角色调度 | Layer 5
- 作用: 专业 AI 角色调度系统：任务复杂/专业时激活，覆盖工程、设计、营销、安全、测试、GIS、游戏开发等 16 个部门 260+ 专业 Agent。只做路由：判断任务是否需要专家角色→搜索匹配 Agent→加载其专业 prompt 后由 Agent 自行执行。
- 提供: ['search-agents.ps1 搜索索引（agent-index.json，Top 5 候选）', '/agency-search 与 /agency-rebuild 命令', 'Agent prompt 加载执行机制（agency-agents/ 目录文件作为 System Prompt）']
- **为什么存在（历史）**: 0802 盘点标注开源+改造，上游 agency-agents 仓库（msitarzewski/agency-agents，260+ Agent 角色文件、16 部门），本地改造为 search-agents.ps1 集成 + SKILL.md 改写为 opencode 路由模式。引入动机：DeepSeek 纯文本模型缺乏专业领域角色 prompt，复杂/专业任务（工程/设计/安全/测试/GIS/游戏等）需要专家角色系统提示词提升输出质量。0808-MCP四件套源码深挖任务实证使用：加载 agency-agents 后用 agent-index.json 检索，命中 Codebase Onboarding Engineer 角色。
- **为什么存在（当前）**: 专业任务委派前的角色路由入口：判断任务是否需要专家角色、搜索匹配、加载角色 prompt 作为 System Prompt。高频使用（0815 决策清单 item13 agent-role-library 标注高频使用（专业任务委派专家角色），流程顺）。与 plan/build 主Agent 的 Agent 调度协议（search-agents.ps1 搜索角色）互补。
- **怎么用（触发）**: 触发关键词：工程师、前端、后端、架构、测试、安全、设计、UX、营销、SEO、数据、数据库、DevOps、CI/CD、移动端、游戏、GIS、地图、财务、法务、HR、客服、产品经理、项目管理、写代码、重构、优化性能、部署、安全审计、渗透测试、agent、agency、切换到XX模式；复杂/专业任务时激活，简单查询不触发。命令：/agency-search <query>、/agency-rebuild。
- **怎么用（工作流）**: 1) 触发判断（软件开发/系统设计/专业领域/专业方法论/用户请求切角色则加载）；2) powershell search-agents.ps1 -Query '<任务描述>' -Top 5 搜索匹配；3) 解析 JSON 以表格呈现 1-5 供用户选择；4) 用户选择后读取 agency-agents/<RelativePath> 角色文件，作为 System Prompt 指导执行。
- **怎么用（协作）**: 与 plan/build 主Agent（Agent 调度协议中的 search-agents.ps1 角色搜索）、delegation-subagent（dsh 侧 agent-role-library 对应物，角色 prompt 注入 subagent persona）、search-agents.ps1 + agent-index.json 协作。

## skill-agent-reflection — agent-reflection
- 组: A6m-自进化 | Layer 6
- 作用: Agent 自进化系统：Plan+Build 周期后异步反思，提炼经验写入 Memory（MEMORY.md）或创建新 Skill（Reflection/skills）。经 pending.json 状态机 + reflection-worker 子Agent 处理 + /reflection 交互确认。
- 提供: ['4 层输入封装写入 pending.json', 'pending.json 状态机（waiting/processing/done/confirmed）', 'reflection-worker 委派（仅文件读写最小集）', 'Memory/Skill 双轨道写入', '/reflection 交互式逐条确认']
- **为什么存在（历史）**: 2026-08-05 由 Reflection 系统设计部署时创建（Reflection 系统本身非反思产物，而是基础设施——Hermes 式自进化系统的核心 Skill）。0805-Reflection系统设计文档记载：用户发现当前仅有 Plan-and-Execute 模式，缺少系统化 Reflection 层（MEMORY.md 事后反馈、留档反思段、openspec-verify 都是零散被动的），参考 Hermes Agent 自进化架构（Background Review/Curator/Skills+Memory 双轨），35 项决策收敛后实现。动机三优先级：持续自我改进 > 减少重复错误 > 提升 Plan 质量。架构：Plan+Build 周期结束封装 4 层输入写 pending.json，下轮启动委派 reflection-worker（Flash 仅文件读写）分析产出 memory/skill 条目，/reflection 交互确认后写入 MEMORY.md 或 Reflection/skills/。
- **为什么存在（当前）**: 是全部 Reflection skills 的母系统：每个 Plan+Build 周期结束自动触发反思沉淀，维持"系统越用越聪明"的进化回路；当前 0817 批量确认的 DAG/cdisk/github 等 7 个 skills 均由本系统的 reflection-worker 提炼（pending.json 有完整 skill_entries 证据）。
- **怎么用（触发）**: MEMORY.md 自引用规则：用户下一条消息时主Agent 检查 meta.waiting_count>0 自动加载；用户随时 /reflection 交互式逐条确认 pending 条目；触发词 reflection、同步记忆、反思。
- **怎么用（工作流）**: ['Plan+Build 周期结束 → 主Agent 封装 4 层输入写 pending.json（waiting）', '下一轮用户消息 → 委派 reflection-worker（Flash，仅文件读写）分析产出 memory/skill 条目（status=done），主Agent 不阻塞继续正常流程', '用户 /reflection → 逐条确认 → Memory 写 MEMORY.md（§-分段）/ Skill 写 Reflection/skills/{category}/{name}/SKILL.md → 条目 confirmed']
- **怎么用（协作）**: 调度 reflection-worker 子Agent；产出物（Reflection skills/memory）供全部主Agent 加载；与 MEMORY.md、留档系统、agent-protocol.md 深度耦合

## skill-amap-budget-control — amap-budget-control
- 组: A6k-地图 | Layer 5
- 作用: 高德地图调用预算控制技能：严格管控 API 调用次数，记录用量到 amap-usage.json，接近 5000 次/天免费限额时预警，额度不足给出清晰报错与替代方案。三 skill 协作中负责结构化数据（批量 POI/路径步骤 JSON，计次），优先引导用 amap-lbs-skill 免费链接。
- 提供: ['触发词分级规则（一级强制触发/二级上下文判断/明确不激活场景）', '用量计数文件 C:\\Users\\15057\\.config\\opencode\\amap-usage.json', '13 个 amap_* MCP 工具授权（geocode/direction×4/poi×4/weather/distance/ip_location）', '预算预警与替代方案逻辑', '三 Skill 协作策略表']
- **为什么存在（历史）**: 完全自创 skill（0802 盘点标注完全自创，无上游）。引入动机：高德 Web 服务 API 有 5000 次/天免费额度，Agent 若不加控制地调用 MCP amap 工具会超限产生费用。0802 盘点（附录 C 时间线）确认 amap 三件套为早期引入（Provider 迁移同期）。本 skill 负责三级预算预警 + 用量追踪（amap-usage.json 计数文件），解决 API 成本失控问题。0802 盘点发现 amap 系列用 _SKILL.md 命名刻意禁用（amap MCP disabled），MCP 精兵策略裁撤。
- **为什么存在（当前）**: amap MCP 已禁用（enabled=false，精兵策略：12 工具约 2000 tokens 极低频），本 skill 随 _SKILL.md 命名保持存档/休眠状态，仅当用户显式提及地图/导航/位置/POI/天气/路径规划等关键词时激活（description 声明）。保留价值：若按需重新启用 amap MCP，预算控制规则（精准触发/用量追踪/超限预警/替代方案）即生效。
- **怎么用（触发）**: 触发关键词：导航、路线、路径规划、驾车、公交、地铁、步行、骑行、地图、高德、POI、周边搜索、附近、餐厅、酒店、加油站、停车场、评分榜单、天气、测距、距离、地址转坐标、经纬度、IP定位、我在哪、amap。一级触发词必须激活；二级结合上下文判断；纯聊天地名提及/比喻/产品定位明确不激活。
- **怎么用（工作流）**: 1) 精准触发匹配（一级/二级触发词规则）；2) 每次调用前检查 amap-usage.json 用量计数；3) 接近 5000 次/天免费限额时预警；4) 额度不足给出清晰报错与替代方案（优先引导 amap-lbs-skill 免费链接）；5) 三 skill 协作策略：简单搜索用 amap-lbs-skill（免费）；结构化数据用本 skill（计次 MCP API）；前端 JS 代码用 amap-jsapi-skill（免费）。
- **怎么用（协作）**: 与 amap-lbs-skill（免费链接，优先路由）、amap-jsapi-skill（前端 JS 开发）、amap MCP（13 个 amap_* 工具授权）、amap-usage.json 计数文件协作。

## skill-amap-jsapi-skill — amap-jsapi-skill
- 组: A6k-地图 | Layer 1
- 作用: 高德地图 JSAPI v2.0 (WebGL) 前端开发技能，用于编写/调试地图前端 JS 代码。涵盖地图生命周期、安全配置（密钥/代理）、3D 视图、覆盖物绘制、图层管理、LBS 服务集成，附完整 API 参考文档。
- 提供: ['references/ 主题指南 14 份（map-init/view-control/marker/vector-graphics/info-window/context-menu/events/layers/geocoder/search/routing/custom-layers/security）', 'references/api/ 全量 API 参考 19 份', 'AMapLoader 初始化与安全密钥配置规范（AMAP_SECURITY_JS_CODE 环境变量）', 'skill-card.md 与 _meta.json 元数据']
- **为什么存在（历史）**: 0802 盘点标注开源+改造，上游为高德官方 JSAPI MCP 改造（35 个引用文件：references/ 16 个 + references/api/ 17 个），_meta.json 定义版本 1.1.1。引入动机：为编写/调试高德地图前端 JS 代码提供完整 API 参考（地图生命周期/安全配置/3D 视图/覆盖物绘制/图层管理/LBS 服务集成），安全密钥强制 env 配置（AMAP_SECURITY_JS_CODE）。与另两个 amap skill 构成三件套协作（早期引入，Provider 迁移同期）。
- **为什么存在（当前）**: amap MCP 已禁用后随 _SKILL.md 命名存档/休眠（0815 桥接 opencode-skill-index 标注 amap-jsapi-skill 存档）。保留价值：若重新启用地图开发场景（编写/调试地图前端 JS 代码），本 skill 提供 JSAPI v2.0 (WebGL) 完整参考，且不消耗 API 配额（免费）。
- **怎么用（触发）**: 触发关键词：地图开发、JSAPI、WebGL地图、地图初始化、覆盖物、点标记、Marker、Polyline、Polygon、InfoWindow、热力图、图层、地理编码、路径规划开发、AMap、amap-jsapi（_SKILL.md description）。当前因 _SKILL.md 命名不被 opencode glob 匹配而不会自动加载（需显式引用）。
- **怎么用（工作流）**: 1) script 标签加载 loader.js（webapi.amap.com/loader.js）；2) 强制安全密钥配置（window._AMapSecurityConfig.securityJsCode，从环境变量取，禁硬编码，生产用 serviceHost 代理）；3) AMapLoader.load({key, version 2.0, plugins}) 初始化地图（3D 视图/缩放/中心点）；4) 按场景查 references/（map-init/view-control/marker/vector-graphics/info-window/context-menu/events/layers 等）写覆盖物与交互代码。
- **怎么用（协作）**: 与 amap-lbs-skill（免费链接）、amap-budget-control（结构化数据计次）三 skill 协作（_SKILL.md 协作说明：本 skill 只负责前端 JS 代码）。

## skill-amap-lbs-skill — amap-lbs-skill
- 组: A6k-地图 | Layer 0
- 作用: 高德地图综合服务：POI 搜索、路径规划、旅游规划、周边搜索、热力图数据可视化。生成免费的高德网页链接（不消耗 API 配额），优先用于简单搜索/导航/周边查询，需要结构化数据时转交 amap-budget-control。
- 提供: ['场景判断分流（明确类别搜索/周边搜索/热力图/POI 详情/路径规划/旅游规划）', 'index.js + gaode_skill.py 服务实现', 'scripts：poi-search.js / route-planning.js / travel-planner.js', 'AMAP_WEBSERVICE_KEY 环境变量 + 本地持久化配置', 'package.json（Node 依赖）与 config.example.json']
- **为什么存在（历史）**: 0802 盘点标注开源+改造，上游为高德官方 MCP 改造，_meta.json 定义版本 2.0.1，含 Python（gaode_skill.py）+ Node（scripts/）+ JS（index.js）三类脚本。引入动机：生成免费的高德网页链接（POI 搜索/路径规划/旅游规划/周边搜索/热力图），不消耗 API 配额，解决简单地图查询也烧 API 配额的成本问题。7 大场景覆盖（关键词搜索/周边/热力图/路径规划/旅游规划等）。
- **为什么存在（当前）**: amap MCP 已禁用后随 _SKILL.md 命名存档/休眠。保留价值：地图场景的零成本入口——简单搜索/导航/周边查询优先用本 skill 生成免费链接，需要结构化数据（批量 POI/路径步骤 JSON）时才转交 amap-budget-control（计次）。
- **怎么用（触发）**: 触发关键词：搜、找、查、附近、周边、路线、规划、旅游、热力图、美食、酒店、景点、加油站、停车场（_SKILL.md description）；用户表达搜索地点/周边/路线/旅游/热力图意图时。当前因 _SKILL.md 命名不会自动加载（需显式引用）。
- **怎么用（工作流）**: 1) 首次配置高德 Web Service Key（环境变量 AMAP_WEBSERVICE_KEY 或本地配置文件）；2) 场景判断（明确类别/位置周边/热力图/POI 详细/路径规划/旅游规划六场景）；3) 生成免费高德网页链接（不消耗配额）；4) 需要结构化数据时转交 amap-budget-control 用 MCP API。
- **怎么用（协作）**: 与 amap-budget-control（结构化数据转交）、amap-jsapi-skill（前端 JS 代码）、高德 Web Service Key + restapi.amap.com 埋点统计协作。

## skill-browser-harness — browser-harness
- 组: A6h-浏览器 | Layer 0
- 作用: 统一浏览器交互入口（自动化/爬取/测试/站点应用工作）。通过 CDP 直接控制浏览器：browser-harness daemon 经 BU_CDP_URL (localhost:9222) 连接 Chrome 远程调试实例，Python 代码经管道发给 browser-harness.exe 执行，helpers 预导入。
- 提供: ['browser-harness.exe CLI（PowerShell @"..."@ heredoc 管道编程）', '预导入 helpers（new_tab/page_info 等，js() 需 return/print）', 'chrome-debug.ps1 一键启动远程调试 Chrome（独立 profile）', '--doctor 连接诊断 + runtime 目录清理', 'agent-workspace/agent_helpers.py 任务级编辑辅助']
- **为什么存在（历史）**: 0802 盘点标注开源+改造，上游 browser-use/browser-harness 仓库，本地改造为 Windows 适配 + 脚本路径绑定 + chrome-debug.ps1（一键启动 9222 端口远程调试 Chrome）。引入动机：为 Agent 提供统一浏览器交互入口（自动化/爬取/测试/站点应用），解决招聘投递（网申表单填写）、网页数据采集等需要真实浏览器操作的需求。0804-recruit优化实证：京东校招投递靠 browser-harness CDP 完成（投递跟踪表 row 774 写入成功），并沉淀 6 条环境限制实测教训（无 sleep/JS 需 IIFE/SPA 需轮询等）。
- **为什么存在（当前）**: recruit-assist 投递核心依赖（browser-harness CDP 自动化投递，exec-recruit preset 追加），0811 深圳大数据研究院调研用浏览器自动化登录知乎/脉脉采集员工评价，0813-Agent评测知识体系三重验证门控含浏览器渲染验证，create-web preset 前端设计实测渲染。0817-opencode-dag 复用 MEMORY 经验（js() 陷阱：复杂箭头函数 heredoc 转义易错，改用简单表达式+分块抓取，最终用 chrome headless --dump-dom 更可靠）。
- **怎么用（触发）**: SKILL.md description：Always use browser-use for any web interaction: automation, scraping, testing, or site/app work——任何网页交互/自动化/爬取/测试/站点应用工作。skill/browser-harness 目录为 skills.paths 单独注册路径（0802 起双路径之一）。
- **怎么用（工作流）**: 1) 前置：chrome-debug.ps1 启动 Chrome 远程调试（检查 9222 端口，无则独立 profile 启动）；2) PowerShell @"..."@ heredoc 写 Python 代码后管道发给 browser-harness.exe（helpers 预导入，首次导航 new_tab(url)）；3) js() 需 return/print，复杂操作分块抓取；4) 连接失败用 --doctor 诊断，daemon 挂了重跑 chrome-debug 脚本，runtime 目录残留则删除重建。
- **怎么用（协作）**: 与 recruit-assist（投递核心依赖）、frontend-design（create-web preset 渲染实测）、create-web preset、Chrome（ext-chrome 外部）、browser-harness daemon（BU_CDP_URL localhost:9222）、VLM 图片校验协作。

## skill-cdisk-space-optimization — cdisk-space-optimization
- 组: A6n-系统优化 | Layer 0
- 作用: Windows C 盘空间优化方法论：先实测（注册表/磁盘）再动手，junction 软链接零风险迁移开发缓存，还原点等高危清理项半自动确认，双轨交付（对话+MD 手册）。
- 提供: ['空间盘点与占用大头识别', '社交数据注册表实测（微信/QQ/企微）', '开发缓存 junction 搬迁（mklink /J）', '高危清理项量化风险收益确认', '双轨交付（对话摘要+MD 操作手册）']
- **为什么存在（历史）**: 由 cycle-20260817-cdisk-space-optimization 反思提炼（pending.json.bak-20260817-final 证据：sk-20260817-cdisk-optimization，category=system，创建时间 2026-08-17，verdict"社交数据搬迁前先查注册表实测实际存储位置…junction 软链接零风险迁移…高危项半自动确认，提炼 1 个 Skill + 3 条 Memory"）。源任务 0817-C盘空间优化：C 盘仅剩 11.6GB/128.8GB，用户提供 WizTree 4.31 全盘扫描 CSV（96 万文件条目），要求识别可搬迁/可清理项。关键发现：微信/QQ/企微数据经注册表实测全部已在 D 盘（微信 4.24G/QQ 9.64G/企微 1.24G），原计划"社交数据搬迁"全部取消；开发缓存（opencode 3.9G/npm 823M/pnpm 486M/m2 899M 等）用 junction 零风险迁移；还原点 10-12G 等高危项半自动确认模式。方法论核心：先查注册表/实测数据位置不凭默认路径假设；不可逆操作必先确认；不报告成功除非有新鲜验证证据。
- **为什么存在（当前）**: Windows C 盘空间不足的标准处理流程：空间盘点→社交数据实测（注册表）→开发缓存 junction 搬迁→系统清理（高危项半自动确认）→验证+MD 手册留档；当前 C 盘空间管理持续复用（本 skill 是系统类元知识：关于"如何安全做磁盘优化"的方法论）。
- **怎么用（触发）**: 触发关键词：C盘空间、磁盘清理、空间优化、junction、软链接、缓存搬迁、微信数据、QQ数据、还原点、系统清理；C 盘空间不足需要分析优化时。
- **怎么用（工作流）**: ['空间盘点（统计各目录占用识别大头，确定搬迁目标盘并确认空间充足）', '社交数据实测（微信/QQ/企微数据位置存注册表，勿按默认路径假设；实测已在 D 盘则取消搬迁避免无意义操作）', '开发缓存 junction 搬迁（复制→删除原目录→mklink /J 保留原路径，对应用透明零风险可逆）；系统清理（还原点高危半自动确认、Edge 缓存低危直接清、未勾选一律不处理）；验证释放空间数字+MD 手册双轨留档']
- **怎么用（协作）**: 与用户协作（高危项逐项确认、暂存区用户验证后删除）；委派 reflection-worker 处理 pending 队列（本任务报告中记载）；产出 MD 操作手册留档

## skill-cytoscape-dag-visualization — cytoscape-dag-visualization
- 组: A6m-自进化 | Layer 5
- 作用: cytoscape.js 交互 DAG 可视化构建：单页组级+下钻总览与批量 HTML 页源码级动态 DAG 插入。含 DATA 按行注入、环修复方法论、disabled 节点标注、幂等防累积、VLM 双轨视觉验证。
- 提供: ['数据合并与环修复（E3 过滤/slot 修正/dependents 不反推）', 'DATA 注入（按行替换 const DATA，CRLF+UTF-8 无 BOM）', '两级视图（组级+下钻，缩放联动三级）', '样式语义化标注（disabled 红色+图例同步）', '试点先行批量插入（幂等防累积）', 'VLM 视觉验证（headless 截图抓盲区）']
- **为什么存在（历史）**: 由 0816-plugin-dag 的 L2 与动态 DAG 两个 cycle 反思合并提炼（pending.json.bak-20260817-final 证据：cycle-20260817-plugin-dag-l2 产出 sk-20260817-interactive-dag-viz（interactive-dag-visualization，含环修复方法论/DATA 注入/disabled 标注），cycle-20260817-plugin-dag-dyn-github 产出 sk-20260817-cytoscape-dyn-dag（cytoscape-dynamic-dag，源码级动态图批量插入/染色/幂等）；最终 2026-08-17 23:00 合并为 cytoscape-dag-visualization）。源任务：0816-plugin-dag L2（134 节点/434 边/17 层/29 组，组级+下钻交互总览）+ 动态 DAG 批量插入（215 插件/1130 模块/1073 边/171 页）。方法论核心：数据注入零风险（按行替换 const DATA 而非 __DATA__ 占位符）、样式标注语义化（node[kind=disabled]）、环修复方法论、批量插入幂等、渲染必须视觉验证（VLM+headless 双轨）。
- **为什么存在（当前）**: cytoscape.js 交互 DAG 可视化构建的标准方法论：单页交互总览（组级+下钻）+ 批量 HTML 页源码级动态 DAG；当前 0817-opencode-dag 三图交互交付（104 节点/154 边/38 组）即其应用；DAG 交付链的渲染层标准。
- **怎么用（触发）**: 触发关键词：cytoscape、交互式DAG、DAG总览、下钻、DATA注入、disabled标注、环修复、动态DAG、模块依赖图、批量插入；构建组级+下钻交互 DAG 总览或批量动态 DAG 时。
- **怎么用（工作流）**: ['场景A 单页总览：数据合并与环修复 → DATA 注入（按行替换）→ 两级视图（组级+下钻）→ 样式标注（disabled 红色）→ 视觉验证（headless+VLM）', '场景B 批量插入：试点先行（4 核心 3 轮迭代）→ 全量解析（Windows 路径统一）→ 幂等批量插入（gen-html 干净页+apply 单次插入）→ 质量门控 → 上传/交付', '关键坑：cytoscape 缺 dagre 布局扩展→节点 0 渲染（vendor 补 cytoscape-dagre 4.0.0）；data(cls) 直接存颜色值；rankDir 按节点数（≥12 LR 横排）']
- **怎么用（协作）**: 上游接 multi-window-dag-delivery（消费其 DAG JSON 节点/边/组/seam/disabled）；下游接 dag-tutorial-authoring（教程交互图）；共享 _shared/dag-core-methods.md（环修复/DATA 注入/双轨视觉验证）；drawio-worker 绘制静态图

## skill-dag-tutorial-authoring — dag-tutorial-authoring
- 组: A6m-自进化 | Layer 4
- 作用: DAG 教程编写方法论（零基础读者导向）：调研驱动编写（4 路并行交叉验证）、可读性规律编码为门控、统一 schema 并行写节点、双轨验证（VLM+headless）、新手走查闭环。
- 提供: ['4 路并行调研（官方 A/B+英文 C+中文 D）', '五要素可读性门控（心智模型/无孤立/术语统一/场景链/走查）', '8 区块节点模板（why/intro/scenario/web/cli/terms/summary/official_links）', '边方向=学习顺序约定+层序门控校验', '功能 why 分层（功能层+历史层）', '双轨视觉验证+新手走查']
- **为什么存在（历史）**: 由 cycle-20260817-github-dag 反思提炼（pending.json.bak-20260817-final 证据：sk-20260817-dag-tutorial，category=coding，创建时间 2026-08-17，verdict"调研驱动编写、可读性规律编码为门控、DAG 边方向=学习顺序写进 schema、VLM 双轨验证抓脚本盲区…提炼 1 个 Skill(dag-tutorial-authoring) + 2 条 Memory"）。源任务 0817-github-dag：GitHub 新手全功能 DAG 教程（35 节点/41 边/7 组/9 层，零基础读者），4 路并行调研（官方 A/B + 英文 C + 中文 D）交叉验证驱动编写，把"好教程"可读性规律（心智模型字段/无孤立节点/术语统一/场景链/新手走查）编码为可校验门控，节点页 8 区块模板（why/intro/scenario/web/cli/terms/summary/official_links）。实战事故：DAG 边方向写反导致拓扑分层颠倒（Layer0 出现 20 个高级节点），教训是边方向=学习顺序必须写进 schema。
- **为什么存在（当前）**: 面向零基础读者的概念/技能 DAG 教程编写标准方法论：调研先行→可读性规律编码为门控→统一 schema 并行写节点→双轨验证→新手走查→用户反馈闭环；当前知识 DAG 类交付（如 GitHub/Git 教程）复用；"双轨交付一致性三原则"（人类入口 .html/.md 仅 AI 镜像）亦由本 skill 固化为门控。
- **怎么用（触发）**: 触发关键词：DAG教程、教程编写、学习路径、knowledge DAG、可读性门控、调研驱动编写、新手教程；编写面向初学者的概念/技能 DAG 教程时。
- **怎么用（工作流）**: ['调研先行（4 路并行：官方 A/B+英文 C+中文 D 交叉验证）→ 先写分析报告（5 段+方法论映射）再驱动节点内容', '可读性规律编码为门控（五要素）→ 统一 schema（8 区块模板+字段长度约束）交 3 路 general 并行写节点 → DAG 边方向=学习顺序写进 schema 注释', '双轨视觉验证（门控脚本结构检查+headless 截图+VLM 抓视觉盲区）→ 新手走查（零基础视角 N 页五要素全齐）→ 用户反馈修复后同步 README+quality-gate']
- **怎么用（协作）**: 4 路调研子Agent（代理 127.0.0.1:7890+谷歌）+ 3 路 general 并行写节点；上游接 multi-window-dag-delivery（先分析再成教程）与 cytoscape-dag-visualization（交互总览）；共享 _shared/dag-core-methods.md

## skill-drawio-reference — drawio-reference
- 组: A6a-图表 | Layer 1
- 作用: draw.io 图表完整参考文档，包含 XML schema 样式库、Mermaid.js 全语法参考（28 种图表类型）、shape 搜索指南与强制导出规范。为 drawio-worker 子Agent 强制加载项（含防截断规则），用于生成含嵌套容器、跨功能泳道、自定义样式、多节点(≥15)的复杂 draw.io XML 图表。内置刚性网格布局规则，由 ELK 完成路由，不做坐标数学。
- 提供: ['draw.io XML 样式/边/容器/泳道/图层参考', '28 种 Mermaid.js 图表语法参考', 'search_shapes 使用决策指南（何时搜索领域图标）', '刚性网格布局规则（col*180+40 / row*120+40）', '强制导出规范与 reasoning budget 防截断规则']
- **为什么存在（历史）**: 2026-08-01 system-prompt-optimization 任务引入：drawio MCP（@drawio/mcp v1.5.0）的 open_drawio_xml / open_drawio_mermaid 工具描述内嵌完整 XML 参考（约 33,000 chars）和 Mermaid 参考（约 12,000 chars），导致每个子Agent 固定 System Prompt 达 18K-20K tokens，其中 MCP 工具定义占 50-60%（12K-14K tokens）。方案为 Fork drawio MCP 到 D:\Opencode\drawio-mcp-minimal，将工具描述替换为 5 行摘要 + skill('drawio-reference') 引用，参考文档独立为懒加载 skill（47,794 bytes）。2026-08-03 Drawio工具链优化：新增第五章导出与验证（强制导出规范 + VLM 校验规则），并定为 drawio-worker 子Agent 强制加载项。
- **为什么存在（当前）**: 主Agent 委派 drawio-worker 生成复杂图表（嵌套容器/泳道/自定义样式/15+ 节点）时仍必须精确写入本 skill（刚性约束），防止子Agent 用不可靠 CLI 导出产生截断 PNG。0816-plugin-dag / 0817-opencode-dag / 0817-github-dag 等 DAG 项目均靠 drawio-worker + drawio-reference 批量产出架构图（0817 三次任务合计 135+ 张 drawio）。简单流程图不加载，避免 token 浪费。
- **怎么用（触发）**: drawio-worker 子Agent 被委派生成复杂图表时强制加载（skill('drawio-reference')）；或生成含嵌套容器、跨功能泳道、自定义样式、多节点(15+)的复杂图表时由主Agent 路由触发。简单流程图/线框图/ER 图不触发（SKILL.md '何时加载' 节）。
- **怎么用（工作流）**: 1) 简单图表直接调 drawio_open_drawio_xml / drawio_open_drawio_mermaid（不加载）；2) 需要领域图标先 drawio_search_shapes 取 style 字符串；3) 复杂图表先加载本 skill 按参考生成 XML（刚性网格布局，不做坐标数学，ELK 自动路由）；4) 生成后强制 drawio_export 导出 PNG（scale=2~4）+ VLM 校验无截断。
- **怎么用（协作）**: 与 drawio-worker 子Agent（强制加载项）、drawio MCP（本地精简版 D:\Opencode\drawio-mcp-minimal）协作；由 plan/build 主Agent 按 MCP 路由规则委派。VLM（GLM-4V describe_image）负责导出图片校验。

## skill-frontend-design — frontend-design
- 组: A6b-前端设计 | Layer 0
- 作用: 前端设计双引擎系统：数据引擎（192 色板/74 字体/84 风格数据库）先推荐 Top K 候选设计系统，再由设计主管做创意裁决。覆盖网页设计、UI 页面、组件、配色、排版、布局、动效、可访问性、交互、表单、响应式、landing page、设计系统等场景。
- 提供: ['search.py 数据引擎 CLI（--design-system/--domain/--stack 22 种技术栈）', 'token 设计系统构建（4-6 命名 hex + 2+ 字体角色 + ASCII wireframe）', '双轮审查（方案 vs 简报比对 + 唯一性测试）', '冲突裁决规则（Inter 字体禁用/动效上限 Subtle）', 'references 三件套：design-philosophy / quick-reference / pro-rules']
- **为什么存在（历史）**: 2026-08-05 frontend-skill-fusion 任务引入：用户想安装 GitHub 上的前端设计 Skill，5 子Agent 并行分析 5 个候选（modern-frontend-skill / taste-skill / Anthropic frontend-design / impeccable / UI-UX-Pro-Max）对 DeepSeek 纯文本模型的适配度，最终选定 Anthropic frontend-design + UI-UX-Pro-Max 融合。融合目标是解决 DeepSeek 无视觉能力导致前端设计缺乏数据支撑的问题，设计为双引擎：数据引擎（192 色板/74 字体/84 风格数据库 search.py）给 Top K 候选 + 设计主管创意裁决。用户 4 条冲突裁定：不禁用色板/硬性禁 Inter 字体/动效 cap Subtle/数据给候选主管裁决。2026-08-15 桥接时吸收 ux-ui-agent-skills 精华（WCAG 无障碍/design-tokens/反 slop 规则）。
- **为什么存在（当前）**: 所有前端/网页/UI 设计任务的持续入口：新建页面/组件、UI 重构、设计审查、配色/字体选型、landing page、设计系统。0816 起 create-web preset（前端设计特化）将 frontend-design + browser-harness 作为核心领域技能。mission-archiving 的 HTML 版 5 段报告输出规范也由 frontend-design 支撑设计能力。
- **怎么用（触发）**: 触发关键词：网页设计、UI 页面、组件、配色、排版、布局、动效、可访问性、交互、表单、响应式、前端开发、landing page、设计系统；新建页面/组件、UI 重构、设计审查、配色/字体选型时（SKILL.md description）。
- **怎么用（工作流）**: 1) Phase 1 数据驱动：python search.py '<产品> <行业> <风格>' --design-system -p 项目名，得到 3-5 个候选设计系统（可用 --domain/--stack 精化，0 结果时放宽关键词或降级内置优先级表）；2) Phase 2 设计主管裁决：挑候选/定制/超越，构建 token 系统（4-6 命名 hex + 2+ 字体角色 + ASCII wireframe + 签名元素），双轮审查（简报比对 + 唯一性测试）后确认编码；3) 交付前按 references/pro-rules.md 清单核对（图标/对比度/安全区域）。
- **怎么用（协作）**: 与 browser-harness（create-web preset 组合，浏览器实测渲染）、mission-archiving（HTML 版报告设计支撑）、create-web 特化 agent 协作。参考文件 design-philosophy/quick-reference/pro-rules 按需加载。

## skill-github-bulk-upload — github-bulk-upload
- 组: A6m-自进化 | Layer 0
- 作用: GitHub 大仓库全量上传方法论：处理嵌套 .git 被识别为 gitlink、大文件推送 schannel 中断（postBuffer 调优）、gh CLI 代理设备码登录、权限 deny 转手动 push，10 步流程含上传后验证清单。
- 提供: ['上传前预检（README/LICENSE/.gitignore/敏感扫描）', '代理设备码登录（HTTPS_PROXY=127.0.0.1:7890）', '嵌套 .git 剥离（gitlink 修复）', 'http.postBuffer 调优', '权限协作转用户手动 push', '上传后验证清单+批量仓库上传']
- **为什么存在（历史）**: 由 cycle-20260815-deepseek-harness-upload-github 反思提炼（pending.json.bak-20260817 证据：sk-20260815-github-upload，category=coding，创建时间 2026-08-17，verdict"大仓库 schannel 中断 postBuffer、gh CLI 代理设备码登录、权限 deny 转用户手动 push，提炼 1 个可复用 Skill + 2 条 Memory"）。源任务 0815-deepseek-harness-上传github：将 100+MB/8102 文件交付物全量上传 GitHub（zako-mio/deepseek-harness-analysis），经历 gh 未安装、直连超时走代理设备码登录、嵌套 .git 被识别为 gitlink（仅暂存 691 文件）、schannel 中断（postBuffer 500MB 调优）、git push 权限 deny 转用户手动 push 等坑。方法论还吸收 jiayu6954-sudo/github-upload-skill、Superstar0000/github-auto-upload-skill、zeke/faster-gh-cli-skill 三处开源方法论（本 skill 独立自建，覆盖其差距：嵌套 .git 剥离/postBuffer/代理登录/权限协作）。
- **为什么存在（当前）**: 大型交付物/源码克隆（100+MB/数千文件）上传 GitHub 的标准流程：预检（README/LICENSE/敏感扫描）→ 代理登录 → git 初始化 → 嵌套 .git 处理 → 全量提交 → postBuffer 调优 → 推送与协作（权限 deny 转用户）→ 上传后验证清单；当前 DAG 交付物（plugin-dag/opencode-dag）上传 GitHub Pages 持续复用。
- **怎么用（触发）**: 触发关键词：上传GitHub、GitHub上传、大仓库上传、gh repo create、git push、嵌套git、postBuffer、设备码登录；大型目录/交付物上传 GitHub 时。
- **怎么用（工作流）**: ['准备环境（安装 gh CLI、git 身份、预检 README/LICENSE/.gitignore + 敏感信息扫描）→ 代理登录（直连超时 HTTPS_PROXY=127.0.0.1:7890，设备码浏览器登录，gh auth status 先行）', 'git init（main 分支）+ 断链修复 + 嵌套 .git 处理（git rm --cached + 删除内部 .git 后全量 add）', '全量 commit → gh repo create --public --source --push → schannel 中断时 http.postBuffer 调优 → 权限 deny 时转用户手动 push → 验证 remote tree 条目数/README/topics']
- **怎么用（协作）**: 与用户协作（权限 deny 时移交手动 push）；被 DAG 交付链引用（0816/0817 DAG 交付物上传）；吸收三个开源 skill 方法论

## skill-grill-me — grill-me
- 组: A6f-角色调度 | Layer 7
- 作用: 对用户的计划/设计进行持续质询直到达成共享理解，逐分支解析决策树。用 question 工具一次一问（2-4 个多选选项），强制协议：每条消息必须以 [GRILL] ack + 一个 question 调用结尾。用户想压力测试方案、被拷问设计时使用。
- 提供: ['提问协议（[GRILL] 确认 + question 工具同消息）', '决策树收敛流程（4 步：逐问→自探索→全分支解析→收敛总结）', '漂移护栏（one-message rule / pre-output gate / convergence audit）', '语言规则（跟随用户会话语言，UTF-8）']
- **为什么存在（历史）**: 0802 盘点标注开源+改造，上游 RobMitt/grill-me-skill（171 星，基于 Matt Pocock 作品 MIT），原为 Claude Code（AskUserQuestion tool），改造为独立 opencode skill。0802-P0 任务（输入缓存优化）将其固化进 plan/build agent prompt 开头（+500 tokens，缓存后免费），从负收益变正。引入动机：Plan 阶段对用户的模糊需求逐条追问收敛决策树，防止拍脑袋决策。0802-Mission留档系统/后期改造.md 记录一次关键修复：原两段式协议（先 [GRILL] 文字再 question 工具）制造天然断裂点，多次出现 question 工具被跳过故障，改造为一段式（[GRILL] ack + question 同消息）。0807-opencode原理分析确认 plan/build prompt 经 agent.prompt 注入完全替换内置模板。
- **为什么存在（当前）**: Plan 模式决策收敛的核心协议：0817-opencode-dag 收敛 13 项决策、0817-github-dag 收敛 12 项、0816-plugin-dag 6 项、0806-网申扩展v2 21 轮决策拆解、0807-华洋达面试复盘 27 轮结构化拷问等几乎所有 Mission 任务 Plan 阶段都在用。三层防漂移护栏（one-message rule / pre-output gate / convergence audit）保证长会话协议不退化。
- **怎么用（触发）**: 用户说 grill me / 拷问我 / 面试我的方案 / 压力测试这个方案 时激活（SKILL.md description）；或 Plan 模式自动进入（plan prompt 内嵌协议）。
- **怎么用（工作流）**: 1) 用 question 工具一次一问（2-4 个多选选项 + Other 自定义），输出 [GRILL] ack（1-2 句）+ question 必须在同一消息；2) 能查代码库的答案自己查，不问用户；3) 逐分支解析决策树直到所有决策依赖解析；4) 收敛时输出 [GRILL] Decision tree resolved. + 一句话总结 + 决策编号列表。
- **怎么用（协作）**: 与 plan/build 主Agent（prompt 内嵌，agent.prompt 注入）、question 工具（opencode 原生，UTF-8 支持中文）、Mission 留档系统（决策清单实时落盘）、plan-grill（dsh 侧映射 ask_user_question）协作。

## skill-headroom — headroom
- 组: A6i-上下文压缩 | Layer 0
- 作用: Headroom 上下文压缩层（CLI 版）。支持 proxy/audit-reads/savings/inspect/diff/memory 命令，用于手动压缩超大工具输出、审计 Read-tool 流量、查看压缩节省统计。MCP 服务器已禁用（2026-08-12 量化亏损），CLI 仍可用。
- 提供: ['headroom CLI 命令表（proxy 8787 端口 / audit-reads / savings / inspect / memory）', '压缩触发阈值（>500 行文件 / >2000 字符工具输出 / >3000 字符网页）', 'MCP 禁用状态说明与恢复路径（切 Claude Code/Codex 时 enabled 改回 true）']
- **为什么存在（历史）**: 0802 盘点标注开源+改造，上游 chopratejas/headroom（63.9k 星，Apache 2.0），上游为 MCP 服务器（无独立 skill 文件），本地编写 SKILL.md 使用规则。引入动机：opencode 缺少原生上下文压缩（dsh cache-performance skill 明确记载 opencode 因缺原生压缩才引入 headroom），需要压缩超大工具输出/长文件减少 token 消耗。0803-opencode-vs-claude 对比改进报告提出阶梯式压缩（L1 headroom_compress 到 L2 结构化模板到 L3 兜底摘要），headroom 为 L1。2026-08-12 发现 MCP 无法使用，0812-headroom修复报告根因：8/5 Stop-Process -Force 误杀 headroom python 进程 + 重连失败；同日量化亏损评估（工具定义约 279 tokens/请求大于历史收益 0.001 美元）导致 0812/0813 决策禁用 MCP，CLI 仍可用。
- **为什么存在（当前）**: CLI 版持续可用：headroom proxy / audit-reads / savings / inspect / memory 用于手动压缩超大输出、审计 Read-tool 流量、查看节省统计。0815 桥接确认不迁移（dsh 有原生 compaction-basic + tool-result-pruner，headroom 为已解决项）；MEMORY.md 2026-08-12 记录 MCP 禁用但 CLI 仍可用。切 Claude Code/Codex 走 proxy 时可将 enabled 改回 true。
- **怎么用（触发）**: 触发关键词：headroom、上下文压缩、压缩大输出、audit-reads、savings（SKILL.md description）。使用时机：读取 500+ 行文件后、工具输出 2000+ 字符、大 JSON payload 前、爬取网页 3000+ 字符、任务完成后 savings 看节省。
- **怎么用（工作流）**: 1) headroom audit-reads 审计 Read-tool 流量找压缩机会；2) 大文件/大输出按阈值评估压缩（headroom inspect 对比原始 vs 压缩内容，验证不丢关键信息）；3) 需要全链路代理时手动 headroom proxy（8787 端口）；4) headroom savings 查看持久化压缩节省统计；5) 小内容 500 字符内不压缩（懒调用）。
- **怎么用（协作）**: 与 auto-mode.md（Output Discipline 压缩大输出规则）、compaction 阶梯（L1 剪枝）、MEMORY.md（Compaction 阶梯式 L1/L2/L3 约定）、headroom-mcp-launcher.ps1（MCP 路径纯 stdio 转发）协作。

## skill-large-scale-source-parse — large-scale-source-parse
- 组: A6m-自进化 | Layer 3
- 作用: 大规模源码库静态解析方法论：主Agent 只做调度/聚合/裁决，explore 子Agent 并行解析，三源交叉验证，分层抽象+跨层联动矩阵+端到端路径，双集群交付（MD AI 友好+HTML 人友好）。
- 提供: ['快照准备（浅 clone+官方文档镜像双依据）', '层级骨架先行（9 层抽象主线）', '三源交叉验证（印证/矛盾/独家/待裁决/参考 5 类）', '并行解析（三硬依据 E1/E2/E3+行引用）', '口径归一化终裁（主Agent 裁决）', '跨层联动矩阵+端到端路径', 'drawio 分批发+VLM 抽验', '质量门控+checkpoint 续传']
- **为什么存在（历史）**: 由 cycle-20260814-deepseek-harness-parse 反思提炼（pending.json.bak-20260817 证据：sk-20260814-source-parse，category=coding，创建时间 2026-08-17，verdict"9层架构/7阶段委派，提炼 1 个可复用 Skill + 2 条 Memory"）。源任务 0814-deepseek-harness源码解析：DeepSeek Harness 源码浅 clone（1316+ ts 文件+vendor），9 层抽象/235 modules/816 functions/31 drawio/双集群交付（AI 友好 MD 集群+人友好 HTML 集群）。方法论核心：主Agent 只做调度/聚合/裁决，解析工作量委派子Agent 并行；三源交叉验证（官方文档/Discussions/社区）+ 三硬依据（E1 编译/E2 运行时/E3 组合）+ 子Agent 口径不一致由主Agent 终裁。
- **为什么存在（当前）**: 大型开源项目源码架构解析的标准流程（数百至数万文件）：浅 clone 快照 + 层级骨架先行 + 三源交叉 + 并行解析 + 归一化裁决 + 双交付；是 DAG 分析（multi-window/cytoscape）的上游互补方法论（三个 DAG skill 均声明引用其为通用基础）。
- **怎么用（触发）**: 触发关键词：源码解析、架构解析、source analysis、9层解析、DAG依赖链、跨层联动、源码clone、架构文档；解析大型开源项目源码架构时。
- **怎么用（工作流）**: ['快照准备（浅 clone+官方文档镜像双依据）→ 层级骨架先行（9 层抽象+目录交叉索引）→ 三源交叉验证（印证/矛盾/独家/待裁决/参考五类管理）', '按层分派 explore 子Agent 并行解析，每条结论要求三硬依据+源码行引用，返回结构化 JSON', '归一化与裁决（口径不一致由主Agent 终裁，异构结构统一 schema ≤2 次重试）→ 跨层联动矩阵 → 图表/文档生成 → 质量门控 → checkpoint 续传']
- **怎么用（协作）**: 委派 explore 子Agent 按层并行；产出供 multi-window-dag-delivery（DAG 分析）与 cytoscape-dag-visualization（渲染）消费；与 drawio-worker（图表）协作

## skill-lark-suite — lark-suite
- 组: A6c-办公集成 | Layer 0
- 作用: 飞书/Lark 全功能操作入口，通过已安装的 lark-cli v1.0.76 命令操作飞书全部业务域（日历、消息、文档、云盘、多维表格、电子表格、幻灯片、任务、邮件、通讯录、知识库、视频会议、审批、OKR、白板、笔记、事件订阅、应用开发等）。以意图路由映射表按用户关键词加载对应域文件，未手写的域走 lark-cli skills read 动态加载 Fallback。
- 提供: ['意图路由映射表（IM/邮件/日历/文档/表格/多维表格/任务/云盘/幻灯片/通讯录/知识库/会议/纪要/考勤/审批/OKR/白板/笔记等 20+ 域）', '强制前置 Step 0：references/shared.md（认证/身份选择/JSON 合约/安全规则）', 'Windows 下 cmd /c lark-cli 调用规范', 'lark-cli skills read 动态加载 Fallback']
- **为什么存在（历史）**: 改造盘点（2026-08-02）标注为开源+改造，上游 yjwong/lark-cli（53 星，Go，MIT），lark-cli v1.0.76 已本地安装。SKILL.md 为路由包装层（意图路由映射表指向 23 个域文件），引入动机是让 Agent 能通过 CLI 操作飞书全部业务域（日历/消息/文档/云盘/多维表格等），解决简历求职流程中飞书表格同步（网申进度表）与日常办公文档操作需求。0802 盘点发现 23 个域文件中 20 个为占位，修复为 Fallback 策略首位加 lark-cli skills read 动态加载（v1.0.76 自带 27 个官方内置 skill）。
- **为什么存在（当前）**: recruit-assist 的飞书网申进度表同步（sync_feishu.py 增量上传/全量下载）依赖 lark-cli 认证与调用规范（前置 Step 0 shared.md）。exec-recruit preset 将 lark-suite 列为 4 个降权 skill 之一，用户手势 /lark-suite 唯一入口。日常飞书文档/表格/日历/消息操作持续需要。
- **怎么用（触发）**: 触发关键词：飞书、lark、lark-cli、feishu、消息/发消息、群聊、日程、日历、文档、表格、电子表格、sheet、多维表格、base、任务、云盘、上传/下载文件、知识库、会议、审批、OKR、邮件等 20+ 域（SKILL.md description）。用户手势 /lark-suite。
- **怎么用（工作流）**: 1) 强制 Step 0：先 Read references/shared.md（认证状态检查/登录/身份选择 --as user|bot/JSON 输出合约/安全规则/高风险白名单）；2) 按意图路由映射表匹配关键词，Read 对应 references/<domain>.md 或走 lark-cli skills read lark-<domain> Fallback；3) Windows 下必须 cmd /c 'lark-cli <domain> +<shortcut> [flags]' 调用，解析 JSON 输出。
- **怎么用（协作）**: 与 recruit-assist（飞书同步前置）、resume-builder/soe-resume（exec-recruit preset 手势组）、lark-cli CLI + 飞书开放平台（external）、create-doc preset（文档创作领域 skill 之一）协作。

## skill-minimax-docx — minimax-docx
- 组: A6c-办公集成 | Layer 0
- 作用: 基于 OpenXML SDK (.NET) 的专业 DOCX 文档创建、编辑与格式化技能，三管线：从零创建新文档、填充/编辑已有文档内容、套用模板格式化并带 XSD 验证门控。任何最终输出为 .docx 的任务（写报告/起草提案/做合同/填表/套模板）都强制使用本技能。
- 提供: ['MiniMaxAIDocx.Cli 命令集（create/edit-content/apply-template/diff/validate/fix-order/merge-runs/analyze）', 'XSD 校验器（wml-subset/aesthetic-rules/business-rules/common-types）', 'CJK 排版库（Typography：CjkHelper/FontDefaults/PageSizes）', '17 份 references 文档（OpenXML 百科全书×3/设计原则/场景指南/排障）', 'python-docx 文本提取 + 预览/转换脚本（docx_preview/doc_to_docx）']
- **为什么存在（历史）**: 来自 MiniMaxAI（skill marketplace 分发，无独立 GitHub），本地重度改造：完整 .NET C# 工程（198 文件），net8.0 到 net9.0 适配，Windows 环境变量绑定，添加 python-docx 文本提取备用管线，18 个 reference 覆盖 IEEE/ACM/APA/MLA/Chicago 等学术格式。引入动机：DeepSeek 纯文本模型需要可靠的程序化 Word 文档生成管线（OpenXML SDK 三管线 A 创建/B 填充/C 模板套用 + XSD 校验门），解决手工写 docx XML 易错且格式不专业的问题。
- **为什么存在（当前）**: 所有 Word 文档交付的骨干引擎：0811 英文简历制作（A4/Calibri/17pt 深蓝居中/54 段，business-rules 校验）；soe-resume 的 Word 管线自 2026-08-15 起改调 minimax-docx（替代 python-docx 直写）；create-doc preset 文档创作核心。0816 已制作 journal-cn/journal-en/report 3 份期刊模板存 ~/.dsh/tools/minimax-docx/templates/。
- **怎么用（触发）**: SKILL.md 声明：任何产出/修改/格式化 Word 文档的任务 MUST 使用本 skill——包括用户说 write a report、draft a proposal、make a contract、fill in this form、reformat to match this template，即使没明说 docx，只要最终输出是 .docx 就触发。
- **怎么用（工作流）**: 1) 三管线：A 从零创建 / B 填充编辑现有文档 / C 模板套用（XSD 校验门 gate-check）；2) Windows 下先 $env:PATH 前置 dotnet 路径，dotnet run --project $SKILL_DIR/scripts/dotnet/MiniMaxAIDocx.Cli -- <cmd>；3) 结构性操作（复杂表格/多节/页眉页脚/TOC/图片）直接写 C# task.csx（先读 Samples/*.cs 测试过的模式）；4) 输出后 XSD 校验 + 预览验证。
- **怎么用（协作）**: 与 minimax-xlsx（create-doc 文档创作组）、soe-resume（Word 管线依赖）、resume-builder、docx-template-translator（复杂期刊排版互补）、general 子Agent（翻译任务委派时附带本 skill）协作。

## skill-minimax-xlsx — minimax-xlsx
- 组: A6c-办公集成 | Layer 0
- 作用: 打开/创建/读取/分析/编辑/验证 Excel 电子表格（.xlsx/.xlsm/.csv/.tsv）。覆盖从零创建 xlsx、无格式损失编辑已有文件、公式重算与校验、专业财务格式化标准。内置 Windows 非 ASCII 编码双层防御（UTF-8 文件路由）与强制写后读回验证。
- 提供: ['Python 脚本集（json2xlsx/xlsx_reader/xlsx_pack/unpack/formula_check/style_audit/add_column/insert_row/shift_rows/libreoffice_recalc/shared_strings_builder）', 'minimal_xlsx 模板（workbook/styles/sharedStrings）', 'OOXML 速查表 + 创建/编辑/修复/格式化/验证/读取分场景 references', 'Readback 验证规则（列数/行数/抽样单元格三重确认）', '编码安全两层防御规范']
- **为什么存在（历史）**: 来自 MiniMax（skill marketplace 分发），本地重度改造：Python 管线（11 脚本）+ templates/ + references/（7 文件）。引入动机：Agent 需要程序化处理 Excel/电子表格（创建/编辑/分析/验证），且曾遭遇 Windows PowerShell 5.1 编码事故——$OutputEncoding 默认 ASCII，管道传中文导致 Python dict 静默去重（真实事故：11 列变 3 列），因此内置 UTF-8 编码双层防御（非 ASCII 入文件不走管道）+ 回读验证规则（写后必回读校验列数/行数/采样值）。
- **为什么存在（当前）**: 简历投递跟踪表读写（recruit-assist 的 tracker_writer.py 调用其 XML 解包-编辑-打包流程，严禁 COM）、网申数据导出、财务分析（0807 利润表任务）、create-doc preset Excel 能力。0815 补 LibreOffice 26.2.5.2 解锁动态重算 + .xls 转换（P6 实测 SUM/IF/乘法重算 + xlsx-xls-xlsx 双程无损）。
- **怎么用（触发）**: 触发词：spreadsheet、Excel、.xlsx、.csv、pivot table、financial model、formula、或任何要求以 Excel 格式产出表格数据的请求（SKILL.md description）。
- **怎么用（工作流）**: 1) 首选 json2xlsx.py：JSON 数组 + map.json 生成带样式/验证的工作簿（中文全在 UTF-8 JSON 文件，退出码 0=写并验证通过）；2) 编辑现有文件：解包后 xlsx_insert_row.py / xlsx_add_column.py 结构性修改再打包（自动更新 sharedStrings/样式/SUM 公式，零格式损失）；3) 行定位规则：grep sheet XML 找标签文本，绝不依赖预览行号；4) 每次写入后回读验证（列数/行数/采样单元格）。
- **怎么用（协作）**: 与 recruit-assist（tracker_writer.py 依赖）、minimax-docx（create-doc 组）、create-doc preset、LibreOffice（动态重算外部工具）协作。

## skill-multi-window-dag-delivery — multi-window-dag-delivery
- 组: A6m-自进化 | Layer 6
- 作用: 多层窗口接力 DAG 依赖链分析与交付：大型插件库拆窗口接力，每窗口完整执行（采集→建模→注入→生成→门控）并落盘 PLAN-layerN.md 接力文件，交付物同目录累计，门控逐层升级，PACKAGE-MAP 覆盖度终核。
- 提供: ['窗口划分与 PLAN-layerN.md 接力文件', '三硬依据溯源（E1 编译/E2 运行时/E3 组合+文件:行号）', 'build-dag.py 层次遍历（BFS 拓扑分层+无环校验）', '多形态交付（HTML 插件页+MD 镜像+drawio+交互 DAG 总览）', '数据源逐层合并（core→webapp→全量）', 'PACKAGE-MAP 覆盖度终核（缺包=0 多包=0）']
- **为什么存在（历史）**: 由 cycle-20260816-plugin-dag 反思提炼（pending.json.bak-20260817-final 证据：sk-20260817-multi-window-dag，category=coding，创建时间 2026-08-17，verdict"多层窗口接力 DAG 方法论…提炼 1 个 Skill(multi-window-dag-delivery) + 3 条 Memory"）。源任务 0816-plugin-dag：DeepSeek Harness 插件级 DAG 依赖链分析，76 核心插件+36 seam+194 边+8 拓扑层+24 组，与 L2/L3 窗口共同构成 219/219 包闭环。方法论核心：大型 DAG 分析拆窗口接力（核心集→web-app→其余），每窗口独立执行+落盘 PLAN-layerN.md 接力文件，下一窗口继承数据源+接力文件，PACKAGE-MAP 覆盖度终核，三硬依据（E1 编译/E2 运行时/E3 组合）+ 源码行引用。
- **为什么存在（当前）**: 大型源码/插件库（数百包）DAG 依赖链分析的标准方法论：单窗口无法完成时拆窗口接力，每窗口可独立执行、交付物同目录累计、门控逐层升级；是多窗口 DAG 交付（HTML/MD/drawio/交互图多形态）的分析层标准。
- **怎么用（触发）**: 触发关键词：多层窗口DAG、DAG接力、插件依赖分析、层次遍历、拓扑分层、PACKAGE-MAP覆盖度、多窗口交付；大型源码库 DAG 分析需要拆窗口接力时。
- **怎么用（工作流）**: ['窗口划分（核心集 base bundle → web-app → 其余），每窗口执行边界明确（完整执行+制定下一层计划）', '每窗口内部：N 路并行 explore 采集（三硬依据+文件:行号）→ build-dag.py 层次遍历（BFS）拓扑分层+无环校验 → DATA 注入交互总览 → gen-html/gen-md/drawio 批量 → quality-gate 门控', '窗口末尾落盘 PLAN-layerN.md 接力文件（数据接口+坑经验）→ 下一窗口继承 → PACKAGE-MAP 覆盖度终核（缺包=0 多包=0）+ 交付物逐项核对']
- **怎么用（协作）**: 委派 N 路 explore 子Agent 并行采集；下游接 cytoscape-dag-visualization（渲染其 DAG JSON）；与 dag-tutorial-authoring（内容层）、large-scale-source-parse（通用基础）互补；drawio-worker 绘制静态图

## skill-opencode-config — opencode-config
- 组: A6j-配置知识 | Layer 5
- 作用: OpenCode 配置（opencode.jsonc）分级知识库：覆盖官方 Schema v2 全量字段、本项目实际配置的深度本地化说明、操作指南、安全规则与排障手册。LLM 通过三阶自检路由按需加载子文件，不一次加载全部。
- 提供: ['路由矩阵四组子文件（ref/ 官方参考 7 份、local/ 本地化 5 份、ops/ 操作指南 6 份、troubleshooting/ 排障）', '版本哈希表（配置 SHA256 01E07DA4... + 17 子文件哈希）', '修改安全链（备份→修改→JSON 验证→重算哈希→同步子文件→零旧值残留检查）', '对标 opencode 1.18.16']
- **为什么存在（历史）**: 0802 盘点标注文档改编，上游 opencode.ai/config.json Schema v2。0803-opencode-config-skill重写/01-信息收集：用户发现原 SKILL.md 不完善（646 行单文件基于旧 Schema、无分层路由、与实际配置脱节——示例还用 @ai-sdk/openai-compatible 实际已迁 deepseek、max_tokens 4096 与实际 8192 不一致、缺本地化标注），要求重写为多文件分级知识库（ref/ 官方 Schema 参考 + local/ 本项目本地化 + ops/ 操作指南 + troubleshooting/ 排障），基于官方文档+源码+实际配置三元验证，建立维护策略。后续 0805-opencode-config过时修正（SHA256 C6A1 到 FC85，Skill 14 到 30）与 0813-opencode-config-skill更新（对标 1.18.16，覆盖 0802-0812 六次配置变更，headroom MCP 禁用同步）持续维护。
- **为什么存在（当前）**: 任何查看/修改/编写/验证 opencode.jsonc 的操作入口：三阶自检路由按需加载子文件（不一次加载全部）。0802 缓存优化/P0、0803 编码安全纵深防御、0805 Reflection、0807 原生命令、0813 配置更新等所有配置改造任务均在本 skill 指导下进行。opencode.jsonc 每次变更后需按 edit-guide 同步 SKILL.md 哈希表（SHA256 01E07...，对标 1.18.16）。
- **怎么用（触发）**: 触发关键词：opencode配置、opencode参数、opencode.jsonc、config schema、permission配置、provider配置、mcp配置、opencode设置、opencode文档、配置参考（SKILL.md description）。用户需要查看/修改/编写/验证 opencode 配置时。
- **怎么用（工作流）**: 1) 三阶自检路由矩阵定位需求（改 Schema 参数到 ref/；查本项目实际配置到 local/；操作步骤到 ops/；故障到 troubleshooting/）；2) 修改 opencode.jsonc 前先备份（.bak-日期）；3) 修改后 JSON 验证 + 重算 SHA256 + 同步 SKILL.md 子文件哈希表 + 零旧值残留检查（MEMORY.md 0813 安全链）；4) 按 ops/security.md 编码安全规则（edit 优先，禁 python -c 管道）。
- **怎么用（协作）**: 与 opencode.jsonc 配置本体、auto-mode.md（配置同步安全链）、MEMORY.md（0813 修改安全链记录）、opencode 官方文档（Schema v2）、D:\Opencode_Download\Opencode-全量备份（备份链）协作。

## skill-openspec-apply-change — openspec-apply-change
- 组: A6l-工作流 | Layer 1
- 作用: 执行 OpenSpec 变更中 tasks.md 的实现任务，逐条完成并打勾。通过 openspec status 与 instructions apply 获取上下文文件、进度与任务列表，处理 blocked/all_done 状态。
- 提供: ['变更选择与状态解析（schemaName/planningHome/actionContext）', 'apply 指令获取（contextFiles/进度/任务列表）', '任务逐条执行与勾选', 'blocked 状态引导转 continue-change', 'store 感知（--store 标志）']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。spec-driven 工作流的实施端：tasks.md 就绪后逐条完成实现任务并打勾。引入动机：OpenSpec 强调"先同意要构建什么再写代码"，apply 是锁定规格后的编码执行器，通过 openspec instructions apply 获取 contextFiles/进度/任务列表，处理 blocked/all_done 状态。
- **为什么存在（当前）**: 所有 OpenSpec 变更的实施环节（specs 锁定后进入编码）；与 propose/ff 配对构成完整闭环；本地装配层代码改动若走 OpenSpec 流程即经此实施。
- **怎么用（触发）**: tasks.md 就绪开始编码时（description 触发词"实现任务""打勾"）；或显式 /openspec-apply-change；被 propose/ff 完成后提示接续。
- **怎么用（工作流）**: ['选择变更并解析 status（schemaName/planningHome/actionContext）', '获取 apply 指令（contextFiles/任务列表/进度/动态指令），blocked 状态转 continue-change，all_done 建议归档', '逐条实现任务并打勾，遵守 context 项目约束与 operationGuidance 建议']
- **怎么用（协作）**: 上游衔接 propose/ff/new-change；blocked 时转 continue-change；完成后转 verify-change 验证、archive-change 归档

## skill-openspec-archive-change — openspec-archive-change
- 组: A6l-工作流 | Layer 1
- 作用: 归档已完成的变更：将 delta spec 合并到主 spec 并移动到 archive。先加载 archive 指令上下文，检查工件与任务完成度，处理未完成警告与冲突。
- 提供: ['归档前上下文加载（instructions archive）', '工件完成度检查（done/skipped）', '任务完成度检查（-[ ] 计数）', 'delta spec 合并到主 spec', '变更归档移动']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。实现完成并验证通过后归档：将 delta spec 合并到主 spec 并移动到 archive。引入动机：OpenSpec 的 Delta Spec 机制——变更中的 spec 是增量（ADDED/MODIFIED/REMOVED/RENAMED），归档时才合并到主 spec，保证并发变更与审视回滚能力（0803 解析报告）。
- **为什么存在（当前）**: 每个 OpenSpec 变更生命周期的收尾；归档时智能合并 delta 到主 spec（agent 驱动读 delta 编辑主 spec）；本地长期维护的规格知识库依赖此增量合并。
- **怎么用（触发）**: 变更实现完成并验证通过后（description 触发词"归档""合并 delta"）；或显式 /openspec-archive-change。
- **怎么用（工作流）**: ['选择变更，加载归档指令上下文（instructions archive）', '检查工件与任务完成度（未完成警告/冲突处理）', 'delta spec 合并到主 spec（调用 sync-specs 逻辑）并移动变更到 archive']
- **怎么用（协作）**: 上游衔接 verify-change；内部调用 sync-specs；被 superpowers 编排器作为归档收尾步骤

## skill-openspec-bulk-archive-change — openspec-bulk-archive-change
- 组: A6l-工作流 | Layer 1
- 作用: 单次批量归档多个已完成变更，智能处理 spec 冲突——通过检查代码库判断实际实现。逐变更收集工件状态、任务完成度与 delta spec 列表后统一归档。
- 提供: ['多选变更批量归档（含全选）', '批量校验（工件/任务/delta spec）', '冲突检查与代码库核对', '窄化 delta 同步范围（排除未实现 delta）', '混合 schema 独立评估']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。批量归档多个已完成变更的单次操作：多选（含全选），智能处理 spec 冲突——通过检查代码库判断实际实现。引入动机：多变更并行推进后需要批量收尾，避免逐条归档的低效；冲突处理是批量场景特有需求。
- **为什么存在（当前）**: 累积多个已完成变更需要批量收尾时；本地多线程/多窗口任务（如 DAG 多窗口交付）产生多个并行变更，批量归档是配套收尾能力。
- **怎么用（触发）**: 用户要求批量归档多个变更（description 触发词"批量归档""多个"）；或显式 /openspec-bulk-archive-change。
- **怎么用（工作流）**: ['openspec list 获取全部 active changes（无则提示停止）', '用户多选变更（含 All changes 选项，绝不自动全选）', '逐变更收集工件状态/任务完成度/delta spec，统一校验（冲突检查与代码库核对），窄化 delta 同步范围（排除未实现 delta），混合 schema 独立评估后统一归档']
- **怎么用（协作）**: 上游衔接多个 verify-change 完成的变更；内部复用 sync-specs 合并逻辑

## skill-openspec-continue-change — openspec-continue-change
- 组: A6l-工作流 | Layer 0
- 作用: 继续已有变更，按 DAG 依赖顺序生成下一个未完成工件。解析状态判断 ready/blocked，获取 instructions（模板+context+rules）创建单个工件后停止，适合恢复中断工作。
- 提供: ['变更选择（最近修改推荐）', 'DAG 工件状态解析（done/skipped/ready/blocked）', '单工件生成（模板+context+rules+resolvedOutputPath）', 'skip_specs 工件跳过', '依赖文件磁盘重读']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。对应 OpenSpec 工件 DAG 的"增量路径"：按 DAG 依赖顺序生成下一个未完成工件后停止。引入动机：恢复中断的工作——会话打断后不需重头再来，一条命令续上缺失工件。0803 解析报告明确指出 continue 走增量路径是工件 DAG 相对瀑布流程的关键优势。
- **为什么存在（当前）**: 本地任务跨会话/被中断频繁（如多阶段 DAG 交付、长任务 checkpoint），continue-change 是恢复上下文的标准入口；也用于 openspec-apply-change 检测到 blocked 状态时的引导。
- **怎么用（触发）**: 继续已有变更时触发（用户说"继续上次的变更"）；description 触发词"继续""恢复中断"；或显式 /openspec-continue-change。
- **怎么用（工作流）**: ['选择变更（按最近修改排序并推荐最新者）', '解析 status 判断 artifacts 状态（done/skipped/ready/blocked）', '对首个 ready 工件获取 instructions（模板+context+rules）创建单个工件后停止，全部完成则提示可实施或归档']
- **怎么用（协作）**: 上游衔接 new-change/propose（工件创建续作）；被 apply-change 在 blocked 时推荐；被 superpowers 编排器用作 continue-dev 交接命令

## skill-openspec-explore — openspec-explore
- 组: A6l-工作流 | Layer 0
- 作用: 探索模式立场：分析代码、理清需求、比较方案，不写代码。自由提问与 ASCII 可视化，可创建 proposal/design/specs 等思考产物（捕获思考非实施）。
- 提供: ['问题空间探索与澄清提问', '代码库调查与集成点分析', '方案对比表与权衡', 'ASCII 图可视化', '风险与未知面识别', 'OpenSpec 思考产物创建']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装批量引入（来自 OpenSpec 上游 14 skills，作者 openspec）。0803 完成 OpenSpec/Superpower 设计细粒度解析后，用户决定取长补短、按需本地化，在 Plan 阶段识别出 openspec-superpowers 与已有 skill 重叠而剔除，最终保留 13 个 openspec skills + README，全部改为中文简短描述（zero-shot CoT）。explore 是其中"思考立场"型 skill：OpenSpec 设计哲学是 CLI 提供信息、Agent 做决策，探索模式不写代码、只分析需求与方案，作为进入工件 DAG 前的自由思考入口。
- **为什么存在（当前）**: 所有 OpenSpec 变更的思考前置：分析代码、理清需求、比较方案、可视化权衡。当前 DAG 化改造（0817-opencode-dag）中，装配层历史事件采集即由 explore 型子Agent 完成；本地系统强调 Plan 先行（Grill-Me 协议），explore 是 Plan 阶段的分析立场。
- **怎么用（触发）**: 用户不确定要做什么、需要先思考再动手时触发；description 触发词含"探索""分析需求""比较方案"；或显式 /openspec-explore。
- **怎么用（工作流）**: ['进入探索立场：自由提问、挑战假设、重构问题，允许 ASCII 图可视化', '调查代码库：映射现有架构、找集成点、识别隐藏复杂度、做方案对比表', '绝不写实现代码；可创建 proposal/design/specs 等思考产物（捕获思考而非实施），想实施时提示先退出 explore 创建变更提案']
- **怎么用（协作）**: 与 openspec-propose/ff-change/new-change 衔接（探索结论 → 工件生成）；可作为子Agent 采集语义时使用

## skill-openspec-ff-change — openspec-ff-change
- 组: A6l-工作流 | Layer 2
- 作用: 快速通道一键生成所有 OpenSpec 工件，跳过逐步交互。按 requires 依赖边传递闭包确定必建工件集合（applyRequires 可达集），循环创建 proposal/specs/design/tasks。
- 提供: ['变更名 kebab-case 派生', '依赖序工件批量生成', 'applyRequires 传递闭包计算', '条件工件跳过（design 可选）', '进度 todo 跟踪']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。FF = fast-forward，一键生成所有 OpenSpec 工件跳过逐步交互。0803 解析报告识别其机制：按 requires 依赖边传递闭包（applyRequires 可达集）确定必建工件集合，循环创建。引入动机：为有经验用户或简单变更提供快速通道，避免逐个确认的低效。
- **为什么存在（当前）**: 简单变更或用户有经验时的默认快速路径；本地 DAG 化任务中作为快速建模入口，减少交互轮次。
- **怎么用（触发）**: 用户要求快速生成全部 OpenSpec 工件（"快速通道""ff"）；或显式 /openspec-ff-change；有经验用户处理简单变更时。
- **怎么用（工作流）**: ['派生变更名（无输入则询问要构建什么）', 'openspec new change 创建脚手架，解析 status 的 applyRequires 与 artifacts requires 边', '按依赖序循环对每个 ready 工件获取 instructions 并生成，todo 列表跟踪进度，处理 skip_specs/可选 design 条件跳过']
- **怎么用（协作）**: 与 propose 等价入口（两者都封装全生成）；下游交给 apply-change 实施

## skill-openspec-new-change — openspec-new-change
- 组: A6l-工作流 | Layer 1
- 作用: 逐步交互式创建新变更，比 propose 更细粒度。仅创建变更目录并展示第一个工件模板后停止，等待用户方向，适合复杂或需精细控制的场景。
- 提供: ['schema 选择（--schema 或 openspec schemas）', '变更脚手架创建', '首个工件 instructions 展示', '防越步守门（不创建任何工件）', 'kebab-case 名称校验']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。与 propose 互补：propose 一键全生成，new-change 是实验性 artifact-driven 逐工件交互式创建——只创建变更目录并展示首个工件模板后停止，等待用户逐级确认。引入动机：为"复杂或需精细控制的场景"提供比 propose 更细粒度的路径，防止一次生成导致方向偏差。
- **为什么存在（当前）**: 复杂变更需要逐步确认每个工件时使用；本地改造强调 Grill-Me 逐项决策，new-change 与之同构（一步一确认），适合精细控制场景。
- **怎么用（触发）**: 用户要求逐步创建新变更、需要精细控制时；description 触发词"逐步创建""细粒度"；或显式 /openspec-new-change。
- **怎么用（工作流）**: ['询问要构建什么，派生 kebab-case 变更名', '选择 workflow schema（默认 spec-driven，用户点名时用 openspec schemas 选择）', '创建变更脚手架后展示第一个工件模板即停止，等待用户方向后再继续（防越步守门）']
- **怎么用（协作）**: 与 openspec-continue-change 衔接（后续工件逐个续做）；被 superpowers-openspec-superpowers-workflow 作为细粒度模式引用

## skill-openspec-onboard — openspec-onboard
- 组: A6l-工作流 | Layer 2
- 作用: 引导首次用户完成完整 OpenSpec 流程的教学技能，边做边讲。预检 CLI 安装后走 welcome→选任务→建变更→proposal/specs/design/tasks→实现→归档的完整周期。
- 提供: ['CLI 安装预检', '任务选择（TODO/FIXME 扫描+git 活动）', '完整周期教学引导', '15-20 分钟实战走查']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。引导首次用户完成完整 OpenSpec 流程的教学 skill：预检 CLI 后走 welcome→选任务→建变更→proposal/specs/design/tasks→实现→归档完整周期。引入动机：OpenSpec 工件 DAG 概念（requires 边/Delta/归档）对新手有学习曲线，需要边做边讲的实战教学入口，降低首次使用门槛。
- **为什么存在（当前）**: 新成员/新项目引入 OpenSpec 工作流时；教学式引导保证首次使用者理解工件 DAG 全流程（与本地"培训/教学"类任务需求一致）。
- **怎么用（触发）**: 首次使用 OpenSpec 的用户请求引导（description 触发词"引导""教程""首次"）；或显式 /openspec-onboard。
- **怎么用（工作流）**: ['预检 OpenSpec CLI 是否安装（未装则提示先安装）', '欢迎 + 选任务（TODO/FIXME 扫描 + git 活动）', '在真实代码库边做边讲完整周期（建变更→四工件→实现→归档），15-20 分钟实战走查']
- **怎么用（协作）**: 教学主入口；周期内各步骤映射到 new-change/propose/apply/verify/archive 各 skill

## skill-openspec-propose — openspec-propose
- 组: A6l-工作流 | Layer 2
- 作用: 一键生成变更提案：创建 change 并生成全部工件（proposal/specs/design/tasks）。明确知道要做什么时使用，生成后交给 apply-change 实施。
- 提供: ['一键提案生成', 'spec-driven 四工件生成', '依赖序循环生成', 'skip_specs 感知', '接续 apply-change']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。0803 解析报告识别其本质是封装 continue+ff 的一步式入口：创建 change 并一键生成全部工件（proposal/specs/design/tasks）。引入动机：让"明确知道要做什么"的场景不必逐步交互，直接产出 spec-driven 四工件，交给 apply-change 实施。对应 OpenSpec 工件 DAG 的快速入口设计。
- **为什么存在（当前）**: 当前用于本地装配层改造（如 openspec 系列技能自身维护、DAG 交付物生成）等明确变更的提案创建；与 apply-change 配对构成"提案→实施"主链路。
- **怎么用（触发）**: 用户明确知道要做什么、需要创建变更提案时；description 触发词"变更提案""propose"；或显式 /openspec-propose <变更名>。
- **怎么用（工作流）**: ['从用户描述派生 kebab-case 变更名（无输入则开放式提问）', '创建 change 目录，按 spec-driven 默认 schema 生成 proposal/specs/design/tasks 四工件（依赖序循环）', '完成后提示接续 /openspec-apply-change 实施']
- **怎么用（协作）**: 上游衔接 openspec-explore；下游交给 openspec-apply-change；被 superpowers-openspec-superpowers-workflow 编排器作为工件生成步骤引用

## skill-openspec-sync-specs — openspec-sync-specs
- 组: A6l-工作流 | Layer 0
- 作用: 将 delta spec 同步到主 spec（不归档），agent 驱动读取 delta 并智能编辑主 spec，处理 ADDED/MODIFIED/REMOVED/RENAMED 段。仅被 archive-change 或显式召唤时使用。
- 提供: ['delta spec 定位（existingOutputPaths 唯一来源）', '主 spec 路径解析（store 感知 planningHome.root）', 'ADDED/MODIFIED/REMOVED/RENAMED 合并', '窄化同步范围（显式名单）']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。agent 驱动的 delta→主 spec 同步操作（不归档）：读 delta specs 直接编辑主 specs，允许智能合并（如加场景不复制整个需求）。引入动机：Delta Spec 机制的中间态——归档前需要把增量合并进主 spec，但合并要"智能"而非机械覆盖，故做成独立 agent 驱动 skill。仅被 archive-change 或显式召唤时使用。
- **为什么存在（当前）**: 归档流程内部依赖（archive-change 调用）；需要独立合并 delta 不归档时显式使用；是主 spec 知识库保持新鲜的机制。
- **怎么用（触发）**: 仅被 archive-change 内部调用或用户显式召唤（description 明确"仅被 archive-change 或显式召唤时使用"）。
- **怎么用（工作流）**: ['选择有 delta spec 的变更（specs/ 目录）', '解析 status 的 planningHome.root（store 感知主 spec 路径）', '按 existingOutputPaths 唯一定位 delta，对 ADDED/MODIFIED/REMOVED/RENAMED 段智能合并进主 spec，窄化同步范围（显式名单）']
- **怎么用（协作）**: 被 archive-change/bulk-archive-change 内部调用；与 openspec-update-change 互补（update 管工件，sync 管 spec）

## skill-openspec-update-change — openspec-update-change
- 组: A6l-工作流 | Layer 2
- 作用: 编辑/协调已有 OpenSpec 工件并保持一致性，处理手动修改后的重新同步。按请求做定向修改或一致性审查，逐工件确认后写入，不创建缺失工件。
- 提供: ['一致性审查（矛盾/缺口/重复）', '跨工件双向协调（任意方向）', '逐工件确认写入', '不创建缺失工件（指向 continue-change）']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。编辑/协调已有 OpenSpec 工件并保持一致性，处理手动修改后的重新同步，不创建缺失工件。引入动机：OpenSpec 工件是文件系统状态（状态=文件系统内容，0803 解析），用户可能手动改工件导致漂移，需要协调工具保持 proposal/specs/design/tasks 间一致。
- **为什么存在（当前）**: 工件被手动修改或需求变更需要跨工件协调时；本地改造中 SKILL.md/规格文档被人工编辑后的一致性校验，与"修改安全链"理念一致。
- **怎么用（触发）**: 编辑/协调已有 OpenSpec 工件时（description 触发词"编辑""协调""重新同步"）；或显式 /openspec-update-change。
- **怎么用（工作流）**: ['选择变更（按最近修改推荐）', '一致性审查（矛盾/缺口/重复）或按请求定向修改', '跨工件双向协调（任意方向），逐工件确认后写入；不创建缺失工件（缺失时指向 continue-change）']
- **怎么用（协作）**: 与 continue-change 区分（update 不新建工件）；上游衔接手动编辑场景；被 apply/archive 作为一致性保障

## skill-openspec-verify-change — openspec-verify-change
- 组: A6l-工作流 | Layer 0
- 作用: 归档前可选校验：验证实现是否匹配 spec/design/tasks。从完整性/正确性/一致性三维度生成 CRITICAL/WARNING/SUGGESTION 级别的验证报告。
- 提供: ['三维验证报告（完整性/正确性/一致性）', '任务与 spec 覆盖核对', '严重级别分类（CRITICAL/WARNING/SUGGESTION）', '修复建议']
- **为什么存在（历史）**: 2026-08-04 随 Superpower 安装引入（OpenSpec 上游，author openspec）。归档前的可选校验步骤：验证实现是否匹配 spec/design/tasks，从完整性/正确性/一致性三维度生成 CRITICAL/WARNING/SUGGESTION 报告。引入动机：OpenSpec 的"先规格后实现"需要回环验证，防止实现漂移；0805-Reflection系统设计文档将其列为"已有类似 Reflection 机制"之一（Plan 验证信号）。
- **为什么存在（当前）**: 归档前的质量闸门：验证实现与工件一致后才允许归档；当前 DAG 交付与装配层改造中的规格实现均以此为一致性校验参照。
- **怎么用（触发）**: 实现完成后、归档前可选调用（description 触发词"验证""校验"）；或显式 /openspec-verify-change。
- **怎么用（工作流）**: ['选择有 tasks 工件的变更（未完成任务标 In Progress）', '解析 status 与 schema，比对 tasks/spec/design 与实现', '输出三维验证报告（CRITICAL/WARNING/SUGGESTION）与修复建议']
- **怎么用（协作）**: 上游衔接 apply-change；下游衔接 archive-change/sync-specs；被 Reflection 系统作为验证信号参照

## skill-pdf-ocr — pdf-ocr
- 组: A6d-文档处理 | Layer 1
- 作用: PDF OCR 识别专项，处理扫描件、图片型 PDF、含水印/印章的文档。支持中英多语言 OCR、表格区域提取、印章检测。仅在 PDF 无文本层（read_pdf 返回空）时加载，先检测再按需补充 OCR 空页面。
- 提供: ['pdf-reader MCP pdf_evidence 工具调用规范（ocr_pages/extract_regions/analyze_regions/render_page）', '/pdf-ocr 与 /pdf-ocr-table 指令路由（含极简参数自动选择）', '文本层检测-补充-合并流程']
- **为什么存在（历史）**: 从 @sylphx/pdf-reader-mcp 分离的轻量路由包装（87 行），引入动机：pdf-reader MCP 的 read_pdf 对扫描件/图片型 PDF 返回空文本层，需要 OCR 降级链路。0807-VLM图片识别修复前 read 工具读图片不可靠，PDF 无文本层时需 pdf_evidence 的 ocr_pages/extract_regions/analyze_regions/render_page 四操作。0802 盘点定位为仅在 PDF 无文本层时触发 OCR 的专用 skill。
- **为什么存在（当前）**: 扫描件/图片型 PDF/含水印印章文档的持续需求（简历评审、offer 拒绝决策、证件扫描件等）。pdf-worker 子Agent（Flash + pdf-reader MCP 最小权限）专职 PDF 提取/OCR/文档分析，主Agent MCP 路由将 PDF/OCR 任务固定委派给它。0815 桥接后降权（disable-model-invocation），仅手势 /pdf-ocr 触发。
- **怎么用（触发）**: 满足任一条件加载：1) read_pdf 返回空文本层（扫描件）；2) 用户明确要求 OCR/扫描件识别；3) PDF 含印章、手写、水印等需图像识别元素（SKILL.md 触发条件）。指令：/pdf-ocr {路径} [--lang zh+en]、/pdf-ocr-table、/pdf-ocr-check。
- **怎么用（工作流）**: 1) 先 read_pdf（include_text_layer: true）检查文本层；2) 部分页面空则仅 OCR 空页面，全空则全量 OCR（ocr_pages，languages zh/en，scale 2，max_pages 20）；3) 表格提取：analyze_regions 定位边界框后 extract_regions 提取；4) 极简用法 read_pdf include_ocr_text_layer=true 自动选参。
- **怎么用（协作）**: 与 pdf-reader MCP（@sylphx/pdf-reader-mcp，pdf_evidence 工具）、pdf-worker 子Agent（L3 最小权限仅放行 pdf-reader_*）、vision-interceptor/GLM-4V（图片辅助校验）协作。

## skill-postmortem-failure-review — postmortem-failure-review
- 组: A6m-自进化 | Layer 1
- 作用: 失败项目复盘方法论：先区分路线错误与执行错误，五因框架分类失败，双 explore 并行探索（失败项目+参考项目），A/B/C 资产盘点，产出 v2 设计建议与 MVP 最小化清单。
- 提供: ['根因层级判定（路线 vs 执行）', '五因分类框架（路线/能力未就绪/过度工程/门控缺失/门槛过高）', '双 explore 委派+dead code 审计', 'A/B/C 资产分级（复用价值×影响力排序）', 'v2 设计建议+MVP 范围最小化', '5 段式复盘报告']
- **为什么存在（历史）**: 2026-08-05 23:43 创建（文件 CreationTime 证据），由 0805-网申扩展失败复盘 提炼（推断：当天失败复盘完成并留档，随即固化为方法论 skill）。0805-网申扩展失败复盘报告记载：自制网申扩展（10 Agent 矩阵、60+ 源码文件、13 BLOCKER 全修复）最终被标记失败，复盘发现五类根因——路线选择错误（架构与参考模式背道而驰）、核心能力从未就绪、过度工程（架构幻影死代码）、产品质量门控缺失、用户门槛过高（7 步安装 vs 参考方案加载即用），并产出可复用资产清单（A/B/C 三级）。本 skill 将这套复盘方法论固化为五因框架 + 双 explore 并行 + 资产盘点 + v2 建议的标准化流程。
- **为什么存在（当前）**: 失败/部分失败项目的系统性复盘入口：先区分路线错误与执行错误（路线错误代价高且无法修补），五因框架分类，产出 5 段式复盘报告+可复用资产清单；当前 DAG 改造等高风险任务完成后可用作事后质量审计。
- **怎么用（触发）**: 触发关键词：失败复盘、为什么失败、复盘、postmortem、教训、项目失败分析；用户对失败项目要求系统性复盘时。
- **怎么用（工作流）**: ['Step1 根因层级判定：对照参考项目判断架构模式是否一致（路线错误最高优先级）', 'Step2 并行探索：委派 explore-failed-project（dead code 审计）与 explore-reference（核心模式统计+gap 分析）两个 explore Agent', 'Step3 资产盘点 A/B/C 三级（复用价值×影响力排序）+ 产出 v2 设计建议与 MVP 最小化清单 + 5 段式复盘报告']
- **怎么用（协作）**: 委派 2 个 explore 子Agent（失败项目/参考项目）；产出资产清单交给 reusable-asset-inventory；复盘结论回流 Reflection 系统（本 skill 自身即反思产物）

## skill-recruit-assist — recruit-assist
- 组: A6e-简历求职 | Layer 1
- 作用: 简历投递辅助：投简历（浏览器打开招聘页+记录跟踪表）、识别简历（扫描表单字段匹配信息库）、维护信息库、记录投递状态、跟踪企业，飞书增量同步跟踪表。
- 提供: ['浏览器自动化投递（browser-harness CDP）', '表单字段识别与信息库匹配', 'Excel 跟踪表读写（tracker_writer.py）', '飞书增量上传/全量下载同步（sync_feishu.py）', '企业类型识别（detect_enterprise_type.py）', 'URL 到渠道映射（url_to_channel.py）', '同步状态机（.sync_state.json）']
- **为什么存在（历史）**: 完全自创（无上游），2026-07-04 创建（早于 8 月改造周期），2026-08-05 重大优化。初始动机：简历投递全流程自动化——投简历（浏览器打开招聘页+记录跟踪表）、识别简历（扫描表单字段+匹配信息库）、飞书表格双向同步。0804-recruit优化报告记载：京东校招投递（campus.jd.com）执行严重卡壳（浏览器脚本试错 4+ 次、行定位误判、row 追加失败），用户反馈"执行过程很卡壳，反思总结经验然后计划优化原 skill"，据此新增 tracker_writer.py 一体化脚本（JSON 输入→备份→定位→写入→打包→全量验证→失败回滚）并修正 SKILL.md 三处错误。0805 又发生简历跟踪上传事故（京东数据误写 row 774 导致 737 空行污染飞书），再修正则+游标定位。0802-opencode改造盘点报告认定其为"完全自创"。
- **为什么存在（当前）**: 求职季投递主场景：投简历、跟踪企业、飞书同步持续使用；browser-harness（CDP 浏览器自动化）与 tracker_writer.py 组成的投递管线是当前求职流程核心工具（0815-opencode-dsh桥接将其收入 exec-recruit 特设 preset 与 browser-harness 搭配）。
- **怎么用（触发）**: 触发关键词：投简历、识别简历、更新信息库、记录投递、跟踪企业、招聘、简历投递、上传简历跟踪、下载简历跟踪、提取表单；或显式 /recruit-assist（0815 起为 user-invocable 手势）。
- **怎么用（工作流）**: ['投简历：启动 Chrome 远程调试（chrome-debug.ps1）→ browser-harness CDP 打开招聘页 → tracker_writer.py add 写入投递跟踪表', '识别简历/更新信息库/记录投递/跟踪企业：表单字段扫描（JS IIFE 提取）匹配信息库', '飞书同步：sync_feishu.py 增量上传/全量下载（.sync_state.json 状态机），上传/下载简历跟踪']
- **怎么用（协作）**: 依赖 browser-harness skill（CDP 浏览器自动化）；与 resume-builder/soe-resume 构成简历求职 skill 群（0815 起共同收入 exec-recruit preset）；Excel 跟踪表/飞书表格为外部数据源

## skill-release-openspec — release-openspec
- 组: A6l-工作流 | Layer 0
- 作用: OpenSpec 自身发布管理技能，以可恢复状态机运行发布工作流：每次调用检查 GitHub 实时状态，只执行下一步安全动作，不假设前次调用已完成。仅 OpenSpec 维护者使用，Fission-AI/OpenSpec 与 origin/main 为发布源。
- 提供: ['发布审计流程（gh repo view / gh release list / gh pr list 检查）', 'Changeset PR 与 Version Packages PR 双类型区分与处理', '临时 worktree 发布提交（脏工作区时）', 'merge-queue 中间态处理（等待 mergedAt 确认）', 'agents/ 与 references/ 子目录支持文档']
- **为什么存在（历史）**: 2026-08-04 Superpower 安装引入：随 OpenSpec 14 Skills 一同从 Fission-AI/OpenSpec 仓库复制（0803-OpenSpec_Superpower解析/source/openspec/skills/release-openspec/ 为源）。上游定位：OpenSpec 自身发布管理 skill，仅 OpenSpec 维护者使用。安装时即作为 16 个新增 SKILL.md 之一，description 为 YAML 多行格式（安装时需精确匹配 >- 段落字符串）。
- **为什么存在（当前）**: 本机作为 OpenSpec 维护者的发布操作入口（Fission-AI/OpenSpec 仓库维护场景）；0815 桥接后降权（disable-model-invocation，item28 决策），仅维护者在 openspec-plan preset 内显式召唤。以可恢复状态机运行发布工作流（每次检查 GitHub 实时状态，只做下一步安全动作），不假设前次调用完成。
- **怎么用（触发）**: 仅 OpenSpec 维护者使用（SKILL.md description）；用户请求 release / prepare a release / continue / resume 时触发；请求 status/readiness/advice 时默认只读审计。
- **怎么用（工作流）**: 1) 发布审计：gh repo view 验证仓库、要求 gh/git/pnpm 认证、git fetch origin main；2) 找最新稳定 release（gh release list --exclude-drafts --exclude-pre-releases）；3) 区分两类 PR（Changeset PR 人工添加 .changeset/*.md；Version Packages PR 自动化 changeset-release/main）；4) 脏 checkout 时用临时 worktree 做发布提交；5) 永不批准自己的 PR（人工审查是刻意门）；6) merge-queue 进队不等于合并，等 GitHub 报 mergedAt 且 main 上有该 commit；7) 暂停时报告 URL/状态/所需人工动作。
- **怎么用（协作）**: 与 gh/git/pnpm CLI、GitHub（Fission-AI/OpenSpec）、Changesets action（Version Packages PR）、openspec 系列 skill（openspec-plan preset 内降权成员）协作。

## skill-resume-builder — resume-builder
- 组: A6e-简历求职 | Layer 0
- 作用: 简历制作助手：从零创建、ATS 优化、岗位定制（JD 关键词提取）、求职信、面试准备（STAR）与简历评分修改建议，基于 Novoresume/Jobscan 等权威来源方法论。
- 提供: ['/resume-create 从零创建', 'ATS 优化与简历评分', 'JD 岗位定制', 'cover letter 生成', 'STAR 面试演练', '6 大板块简历模板']
- **为什么存在（历史）**: 自创/整合，2026-05-28 创建（早于 8 月改造周期）。0802-opencode改造盘点报告：上游最接近 yanliudesign/resume-builder-skill（36 星），本地整合 Novoresume/Jobscan/Coursera/ResumeGenius/freeCodeCamp 等 5+ 权威来源方法论，5 大命令体系（/resume-create 从零创建、ATS 优化、岗位定制、求职信、面试准备）。引入动机：用户处于求职季（硕士在读，需中英文简历多版本），需要系统化的 ATS 友好简历方法论与岗位定制能力，而非零散技巧。参考文档存放于 D:\学，都可以学\研一\简历相关\opencode缓存\。
- **为什么存在（当前）**: 求职季简历创作主工具：从零创建、ATS 优化、JD 关键词定制、cover letter、STAR 面试演练持续使用（0811-英文简历制作任务即其方法论应用）；0815 起与 recruit-assist/soe-resume 共同收入 exec-recruit preset（简历求职域）。
- **怎么用（触发）**: 触发关键词：简历、resume、CV、求职信、cover letter、面试、改简历、写简历、优化简历、找实习、找工作、STAR、ATS；或显式 /resume-builder（user-invocable 手势，0815 起 disable-model-invocation 仅手势入口）。
- **怎么用（工作流）**: ['/resume-create 从零创建：收集背景+目标岗位 → 分析 JD → 生成完整简历内容', 'ATS 优化与评分：按 ATS 标准检查格式/关键词，简历评分与修改建议', '岗位定制（JD 关键词提取）→ 生成配套 Cover Letter → STAR 法则面试准备']
- **怎么用（协作）**: 与 recruit-assist（投递）、soe-resume（央国企简历）构成简历求职三件套；知识源来自 5+ 权威英文来源；输出到简历相关目录供后续投递使用

## skill-reusable-asset-inventory — reusable-asset-inventory
- 组: A6m-自进化 | Layer 0
- 作用: 从失败/遗留项目提炼可复用资产：A/B/C 三级分类（直接复用/需修改/仅思路）+优先级排序公式+参考项目对标，gap 清单直接映射 v2 补全优先级。
- 提供: ['A/B/C 三级分类标准', '复用价值×影响力优先级排序', '参考项目对标（组件数/核心模式/gap）', 'gap 清单→v2 补全优先级映射', '可复用资产清单产出']
- **为什么存在（历史）**: 2026-08-05 23:43 创建（文件 CreationTime 证据），由 0805-网申扩展失败复盘提炼（推断：与 postmortem-failure-review 同批固化）。0805-网申扩展失败复盘的可复用资产清单.md 是其直接原型：从自制扩展+参考塔塔网申神器两项目中提取 A/B/C 三级资产（A1 Handler trigger 逻辑 54 个函数、A2 表单扫描管道、A3 XPath 生成工具、A4 CSS、A5 元素分组系统），按"复用价值×影响力"排序，gap 清单映射 v2 补全优先级。本 skill 将"失败项目≠全盘皆输"的抢救方法论固化为独立 skill：三级分类标准 + 优先级排序公式 + 参考项目对标。
- **为什么存在（当前）**: 项目失败或重写 v2 前抢救可复用资产的标准流程；客观评估哪些代码值得保留、哪些该丢弃；与 postmortem 配对构成"失败→抢救"闭环（失败复盘后必接资产盘点）。
- **怎么用（触发）**: 触发关键词：可复用资产、资产盘点、复用清单、资产清单、asset inventory、代码复用评估；项目失败/重写前需要盘点旧资产时。
- **怎么用（工作流）**: ['A/B/C 三级分类：A 可直接复用（成熟独立已验证）→ 直接移植；B 需修改复用（耦合旧架构）→ 列修改点再移植；C 仅参考思路（依赖已废弃路线）→ 只提取设计思路', '优先级排序：复用价值（独立完整性×逻辑成熟度）× 影响力（对填入成功率/核心能力贡献），输出"最高优先级 > ... > 最低"', '对标参考项目：统计关键组件数（如 Handler 数）+ 提炼核心模式（如"服务端驱动+4 级 fallback 链"）+ 找 gap → gap 清单直接映射 v2 补全优先级']
- **怎么用（协作）**: 被 postmortem-failure-review Step3 调用（资产盘点环节）；产出供 v2 重写规划；参考项目探索依赖 explore 子Agent

## skill-soe-resume — soe-resume
- 组: A6e-简历求职 | Layer 0
- 作用: 央国企/体制内简历制作、评审与优化助手。三大功能：简历评审（8 维度评分 + 红黄绿灯）、简历修改（先评审确认后改写）、从零生成（读取个人信息 + 交互问答）。内置 CV4SOE 4 维度转换方法论（动词行政化升级/视角宏观化包装/关键词安全合规/软实力组织化呈现）。
- 提供: ['/央国企简历评审 指令（8 模块×红黄绿灯逐模块评分）', '/央国企简历修改 指令（前置评审→方案确认→改写）', '/央国企简历生成 指令（本地文件+交互问答）', '自动识别规则（pdf/docx/md 输入→评审或修改；无文件→生成）', 'reference/ 方法论文档']
- **为什么存在（历史）**: 完全自创 skill（无上游，0802 盘点标注），2026-08 求职季为央国企/体制内求职需求自建：应届生校招（央企国资委直管 97 家/地方国企/事业单位/公务员）+ 往届社招。内置 CV4SOE 四维度转换方法论（动词行政化升级/视角宏观化包装/关键词安全合规/软实力组织化呈现），解决普通简历写法不符合央国企网申系统规范与 HR 评审偏好的问题。三指令：评审（8 模块红黄绿灯）/修改（先评审后改写）/生成（本地文件+问答）。
- **为什么存在（当前）**: 央国企求职持续场景（国家电网/中石化等网申前必经评审）。0815 起收入 exec-recruit preset（简历投递特化 agent），与 resume-builder/recruit-assist/lark-suite 并列降权 skill，用户手势 /soe-resume 唯一入口；Word 管线改调 minimax-docx。0816 补 user-invocable: true 字段。
- **怎么用（触发）**: 触发关键词：央国企简历、央企简历、国企简历、SOE简历、体制内简历、央企求职、国企求职、国家电网简历、中石化简历（SKILL.md description）。自动识别：pdf/docx/md 简历输入则评审或修改；帮我做/写/生成一份央国企简历且无文件则生成模式。用户手势 /soe-resume。
- **怎么用（工作流）**: 1) /央国企简历评审 {路径}：8 模块评分（个人信息/教育/实习/项目等）+ 红黄绿灯速览；2) /央国企简历修改 {路径}：先评审（如未评审）后展示修改方案，用户确认后执行；3) /央国企简历生成：读个人信息文件 + 交互问答补全后生成 SOE 风格简历（Word 输出走 minimax-docx 三管线）。
- **怎么用（协作）**: 与 minimax-docx（Word 输出管线）、resume-builder / recruit-assist / lark-suite（exec-recruit preset 手势组）、CV4SOE 方法论来源（github.com/Ignareo/CV4SOE）协作。

## skill-superpowers-feature-workflow — superpowers-feature-workflow
- 组: A6l-工作流 | Layer 1
- 作用: 规范开发流程：需求澄清→方案设计→TDD 实现→验证。不依赖 OpenSpec CLI 的轻量级规范编程工作流。显式 opt-in 技能，仅当用户明确要求、点名 $superpowers-feature-workflow 或仓库策略强制时使用。
- 提供: ['10 步工作流（探索→逐条澄清→2-3 方案→设计文档→确认→实施计划→worktree→TDD→新鲜验证→记忆更新）', 'docs/superpowers/specs 与 plans 目录约定', '4 条 Guardrails（无设计批准不写生产代码等）']
- **为什么存在（历史）**: 2026-08-04 Superpower 安装引入（0804-Superpower安装/安装报告.md）：用户需求为本地 OpenCode 安装 Superpower skill，用于提高编程和源码解析的流程规范性。来源 obra/superpowers 仓库（shallow clone 解析后安装 3 Bundles 之一）。选择理由：不依赖 OpenSpec CLI 的轻量级规范编程工作流（需求澄清到方案设计到 TDD 实现到验证）。安装时明确不安装冗余组件：openspec-superpowers/openspec-feature 与已有 skill 重叠，.superpowers-memory/ 模板与 MEMORY.md + headroom 重叠。
- **为什么存在（当前）**: 显式 opt-in 的规范开发流程：当用户要求纪律化功能交付（且不想要 OpenSpec 工件生成）时提供 10 步工作流 + 4 条 Guardrails。0815 桥接时记忆载体从 .superpowers-memory/ 改为 dsh 原生 .agents/notes（避免第二套记忆体系）。适合中小型功能开发的质量门控。
- **怎么用（触发）**: 显式 opt-in：仅当用户明确要求、点名 $superpowers-feature-workflow 或仓库策略强制时使用；不默认启用（SKILL.md）。
- **怎么用（工作流）**: 1) 探索项目上下文（.superpowers-memory/ 存在则读 PROJECT_CONTEXT/CURRENT_STATE/journal）；2) 一次一问澄清需求；3) 给 2-3 方案并推荐一个；4) 设计写入 docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md；5) 用户确认设计；6) 实施计划写 docs/superpowers/plans/；7) 非平凡任务用 repo-local worktree；8) TDD 实现（红灯到最小代码到绿灯）；9) 新鲜验证后才声称完成；10) 更新记忆文件。Guardrails：设计批准前不写生产代码、新行为不跳失败测试、无新鲜命令输出不声称完成。
- **怎么用（协作）**: 与 superpowers-learning-workflow（记忆沉淀）、superpowers-openspec-superpowers-workflow（编排依赖：组合工作流 standalone:false 依赖本 skill）、.superpowers-memory/（opencode 侧）/ .agents/notes（dsh 侧）协作。

## skill-superpowers-learning-workflow — superpowers-learning-workflow
- 组: A6l-工作流 | Layer 0
- 作用: 会话后知识沉淀工作流，回写项目记忆、决策记录与可复用教训。将学习成果分类为持久事实、当前状态、会话结果、可复用教训四类，写入 .superpowers-memory/ 记忆文件。显式 opt-in，按需显式召唤。
- 提供: ['6 步学习分类工作流（回顾→分类→更新记忆文件→总结下会话应记住的内容）', '记忆文件更新（PROJECT_CONTEXT/CURRENT_STATE/journal/LEARNING_BACKLOG）', '3 条 Guardrails（稳定事实与临时笔记分离等）']
- **为什么存在（历史）**: 2026-08-04 Superpower 安装引入（同 superpowers-feature-workflow），obra/superpowers 仓库 3 Bundles 之一。引入动机：会话后知识沉淀的规范化——把近期工作教训按四类分类（持久事实/当前状态/会话结果/可复用教训）回写项目记忆，防噪音、防一次性修复升格为规则。安装时评估认为 .superpowers-memory/ 模板与本地 MEMORY.md 体系重叠故不装脚手架，仅保留 workflow skill 本身。
- **为什么存在（当前）**: 显式召唤的知识沉淀工作流：项目结束/里程碑后主动回写记忆、决策记录、可复用教训，解决 AI 是金鱼（跨会话记忆缺失）的痛点。0815 桥接后与本地 learning-workflow skill（来源同款）等价，载体映射为 AGENTS.md + .agents/notes 或 Mission 5 段报告。
- **怎么用（触发）**: 显式 opt-in：用户想保留近期工作教训、点名 $superpowers-learning-workflow 或仓库策略要求时触发；不默认启用（SKILL.md）。
- **怎么用（工作流）**: 1) 回顾近期工作/决策/验证证据；2) 分类为持久事实、当前状态、会话结果、可复用教训四类；3) .superpowers-memory/ 存在则更新 PROJECT_CONTEXT.md、CURRENT_STATE.md、journal、LEARNING_BACKLOG.md；4) 不存在则告知用户装脚手架或存普通项目文档；5) 稳定事实与临时笔记分离；6) 总结下一会话该记住什么。Guardrails：不写任务噪音进 PROJECT_CONTEXT、一次性修复不升格规则、不自动编辑 skill 库。
- **怎么用（协作）**: 与 superpowers-feature-workflow（交付流程配套）、Reflection 系统（0805 引入的本地替代/互补机制：pending.json + reflection-worker）、MEMORY.md 记忆体系协作。

## skill-superpowers-openspec-superpowers-workflow — superpowers-openspec-superpowers-workflow
- 组: A6l-工作流 | Layer 3
- 作用: 完整交付流程编排器：Superpowers 探索→OpenSpec 锁定→TDD 实施→验证→归档，全程门控。作为路由控制者防止误路由到 OpenSpec proposal skill，要求先完成 Superpowers 探索才允许 OpenSpec 工件生成。
- 提供: ['25 步编排工作流（探索→设计→OpenSpec 工件依赖序 proposal→design→spec→tasks→TDD→验证→归档）', 'openspec status/instructions --json 检查流程', '交接命令（continue-dev/continue-review/continue-archive）', '严格 Guardrails（路由保护：不得先路由到 openspec-propose）']
- **为什么存在（历史）**: 2026-08-04 Superpower 安装引入（obra/superpowers 3 Bundles 之一），type: orchestrator 编排器工作流。引入动机：完整交付流程编排——Superpowers 探索到 OpenSpec 锁定到 TDD 实施到验证到归档，全程门控。0803-OpenSpec_Superpower解析确认其 activation.mode: explicit-only（显式命名才激活，AI 不应该背着我做事安全需求）、standalone: false（依赖 superpowers-feature-workflow）。安装时明确不装 openspec-superpowers（与 openspec-propose + superpowers-feature 重复）。
- **为什么存在（当前）**: 复杂功能交付的全流程编排器：路由控制者，防止误路由到 OpenSpec proposal skill（Guardrails 明确：用户点名本 workflow 时不先路由到 openspec-propose）。0815 桥接后收入 openspec-plan preset 并降权（disable-model-invocation），与 13 个降权 openspec skill 配套。本 0817-opencode-dag 项目的 DAG 展开（proposal-specs-design-tasks）即受此流程启发。
- **怎么用（触发）**: 显式 opt-in：用户点名 $superpowers-openspec-superpowers-workflow 或仓库策略强制时触发；一旦产出 tasks.md 且用户确认/继续，流程保持激活（即使不重复点名）。
- **怎么用（工作流）**: 25 步状态机：1) 探索上下文；2) 一次一问澄清；3) 2-3 方案推荐等待批准；4) 设计写 docs/superpowers/specs/；5) 确认设计；6) 派生 kebab-case OpenSpec change 名；7) openspec status --change 检查工件顺序；8) 每工件前 openspec instructions <artifact>；9) 按依赖序完成 proposal-design-specs-tasks；10) 检查 status 直到齐备；11) 停止 OpenSpec apply 执行；12) 汇总任务；13-16) 确认任务清单/继续开发（continue-dev 主续接命令）；17-21) 实施计划/TDD/验证/continue-review；22-25) 对齐后归档（continue-archive），更新记忆。
- **怎么用（协作）**: 编排 superpowers-feature-workflow（实施）+ openspec 全家（propose/apply/archive-change 等工件）+ openspec-plan preset（dsh 侧）+ .superpowers-memory/ 记忆。
