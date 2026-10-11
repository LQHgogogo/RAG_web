import os
import json

from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from backend.service.knowledgeBase import KnowledgeBase
from backend.service.ragService import RagService
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel
from backend.config import config_data

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
knowledge_base = KnowledgeBase()
rag_service = RagService()

class SaveMessageRequest(BaseModel):
    id: str
    role: str
    message: str

class GetAIResponseRequest(BaseModel):
    id: str

@app.post("/api/saveMessage")
def save_message(request: SaveMessageRequest):
    os.makedirs(config_data.history_message_path, exist_ok=True)
    filepath = os.path.join(config_data.history_message_path, request.id + '.json')

    if os.path.exists(filepath):
        with open(filepath, "r", encoding='utf-8') as f:
            messages = json.load(f)
    else:
        messages = []

    messages.append(
        {
            "role": request.role,
            "message": request.message,
        }
    )

    with open(filepath,"w", encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)


@app.post("/api/getAIresponse")
async def get_ai_response(params: GetAIResponseRequest):
    filepath = os.path.join(config_data.history_message_path, params.id + '.json')

    if not os.path.exists(filepath):
        return {"content": "没有找到该会话的上下文"}

    with open(filepath, "r", encoding='utf-8') as f:
        messages = json.load(f)

    if not messages:
        return {"content": "会话内容为空"}

    question = messages[-1]["message"]
    history = []
    for msg in messages[:-1]:
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["message"]))
        elif msg["role"] == "ai":
            history.append(AIMessage(content=msg["message"]))

    async def generate():
        async for chunk in rag_service.chain.astream({
            "question": question,
            "history": history,
        }):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/api/getHistoryList")
def get_history_list():
    path = config_data.history_message_path
    if not os.path.exists(path) or not os.path.isdir(path):
        return {"result": []}
    return {"result": [os.path.splitext(os.path.basename(f))[0] for f in os.listdir(path)]}

@app.get("/api/getHistoryMsg")
def get_history_msg(id: str):
    filepath = os.path.join(config_data.history_message_path, id + '.json')
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding='utf-8') as f:
        messages = json.load(f)

    result = []
    for msg in messages:
        result.append({"role": msg["role"], "content": msg["message"]})

    return result



@app.delete("/api/deleteHistory")
def delete_history(id: str):
    filepath = os.path.join(config_data.history_message_path, id + '.json')
    if os.path.exists(filepath):
        os.remove(filepath)
    return {"content": "删除成功"}

@app.post("/api/uploadKnowledge")
async def upload_knowledge(files: List[UploadFile] = File(...)):
    for file in files:
        result = []
        content = (await file.read()).decode("utf-8", errors="ignore")
        r=knowledge_base.add_knowledge(content, file.filename)
        result.append({"filename": file.filename, "result": r})
    return {"result": result}