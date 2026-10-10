from os import getenv

embedd_KEY = getenv('BAILIAN_API_KEY')

embedding_model = 'text-embedding-v4'

chat_KEY = getenv('DEEPSEEK_API_KEY')

chat_model = 'deepseek-v4.1-flash'

persist_dir = 'D:\code\PC\RAG_web\backend\data\chroma_db'

collection_name = 'rag_db'

chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "?","!",",",".","，","。"]

md5_path = 'D:\code\PC\RAG_web\backend\data\md5.txt'

max_split_char_num = 1000

history_message_path = 'D:\code\PC\RAG_web\backend\data\history\\'
