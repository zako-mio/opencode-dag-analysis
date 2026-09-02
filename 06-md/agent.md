# agent 节点（8）

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

## agent-vision-worker — vision-worker
- 组: AG2-子Agent | Layer 7
- 作用: Vision analysis specialist using DeepSeek vision model. Use for image understanding, screenshot analysis, UI restoration, and any task requiring direct image input.
- 提供: 
- **为什么存在（历史）**: 原先 pdf-worker/drawio-worker 曾绑定 vision-exp 模型以看图，0826 解绑改走外部 VLM/read.ts；但通用图片理解仍缺一个专职视觉执行者，故 0822 独立抽象出带 DeepSeek 视觉模型的子Agent。
- **为什么存在（当前）**: 需要图片理解/截图分析/UI对照还原能力，且主Agent已换用 vision-exp 具备看图，委派链路上需要一个明确可路由的视觉执行角色。
- **怎么用（触发）**: 被 agent-protocol 的 MCP 路由规则触发：通用图片理解/截图分析/UI还原 → 委派 vision-worker 子Agent（DeepSeek 视觉模型）。
- **怎么用（工作流）**: 直接以图片作为输入理解内容、分析截图、做 UI 还原。
- **怎么用（协作）**: 与 pdf-worker(文本/OCR链路)、drawio-worker(图表导出) 分工；供 agent-protocol 路由；依赖 deepseek 官方 provider 的 deepseek-v4-flash-vision-exp 模型。
