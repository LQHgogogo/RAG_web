# RAG 智能知识问答系统

一个基于 **RAG（检索增强生成）** 的端到端智能知识问答系统。用户上传知识库文档后，可通过向量检索 + 大模型生成的方式，基于文档内容进行问答。支持会话历史持久化、多轮对话、流式输出（打字机效果）、知识库去重入库等完整能力。

## 技术栈

| 端 | 技术 |
|------|------|
| 后端 | Python · FastAPI · LangChain · ChromaDB |
| 前端 | 原生 HTML / CSS / JavaScript |
| 向量模型 | 阿里云 DashScope（`text-embedding-v4`，需 `BAILIAN_API_KEY`）|
| 大模型 | DeepSeek（`deepseek-flash`，需 `DEEPSEEK_API_KEY`）|

## 核心特性

- **RAG 检索增强**：上传文档 → 分片 → 向量化 → 入库；提问时检索相关片段作为上下文注入大模型。
- **流式输出**：AI 回答以 SSE 流式逐段返回，前端打字机效果；首字前显示带呼吸动画的"检索思考中..."。
- **知识库去重**：基于 MD5 校验，重复文件自动跳过，避免重复入库。
- **会话管理**：历史会话以 JSON 落盘持久化，支持加载、切换、删除。
- **前端体验**：侧边栏折叠、空状态引导、当前会话 ID 顶部展示、多文件上传弹窗。

## 目录结构

```
RAG_web/
├── backend/                    # 后端源码
│   ├── __init__.py
│   ├── config/
│   │   └── config_data.py      # 全局配置（密钥、模型、路径、分片参数、提示词）
│   ├── routes/
│   │   └── app_routes.py       # FastAPI 接口定义（全部 REST API + CORS）
│   ├── service/
│   │   ├── ragService.py       # RAG 链组装（检索→提示词→模型→解析）
│   │   ├── vector_service.py   # Chroma 向量库封装
│   │   └── knowledgeBase.py    # 知识库入库、分片、MD5 去重
│   └── data/                   # 运行时数据
│       ├── chroma_db/          # 向量索引（Chroma）
│       ├── history/            # 会话历史（JSON 文件）
│       └── md5.txt             # 已入库内容 MD5 记录
│
├── domain/                     # 前端源码（纯静态）
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── start.bat                   # Windows 一键启动脚本（同时拉起前后端）
└── 启动服务命令.txt              # 启动命令说明
```

## 快速开始

### 1. 前置条件

- 安装 Python 3.9+
- 安装依赖（手动 pip 安装以下核心包）：
  - `fastapi`、`uvicorn`
  - `langchain`、`langchain-core`、`langchain-community`
  - `langchain-deepseek`
  - `chromadb`、`dashscope`

### 2. 配置环境变量

| 变量 | 说明 |
|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek 大模型密钥（对话生成）|
| `BAILIAN_API_KEY` | 阿里云百炼密钥（文档向量化）|

### 3. 启动服务

**方式一：一键启动（Windows）**
直接双击 `start.bat`，会自动弹出两个窗口分别启动后端（8080）与前端（3000）。

**方式二：手动启动**
两个终端分别执行：

```bash
# 终端 1：后端（项目根目录执行）
python -m uvicorn backend.routes.app_routes:app --host 0.0.0.0 --port 8080

# 终端 2：前端（domain 目录执行）
cd domain
python -m http.server 3000
```

### 4. 访问

浏览器打开 <http://localhost:3000>。

## 使用流程

1. 点击左侧"**添加知识库**"，选择一份或多份文档上传（系统会自动分片、向量化并入库）。
2. 在底部输入框提问，Enter 发送。
3. AI 会先显示"检索思考中..."，随后以流式输出回答。
4. 对话自动保存为历史会话，可在左侧历史列表点击切换、删除。

## API 接口

后端默认运行在 `http://localhost:8080`：

| 方法 | 路径 | 作用 |
|------|------|------|
| POST | `/api/saveMessage` | 保存一条消息到会话 |
| POST | `/api/getAIresponse` | 获取 AI 回复（SSE 流式）|
| GET | `/api/getHistoryList` | 获取历史会话列表 |
| GET | `/api/getHistoryMsg?id=xxx` | 获取某会话全部消息 |
| DELETE | `/api/deleteHistory?id=xxx` | 删除某个会话 |
| POST | `/api/uploadKnowledge` | 上传知识库文件（多文件）|

> `/api/getAIresponse` 返回 `text/event-stream`，数据格式为 SSE 的 `data: {...}\n\n`，以 `data: [DONE]\n\n` 结束。

## 配置说明

核心配置集中在 `backend/config/config_data.py`：

| 配置项 | 说明 |
|------|------|
| `chat_key` / `chat_model` | 对话大模型与密钥（DeepSeek）|
| `embedd_key` / `embedding_model` | 向量模型与密钥（DashScope）|
| `chunk_size` / `chunk_overlap` | 文档分片大小与重叠 |
| `persist_dir` | Chroma 向量库持久化路径 |
| `md5_path` | 去重 MD5 记录文件路径 |
| `history_message_path` | 会话历史 JSON 存储路径 |
| `system_prompt` | 系统提示词（问答规则）|

## 停止服务

- 在对应终端按 `Ctrl + C` 停止。
- 若端口被占用：`netstat -ano | findstr :8080` 查 PID，再 `taskkill /F /PID <PID>`。
