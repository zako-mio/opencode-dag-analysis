# opencode DAG 依赖分析

## 简介

对 **opencode** 做 DAG 依赖分析，三图渐进式理解"官方原版 → 改造对比 → 改造版装配"：
1. **图1 官方包级 DAG**：36 个 `@opencode-ai/*` workspace 包依赖关系（未改造基线，v1.18.35 版本标注；包级结构沿用 v1.18.29，v1.18.35 未变）
2. **图2 官方+改造对比 DAG**：官方基线 + 被改造引用的包染色 + 外部服务
3. **图3 改造版双层 DAG**：包级 + 装配层（skills/agents/mcp/commands/instructions/config/mechanisms）+ 外部服务

本次更新（2026-09-11）：**官方源码 v1.18.29 → v1.18.30 点检 + 装配层全量重建 + 架构判断能力入图**。官方侧仅版本标注/外部 SDK 升号，包级结构与依赖边无变化；装配层从 73 组件扩到 83 组件，新增 `architect-worker` 子Agent、8 个 skill（architecture-judgment / github-bulk-upload / job-listing-filter / kb-construction / opencode-capability-extension / restricted-corpus-acquisition / resumable-content-pipeline / single-source-docs-pipeline）、`architecture-behavior` 指令与 `/arch` 命令，并新增「架构三层栈」机制节点；退役 `tool-read`（改模型原生多模态）与 `instr-agent-protocol`（并入 auto-mode）。DAG 从"联网能力增强体系"进一步演化为"架构判断 + 交付发布 + 知识库构建"的多能力装配体系。

本次更新（2026-10-11）：**官方基线 v1.18.30 → v1.18.35 点检 + 装配层再全量重建 + 需求发现能力入图**。官方侧 `29→35` 变更 328 文件（+17411/−8779），其中核心 `core` 仅 10 文件，**36 包集合与 v1.18.29 逐一致（无增删）**，包级依赖图仍为 36 包 / 68 边 / 6 层 / 19 组；装配层从 83 组件扩到 **87 组件**（skills 41→**46**、agents 10→**9**、mcp 6→**4**、instructions 5→**6**、commands 2→**3**、config 1、mechanisms 18 不变）：新增 `criterion-design-validation` / `design-material-library` / `diagram-lite` / `opencode-capability-audit` / `requirement-discovery` / `version-upgrade-cascade` / `frontend-design-methodology` 七个 skill、`requirement-discovery-worker` 子Agent、`requirement-discovery-behavior` 指令与 `/rd` 命令；退役 `drawio-worker` / `vision-worker` 子Agent、`drawio` / `drawio-local` 两个 mcp 与 `downloads` 指令（4 件停用 skill 迁入 `skills/disabled/`，不入图）。DAG 从 129 节点 / 190 边 / 43 组演进为 **133 节点 / 177 边 / 8 层 / 42 组**（diff 图 46 节点 / 68 边 / 20 组；差异清单 94 条）。

## 为什么与 deepseek-harness 分析不同

| 维度 | deepseek-harness (0816) | opencode (本项目) |
|------|------------------------|-------------------|
| 架构 | cordis 插件装配 | monorepo 36 包 + 配置装配层 |
| 分析单元 | 插件（cordis） | workspace 包 + 配置组件 |
| 改造载体 | 插件装配 | ~/.config/opencode 装配层 |
| DAG 形态 | 单层插件图 | 三图递进（官方→对比→双层） |

## 快速开始

| 想做什么 | 去哪 |
|---------|------|
| **三图交互总览**（官方/对比/改造切换） | `04-interactive/view-{official,diff,modified}.html` |
| 根入口（简介+结论+时间线+导航） | `index.html` |
| 每节点一页（**七段**：作用/提供/依赖/被依赖/**为什么存在(why)**/**怎么用(how)** + 内部结构 DAG） | `02-nodes/`（133 页） |
| 组目录 | `03-groups/index.html`（42 组） |
| 改造差异清单表 | `05-diff/diff-list.html` |
| AI 检索 MD 镜像（含 why/how） | `06-md/00-index.md` |
| 静态 drawio 图 | `05-drawio/main/`（3 主图）+ `05-drawio/assembly/`（关键装配） |
| DAG 数据（JSON） | `01-dag-data/{official,diff,modified}-dag.json` |
| 内部模块 import 数据 | `08-collect/internal-v1.18.29.json`（33 包 2251 模块 6079 边，v1.18.29 基线；v1.18.35 包级结构未变，内部结构本轮不重采） |

