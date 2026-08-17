# mcp 节点（6）

## mcp-amap — amap
- 组: A2-MCP | Layer 4
- 作用: 本地 MCP，经 powershell amap-mcp-wrapper.ps1 启动。已禁用（enabled=false）：12 个工具 ~2000 tokens 极低频（高德地图能力），与 vscode-mcp-server 同属 MCP 精兵策略裁撤对象。
- 提供: （禁用中）高德地图 12 工具；保留配置便于按需启用
- **为什么存在（历史）**: 高德官方 MCP 改造引入：经 amap-mcp-wrapper.ps1 启动（环境变量注入 + npx 包装）；与 amap-jsapi-skill/amap-lbs-skill/amap-budget-control 三 skill 构成渐进式消耗模型（先免费网页链接→再计次 API→最后 JSAPI 文档）；0801 P1-2 固化时已列'✅ 已禁用'；0802 盘点精兵策略裁撤：12 个工具 ~2000 tokens 很少使用。
- **为什么存在（当前）**: enabled=false；description'【已禁用】12 个工具 ~2000 tokens 极低频'（0813 精简 description 省 token）；三个 amap skill 也转为 _SKILL.md 存档（0815 map 标注'存档'，_SKILL.md 前缀不被 glob 加载）；高德能力低频需求与 token 成本不成比例。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 无（禁用）；曾与 amap-jsapi-skill/amap-lbs-skill/amap-budget-control 三 skill 协作（免费链接优先→结构化数据转交 budget-control）。

## mcp-drawio — drawio
- 组: A2-MCP | Layer 0
- 作用: 本地 MCP，命令 node D:\Opencode\drawio-mcp-minimal\package\src\index.js（本地精简版 v1.5.0）。已启用（enabled=true）：draw.io 图表创建，仅 drawio-worker 子Agent 使用（drawio_* 全局 deny，子Agent 层 allow）。
- 提供: draw.io 图表创建能力（在线服务模式）
- **为什么存在（历史）**: jgraph/drawio-mcp v1.5.0 本地精简版（node D:\Opencode\drawio-mcp-minimal\package\src\index.js）；0802 盘点：启用 3 个之一（~8 工具）；0803 Drawio工具链优化：新增 drawio_export 工具（第 8 个）——因 draw.io CLI --scale 4 渲染 bug（只渲染顶部 25%），3 次迭代找到 Puppeteer lightbox 模式（?lightbox=1 + deviceScaleFactor + waitForFunction）→ 10280×5760 PNG 成功；同时把 tool description 中的参考文档抽离为 drawio-reference skill（998 行）。
- **为什么存在（当前）**: enabled=true；description'【启用】draw.io 图表创建（本地精简版 v1.5.0）。仅 drawio-worker 子Agent 使用'；全局 permission drawio_* deny + drawio-worker L3 allow 构成三层纵深；是图表能力的事实标准（导出验证链经 drawio-reference 第五章）。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: agent-drawio-worker（唯一使用方）、drawio-reference skill（XML/Mermaid 参考+导出验证）、mcp-drawio-local（同实例离线兜底）、VLM（内容校验）。

## mcp-drawio-local — drawio-local
- 组: A2-MCP | Layer 0
- 作用: 本地 MCP，与主 drawio 同一实例（同 index.js），但注入环境变量 DRAWIO_BASE_URL=http://localhost:8080/ 走本地服务。已禁用（enabled=false）：离线兜底角色，断网时启用。
- 提供: （兜底）离线模式 draw.io 图表创建（本地 8080 实例）
- **为什么存在（历史）**: 与主 drawio 同一实例（同 index.js），但注入环境变量 DRAWIO_BASE_URL=http://localhost:8080/ 走本地服务；0801 P1-2 固化 MCP 工具集时已列为'✅ 已禁用'；0802 盘点禁用原因：离线兜底，与主 drawio 指向同一本地版，工具重复。
- **为什么存在（当前）**: enabled=false；description'【禁用·离线兜底】断网时启用，与主 drawio 同一实例'（0813 description 统一为【禁用·离线兜底】格式）；定位为断网/离线场景的启用开关；0812 headroom 报告亦提及同思路兜底（'断网/离线场景可启用 drawio-local 同思路的 headroom 兜底'）。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: mcp-drawio（同 index.js 双配置）、agent-drawio-worker（使用方）。

