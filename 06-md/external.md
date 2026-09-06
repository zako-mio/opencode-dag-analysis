# external 节点（10）

## ext-amap-api — 高德地图 API
- 组: X-外部服务 | Layer 0
- 作用: 地图 POI/路径规划服务
- 提供: 地图能力
- **为什么需要**: 地图类任务（amap skill 引用）
- **当前状态**: 已禁用 mcp-amap
- **怎么接入**: amap-mcp-wrapper.ps1
- **装配层调用**: 

## ext-chrome — Chrome 浏览器
- 组: X-外部服务 | Layer 0
- 作用: browser-harness 自动化浏览器
- 提供: 网页自动化
- **为什么需要**: browser-harness skill 依赖
- **当前状态**: WSL2 用 agent-browser
- **怎么接入**: PowerShell CDP + close-chrome-tabs.ps1
- **装配层调用**: 

## ext-deepseek-api — DeepSeek API（官方直连）
- 组: X-外部服务 | Layer 0
- 作用: deepseek-v4-pro/flash/flash-vision-exp 模型 API
- 提供: LLM 推理 + 视觉
- **为什么需要**: 官方直连兜底 Pro 与视觉；主 Agent 默认模型
- **当前状态**: 承载 deepseek-v4-pro(仅官方) + vision-exp
- **怎么接入**: env DEEPSEEK_API_KEY → api.deepseek.com/v1
- **装配层调用**: 

## ext-drawio-service — draw.io 服务
- 组: X-外部服务 | Layer 0
- 作用: draw.io 在线/本地图表渲染
- 提供: 图表导出
- **为什么需要**: drawio-worker 子Agent 依赖
- **当前状态**: 启用 mcp-drawio
- **怎么接入**: drawio-mcp-minimal + DRAWIO_BASE_URL
- **装配层调用**: 

## ext-glm-api — GLM API（智谱）
- 组: X-外部服务 | Layer 0
- 作用: VLM 图片转文字服务（glm-4.6v / glm-5.3-flash）
- 提供: 图片描述 + 编码模型
- **为什么需要**: VLM 双链路首选（read.ts），响应快、限流额度高
- **当前状态**: GLM-4.6v 视觉 / GLM-5.3-flash 编码
- **怎么接入**: env ZHIPU_API_KEY → open.bigmodel.cn/api/paas/v4
- **装配层调用**: 

## ext-lark-api — 飞书/Lark API
- 组: X-外部服务 | Layer 0
- 作用: lark-cli 调用的飞书开放平台
- 提供: 日历/文档/多维表格等
- **为什么需要**: lark-suite skill 依赖
- **当前状态**: 启用 lark-suite skill
- **怎么接入**: lark-cli
- **装配层调用**: 

## ext-opencode-go — OpenCode Go 套餐
- 组: X-外部服务 | Layer 0
- 作用: OpenAI 兼容协议（@ai-sdk/openai-compatible），baseURL=opencode.ai/zen/go/v1。订阅套餐 $10/月($60 额度)，DeepSeek Flash 包月 3x
- 提供: deepseek-v4-flash(go) / glm-5.2 / kimi-k2.7-code / qwen3.7-plus / muse-spark-1.3-contributor / hy4-preview / omen-alpha(stealth) 模型
- **为什么需要**: 覆盖高性价比编码模型（Flash 包月 3x 额度）+ v1.18.29 新增 Muse Spark 1.3/Hy4/Omen Alpha
- **当前状态**: blacklist deepseek-v4-pro（仅官方直连）
- **怎么接入**: env OPENCODE_GO_API_KEY
- **装配层调用**: 

## ext-opencode-plugin — @opencode-ai/plugin SDK
- 组: X-外部服务 | Layer 0
- 作用: 插件 SDK（node_modules 1.18.x）
- 提供: 插件钩子类型
- **为什么需要**: plugin 开发（已无插件但 SDK 保留）
- **当前状态**: 插件目录已空
- **怎么接入**: node_modules @opencode-ai/plugin
- **装配层调用**: 

## ext-sylphx-pdf — @sylphx/pdf-reader-mcp
- 组: X-外部服务 | Layer 0
- 作用: PDF 文本提取 npm 包
- 提供: PDF 提取
- **为什么需要**: pdf-worker 子Agent 依赖
- **当前状态**: 启用 mcp-pdf-reader
- **怎么接入**: npx @sylphx/pdf-reader-mcp
- **装配层调用**: 

## ext-tavily-api — Tavily Search API
- 组: X-外部服务 | Layer 0
- 作用: 外部搜索 API（web search，1 credit/次），search-methodology/skill 的发现层外部搜索降级链首选
- 提供: 外部事实搜索/网页检索
- **为什么需要**: search-methodology skill 依赖外部搜索后端做发现层；search-worker 子Agent 证据包构建
- **当前状态**: 0905 联网搜索能力架构新增；search-methodology/skill 依赖
- **怎么接入**: env TAVILY_API_KEY → api.tavily.com/search
- **装配层调用**: 
