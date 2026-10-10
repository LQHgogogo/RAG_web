import datetime
import os
import hashlib

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.service import config_data

def save_md5(text: str):
    with open(config_data.md5_path, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

def check_md5(text: str):
    if(os.path.exists(config_data.md5_path)):
        for line in open(config_data.md5_path, 'r').readlines():
            if(line.strip() == text):
                return True
            else:
                return False
    else:
        open(config_data.md5_path, 'w', encoding='utf-8').close()
        return False

def get_str_into_md5(text: str):
    str_bytes = text.encode('utf-8')
    md5 = hashlib.md5(str_bytes)
    md5_hex = md5.hexdigest()
    return md5_hex

class KnowledgeBase:
    def __init__(self):
        os.makedirs(config_data.persist_dir, exist_ok=True)

        self.chroma = Chroma(
            persist_directory=config_data.persist_dir,
            embedding_function=DashScopeEmbeddings(
                dashscope_api_key=config_data.embedd_KEY,
                model=config_data.embedding_model,
            ),
            collection_name=config_data.collection_name,
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config_data.chunk_size,
            chunk_overlap=config_data.chunk_overlap,
            separators=config_data.separators,
            length_function=len
        )

    def add_knowledge(self, knowledge: str, filename: str):
        md5_hex=get_str_into_md5(knowledge)
        if check_md5(md5_hex):
            return '已添加过该知识库'

        if len(knowledge) > config_data.max_split_char_num:
            knowledge_chunks = self.splitter.split_text(knowledge)
        else:
            knowledge_chunks = [knowledge]

        metadata = {
            'source':filename,
            'creatTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata] * len(knowledge_chunks),
        )

        save_md5(md5_hex)
        return '添加成功'