## mcp-headroom — headroom
- 组: A2-MCP | Layer 0
- 作用: 本地 MCP，经 powershell headroom-mcp-launcher.ps1 启动。已禁用（enabled=false，2026-08-12）：量化亏损（工具定义 ~279 tokens/请求 > 收益）。注释明确 CLI 仍可用（proxy/audit-reads/savings），切 Claude Code/Codex 走 proxy 时改回 true。
- 提供: （禁用中）token 审计/代理能力；CLI 保留 proxy/audit-reads/savings 手动压缩
- **为什么存在（历史）**: 开源 headroom（chopratejas/headroom 63.9k⭐）CLI 的 MCP 服务器引入；0802 盘点：启用 3 个之一（3 工具 compress/retrieve/stats，懒调用策略 <500 字符不压缩）；0805 遭 Stop-Process -Force 误杀 python 进程 → server unavailable（果非因）；0812 修复：诊断发现'proxy 缺失'是表象（源码证明 3 工具走本地 store 无需 proxy），真根因是误杀；headroom-mcp-launcher.ps1 v3 纯 stdio 转发（不启动后台进程，规避管道句柄继承导致 EOF 挂起）→ 修复成功；但量化评估：3 工具定义 ~279 tokens/请求、会话级 ~8370 tokens（30 轮），历史真实收益仅 ~357 tokens（$0.001）→ 回本条件每 ~3 轮压一次 800+ tokens 实际触发率极低 → 亏损 → 用户决策禁用。
- **为什么存在（当前）**: enabled=false（2026-08-12 量化亏损：工具开销 > 收益）；CLI 仍可用（headroom proxy/audit-reads/savings）；恢复路径：切 Claude Code/Codex 走 proxy 时改回 true（wrapper v3 或手动 headroom proxy）；0813 skill 更新：headroom SKILL.md 补 frontmatter（原先缺失导致未注册）+ 标注'MCP 禁用但 CLI 可用'；auto-mode.md 移除 6 处 headroom MCP 引用改通用截断做法。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 无（禁用）；headroom skill（frontmatter 补全后注册，文档化 CLI 用法）、auto-mode.md（已移除 MCP 引用）。

## mcp-pdf-reader — pdf-reader
- 组: A2-MCP | Layer 0
- 作用: 本地 MCP，命令 npx -y @sylphx/pdf-reader-mcp@latest。已启用（enabled=true）：PDF 文本提取（4 工具），仅 pdf-worker 子Agent 使用（permission 按工具名前缀隔离），全局层 pdf-reader_* 为 deny（L1），子Agent 层 allow（L3）。
- 提供: PDF 文本提取（4 工具）能力
- **为什么存在（历史）**: 早期引入：npx @sylphx/pdf-reader-mcp@latest（社区 MCP）；0801 P1-2 固化 MCP 工具集时保留启用（~4 工具）；0802 盘点：启用 3 个 MCP 之一（~10 工具，后实际 4 工具）；0803 编码安全修复时删除 glm-vision 等 MCP，pdf-reader 作为核心保留；pdf-ocr skill 从 @sylphx/pdf-reader-mcp 分离（轻量路由包装 87 行，仅无文本层时触发 OCR）。
- **为什么存在（当前）**: enabled=true；description'【启用】PDF 文本提取。仅 pdf-worker 子Agent 使用（4 工具）'；全局 permission pdf-reader_* deny + pdf-worker L3 allow 构成三层纵深（只有 pdf-worker 能调）；MCP 路由规则保证 PDF 任务固定委派 pdf-worker。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: agent-pdf-worker（唯一使用方）、pdf-ocr skill（OCR 兜底）、plan/build（路由决策）。

## mcp-vscode-mcp-server — vscode-mcp-server
- 组: A2-MCP | Layer 4
- 作用: 本地 MCP，经 powershell -ExecutionPolicy Bypass -File vscode-mcp-launcher.ps1 启动。已禁用（enabled=false）：仅 6 个工具（~692 tokens）极少使用，工具定义成本 > 收益。审计报告存于 Mission-file\2026-08\0802-vscode-mcp-server-tools-audit。
- 提供: （禁用中）VS Code 相关 6 工具；保留配置便于按需启用
- **为什么存在（历史）**: 早期引入：semanticworkbenchteam.mcp-server-vscode v0.0.9，经 vscode-mcp-launcher.ps1 启动（轮询 VSCode MCP 端口 6010，就绪时自动桥接 stdio↔SSE，实现'无感知接入'）；0801 P1-2 固化 MCP 工具集：审计发现实际仅 6 个工具（非原预估 72 个），总计 ~692 tokens——收益从'大幅削减数千 token'降为'节省 ~692 tokens'；0802-vscode-mcp-server-tools-audit 全量审计（正则扫描 dist/extension.js：.tool( 出现 6 次）：code_checker/focus_editor/list|start|restart|stop_debug_session → 处置为禁用。
- **为什么存在（当前）**: enabled=false（0802 审计后禁用）；description 注明'【已禁用】仅 6 个工具(~692 tokens) 极少使用'并附审计报告路径；功能缺口：无文件读写/终端/全局搜索通用工具（README 声称的 search_symbol 未打包进 v0.0.9）；permission 层 vscode-mcp-server_* 全局 deny。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 无（已禁用 + 全局 deny）；曾与 VSCode 编辑器联动。
