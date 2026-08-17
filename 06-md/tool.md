# tool 节点（1）

## tool-read — read
- 组: A3-插件工具 | Layer 5
- 作用: 自定义 read 工具（TypeScript，zod 定义参数），覆盖 opencode 内置 read：①目录→列出条目；②9 种图片扩展名→经 GLM-4V VLM 转文字描述（base64 data URL 传图，max_tokens=4096，温度 0.3，中文提示词提取文字/UI/代码/布局/报错信息）；③文本→按 offset/limit 分段读取并加行号（默认 2000 行）。模型优先级付费 glm-4.6v → 429 降级免费 glm-4.6v-flash；GLM_KEY 优先环境变量 ZHIPU_API_KEY，未设置回退硬编码值。
- 提供: 图片 VLM 描述读取、文本分段带行号读取、目录列举（与 vision-interceptor 插件构成双保险的视觉链路）
- **为什么存在（历史）**: 早期用 Bun + TypeScript 重写 opencode 内置 read 工具（tools/read.ts）；0802 盘点：核心增强——图片自动分析（9 种格式调 GLM-4V 描述）、降级处理、目录列表（readdirSync）、文本分段（offset/limit）；同时指出 GLM API Key 硬编码安全问题（Line 15）；0803 编码安全修复时确认此为 custom read 工具（非内置）；0807 VLM 图片识别修复：付费 glm-4.6v 优先 + 429 降级免费 glm-4.6v-flash + Key 改环境变量（process.env.ZHIPU_API_KEY 优先 + 硬编码兜底）。
- **为什么存在（当前）**: 保留图片自动分析能力（IMAGE_EXTS 9 种格式）→ GLM-4V 描述；GLM_MODELS = ['glm-4.6v', 'glm-4.6v-flash'] 付费优先降级链；Key 环境变量化；与 vision-interceptor 构成双保险视觉链路（0807 报告定位）。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: plugin-vision-interceptor（双通道视觉链路，read 通道结果不写入插件 processedImages 缓存）、GLM API（智谱视觉模型）。