## 内容深化（why - how）

**133 节点全部七段**（三种节点类型各自适配的 why/how 结构）：
- **装配层（87 组件）**：⑤ 为什么存在（历史引入动机 + 当前需求驱动）+ ⑥ 怎么用（触发/工作流/协作）
- **官方包（36 包）**：⑤ 为什么存在（设计意图官方 + 改造关联：本机为何引用/为何不引用）+ ⑥ 怎么用（入口/导出 API/命令 + 典型场景与协作）
- **外部服务（10 个）**：⑤ 为什么存在（为什么需要 + 当前状态）+ ⑥ 怎么用（怎么接入 + 装配层调用）

why/how 由多路子Agent 深挖三源还原（留档报告 / MEMORY.md / config 备份链 / SKILL.md 设计意图 / 官方源码实证 / 外部服务官网），每条有据可查。主页面（index.html）提供项目简介 + 三图卡片（含对比）+ 核心结论 + 历史变迁时间线 + 装配体系导航 + 统计面板。

## 核心数据

- **图1 official**：36 包 / 68 边 / 19 组（v1.18.35 版本标注；包级结构沿用 v1.18.29；**包级图不参与拓扑分层**，全部节点 layer=0 ⇒ `stats.layers` = 0，此前 README 记「6 层」为误记，2026-10-11 校准）
- **图2 diff**：46 节点 / 68 边 / 6 层 / 20 组（7 包被改造引用 + 10 外部）
- **图3 modified**：133 节点 / 177 边 / 8 层 / 42 组（36 包 + 87 装配 + 10 外部，含 **18 个自进化机制 mechanism 节点**）
- **装配层**：87 组件（46 skills + 9 agents + 4 mcp + 6 instructions + 0 tools + 3 commands + 1 config + 18 mechanisms）
- **内部结构**：33 包 / 2251 模块 / 6079 边（全量 import 解析，沿用 v1.18.29 基线；opencode 主包 362 模块 / 1504 边）
- **外部服务**：10 个（含 Tavily Search API）
- **版本基线**：官方 v1.18.25 → **v1.18.35**（本机运行时；上游最新 v1.19.0 只登记不追）

## 目录结构

```
0902-opencode-dag/
├── 01-dag-data/          # DAG 数据: official/diff/modified-dag.json + diff-list.json
├── 02-nodes/             # 133 节点页（36 包 + 87 装配 + 10 外部，七段式+内部结构DAG）
├── 03-groups/            # 42 组索引页
├── 04-interactive/       # cytoscape 三图交互（view-official/diff/modified.html）+ vendor
├── 05-drawio/            # main/ 三主图 + assembly/ 关键装配节点图
├── 05-diff/              # 改造差异清单表（94 条）
├── 06-md/                # AI 友好 MD 镜像
├── 07-checkpoint/        # 采集/建模/生成/门控脚本 + 中间数据
├── 08-collect/           # v1.18.35 采集数据 + 各阶段 stage-*.json（内部结构沿用 v1.18.29 基线）
├── opencode-src-v1.18.29/# 官方源码 worktree（v1.18.29 基线；v1.18.35 包级结构未变）
└── index.html            # 根入口
```

## 三图递进逻辑

```
图1 官方包级 ──────────► 图2 官方+改造对比 ──────────► 图3 改造版双层
(未改造基线)              (标明改造点)                  (包级+装配层)
36 包依赖                  7 包被引用 + 外部             36 包 + 87 装配 + 10 外部
```

## 自进化机制（0911 版，18 个）

0906 的 17 个机制本次全量重扫并新增 **架构三层栈（架构判断机制）**，装配层自进化机制体系达 18 个，覆盖"角色编排、缓存与并行、故障自愈、编码安全、留档与记忆、联网与架构判断"：

