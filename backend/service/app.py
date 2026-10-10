import os
import json

from fastapi import FastAPI
from backend.service.knowledgeBase import KnowledgeBase
from pydantic import BaseModel
import config_data

app = FastAPI()
knowledge_base = KnowledgeBase()

class SaveMessageRequest(BaseModel):
    id: str
    role: str
    message: str

@app.post("/api/saveMessage")
def save_message(request: SaveMessageRequest):
    os.makedirs(os.path.dirname(config_data.history_message_path), exist_ok=True)
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


@app.get("/api/getAIResponse")
def get_ai_response():
    pass

@app.get("/api/getHistoryList")
def get_history_list():
    pass

@app.get("/api/getHistoryMsg")
def get_history_msg():
    pass

@app.delete("/api/deleteHistory")
def delete_history():
    pass

@app.post("/api/uploadKnowledge")
async def upload_knowledge(files):
    for file in files:
        result = []
        content = (await file.read()).decode("utf-8", errors="ignore")
        r=knowledge_base.add_knowledge(content, file.filename)
        result.append({"filename": file.filename, "result": r})
    return {"result": result}