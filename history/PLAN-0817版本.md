# opencode DAG 依赖分析 — 初步计划（Plan v1）

> 生成日期：2026-08-17 ｜ 模式：Plan 阶段 Grill-Me 收敛 13 项决策 → Build 阶段执行
> 状态：✅ 解析阶段（S0-S3）已完成，S4 生成中。解析后调整：官方包内部结构 DAG = 35 包全量（用户确认扩展）

## 任务背景

对 opencode 做 DAG 依赖分析，产出与 deepseek-harness（0816-plugin-dag）同构的交互交付物。
与 deepseek 本质差异：opencode 是 **monorepo 35 workspace 包 + 配置装配层**，改造全部集中在 `~/.config/opencode/`，未触及包级源码。

## 三项关键核实

| 项 | 事实 |
|---|---|
| 官方源码 | `0807-opencode原理分析\opencode-src`（v1.18.14，35 个 @opencode-ai/* workspace 包） |
| 本机运行 | npm 全局 `opencode-ai v1.18.16`（官方二进制，非 fork） |
| 改造载体 | `~/.config/opencode/` 装配层：opencode.jsonc / 50+ skills（3 路径）/ 7 agents / plugins(1) / tools(1) / commands(1) / mcp(6) / instructions(2) |

## 三个主 DAG 图（渐进递进）

| 图 | 内容 | 节点 |
|---|---|---|
| 图1 官方包级 | 未改造基线，35 workspace 包 + workspace 依赖/import 边 | 35 包 |
| 图2 官方+改造对比 | 官方基线 + 改造点染色（新增红/修改黄/禁用暗红/外部绿）+ 差异清单表 | 35 包 + 改造标注 |
| 图3 改造版双层 | 包级（语义分组）+ 装配层（类型分组）双层，运行时调用链边 | 35 包 + ~70 装配节点 |

## 13 项决策清单

1. **三个主 DAG 图**：图1官方包级 → 图2官方+改造对比 → 图3改造包级+装配层双层
2. **最小分析单元**：包级（35 workspace 包）+ 装配层（skills/agents/plugins/tools/commands/mcp/instructions）双层节点
3. **依赖判定**：源码实证 workspace:* + import + config 引用
4. **交付形态**：全量复用 0816 链（cytoscape 交互/节点页/组索引/MD/drawio/JSON/门控）
5. **装配层分组**：按类型（G-skills/G-agents/G-plugins-tools/G-mcp/G-commands-instructions）+ 包级按语义
6. **装配层边**：运行时调用链（装配→包、装配→外部服务、装配↔装配）
7. **对比图呈现**：单图染色 + 差异清单表
8. **官方调研**：权重分档 10 核心深度 why（联网）+ 25 简版 why
9. **改造层调研**：MEMORY + config 备份链 + 留档报告三源交叉
10. **装配页内容**：五段（作用/依赖/被依赖/改造原因/内部结构）
11. **交互结构**：单入口三图切换，下钻共享节点页
12. **质量门控**：全链门控 + headless/VLM 三图验证
13. **执行架构**：单 build 会话多阶段（S0-S6）

## 执行架构（S0-S6）

- **S0 清单**：35 包清单 + 装配层全量清单
- **S1 官方包采集**：并行 explore 子Agent 按语义域分路 + 脚本批量解析 TS imports
- **S2 装配层采集**：并行 explore 读 config + SKILL.md + plugins/tools/command + 三源历史
- **S3 建模**：build-dag 生成三图 JSON（官方/对比/改造双层），拓扑分层 + 无环 + 组
- **S4 生成**：gen-html 节点页五段 + 三图交互 + 差异表 + MD + drawio（3 主图 + 7 关键装配）
- **S5 门控**：quality-gate 全链 + headless/VLM 三图
- **S6 收尾**：README + 根入口 + 留档 + GitHub 新仓库

## 关键风险与应对

1. **官方包内部模块量大** → 全量内部结构用脚本自动解析（s1-package-deps + parse-internal-all 正则 import 提取），每包一页下钻渲染
2. **版本差异**（1.18.14 源码 vs 1.18.16 本机）→ 图1以源码为准，差异表注明版本
3. **装配层 50+ skill 的 why** → SKILL.md 描述 + 三源历史交叉，不联网
4. **git push 权限拦截** → GitHub 仓库创建 + commit 自动，push 用户手动

## 解析阶段产出（S0-S3 已完成）

| 数据 | 路径 | 内容 |
|---|---|---|
| 包清单 | 07-checkpoint/s0-packages.json | 35 包（26 主 + 9 console/stats） |
| 装配清单 | 07-checkpoint/s0-assembly.json | 61 装配组件（43 skills + 7 agents + 1 plugin + 1 tool + 1 command + 6 mcp + 2 instructions） |
| 包级依赖 | 07-checkpoint/s1-package-deps.json | 35 节点 / 50 边（49 workspace + 1 import） |
| 包语义 | 07-checkpoint/s1-package-semantics.json | 35 包全量 implementation/provides/depends_on/key_modules/why |
| 装配语义 | 07-checkpoint/s2-assembly-semantics.json | 61 组件 + 18 历史事件（三源交叉） |
| 图1 官方 DAG | 01-dag-data/official-dag.json | 35 节点 / 66 边 / 6 层 / 19 组 |
| 图2 对比 DAG | 01-dag-data/diff-dag.json | 43 节点 / 85 边（6 包 modified + 8 外部） |
| 图3 改造 DAG | 01-dag-data/modified-dag.json | 104 节点 / 158 边 / 8 层 / 38 组（35 包 + 61 装配 + 8 外部） |
| 内部结构 | 07-checkpoint/package-internal-all.json | 32 包 / 1771 模块 / 4466 边（全量） |

## 解析阶段关键发现

1. **改造不深**：仅 6 个官方包被装配层直接引用（opencode/core/schema/plugin/sdk/server），改造主体是配置装配层
2. **skills 依赖外部服务为主**：42 个 skill 中大多数 depends_on 是 GLM/高德/飞书/Chrome/drawio 等外部服务（ext 边 57 条），真正触核心包的只有配置层
3. **历史变迁脉络**：18 事件（2026-08-01~08-17），核心是缓存优化→MCP 精兵→编码安全→Reflection 自进化→VLM 修复→降本（Flash）→回滚 Pro

## 路径

- 交付目录：`D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\`
- 官方源码：`D:\Opencode_Download\Mission-file\2026-08\0807-opencode原理分析\opencode-src\`
- 装配层：`C:\Users\15057\.config\opencode\`
