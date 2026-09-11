# 0911 更新盘点：官方 v1.18.30 点检 + 装配层重建方案

> 生成时间：2026-09-11 ｜ 范围：**仅盘点与方案，不执行重建**
> 基线：交付物当前版本 = 官方 v1.18.29 + 装配层 73 组件（0906 版）
> 目标：官方 v1.18.30 + 装配层现状（本机 `~/.config/opencode`）全量重建
> 只读约束：`~/.config/opencode/**` 只读；本任务只新建本文件，未改动任何交付物

---

## 一、T1 官方侧点检（D1）

### 1.1 事实核验（本机 git 实测，非转述）

| 项 | 值 | 证据 |
|---|---|---|
| 基线 tag | `v1.18.29` = `16747470f976aca3d362ad730bcd3fe82ecc2c9a` | `git ls-remote --tags origin` |
| 目标 tag | `v1.18.30` = `3104c1428ec91f809e5ab86631300de41eb6952e` | 同上；已 fetch 该 commit 供 diff |
| compare 规模 | 105 files / +1676 / −403 | `git diff --stat 16747470f 3104c1428` |
| workspace 包数 | **36 → 36（不变）** | `git ls-tree -r 3104c1428 packages/ \| grep -c '/package.json$'` = 36；packages/ 下 32 个目录（`console/stats/sdk` 为多包目录，合计仍 36） |
| workspace 依赖线 | **0 条增删**（`@opencode-ai/*` 依赖行 diff 为空） | `git diff ... -- '**/package.json' \| grep -E '@opencode-ai/'` 无输出 |

### 1.2 package.json 变更明细（29 个文件，全部为版本/外部 SDK 升号）

- **workspace 包自身 version 1.18.29 → 1.18.30**（28 个 `packages/*/package.json` + `sdks/vscode/package.json`）
- **`packages/opencode/package.json`（唯一实质性 non-version diff，8 行 = 4 增 4 删）**：
  - `@ai-sdk/azure` 3.0.88 → 3.0.93
  - `@ai-sdk/openai` 3.0.84 → 3.0.88
  - `gitlab-ai-provider` 6.13.0 → 6.15.0
  - （均为**外部 npm 依赖**，非 workspace 包）
  - 另有 `patches/@ai-sdk%2Fopenai@3.0.88.patch`（+280 行）新增，即 Bedrock-DeepSeek id 修复补丁
- **无任何 `@opencode-ai/*` workspace 依赖行新增/删除**

### 1.3 变更分布（与主Agent 背景一致）

