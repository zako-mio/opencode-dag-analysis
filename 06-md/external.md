# external 节点（8）

## ext-amap-api — 
- 组: X-外部服务 | Layer 6
- 作用: 地图 POI/路径规划服务
- 提供: 地图能力
- **为什么需要**: 地理/LBS 能力：POI 搜索、周边搜索、路径规划、地理编码、旅游规划。解决 Agent 处理地点/路线/导航类查询需求；无它则无法回答附近美食/两地路线/地点坐标类任务。被依赖方：amap-lbs-skill（网页链接，不耗配额）、amap-budget-control（MCP API 用量预算）、amap-mcp-wrapper（MCP 入口）。
- **当前状态**: 双轨合理：amap-lbs-skill 优先生成免费网页链接（www.amap.com/search?query=、amap.com/dir 等，不消耗 API 配额），结构化数据才走 restapi.amap.com Web 服务（v5/place/text 等）——配额友好；amap MCP（npx amap-mcp-server@latest）因仅 2 工具 ~2000 tokens 极低用已在 opencode.jsonc 中 enabled:false（MCP 精兵策略），靠 skill 层满足日常。
- **怎么接入**: Web Service Key：环境变量 AMAP_WEBSERVICE_KEY（旧 AMAP_KEY 已废弃但兼容），或 config.json 本地持久化（chmod 600）；端点：https://restapi.amap.com/v5/place/text（POI，参数 key/keywords/region）、v3/direction/walking（步行路径）、v3/geocode/geo（地理编码）；埋点 https://restapi.amap.com/v3/log/init；MCP wrapper：amap-mcp-wrapper.ps1 设 $env:AMAP_KEY 后 npx -y amap-mcp-server@latest。
- **装配层调用**: amap-lbs-skill 场景路由：场景一直接拼 www.amap.com/search 链接；场景二先 v3/geocode/geo 取坐标再拼带坐标链接；POI 详情/路径走 scripts/poi-search.js / route-planning.js（node 调用 index.js 的 searchPOI/walkingRoute，axios GET restapi.amap.com）；预算控制由 amap-budget-control skill 记录调用量与 5000 次/日预警。

## ext-chrome — 
- 组: X-外部服务 | Layer 2
- 作用: browser-harness 自动化浏览器
- 提供: 网页自动化
- **为什么需要**: 网页交互/抓取/测试的唯一通道：browser-harness skill 要求 Always use browser-use for any web interaction——爬取（0817 DAG 3 路并行联网调研、简历投递）、页面截图/点击、SPA 轮询、表单填写都需要真实浏览器。解决 DeepSeek 无视觉且纯文本 Agent 无法直接操作网页的需求；被依赖方：browser-harness skill、recruit-assist（京东投递）、create-web preset（前端实测）、frontend-design（渲染验证）。
- **当前状态**: 合理：专用 Chrome 实例（独立 profile %LOCALAPPDATA%\browser-harness-chrome，--remote-debugging-port=9222，chrome-debug.ps1 自动拉起/幂等检测）；BU_CDP_URL=http://localhost:9222 环境变量已设；browser-harness.exe 管道式 Python（new_tab/js/capture_screenshot/click_at_xy/cdp 原始命令）。0804 复盘教训（JS 需完整 IIFE、js() 必须 return、复杂箭头 heredoc 易错）已固化进 skill。
- **怎么接入**: chrome-debug.ps1：powershell -ExecutionPolicy Bypass -File $env:USERPROFILE\.config\opencode\scripts\chrome-debug.ps1（检查 http://localhost:9222/json/version，无则启动 Chrome + --remote-debugging-port=9222 + --user-data-dir 独立 profile）；browser-harness 通过 BU_CDP_URL 连接 daemon；browser-harness --doctor 诊断；远程/云浏览器用 browser-harness auth login（Browser Use cloud）。
- **装配层调用**: 管道喂 Python 脚本：$pyScript | browser-harness.exe（Windows 用 @"..."@ heredoc，不用 <<PY）；流程：new_tab(url) 首次导航 → wait_for_load() → capture_screenshot() 看状态 → js()/click_at_xy() 交互 → 完成后 close-chrome-tabs.ps1 -KeepFirst 收尾；原始能力用 cdp("Domain.method", ...)。

