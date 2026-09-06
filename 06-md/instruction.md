# instruction 节点（5）

## instr-agent-protocol — agent-protocol
- 组: AG4-指令 | Layer 1
- 作用: Agent Protocol (Cache-Stable Prefix)
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

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
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## instr-downloads — downloads
- 组: AG4-指令 | Layer 1
- 作用: 文件导出与下载默认路径
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## instr-search-behavior — search-behavior
- 组: AG4-指令 | Layer 1
- 作用: ---
- 提供: 
- **为什么存在（历史）**: 0905 联网搜索能力架构缺口清单——「无行为层强制（先搜后答）」，行为准则缺失导致搜索能力成孤儿。复用 FactReach 受管标记块范式（BEGIN/END）+ goose 懒加载（frontmatter name+description），编码为全局强制 instruction。
- **为什么存在（当前）**: 需求驱动：为所有 Agent 提供外部信息实证的最低行为红线——凡结论依赖外部事实必须先搜索并打开来源验证；搜索页/摘要仅作线索，须回源原始页面；重要结论 ≥2 独立源交叉验证；区分已验证事实/推断/不确定信息。
- **怎么用（触发）**: 作为全局 instruction 加入 opencode.jsonc instructions 数组（与 auto-mode.md、MEMORY.md 并列），所有 Agent 会话前缀加载。在需要外部事实/时效/多源核查的查询时（Trigger：任何涉及外部事实/时效/多源核查的结论）触发生效。
- **怎么用（工作流）**: ①query 依赖外部事实 → 先搜索并打开来源验证，不得只凭模型记忆；②搜索结果/摘要仅作发现线索，回源原始页面核对来源链接/发布时间/数据日期；③重要/争议/易变结论用 ≥2 个独立来源交叉验证，做不到标「单一来源/未验证」；④按信源优先级（官方一手 > 权威二手 > 社区讨论）分级；⑤输出区分已验证事实/基于证据推断/尚不确定，链接放在对应结论附近；⑥访问失败直接说明限制，不补写看似合理但未经实证的结论；⑦时效分流：稳定知识用 LLM 初发现，实时信息必须走外部搜索。
- **怎么用（协作）**: 作为行为层地基，与 search-methodology skill（执行细节）、search-worker（委派执行）、MEMORY.md 记忆、auto-mode.md（缓存前缀协议）共同注入 system prompt。BEGIN/END 受管标记块保证对 prefix-cache 最小冲击，不污染 auto-mode.md（缓存字节稳定）。
