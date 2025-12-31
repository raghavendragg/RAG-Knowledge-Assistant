from utils.logger import AppLogger1 
from langchain_community.vectorstores import FAISS

class VectorStore:

    def __init__(self, chunks, embedding_model):
        self.chunks = chunks
        self.embedding_model = embedding_model
    
        self.logger = AppLogger1().get_logger()

    def load_vectorstore(self):
        vectorstore = FAISS.from_documents(self.chunks, self.embedding_model)
        self.logger.info("Vectorstore created")
        return vectorstore
    
    def document_search(self, query):
        vectorstore = self.load_vectorstore()
        if vectorstore is None:
            raise ValueError("No vector store found. Create one first")
        
        docs = vectorstore.similarity_search(query)

        return docs





    

    