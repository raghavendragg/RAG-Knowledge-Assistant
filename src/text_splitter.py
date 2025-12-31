from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.document_loader import UniversalDocumentLoader
from utils.logger import AppLogger1
# from config.settings import Settings

class TextSplitter:

    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.loader = UniversalDocumentLoader()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            add_start_index=True

        )
        self.logger = AppLogger1().get_logger()

    
    def split(self, raw_docs):

        # Load
        # self.loggger.info("Loading raw documents for text splitter")
        # raw_docs = self.loader.load_directory(directory_path)

        # Split
        self.logger.info("Splitting documents started")
        chunks = self.splitter.split_documents(raw_docs)

        # Filter tiny chunks
        good_chunks = [c for c in chunks if len(c.page_content.strip()) > 100]

        # Analyze
        stats = self.loader.analyze_load(good_chunks)
        stats['filtered_chunks'] = len(chunks) - len(good_chunks)

        self.logger.info(f"Chunking is complete: {len(good_chunks)} chunks from {stats['total_files']} files")

        return good_chunks

        
