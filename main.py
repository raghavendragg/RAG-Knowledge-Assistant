from utils.logger import AppLogger1 
from src.document_loader import UniversalDocumentLoader
from src.text_splitter import TextSplitter
from src.embeddings import EmbeddingModel
from src.vectore_store import VectorStore
from src.retriever import Retriever
from config.settings import Settings
from src.retriever import Retriever
from src.prompt_builder import PromptBuilder
from src.llm import LLMClient
from pipeline.rag_pipeline import RAGPipeline
import json

logger = AppLogger1().get_logger()

def main():
    logger.info("Starting RAG application")

    # Load document 
    logger.info("Loading raw documents")
    loader = UniversalDocumentLoader(loader_kwargs=None)
    raw_docs = loader.load_directory(Settings.DATA_PATH)
    stats = loader.analyze_load(raw_docs)
    print("📊 Load Summary:")
    print(json.dumps(stats, indent=2))
    logger.info(f"total_files: {stats['total_files']}")
    logger.info(f"file_types: {stats["file_types"]}")

    # Split text
    logger.info("Chunking raw documents")
    splitter = TextSplitter()
    chunks = splitter.split(raw_docs)

    # Embeddings
    logger.info("Embedding started")
    embedder = EmbeddingModel(model_name = "all-MiniLM-L6-v2")
    # embedder = EmbeddingModel()

    # embeddings = embedder.embed_documents([chunk.page_content for chunk in chunks])
    # embedder_info = embedder.get_model_info()
    logger.info(f"Embedding complete: {embedder.model_name}")

    # Vector Store
    logger.info("Vectore Store started")
    vector_store = VectorStore(chunks, embedder.load_model())
    # vector_store = vector_store.load_vectorstore()
    logger.info("Vectore store loaded")


    # Retriever Component
    retriever = Retriever(vector_store)
    prompt_builder = PromptBuilder()
    llm_client = LLMClient(model_name="qwen/qwen3-32b")

    # Pipeline  
    rag_pipeline = RAGPipeline(retriever, prompt_builder, llm_client)

    # Query
    answer = rag_pipeline.run("What are the recent news about GDP?")
    print("🧠 RAG Pipeline Response:")
    print(answer)

    # query = "What are the recent news about GDP?"
    # results = retriever.retrieve(query)
    # for i, doc in enumerate(results):
    #     print(f"{i}--> {doc.page_content}")

    # logger.info(f"Embedder info: {embedder_info}")
    logger.info("RAG application finished successfully")

if __name__ == "__main__":
    main()
