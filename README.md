# RAG 智能知识问答系统（前端）

一个基于 RAG（检索增强生成）的智能知识问答系统前端界面。包含历史会话管理、添加知识库、对话问答等交互功能。

## 目录结构

```
RAG_web/
└── domain/                 # 前端源码
    ├── index.html          # 页面结构
    ├── style.css           # 样式与布局
    └── script.js           # 交互逻辑与接口调用
```

## 前端结构

页面整体分为 **左侧侧边栏（sidebar）** 与 **右侧主区域（main）** 两部分。

| 区域 | 容器 | 说明 |
|------|------|------|
| 侧边栏 | `.sidebar` | 可折叠收起，包含标题、新建对话、添加知识库、历史消息列表 |
| 主区域 | `.main` | 折叠按钮、对话消息展示区 `.dialog-box`、底部输入框 `.input-box` |

### 侧边栏（sidebar）
- **新建对话**：清空当前会话并回到空白状态
- **添加知识库**：弹出遮罩弹窗，支持选择多个文件并上传
- **历史消息列表**：点击加载对应会话并按需高亮，每条带删除按钮

### 主区域（main）
- **对话区 `.dialog-box`**：展示用户与 AI 的消息气泡（`.userMsg` / `.aiMsg`）
- **输入框 `.input-box`**：文本框输入 + 发送按钮，支持 Enter 发送

## 主要交互逻辑（script.js）

| 功能 | 说明 |
|------|------|
| 发送消息 | 渲染用户消息 → 保存 → 请求 AI 回复 → 渲染并保存回复 |
| 历史对话 | `currentMessage` 记录当前会话，切换时自动高亮当前项 |
| 删除会话 | 调后端 DELETE 接口删除 JSON 文件，刷新列表 |
| 新对话 | 清空 `currentMessage` 与对话区，重新渲染列表 |
| 添加知识库 | 动态创建弹窗，`FormData` 多文件上传 |

## 前端依赖的后端接口

前端通过 fetch 调用本地后端接口：

| 方法 | 路径 | 作用 |
|------|------|------|
| GET | `/api/getHistoryList` | 获取历史会话列表 |
| GET | `/api/getHistoryMsg?id=xxx` | 获取某会话的消息列表 |
| POST | `/api/saveMessage` | 保存一条消息到会话 |
| POST | `/api/getAIresponse` | 请求 AI 回复 |
| POST | `/api/uploadKnowledge` | 上传知识库文件 |
| DELETE | `/api/deleteHistory?id=xxx` | 删除某个会话 |

## 运行说明

前端为纯静态页面，直接以本地 HTTP 服务器打开 `domain/index.html` 即可（需自行启动后端服务并保证接口可用）。

```bash
# 示例：在项目根目录启动静态服务
python -m http.server 3000
```
