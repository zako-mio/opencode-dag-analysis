# plugin 节点（1）

## plugin-vision-interceptor — vision-interceptor
- 组: A3-插件工具 | Layer 6
- 作用: opencode 插件，export server(ctx)，挂两个钩子：①chat.message——用户消息到达时把 file 类型 image part 替换为 VLM 文字描述；②experimental.chat.messages.transform——真正组装 LLM 请求前转换 messages（核心修复，确保图片先转文字再发给无视觉模型）。调用智谱 GLM API（GLM_URL=open.bigmodel.cn/api/paas/v4/chat/completions），模型优先级付费 glm-4.6v → 429 限流降级免费 glm-4.6v-flash。processedImages Map 缓存 URL→描述，避免 messages.transform 对历史消息重复调用 VLM（省成本），SKIP 时用缓存补全 text part。日志写入 %USERPROFILE%\.local\share\opencode\log\vision-int.log。
- 提供: 图片→文字描述注入（使仅文本输入的 Flash 模型具备视觉理解）、URL 级缓存去重、VLM 调用日志
- **为什么存在（历史）**: 早期创建（plugins/vision-interceptor.js）；0802 盘点：chat.message 环节拦截图片 Part 调用 GLM-4V 生成描述，作为 DeepSeek V4 Pro 图片输入的备选方案（'即使 Pro 支持图片输入，此插件仍保留作为备选'）；0803 编码安全修复：GLM API Key 硬编码问题暴露；0807 VLM 图片识别修复（关键）：反编译二进制证实 chat.message 钩子修改 parts 永不生效（opencode 用闭包原始 fe 处理图片）→ 新增 experimental.chat.messages.transform 钩子（SessionPrompt.run 组装 LLM 请求前直接修改 messages 数组）修复成功；Set 缓存改 Map（URL→描述），SKIP 时复用描述不丢图；Key 硬编码 → 环境变量 ZHIPU_API_KEY 优先 + 硬编码兜底。
- **为什么存在（当前）**: 保留双钩子：chat.message（日志 + 首次处理）+ experimental.chat.messages.transform（核心修复，每次组装 LLM 请求前触发）；付费 glm-4.6v 优先 + 429 降级免费 glm-4.6v-flash；processedImages Map 内存缓存防重复扣费（但缓存仅内存级，模块重载即失效，历史图片全量重算）。
- **怎么用（触发）**: 
- **怎么用（工作流）**: 
- **怎么用（协作）**: tool-read（双通道视觉链路：read 通道读本地文件、插件通道处理上传附件，机制独立但成本可重叠）、GLM API（glm-4.6v/glm-4.6v-flash，智谱 open.bigmodel.cn）。
