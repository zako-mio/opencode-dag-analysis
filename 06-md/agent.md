# agent 节点（9）

## agent-build — build
- 组: AG1-主Agent | Layer 6
- 作用: 
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## agent-drawio-worker — drawio-worker
- 组: AG2-子Agent | Layer 7
- 作用: Diagram creation specialist using draw.io. Use for flowcharts, architecture diagrams, UML, mind maps, org charts, and any visual diagrams.
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## agent-explore — explore
- 组: AG2-子Agent | Layer 7
- 作用: Fast agent specialized for exploring codebases. Inherits parent session model.
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## agent-general — general
- 组: AG2-子Agent | Layer 7
- 作用: General-purpose agent for researching complex questions and executing multi-step tasks. Inherits parent session model.
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## agent-pdf-worker — pdf-worker
- 组: AG2-子Agent | Layer 7
- 作用: PDF reader, OCR, and document analysis specialist. Use for any task involving PDF files.
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## agent-plan — plan
- 组: AG1-主Agent | Layer 6
- 作用: 
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## agent-reflection-worker — reflection-worker
- 组: AG2-子Agent | Layer 7
- 作用: Reflection specialist for the self-evolution system. Analyzes Plan+Build cycles and generates Memory/Skill entries. Use ONLY for asynchronous post-cycle reflection tasks.
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 

## agent-search-worker — search-worker
- 组: AG2-子Agent | Layer 7
- 作用: 搜索管线执行 Agent。只做搜索管线(发现+获取+交叉验证)，输出结构化证据包。Use for any task requiring external search, query disambiguation, multi-source fact-checking, or evidence-pack construction.
- 提供: 
- **为什么存在（历史）**: 0905 联网搜索能力架构落地时缺口清单最高优先级——「无独立搜索子Agent」，此前搜索被混入 general 子Agent，方法论散落 MEMORY 跨会话不稳。作为搜索执行层，只做发现+获取+交叉验证三段管线，不写报告。
- **为什么存在（当前）**: 需求驱动：需要实体消歧、多源事实核查、证据包构建等高价值搜索场景，由独立子Agent 承担可将方法论/后端退化链固化，且与主Agent 调度解耦（主Agent 只委派不执行）。
- **怎么用（触发）**: 主Agent 在 plan/build prompt 的 MCP 路由中判定「需联网/多源核查/证据包」类任务时委派（Task 调用），模式=subagent，hidden=true，继承父会话模型。
- **怎么用（工作流）**: ①主Agent 委派前注入【时间基线】今日= T 到 prompt 首行；②search-worker 加载 search-methodology skill 走决策树路由（Path1 通用/Path2 垂直域/HYBRID/Path3 登录态），执行 LLM初发现→信用地图导航→外部搜索降级链；③curl 静态→agent-browser 动态回源获取；④多源交叉验证/信源分级；⑤按证据包契约输出结构化 JSON（query/metas/cross_validation/gaps），提交前跑 validate_evpack.py 自动校验；⑥构造失败时降级标注「单一来源/blocked:true」，绝不编造。
- **怎么用（协作）**: 依赖 search-methodology skill（方法论与证据包契约）、search-behavior instruction（行为层强制）、login-auth-channel skill（Path3 命中需登录态时由主Agent 登录后重委派）、browser-harness/agent-browser（动态获取）、source_credibility_map.md（信源导航）、opencode.env（Tavily key）、代理纪律（境内直连/境外 7890）。

## agent-vision-worker — vision-worker
- 组: AG2-子Agent | Layer 7
- 作用: Vision analysis specialist using DeepSeek vision model. Use for image understanding, screenshot analysis, UI restoration, and any task requiring direct image input.
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 