| 机制节点 | 价值 |
|---------|------|
| Grill-Me Protocol | 用持续追问收敛方案，把模糊需求钉成可执行的决策树 |
| Agent 委派协议 | plan/build 委派子Agent 并行执行，主Agent 纯净编排 |
| GATE 强制门控 | 所有任务前自评复杂度（范围/深度/操作/风险），选 Daily/Deep |
| Variant 继承与运行时控制 | daily↔deep 变体切换，max_tokens/reasoning_effort 分级 |
| Reflection 自检系统 | 周期末 4 层输入写 pending.json，委派 reflection-worker 审阅 |
| MEMORY.md 硬门禁 | 记忆只经 pending→reflection→/reflection 链路写入 |
| 缓存感知 (Cache Awareness) | DeepSeek prefix-cache 高命中，前缀字节稳定 |
| Parallel & Batching | 独立工具调用并行发出、相邻只读合并批次 |
| Output Discipline | 分段读取大文件、压缩大输出、只读优先 |
| 故障自愈协议 | 工具/连接 3 次自修复、JSON 解析兜底、超时降级 |
| 编码安全规则 | 优先 edit 工具、禁止 python -c 管道、replaceAll 复核 |
| Mission 留档规则 | 完成后半自动留档，5 段模板 + 质量门控 |
| 浏览器标签页管理 | 多窗口/标签 SPA 操作规范 |
| 联网代理纪律 (WSL2) | 默认直连，境外显式走网关，git 定向代理 |
| Universal SubAgent Rules | 子Agent 身份约束 + 结构化 JSON 返回契约 |
| Universal Coding Discipline | 验证证据、磁盘重读、路径本地化、元数据不入输出 |
| Session Memory 结构化压缩 | compaction 5 段模板（当前状态/关键文件/已做决策/待解决问题/经验教训） |
| 架构三层栈（架构判断机制） | skill + agent + instruction + command + gate 五元机制，技术选型/架构评审必经 `gate_architecture.py` |

本次更新为**官方源码 v1.18.29 → v1.18.30 点检 + 装配层全量重建 + 架构判断能力入图**三合一：官方侧仅版本标注与外部 SDK 升号（36 包结构与依赖边不变），装配层从 73 组件重建成 83 组件（+12 新增 / −2 退役，新增架构三层栈机制），10 个外部服务维持不变。

## 关键发现

1. **架构判断能力落地**：新增 `architecture-judgment` skill + `architect-worker` 子Agent + `architecture-behavior` 指令 + `/arch` 命令 + `gate_architecture.py` 五元机制，装配层从"联网能力增强"扩展为"架构判断 + 交付发布 + 知识库构建"多能力体系
2. **改造仍浅**：仅 7 个官方包（opencode/core/schema/plugin/sdk/server/llm）被装配层直接引用，改造主体仍是配置装配层
3. **装配层能力扩张**：skills 33→41（+8）、agents 9→10（+1），新增能力覆盖 GitHub 大仓库上传、岗位表筛选、知识库构建、能力扩展 SOP、受限语料采集、可续跑流水线、单一真相源文档
4. **退役清理**：`tool-read` 改模型原生多模态退役、`instr-agent-protocol` 并入 auto-mode，装配层去掉冗余工具节点
5. **官方包 v1.18.30 内容演进**：外部 SDK 升号（@ai-sdk/azure、@ai-sdk/openai、gitlab-ai-provider）、Bedrock-DeepSeek id 修复补丁、console i18n 与多语言文档更新，不触及包间依赖图

## 大包内部结构（组级视图）

oc-opencode (362 模块) / oc-core / oc-app 等大包内部 DAG 采用**目录分组组级视图**：第一层显示目录组节点（如 session/、tool/、provider/），点击组节点下钻查看组内模块依赖，避免数百模块一次性渲染导致卡顿/无渲染。

## 质量门控

`08-collect/quality-gate.py` **33 项 ALL PASS**（**黄金期望值改为从 `01-dag-data/modified-dag.json` 的 `stats` 动态读取**，并保留"不得为 0"非空断言，避免下次升级因写死值失效而假红）：JSON 合法 / DAG 无环无悬空 / HTML 断链 0 / drawio 配套齐全 / 节点页 133 覆盖 / 无陈旧节点页 / 交互图 DATA 一致 / 三图节点数 36/46/133 / 装配 87 / 外部 10 / 机制 18 / 组 42 / 包节点 36 / 总节点 133 / 七段完整 / 统计一致。
headless + VLM 验证：三图 view-official/diff/modified 渲染正常，中文完整无截断（zcount 36/46/133 全匹配）。

*基线版本：官方 v1.18.35（包级结构沿用 v1.18.29）｜ 更新日期：2026-10-11*
