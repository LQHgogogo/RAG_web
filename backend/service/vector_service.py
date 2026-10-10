from langchain_chroma import Chroma
from config_data import persist_dir, collection_name


class VectorService:
    def __init__(self,embedding):
        self.embedding = embedding

        self.chroma = Chroma(
            persist_directory=persist_dir,
            collection_name=collection_name,
            embedding_function=self.embedding,
        )

    def get_retriever(self):
        return self.chroma.as_retriever(search_type="similarity", search_kwargs={"k": 3})
