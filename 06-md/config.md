# config 节点（1）

## config-main — main
- 组: AG6-配置本体 | Layer 2
- 作用: 主配置：agent/provider/mcp/compaction/skills/instructions/permission
- 提供: 
- **为什么存在（历史）**: opencode v1.18.14→v1.18.25 配置装配层自进化，新增 OpenCode Go 订阅套餐、智谱 GLM 官方、DeepSeek 官方三套 provider，并抽象出视觉子Agent。
- **为什么存在（当前）**: 用 Go 订阅的包月额度覆盖高性价比编码；用 DeepSeek 官方直连兜底 Pro 与视觉；用智谱官方补 GLM-5.3/GLM-4.6v 双通道，形成多 provider 冗余与视觉出口。
- **怎么用（触发）**: 作为 opencode 全局配置启动加载，决定顶层默认模型/small_model/compaction/agent/instruction/provider/mcp 全栈装配。
- **怎么用（工作流）**: 维护 plan/build(daily变体)、pdf/drawio/vision/reflection 子Agent 权限与模型、provider 模型清单与成本、compaction 参数、权限白名单、MCP 开关。
- **怎么用（协作）**: provider 段经 @ai-sdk/* 连接外部 API；agent 段配置子Agent 供 agent-protocol 路由；instructions 段挂载 auto-mode.md 与 MEMORY.md；mcp 段启用 pdf-reader/drawio。
