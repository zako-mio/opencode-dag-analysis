# opencode DAG 依赖分析

## 简介

对 **opencode** 做 DAG 依赖分析，三图渐进式理解"官方原版 → 改造对比 → 改造版装配"：
1. **图1 官方包级 DAG**：35 个 `@opencode-ai/*` workspace 包依赖关系（未改造基线，v1.18.14 源码）
2. **图2 官方+改造对比 DAG**：官方基线 + 被改造引用的包染色 + 外部服务
3. **图3 改造版双层 DAG**：包级 + 装配层（skills/agents/mcp/tools/commands/instructions）+ 外部服务

## 为什么与 deepseek-harness 分析不同

| 维度 | deepseek-harness (0816) | opencode (本项目) |
|------|------------------------|-------------------|
| 架构 | cordis 插件装配 | monorepo 35 包 + 配置装配层 |
| 分析单元 | 插件（cordis） | workspace 包 + 配置组件 |
| 改造载体 | 插件装配 | ~/.config/opencode 装配层 |
| DAG 形态 | 单层插件图 | 三图递进（官方→对比→双层） |

## 快速开始

| 想做什么 | 去哪 |
|---------|------|
| **三图交互总览**（官方/对比/改造切换） | `04-interactive/view-{official,diff,modified}.html` |
| 根入口（简介+结论+时间线+导航） | `index.html` |
| 每节点一页（**七段**：作用/提供/依赖/被依赖/**为什么存在(why)**/**怎么用(how)** + 内部结构 DAG） | `02-nodes/`（104 页） |
| 组目录 | `03-groups/index.html`（38 组） |
| 改造差异清单表 | `05-diff/diff-list.html` |
| AI 检索 MD 镜像（含 why/how） | `06-md/00-index.md` |
| 静态 drawio 图 | `05-drawio/main/`（3 主图）+ `05-drawio/assembly/`（7 关键装配） |
| DAG 数据（JSON） | `01-dag-data/{official,diff,modified}-dag.json` |
| 内部模块 import 数据 | `07-checkpoint/package-internal-all.json`（1771 模块 4466 边） |

## 内容深化（why - how）

**104 节点全部七段**（三种节点类型各自适配的 why/how 结构）：
- **装配层（61 组件）**：⑤ 为什么存在（历史引入动机 + 当前需求驱动）+ ⑥ 怎么用（触发/工作流/协作）
- **官方包（35 包）**：⑤ 为什么存在（设计意图官方 + 改造关联：本机为何引用/为何不引用）+ ⑥ 怎么用（入口/导出 API/命令 + 典型场景与协作）
- **外部服务（8 个）**：⑤ 为什么存在（为什么需要 + 当前状态）+ ⑥ 怎么用（怎么接入 + 装配层调用）

why/how 由 6 路子Agent 深挖三源还原（留档报告 20+ 份 / MEMORY.md / config 备份链 / SKILL.md 设计意图 / 官方源码实证 / 外部服务官网），每条有据可查。主页面（index.html）全面升级：项目简介 + 三图卡片（含对比）+ 核心结论 4 条 + 历史变迁时间线（18 事件可视化）+ 装配体系导航 + 统计面板。

## 核心数据

- **图1 official**：35 包 / 66 边 / 6 层 / 19 组
- **图2 diff**：43 节点 / 66 边（6 包被改造引用 + 8 外部）
- **图3 modified**：104 节点 / 154 边 / 8 层 / 38 组（35 包 + 61 装配 + 8 外部，含 33 条 skill 间作用关系边）
- **内部结构**：33 包 / 2131 模块 / 5965 边（全量 import 解析）
- **skill 关系**：33 条有证据的 skill↔skill / skill→agent 作用关系（OpenSpec 工作流闭环 / superpowers 家族 / DAG 三 skill 链 / amap 协作 / recruit↔browser）

## 目录结构

```
0817-opencode-dag/
├── 01-dag-data/          # DAG 数据: official/diff/modified-dag.json + diff-list.json
├── 02-nodes/             # 104 节点页（35 包 + 61 装配 + 8 外部，五段式+内部结构DAG）
├── 03-groups/            # 38 组索引页
├── 04-interactive/       # cytoscape 三图交互（view-official/diff/modified.html）+ vendor
├── 05-drawio/            # main/ 三主图 + assembly/ 7 关键装配节点图
├── 05-diff/              # 改造差异清单表
├── 06-md/                # AI 友好 MD 镜像
├── 07-checkpoint/        # 采集/建模/生成/门控脚本 + 中间数据
└── index.html            # 根入口
```

## 三图递进逻辑

```
图1 官方包级 ──────────► 图2 官方+改造对比 ──────────► 图3 改造版双层
(未改造基线)              (标明改造点)                  (包级+装配层)
35 包依赖                  6 包被引用 + 外部             35 包 + 61 装配 + 8 外部
```

## 关键发现

1. **改造不深**：仅 6 个官方包（opencode/core/schema/plugin/sdk/server）被装配层直接引用，改造主体是配置装配层
2. **skills 依赖外部服务为主**：42 个 skill 大多挂 GLM/高德/飞书/Chrome/drawio 等外部服务（核心 8 大外部）
3. **skill 内部协作密集**：OpenSpec 12-skill 工作流闭环、superpowers 家族、DAG 三 skill 上下游链、amap 三 skill 协作路由
4. **历史变迁脉络**：18 事件（2026-08-01~17），缓存优化→MCP 精兵→编码安全→Reflection 自进化→VLM 修复→降本（Flash）→回滚 Pro
5. **装配层核心组件**：plan/build 双主 Agent（Grill-Me + 委派协议）、7 子Agent 全 Flash、2 启用 MCP（pdf-reader/drawio）、vision-interceptor 双钩子 VLM、自定义 read 工具

## 大包内部结构（组级视图）

oc-opencode (360 模块) / oc-core (315) / oc-app (326) 等大包内部 DAG 采用**目录分组组级视图**：第一层显示目录组节点（如 session/、tool/、provider/），点击组节点下钻查看组内模块依赖，避免数百模块一次性渲染导致卡顿/无渲染。

## 质量门控

`07-checkpoint/quality-gate.py` 18 项 ALL PASS：JSON 合法 / DAG 无环 / HTML 断链 0 / drawio 10 配套 / 节点页 104 覆盖 / 交互图 DATA 一致 / MD 覆盖 / 五段完整 / 统计一致。
headless + VLM 验证：三图 zcount 35/43/104 全部渲染正确，中文完整无截断。
