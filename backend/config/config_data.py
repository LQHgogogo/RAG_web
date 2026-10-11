from os import getenv

embedd_KEY = getenv('BAILIAN_API_KEY')

embedding_model = 'text-embedding-v4'

chat_KEY = getenv('DEEPSEEK_API_KEY')

chat_model = 'deepseek-flash'

persist_dir = r'D:\code\PC\RAG_web\backend\data\chroma_db'

collection_name = 'rag_db'

chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "?","!",",",".","，","。"]

md5_path = r'D:\code\PC\RAG_web\backend\data\md5.txt'

max_split_char_num = 1000

history_message_path = 'D:/code/PC/RAG_web/backend/data/history'

system_prompt = """
你是一个专业的问答问答系统，你的任务是根据用户的问题，从数据库中检索相关知识，并回答用户的问题。
回答前请遵守以下规则：
1.严格根据参考信息回答用户的问题，若用户的问题超出参考信息的范围，回答“没有相关知识”，不要自己联想其他内容，但是不要对用户的正常问题也回答“没有相关知识”，例如“你好”、“你是谁”、“你好吗？”、“你能干什么”等问题。
2.不要和用户闲聊。
3.回答时，用语干净利落，强调重点。
"""