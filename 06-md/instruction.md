# instruction 节点（5）

## instr-agent-protocol — agent-protocol
- 组: AG4-指令 | Layer 1
- 作用: Agent Protocol (Cache-Stable Prefix)
- 提供: 
- **为什么存在（历史）**: 由 task-delegation.md.bak-20260817 拆分演进而来，形成主Agent调度总纲。
- **为什么存在（当前）**: 当前配置自动化后主Agent需在发起工具前先做任务分类，并规范子Agent prompt 结构。
- **怎么用（触发）**: 作为 plan/build 内联 prompt 加载，每次会话进入调度流程被读取执行。
- **怎么用（工作流）**: 定义委派 5 步流程、search-agents 角色匹配、MCP 路由规则、子Agent prompt 模板、聚合回写、Variant 继承。
- **怎么用（协作）**: 引用 browser-management.md(标签页)、downloads.md(下载路径)、auto-mode.md(门控)、MEMORY.md；指向 vision/pdf/drawio-worker 三子Agent 与 search-agents.py/ps1、agency-agents skill。

## instr-auto-mode — auto-mode
- 组: AG4-指令 | Layer 1
- 作用: Agent Universal Protocol (Cache-Stable Prefix — Do NOT modify mid-session)
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## instr-browser-management — browser-management
- 组: AG4-指令 | Layer 1
- 作用: 浏览器标签页管理
- 提供: 
- **为什么存在（历史）**: browser-harness 自动化爬取会在 Chrome 留下大量标签页无管理，导致资源与状态泄漏。
- **为什么存在（当前）**: 约束每次 new_tab 用完即关、整批任务完成后经 question 询问是否批量关闭、批量爬取中途不逐页关以免拖慢速度。
- **怎么用（触发）**: 被 agent-protocol 的「浏览器标签页管理」段引用，在浏览器交互场景生效。
- **怎么用（工作流）**: 定义三规则（用完即关/批量关闭提示/不中途干扰）与 close-chrome-tabs.ps1 的 -All/-KeepFirst/-KeepUrlPattern 参数语义。
- **怎么用（协作）**: 经 agent-protocol 引用，配合 browser-harness/browser-use skill；调用 close-chrome-tabs.ps1(PowerShell CDP)。

## instr-downloads — downloads
- 组: AG4-指令 | Layer 1
- 作用: 文件导出与下载默认路径
- 提供: 
- **为什么存在（历史）**: 自动化导出/爬取文件无默认落盘路径时易散落，需统一默认下载目录约定。
- **为什么存在（当前）**: 当用户未指定路径且文件非项目本地文件时，强制保存到 D:\Opencode_Download，避免污染工作目录。
- **怎么用（触发）**: 被 agent-protocol 的「文件下载规则」段引用，导出/下载场景生效。
- **怎么用（工作流）**: 界定 D:\Opencode_Download 适用与不适用的判断条件。
- **怎么用（协作）**: 经 agent-protocol 引用，与 Mission 留档规则、工作目录规则协作划分落盘位置。

## instr-memory — memory
- 组: AG4-指令 | Layer 1
- 作用: 项目记忆索引（§分段格式，上限~5000字符，含[src:]签名）
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 
