# command 节点（2）

## command-arch — arch
- 组: AG5-工具插件 | Layer 1
- 作用: 自定义命令 arch.md
- 提供: 
- **为什么存在（历史）**: 0911 架构能力扩展的显式入口——用户可用 /arch <任务描述> 强制走架构流程（agent: build），命令文件自包含、不依赖其他文档即可执行。
- **为什么存在（当前）**: 需求驱动：为架构能力提供 build 模式下的显式命令入口，串起判场景→定产出→委派 architect-worker→门控→交付→询问架构图全流程，确保门控未过不声称完成。
- **怎么用（触发）**: 用户输入 /arch <任务描述> 或 /arch 选型|评审|边界|技术债 ... 时在 build 模式执行。
- **怎么用（工作流）**: ①读 routing.md §0 场景索引把任务归入 18 场景之一；②定产出类型（adr/boundary 门控级，review/tech-debt 模板级）；③委派 architect-worker（prompt 含 Skills to Load、契约、TEC 约束、Return Format）；④跑 gate_architecture.py（--kind adr|boundary），FAIL 把 checks/errors 原样回传修正最多 2 轮；⑤交付主产物 + 矩阵 + 门控证据 + 命中场景节点；⑥主动询问是否生成 drawio 架构图（是则委派 drawio-worker 且 prompt 必含 drawio-reference）。
- **怎么用（协作）**: 依赖 skill-architecture-judgment（workflow/checklist/templates/schemas/gate_architecture.py）、agent-architect-worker、instr-architecture-behavior；架构图委派 drawio-worker；属架构三层栈显式入口；依赖 config-main（command 目录自动加载）。

## command-reflection — reflection
- 组: AG5-工具插件 | Layer 1
- 作用: 自定义命令 reflection.md
- 提供: 
- **为什么存在（历史）**: 
- **为什么存在（当前）**: 
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: 
