# opencode DAG 依赖分析

## 简介

对 **opencode** 做 DAG 依赖分析，三图渐进式理解"官方原版 → 改造对比 → 改造版装配"：
1. **图1 官方包级 DAG**：36 个 `@opencode-ai/*` workspace 包依赖关系（未改造基线，v1.18.29 源码）
2. **图2 官方+改造对比 DAG**：官方基线 + 被改造引用的包染色 + 外部服务
3. **图3 改造版双层 DAG**：包级 + 装配层（skills/agents/mcp/tools/commands/instructions/config/mechanisms）+ 外部服务

本次更新（2026-09-06）：**官方源码 v1.18.25 → v1.18.29 全量更新 + 装配层全量重建 + 自进化机制扩展**。opencode 自进化持续，装配层从 69 组件扩到 73 组件，新增 4 个联网搜索组件（search-worker / search-methodology / login-auth-channel / search-behavior）与 1 个 Session Memory 机制，DAG 从"自进化体系"进一步演化为"联网能力增强体系"。

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
| 每节点一页（**七段**：作用/提供/依赖/被依赖/**为什么存在(why)**/**怎么用(how)** + 内部结构 DAG） | `02-nodes/`（119 页） |
| 组目录 | `03-groups/index.html`（40 组） |
| 改造差异清单表 | `05-diff/diff-list.html` |
| AI 检索 MD 镜像（含 why/how） | `06-md/00-index.md` |
| 静态 drawio 图 | `05-drawio/main/`（3 主图）+ `05-drawio/assembly/`（7 关键装配） |
| DAG 数据（JSON） | `01-dag-data/{official,diff,modified}-dag.json` |
| 内部模块 import 数据 | `08-collect/internal-v1.18.29.json`（33 包 2251 模块 6079 边） |

## 内容深化（why - how）

**119 节点全部七段**（三种节点类型各自适配的 why/how 结构）：
- **装配层（73 组件）**：⑤ 为什么存在（历史引入动机 + 当前需求驱动）+ ⑥ 怎么用（触发/工作流/协作）
- **官方包（36 包）**：⑤ 为什么存在（设计意图官方 + 改造关联：本机为何引用/为何不引用）+ ⑥ 怎么用（入口/导出 API/命令 + 典型场景与协作）
- **外部服务（10 个）**：⑤ 为什么存在（为什么需要 + 当前状态）+ ⑥ 怎么用（怎么接入 + 装配层调用）

why/how 由多路子Agent 深挖三源还原（留档报告 / MEMORY.md / config 备份链 / SKILL.md 设计意图 / 官方源码实证 / 外部服务官网），每条有据可查。主页面（index.html）提供项目简介 + 三图卡片（含对比）+ 核心结论 + 历史变迁时间线 + 装配体系导航 + 统计面板。

## 核心数据

- **图1 official**：36 包 / 68 边 / 6 层 / 19 组（v1.18.29 源码）
- **图2 diff**：46 节点 / 68 边（7 包被改造引用 + 10 外部）
- **图3 modified**：119 节点 / 183 边 / 8 层 / 40 组（36 包 + 73 装配 + 10 外部，含 **17 个自进化机制 mechanism 节点**）
- **装配层**：73 组件（33 skills + 9 agents + 6 mcp + 5 instructions + 1 tool + 1 command + 1 config + 17 mechanisms）
- **内部结构**：33 包 / 2251 模块 / 6079 边（全量 import 解析，v1.18.29；opencode 主包 362 模块 / 1504 边）
- **外部服务**：10 个（新增 **Tavily Search API**，OpenCode Go 套餐补 Muse Spark 1.3/Hy4/Omen Alpha 模型）
- **版本基线**：官方 v1.18.25 → **v1.18.29**

## 目录结构

```
0902-opencode-dag/
├── 01-dag-data/          # DAG 数据: official/diff/modified-dag.json + diff-list.json
├── 02-nodes/             # 119 节点页（36 包 + 73 装配 + 10 外部，七段式+内部结构DAG）
├── 03-groups/            # 40 组索引页
├── 04-interactive/       # cytoscape 三图交互（view-official/diff/modified.html）+ vendor
├── 05-drawio/            # main/ 三主图 + assembly/ 7 关键装配节点图
├── 05-diff/              # 改造差异清单表
├── 06-md/                # AI 友好 MD 镜像
├── 07-checkpoint/        # 采集/建模/生成/门控脚本 + 中间数据
├── 08-collect/           # v1.18.29 采集数据 + 各阶段 stage-*.json
├── opencode-src-v1.18.29/# 官方源码 worktree（v1.18.29 基线）
└── index.html            # 根入口
```

## 三图递进逻辑

```
图1 官方包级 ──────────► 图2 官方+改造对比 ──────────► 图3 改造版双层
(未改造基线)              (标明改造点)                  (包级+装配层)
36 包依赖                  7 包被引用 + 外部             36 包 + 73 装配 + 10 外部
```

## 自进化机制（0906 版，17 个）

0902 的 16 个机制本次全量重扫并新增 **Session Memory 结构化压缩**，装配层自进化出完整的自进化机制体系（17 个），让装配层从"静态配置"升级为"可持续自进化的体系"：

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

本次更新为**官方源码 v1.18.25 → v1.18.29 + 装配层全量重建 + 联网搜索组件入图**三合一：36 包官方包结构随版本更新，装配层从 69 组件重建成 73 组件（新增 4 联网组件并新增 1 个 mechanism），10 个外部服务（含新增 Tavily Search API）。

## 关键发现

1. **联网搜索能力落地**：0905 架构后新增 search-worker 子Agent + search-methodology skill + login-auth-channel skill + search-behavior instruction（4 组件），装配层从"自进化"扩展为"联网能力增强"
2. **改造仍浅**：仅 7 个官方包（opencode/core/schema/plugin/sdk/server/llm）被装配层直接引用，改造主体仍是配置装配层
3. **装配层从"碎片化"变"能力增强体系"**：17 个机制节点 + 4 个联网搜索组件，DAG 呈现"可持续演进 + 外部事实获取"的双轨结构
4. **skills 依赖外部服务为主**：33 个 skill 大多挂 GLM/高德/飞书/Chrome/drawio/Tavily 等外部服务（核心 10 大外部）
5. **官方包 v1.18.29 内容演进**：Claude 5.1+ thinking block 容错、Azure 插件简化、Console 工作区迁移、Go 套餐新模型（Muse Spark 1.3/Hy4/Omen Alpha）

## 大包内部结构（组级视图）

oc-opencode (362 模块) / oc-core / oc-app 等大包内部 DAG 采用**目录分组组级视图**：第一层显示目录组节点（如 session/、tool/、provider/），点击组节点下钻查看组内模块依赖，避免数百模块一次性渲染导致卡顿/无渲染。

## 质量门控

`08-collect/quality-gate.py` 25 项 ALL PASS：JSON 合法 / DAG 无环 / HTML 断链 0 / drawio 配套齐全 / 节点页 119 覆盖 / 交互图 DATA 一致 / MD 覆盖 / 七段完整 / 统计一致 / 悬空边清洗。
headless + VLM 验证：三图 view-official/diff/modified 渲染正常，中文完整无截断（zcount 36/46/119 全匹配）。

*基线版本：官方 v1.18.29 ｜ 更新日期：2026-09-06*
