from operator import itemgetter
from typing import List

from langchain_core.documents import Document
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_deepseek import ChatDeepSeek

import vector_service
from backend.service.config_data import chat_KEY
from config_data import embedd_KEY, embedding_model, chat_model


class RagService:
    def __init__(self):
        self.vector_store = vector_service.VectorService(
            embedding=DashScopeEmbeddings(
                dashscope_api_key=embedd_KEY,
                model=embedding_model,
            )
        )

        self.prompt_template = [
            ("system_prompt", "你是一个专业的问答机器人，请以参考信息为基础，回答用户的问题。参考信息：{context}"),
            ("system","历史记录如下："),
            MessagesPlaceholder("history"),
            ("human", "{question}")
        ]
        self.chat_model = ChatDeepSeek(
            model=chat_model,
            api_key=chat_KEY
        )

        self.chain = self.get_chain()

    def get_chain(self):
        retriever = self.vector_store.get_retriever()

        def printPrompt(prompt):
            print(prompt.to_string())
            print("="*60)
            return prompt

        def format_docs(docs:List[Document]):
            return "\n".join(doc.page_content for doc in docs)

        chain = (
            {
                "question": itemgetter("question"),
                "history": itemgetter("history"),
                "context": itemgetter("question") | retriever | RunnableLambda(format_docs),
            }
            | self.prompt_template
            | RunnableLambda(printPrompt)
            | self.chat_model
            | StrOutputParser()
        )

        return chain