## ext-deepseek-api — 
- 组: X-外部服务 | Layer 7
- 作用: deepseek-v4-pro/flash 模型 API
- 提供: LLM 推理
- **为什么需要**: 主模型供给：plan=deepseek-v4-pro（规划/委派推理）、build 与全部 7 个子Agent=deepseek-v4-flash（执行降本）都走 DeepSeek。解决本地要有强推理 + 低成本可商用模型的需求；无它则 opencode 无模型可跑，整个装配层（调度/委派/留档/反思）全部失效。
- **当前状态**: 合理：opencode.jsonc 以 provider.deepseek 配置 @ai-sdk/deepseek + baseURL https://api.deepseek.com/v1，model 分 pro(0.435/0.87 刀) 与 flash(0.14/0.28 刀) 两档，daily/deep variant 分别限 max_tokens 8192/16384 + reasoning_effort high/max——与 auto-mode 门控的决策边界表严格对应；缓存前缀策略（auto-mode.md 静态置前、动态置后）就是为 DeepSeek prefix-cache 98-99% 命中设计的。
- **怎么接入**: 环境变量 DEEPSEEK_API_KEY（用户级已 setx，进程内不落盘）；API 端点 https://api.deepseek.com/v1/chat/completions（OpenAI 兼容）；opencode.jsonc 中 provider.deepseek.npm=@ai-sdk/deepseek + options.baseURL/timeout(300s)/headerTimeout/chunkTimeout；模型 modalities（pro 支持 image 输入、flash 仅 text）+ interleaved.reasoning_content 字段解析推理链。
- **装配层调用**: opencode 主进程按 agent 配置选模型：plan 回落到顶层 model（deepseek-v4-pro），build/子Agent 显式 model=deepseek-v4-flash；variant daily/deep 切换 max_tokens 与 reasoning_effort；MEMORY.md 经 instructions 注入系统提示前缀共享缓存。

## ext-drawio-service — 
- 组: X-外部服务 | Layer 3
- 作用: draw.io 在线/本地图表渲染
- 提供: 图表导出
- **为什么需要**: 图表交付能力：流程图/架构图/UML/思维导图/组织图批量生成与 4x PNG 导出（0816-0817 三个 DAG 项目合计 135+ 张）。解决 Agent 要产出专业可视化图表需求；无它则架构对比图、DAG 图无法生成。被依赖方：drawio-worker 子Agent（唯一工具源）、drawio-reference skill（998 行规范+导出验证第五章）。
- **当前状态**: 合理：0801 因 MCP 工具描述内嵌 33K XML + 12K Mermaid 参考导致子Agent System Prompt 18-20K tokens（50-60% 是工具定义），Fork 到 D:\Opencode\drawio-mcp-minimal 把描述替换为 5 行摘要 + 懒加载 skill；0803 加 Puppeteer lightbox 导出修复 CLI --scale 4 只渲染顶部 25% 的 bug（v3: ?lightbox=1 + deviceScaleFactor + waitForFunction，10280×5760 PNG 成功）；opencode.jsonc 中 drawio enabled:true、drawio-local（DRAWIO_BASE_URL=http://localhost:8080/）离线兜底 enabled:false。
- **怎么接入**: MCP 配置：opencode.jsonc mcp.drawio = {type:local, command:[node, D:\Opencode\drawio-mcp-minimal\package\src\index.js], enabled:true}（stdio 传输）；环境变量 DRAWIO_BASE_URL（默认 https://app.diagrams.net/）、DRAWIO_SHAPE_INDEX_URL（CDN jsdelivr，可本地）、DRAWIO_ICON_SERVICE_URL（可 off）；导出走 export.js 的 buildLightboxUrl（pako deflateRaw 压缩 XML → #create= JSON hash → lightbox=1 参数）→ Puppeteer 截全页。
- **装配层调用**: drawio-worker 子Agent 调用 drawio_* 8 工具（open_drawio_xml/open_drawio_mermaid/search_shapes/export 等）创建图表 → 强制 drawio_export 导出 PNG（scale=2~4）→ VLM（GLM-4V）校验无截断 → 越界检查；委派时主Agent prompt 必须精确写入 drawio-reference: 图表规范与导出验证（刚性约束，违者产生截断 PNG）。

