from utils.logger import AppLogger1
from src.vectore_store import VectorStore

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.logger = AppLogger1().get_logger()

    def retrieve(self, query):
        self.logger.info("Retriever function called")
        docs = self.vector_store.document_search(query)
        return docs