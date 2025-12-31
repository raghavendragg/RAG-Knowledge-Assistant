from utils.logger import AppLogger1
from config.settings import Settings
from src.document_loader import UniversalDocumentLoader
from src.text_splitter import TextSplitter
from src.retriever import Retriever
from src.prompt_builder import PromptBuilder
from src.llm import LLMClient

class RAGPipeline:
    def __init__(self, retriever:Retriever, prompt_builder:PromptBuilder, llm:LLMClient):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm  
        self.logger = AppLogger1().get_logger()

    def run(self, query: str) -> str:
        self.logger.info("RAG Pipeline started")
        contexts = self.retriever.retrieve(query)
        prompt = self.prompt_builder.build_prompt(query, contexts)
        return self.llm.generate(prompt)