## ext-glm-api — 
- 组: X-外部服务 | Layer 7
- 作用: VLM 图片转文字服务（glm-4.6v / glm-4.6v-flash）
- 提供: 图片描述
- **为什么需要**: 补 DeepSeek-flash 无视觉能力的短板：read.ts 工具把图片文件经 GLM-4V 转文字描述（DeepSeek 纯文本模型才能理解）；vision-interceptor.js 插件在 chat.message 与 experimental.chat.messages.transform 钩子把用户上传图片替换为 VLM 描述文本，解决 does not support image input 报错。被依赖方：tools/read.ts、plugins/vision-interceptor.js，下游是 opencode 全部读图/图表校验流程（0807 起含 drawio 导出 PNG 的 VLM 校验）。
- **当前状态**: 合理但有过改动史：0807 修复前 glm-4.6v-flash（免费）高峰 429，改为付费 glm-4.6v 优先、429 降级免费 flash 的双模型链；Key 硬编码回退到环境变量 ZHIPU_API_KEY（用户级已 setx），避免明文泄露；插件侧用 Map 缓存 URL→描述防止历史消息重复计费。2026-08 仍为唯一视觉通道。
- **怎么接入**: 环境变量 ZHIPU_API_KEY；端点 POST https://open.bigmodel.cn/api/paas/v4/chat/completions，Header Authorization: Bearer <key>，body: {model:glm-4.6v 或 glm-4.6v-flash, messages:[{role:user, content:[{type:image_url, image_url:{url: 图片URL 或 data:image/png;base64,...}}, {type:text, text:描述提示词}]}], max_tokens:4096, temperature:0.3}；响应取 choices[0].message.content。
- **装配层调用**: read.ts 的 describeImage()：Bun.file→base64→按扩展名映射 mime→付费优先降级循环→返回描述文本；vision-interceptor.js 的 transformParts()：识别 part.type=file 且 mime 以 image/ 开头→调 describeImage→替换为 synthetic text part，并写日志 vision-int.log 记录 FIRED/SKIP/VLM OK 计数。

## ext-lark-api — 
- 组: X-外部服务 | Layer 2
- 作用: lark-cli 调用的飞书开放平台
- 提供: 日历/文档/多维表格等
- **为什么需要**: 协同办公主通道：recruit-assist 的飞书网申进度表同步（sync_feishu.py 增量上传/全量下载）、简历求职流程的表格/文档操作、日常日历/消息/云盘任务都需要。解决 Agent 能操作飞书全部业务域的需求；无它则简历投递跟踪表与办公文档无法程序化读写。被依赖方：skills/lark-suite（路由包装层）、recruit-assist、exec-recruit preset。
- **当前状态**: 合理：lark-cli v1.0.76（Go，MIT，上游 yjwong/lark-cli）本地安装，SKILL.md 强制 Step 0 先读 references/shared.md（认证检查/--as user|bot 身份/JSON 输出合约）；23 域中 20 个占位已在 0802 修复为 lark-cli skills read 动态加载；Windows 下必须 cmd /c 调用。仅 3 个手写 reference（drive/shared/sheets），其余按需拉官方内置 skill。
- **怎么接入**: lark-cli auth login --recommend（输出授权 URL，浏览器完成 OAuth，自动取 token；可 --no-wait + --device-code 轮询）；lark-cli config init --new 首次配 app credentials；调用形态 cmd /c "lark-cli <domain> +<shortcut> [flags]"，如 lark-cli drive +upload <本地路径> <folder_token>、lark-cli drive +download <file_token> <本地路径>；输出 JSON 信封 {ok, identity, data, meta}，成功判 ok==true 而非 code==0。
- **装配层调用**: lark-suite skill 按意图路由表加载 references/<domain>.md → 按域指令执行 lark-cli shortcut → 解析 JSON；Fallback 链：lark-cli skills read lark-<domain> → lark-cli schema → lark-cli api GET/POST → WebFetch 官方文档；recruit-assist 的 sync_feishu.py 直接调 lark-cli 做表格同步。