| 目录 | 文件数 | 说明 |
|---|---|---|
| packages/console/app/src/i18n | 18 | 翻译文件 |
| packages/web/src/content/docs/* | 37+ | 多语言文档（含 zh-cn/zh-tw） |
| packages/ui, packages/opencode/{src,test}/provider, sdks/vscode, patches | 其余 | provider SDK 升级、Astra prompt 移植、Bedrock/DeepSeek id 修复 |

### 1.4 结论（明确）

> **官方侧：仅版本标注更新，无需重算包级结构。**
> - 包级节点集合（36 个 `@opencode-ai/*` workspace 包）**无新增/删除**；
> - 包级依赖边（workspace-dep）**无新增/删除**；
> - 版本间改动全部落在外部依赖版本号、文档、console i18n 与包内源码实现，**不触及 package 间 import/依赖图**。
> - 唯一需要改的是 `official-dag.json` 的 `title` / `version_note`（`v1.18.29` → `v1.18.30`），以及各包 `version_delta` 文案（`v1.18.14 → v1.18.29` 可统一标注为 `… → v1.18.30`）。
> - 内部模块 import 数据（`internal-*.json`）：核心运行时仅 packages/opencode(7)/packages/core(3) 文件变动，模块数/边数会小幅变化，**建议重跑 `s1-parse-internal.py` 以确保内部结构 DAG 与 v1.18.30 一致**（属"重算"但成本低、非结构变化）。
> - 边界说明：`official-dag.json` 的 68 条边中含 51 workspace-dep + 16 semantic-dep + 1 import（`oc-desktop → oc-app`）。semantic/import 边源自 0817 语义采集，非 v1.18.30 自动化产物；因包级源文件改动未涉及跨包引用，可沿用，建议重建时跑一次 `s1-pkg-inventory.py` 复核 workspace 边仍为 58。

---

## 二、T2 装配层全量重建方案

### 2.1 当前装配层全清单（机械采集实测）

按 `08-collect/s2-assembly-inventory.py` 的口径（活体配置 + 目录，只读复算）：

| 类别 | 旧（0906，73 口径） | 现（实测） | 变化 |
|---|---:|---:|---|
| skills（含 `SKILL.md` 的活跃 skill） | 33 | **41** | +8 |
| agents | 9 | **10** | +1 |
| mcp | 6 | **6** | 0 |
| instructions（`instructions/` 目录 .md） | 5 | **5** | 0（组成变） |
| tools（`tools/` 目录） | 1 | **0** | −1 |
| commands | 1 | **2** | +1 |
| config | 1 | **1** | 0 |
| mechanisms | 17 | **18** | +1 |
| **合计（73 口径）** | **73** | **83** | **+10** |

> **口径核对（README「73 组件」）**：旧 73 = 33 skills + 9 agents + 6 mcp + 5 instr + 1 tool + 1 command + 1 config + 17 mechanisms。
> 现机械口径合计 = 41+10+6+5+0+2+1+18 = **83**。
> ⚠️ 全量目录另有 `skills/_shared`（公共方法库，非 skill 节点）与 4 个禁用 skill（`_SKILL.md` 前缀：`amap-budget-control` / `amap-jsapi-skill` / `amap-lbs-skill` / `model-switcher`）。若把禁用也算入则 skills=45、合计=87。**本次沿用 0906 口径（只计 `SKILL.md`，禁用不入图），即 41 / 83。**

**skills（41）**：agency-agents, architecture-judgment, browser-harness, cytoscape-dag-visualization, dag-tutorial-authoring, drawio-reference, frontend-design, github-bulk-upload, grill-me, headroom, job-listing-filter, kb-construction, lark-suite, login-auth-channel, multi-window-dag-delivery, opencode-capability-extension, opencode-config, openspec-apply-change, openspec-archive-change, openspec-bulk-archive-change, openspec-continue-change, openspec-explore, openspec-ff-change, openspec-new-change, openspec-onboard, openspec-propose, openspec-sync-specs, openspec-update-change, openspec-verify-change, pdf-ocr, recruit-assist, release-openspec, restricted-corpus-acquisition, resumable-content-pipeline, resume-builder, search-methodology, single-source-docs-pipeline, soe-resume, superpowers-feature-workflow, superpowers-learning-workflow, superpowers-openspec-superpowers-workflow

**agents（10）**：plan, build, pdf-worker, drawio-worker, **architect-worker**, vision-worker, general, explore, reflection-worker, search-worker

**instructions（5，目录实测）**：architecture-behavior, auto-mode, browser-management, downloads, search-behavior
> ⚠️ 配置 `instructions` 数组只引用 4 个：`auto-mode.md` / `MEMORY.md`（根）/ `search-behavior.md` / `architecture-behavior.md`。`browser-management.md` / `downloads.md` 留在目录但**未被 config 引用**（遗留文件）。

**commands（2）**：reflection, **arch**
**mcp（6）**：vscode-mcp-server, amap, pdf-reader, drawio, drawio-local, headroom（名称不变）
**tools**：空（`tools/read.ts` 已于 0908 退役）
**config（1）**：`~/.config/opencode/opencode.jsonc`

### 2.2 差异清单（vs 实机 `~/.config/opencode/`）

**新增组件（12）**

| id（建议） | 类型 | 来源 | 备注 |
|---|---|---|---|
| skill-architecture-judgment | skill | skills/architecture-judgment | 架构判断能力包（含 `_private/gate_architecture.py`、schemas、templates） |
| skill-github-bulk-upload | skill | skills/github-bulk-upload | GitHub 大仓库上传 |
| skill-job-listing-filter | skill | skills/job-listing-filter | 岗位表批量筛选 |
| skill-kb-construction | skill | skills/kb-construction | 知识库构建主入口 |
| skill-opencode-capability-extension | skill | skills/opencode-capability-extension | opencode 能力扩展 SOP |
| skill-restricted-corpus-acquisition | skill | skills/restricted-corpus-acquisition | 受限/付费语料采集 |
| skill-resumable-content-pipeline | skill | skills/resumable-content-pipeline | 可续跑内容流水线 |
| skill-single-source-docs-pipeline | skill | skills/single-source-docs-pipeline | 单一真相源文档流水线 |
| agent-architect-worker | agent | opencode.jsonc agent 段 | 架构判断子Agent（hidden=false，无 model，继承父会话） |
| instr-architecture-behavior | instruction | instructions/architecture-behavior.md | 架构行为层（三层栈之一） |
| command-arch | command | command/arch.md | `/arch` 命令 |
| mech-architecture | mechanism | 架构三层栈 | skill + agent + instr + command + gate 五元机制 |

**删除/退役组件（2）**

| id | 类型 | 原因 |
|---|---|---|
| tool-read | tool | `tools/read.ts` 于 0908 退役（改模型原生多模态；配置 prompt 已注明） |
| instr-agent-protocol | instruction | `agent-protocol.md` 已并入 `instructions/auto-mode.md`（GATE 段之前为 Agent Protocol 主体） |

**数量变化**：skills 33→41（+8）、agents 9→10（+1）、mcp 6→6、instructions 5→5（−agent-protocol / +architecture-behavior，净 0）、tools 1→0（−1）、commands 1→2（+1）、config 1→1、mechanisms 17→18（+1）；**合计 73→83（+10）**。

**外部服务**：旧 10 个（含 `ext-tavily-api`）。v1.18.30 与新增组件均未引入强制新外部后端，**建议维持 10 个**；`skill-github-bulk-upload` 依赖 GitHub（git/gh），若建模需要可新增 `ext-github`（存量 `ext-opencode-plugin` 之外的候选，见 §五 风险 R4）。

**机制节点（18，建议新增 1）**：旧 17 个沿用；新增 `mech-architecture`「架构三层栈（架构判断机制）」——由 `skill-architecture-judgment` + `agent-architect-worker` + `instr-architecture-behavior` + `command-arch` + `gate_architecture.py` 五元组成，触发点见 `instructions/architecture-behavior.md`。
> 候选（需在重建前确认，见风险 R3）：`opencode-capability-extension`（能力扩展三层栈 + 引用普查）、`restricted-corpus-acquisition`（双仓隔离 + fail-closed 装配）、`single-source-docs-pipeline`（单一真相源 + 派生对账）。当前这些以 **skill** 形态存在，未升格为跨 Agent 的全局机制；若升格则 mechanisms 18→21、合计 83→86。

### 2.3 可执行重建步骤（脚本链）

**脚本目录分工**：`08-collect/` = 0906 最新 v2 链（**重建以此为准**）；`07-checkpoint/` = 0817/0902 旧链（仅存量备份，勿混跑）。

| 步骤 | 脚本 | 输入 | 输出 | 复用性 |
|---|---|---|---|---|
| S0 备份 | `cp -r`（手工） | 现有交付目录 | `0902-opencode-dag.bak-20260911` | 手工 |
| S1 源码 worktree | `git fetch` + `git checkout v1.18.30`（手工） | remote anomalyco/opencode | `opencode-src-v1.18.30/` | 手工，需同步脚本内 SRC 路径 |
| S2 基线元数据 | 手工编辑 | — | `stage-00-version-baseline.json`（v18_30_actual 段） | **需改** |
| S3 包级清单 | `s1-pkg-inventory.py` | `opencode-src-v1.18.30/packages/*/package.json` | `s1-package-deps.json` | 复用，**改 SRC 路径** |
| S4 内部模块 | `s1-parse-internal.py` | v1.18.30 源码 + `s1-package-deps.json` | `internal-v1.18.30.json` | 复用，**改 SRC 路径 + 输出文件名** |
| S5 装配清单 | `s2-assembly-inventory.py` | `~/.config/opencode`（只读） | `s2-assembly-inventory.json` | **可直接复用**（自动纳入新组件；已修 `.bak-` 过滤） |
| S6 机制重扫 | explore 子Agent + 手工 | auto-mode.md / architecture-behavior.md | `stage-03-mechanisms.json`（+mech-architecture） | **需改**（新增机制条目） |
| S7 新组件 why/how | explore 子Agent + 手工 | SKILL.md / config | `stage-03-new-assembly.json`（+9 新组件 why/how/deps） | **需改**（内容深挖） |
| S8 版本变化 | explore 子Agent + 手工 | v1.18.29→v1.18.30 diff | `stage-03-package-updates.json` | **需改**（version_delta / what_changed） |
| S9 合并装配 | `s2-merge-assembly.py` | S5 + `stage-03-mechanisms.json` + `stage-03-new-assembly.json` | `s2-all-components.json` | **需改**（`MECH_META` 补 18th 机制；更新注释计数） |
| S10 建模三图 | `build-dag.py` | `s1-package-deps.json` + `s2-all-components.json` + stage-03-* | `01-dag-data/{official,diff,modified}-dag.json` + `diff-list.json` | **需改**（见 §2.3.1 清单） |
| S11 节点页 | `gen-nodes-v2.py` | `modified/diff/official-dag.json` + `internal-v1.18.30.json` + `diff-list.json` | `02-nodes/*.html`（129+index） | **需改**（内部文件名 + 副标题计数） |
| S12 交互三图 + 根入口 | `gen-interactive-v2.py` | 三 dag json | `04-interactive/view-*.html` + 根 `index.html` | **需改**（版本标题 + index 硬编码计数"114/39/36+69+9"） |
| S13 组页/diff 表/MD | `gen-groups-diff-md-v2.py` | 三 dag json + diff-list | `03-groups/` + `05-diff/diff-list.html` + `06-md/` | **需改**（版本副标题；组页/旧文件自动清理） |
| S14 drawio 静态图 | `drawio-worker` 子Agent（手工委派） | 新 DAG / 关键装配 | `05-drawio/main/`（3 主图）+ `05-drawio/assembly/` | 手工，需重绘 |
| S15 质量门控 | `quality-gate.py` | 全部交付物 | 控制台 PASS/FAIL | **需改**（硬编码 119/46/36 期望值 → 129/46/36） |
| S16 headless 验证 | `07-checkpoint/headless-final-v11829.py` | 三视图 | `07-checkpoint/screenshots/` + zcount | **需改**（期望 36/46/119 → 36/46/129）+ VLM |
| S17 README/报告 | 手工 | — | `README.md` + `执行报告-0911.{md,html}` | **需改** |

#### 2.3.1 `build-dag.py` 必改点（逐条定位）

| 行段 | 现状 | 需改为 |
|---|---|---|
| L112–113, L209, L364, L47–48 | 标题/`version_note` 写死 `v1.18.29` | `v1.18.30` |
| L216–226 `SKILL_GROUP` | 仅映射 33 个旧 skill | 补 8 个新 skill 组（architecture-judgment / github-bulk-upload / job-listing-filter / kb-construction / opencode-capability-extension / restricted-corpus-acquisition / resumable-content-pipeline / single-source-docs-pipeline） |
| L153–177 `asm_to_pkg` 规则 | 未覆盖 `architect-worker`、新 skill、`command-arch` | 补规则（command 的分支已有兜底，可自动纳入两条 command；agent 需显式加 `agent-architect-worker`） |
| L272–290 `asm_ext_rules` | 含 `ext-*-api → tool-read` 两条（L294–295） | **删除 tool-read 相关边**；按需新增新 skill→外部边 |
| L298–300 委派边 | 子Agent 列表 7 个 | 加 `agent-architect-worker`（plan/build 委派） |
| L322–343 `mech_edges` | 17 机制边 | 加 `mech-architecture` 边（→skill-architecture-judgment / agent-architect-worker / instr-architecture-behavior / command-arch / config-main / gate） |
| L364 `version_note` | 写死"装配层 69 组件 + 外部服务 9" | 改为实际计数（83 / 10） |
| L23–38 `PKG_GROUP` / `SHORT_ORDER` | 36 包 | **无需改**（包集不变） |

#### 2.3.2 其他脚本必改点

- `s1-pkg-inventory.py` L6 `SRC=…opencode-src-v1.18.29` → `…v1.18.30`
- `s1-parse-internal.py` L9 `SRC` 同上；L7/L93 输出文件名 `internal-v1.18.29.json` → `internal-v1.18.30.json`
- `s2-merge-assembly.py` L17–35 `MECH_META` 补 `mech-architecture`；L1 注释计数
- `gen-nodes-v2.py` L25 读 `internal-v1.18.29.json` → `v1.18.30`；L486 副标题 `36 官方包 + 69 装配组件 + 9 外部服务` → `36 + 83 + 10`
- `gen-interactive-v2.py` L256–258 三视图标题版本；L308 `v1.18.29 源码`；L333–335 硬编码 `114 节点`/`39 组`/`36 包 + 69 装配 + 9 外部`
- `gen-groups-diff-md-v2.py` L189 diff 表副标题 `v1.18.29`（及 L159 等文案）→ `v1.18.30`
- `quality-gate.py` L58 `节点页全覆盖(119)`、L82 期望 `119/36/46` → 新值（`129/36/46`）
- `07-checkpoint/headless-final-v11829.py` L30–32 期望 `36/46/119` → `36/46/129`；截图文件名前缀 `v11829` → `v11830`

### 2.4 预期受影响文件清单（按目录归类）

| 目录 | 数量 | 说明 |
|---|---:|---|
| `01-dag-data/` | 4 | official/diff/modified-dag.json + diff-list.json（覆盖写） |
| `02-nodes/` | 130 | 129 节点页（36 包 + 83 装配 + 10 外部）+ index.html；**删除陈旧 `tool-read.html`** |
| `03-groups/` | ~48+1 | 新组页约 48（旧 40，因新增 skill 组分群 +1~8）；index.html；旧组页自动清理 |
| `04-interactive/` | 3 | view-official/diff/modified.html（覆盖写） |
| `05-drawio/main/` | 3+3 | official/diff/modified 的 .drawio + .png（drawio-worker 重绘） |
| `05-drawio/assembly/` | ~7-16 | 关键装配详图（需补 architect-worker / 架构机制；旧 tool-read 图需处理） |
| `05-diff/` | 1 | diff-list.html |
| `06-md/` | ~12 | 00-index.md + 各 kind md（kind 数随新组件变化） |
| `07-checkpoint/` | 1+ | 本盘点文档 + 更新后的 headless 脚本 + screenshots |
| `08-collect/` | ~14 | 再生数据（s1-package-deps / internal-v1.18.30 / s2-assembly-inventory / s2-all-components / stage-00/03-*）+ 修改脚本 8 个；**新增 `opencode-src-v1.18.30/` worktree** |
| 根目录 | 4 | `index.html`、`README.md`、`执行报告-0911.md`、`执行报告-0911.html` |
| `.gitignore` / `.gitattributes` | 0-2 | 若 worktree 目录命名 v1.18.30 需同步通配 `opencode-src-v1.18.*` |

---

## 三、风险点

| # | 风险 | 影响 | 缓解 |
|---|---|---|---|
| R1 | **skills 计数口径分歧**：目录 45 个 vs 活跃 `SKILL.md` 41 个 | 合计 83 或 87，README 与门控数字不一致 | 明确沿用 0906 口径（只计 `SKILL.md`，禁用/`_shared` 不入图），在 README 与 stage-00 注明 |
| R2 | **陈旧产物残留**：`tool-read` 节点页/drawio 图、旧组页、旧 MD kind 文件 | 门控"无陈旧节点页"FAIL、断链 | `gen-nodes` 不会自动删非节点页；需在 S11/S13 后清理 `02-nodes/tool-read.html`、`05-drawio/assembly/tool-read.*`；组页/MD 由脚本自动清理 |
| R3 | **机制升格判定**：能力扩展/受限语料/单一真相源是否算独立 mechanism | mechanisms 18 或 21，影响节点数与机制边 | 重建前向用户确认口径；默认保守只加 `mech-architecture`（有明确三层栈 + gate + 命令） |
| R4 | **外部服务是否新增 `ext-github`**（github-bulk-upload 依赖 GitHub） | 外部服务 10 或 11，影响 diff 图 | 若该 skill 建模需要则新增；否则沿用 10 |
| R5 | **未引用 instruction**：`browser-management.md` / `downloads.md` 在目录但 config 未引用 | 建了"僵尸节点" | 二选一：补进 config `instructions` 数组，或从 DAG 剔除；需决策 |
| R6 | **drawio 手工链路**：三主图/装配图非脚本生成 | 易漏更、易与新 DAG 漂移 | 必须委派 drawio-worker（prompt 强制 `drawio-reference`），导出后 VLM + PNG 结构校验 |
| R7 | **版本字符串散落**：多脚本硬编码 `v1.18.29`/计数 | 漏改导致标题与数据不一致 | 按 §2.3.1/2.3.2 清单逐项 grep `v1.18.29`、`119`、`114`、`69 装配`、`9 外部` 全局核对（"旧值零残留"检查） |
| R8 | **source worktree 改名**：`opencode-src-v1.18.29/` → `v1.18.30/` | 所有脚本 SRC 路径 .gitignore 同步失效 | 先做路径引用普查再改名；或保留目录名、仅 checkout tag（成本更低） |
| R9 | **semantic-dep/import 边非自动产物** | 官方 v1.18.30 边沿用 0817 语义可能过时 | 包级源改动未涉跨包引用，可沿用；重建时跑 S3 复核 workspace 边计数 = 58 |

---

## 四、验收（重建后，非本次执行）

1. `quality-gate.py` 全 PASS（期望值已更新为 36/46/129）
2. headless Chromium 三视图 `zcount` = 36 / 46 / 129
3. VLM 验证三图中文完整无截断
4. "旧值零残留"：`grep -rn 'v1.18.29\|119 节点\|69 装配\|tool-read'` 在交付物目录无命中（历史报告除外）
5. 节点页无陈旧、无断链；`02-nodes/` 129+index
6. README/执行报告计数与 `modified-dag.json.stats` 一致

---

*盘点文档结束 ｜ 仅盘点，未执行任何重建或产物改动*
