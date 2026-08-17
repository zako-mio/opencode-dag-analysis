# -*- coding: utf-8 -*-
"""补 ext-opencode-plugin 的 why/how"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

fp = r"D:\Opencode_Download\Mission-file\2026-08\0817-opencode-dag\01-dag-data\modified-dag.json"
with open(fp, encoding="utf-8") as f:
    dag = json.load(f)

for n in dag["nodes"]:
    if n["id"] == "ext-opencode-plugin":
        n["why_need"] = "vision-interceptor.js 插件依赖 @opencode-ai/plugin SDK（node_modules 1.18.9）提供的插件钩子类型与结构（Plugin/PluginInput/Hooks 等），使自定义插件能以官方插件协议接入 opencode 消息管线。装配层的插件机制复用官方 SDK，而非自行发明协议。"
        n["why_current"] = "当前用于 vision-interceptor 插件的类型基础（chat.message + messages.transform 双钩子）。本机 ~/.config/opencode/package.json 安装了 @opencode-ai/plugin，与官方 SDK 包（packages/plugin）同源，版本 1.18.9 与本机 opencode 1.18.16 基本对齐。"
        n["how_integrate"] = "通过 npm 安装：npm i @opencode-ai/plugin（本机 ~/.config/opencode/package.json 依赖）。插件文件在 ~/.config/opencode/plugins/*.js，通过 opencode 的 plugins 机制加载。"
        n["how_usage"] = "vision-interceptor.js 从 '@opencode-ai/plugin' 导入类型，定义 Plugin 结构（id/name/tools 钩子），注册 chat.message 与 messages.transform 钩子拦截消息做 VLM 图片转文字。"
        n["evidence"] = "C:\\Users\\15057\\.config\\opencode\\node_modules\\@opencode-ai\\plugin（package.json）+ plugins/vision-interceptor.js"
        break

with open(fp, "w", encoding="utf-8") as f:
    json.dump(dag, f, ensure_ascii=False, indent=2)
print("ext-opencode-plugin updated")

# 验证 8/8
ext = [n["id"] for n in dag["nodes"] if n.get("layer_type") == "external" and not n.get("why_need")]
print("ext missing why_need:", ext if ext else "none")