## ext-opencode-plugin — 
- 组: X-外部服务 | Layer 7
- 作用: 插件 SDK（node_modules 1.18.9）
- 提供: 插件钩子类型
- **为什么需要**: vision-interceptor.js 插件依赖 @opencode-ai/plugin SDK（node_modules 1.18.9）提供的插件钩子类型与结构（Plugin/PluginInput/Hooks 等），使自定义插件能以官方插件协议接入 opencode 消息管线。装配层的插件机制复用官方 SDK，而非自行发明协议。
- **当前状态**: 当前用于 vision-interceptor 插件的类型基础（chat.message + messages.transform 双钩子）。本机 ~/.config/opencode/package.json 安装了 @opencode-ai/plugin，与官方 SDK 包（packages/plugin）同源，版本 1.18.9 与本机 opencode 1.18.16 基本对齐。
- **怎么接入**: 通过 npm 安装：npm i @opencode-ai/plugin（本机 ~/.config/opencode/package.json 依赖）。插件文件在 ~/.config/opencode/plugins/*.js，通过 opencode 的 plugins 机制加载。
- **装配层调用**: vision-interceptor.js 从 '@opencode-ai/plugin' 导入类型，定义 Plugin 结构（id/name/tools 钩子），注册 chat.message 与 messages.transform 钩子拦截消息做 VLM 图片转文字。

## ext-sylphx-pdf — 
- 组: X-外部服务 | Layer 6
- 作用: PDF 文本提取 npm 包
- 提供: PDF 提取
- **为什么需要**: PDF 文档读取能力：简历解析、财报读取、论文提取。解决 Agent 无法直接读 PDF 二进制需求；无它则所有 PDF 类任务（招聘简历、学术文档）不可用。被依赖方：pdf-worker 子Agent（唯一工具源，permission 仅放行 pdf-reader_*）。
- **当前状态**: 合理：opencode.jsonc mcp.pdf-reader = {type:local, command:[npx, -y, @sylphx/pdf-reader-mcp@latest], enabled:true}——唯二启用的 MCP 之一（MCP 精兵策略 6 台仅留 2 台）；pdf-worker 固定 Flash + L3 最小权限（仅 pdf-reader_* allow），全局 deny 兜底；无文本层时走 pdf-ocr skill 路由 OCR。
- **怎么接入**: npx -y @sylphx/pdf-reader-mcp@latest 按需拉取（latest 随 npm 发布更新）；stdio MCP 协议；暴露 4 个工具（read_pdf 等文本提取类）；无需 API Key/环境变量（纯本地解析）。
- **装配层调用**: pdf-worker 子Agent 经 pdf-reader_* 工具提取文本 → 返回 8 字段 JSON（status/summary/data/files_created 等）；MCP 路由规则保证 PDF 任务始终委派 pdf-worker 且不重复加载 pdf-ocr skill（省 token）；0707 简历任务用 explore 读 xlsx 而非 PDF 的案例证明路由按文件类型分流。
