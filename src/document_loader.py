from utils.logger import AppLogger1
from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import (
    PyPDFLoader, CSVLoader, TextLoader, JSONLoader, 
    Docx2txtLoader, UnstructuredEPubLoader,
    UnstructuredWordDocumentLoader
)
# from langchain.docstore.document import Document
from collections import defaultdict, Counter
import json

from config.settings import Settings

# class DocumentLoader:

#     """ Loader for different file types"""
#     SUPPORTED_EXTENSIONS = {
#         '.pdf': PyPDFLoader,
#         '.csv': CSVLoader,
#         '.txt': TextLoader,
#     }
    
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.logger = AppLogger1().get_logger()

#     def _get_loader_class(self, file_path: str) -> Any:
#             """Get appropriate loader for file extension."""
#             ext = Path(file_path).suffix.lower()
#             if ext in self.SUPPORTED_EXTENSIONS:
#                 return self.SUPPORTED_EXTENSIONS[ext]
#             raise ValueError(f"Unsupported file type: {ext}")

#     def load(self):
#         try:
#             self.logger.info(f"Loading document from {self.file_path}")

 

#             # # Define your loaders
#             # pdf_loader = DirectoryLoader(self.file_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
#             # csv_loader = DirectoryLoader(self.file_path, glob="**/*.csv", loader_cls=CSVLoader)
#             # txt_loader = DirectoryLoader(self.file_path, glob="**/*.txt", loader_cls=TextLoader)    
#             # # Combine them
#             # loaders = [pdf_loader, csv_loader, txt_loader]
#             # docs = []
#             # for loader in loaders:
#             #     docs.extend(loader.load())


            
#             # no_of_docs = set([doc.metadata['source'] for doc in docs])


#             loader = DirectoryLoader(
#                 self.file_path,
#                 glob="**/*", # All files recursively
#                 loader_cls=self.loader_cls
#             )

#             docs = loader.load()
#             no_of_docs = set([doc.metadata['source'] for doc in docs])

#             self.logger.info(f"Loaded {len(no_of_docs)} documents")
#             self.logger.info("Document loaded successfully")
#             return docs
       
#         except Exception as e:
#             raise self.logger.error(f"Error in loading document: {e}")




class UniversalDocumentLoader:
    """Universal loader for all common file types with smart metadata."""
    
    SUPPORTED_EXTENSIONS = {
        '.pdf': PyPDFLoader,
        '.csv': CSVLoader,
        '.txt': TextLoader,
        '.json': JSONLoader,
        '.jsonl': lambda path: JSONLoader(path, jq_schema=".[]", content_key="text"),
        '.docx': Docx2txtLoader,
        '.epub': UnstructuredEPubLoader,
        '.doc': UnstructuredWordDocumentLoader,
        '.md': TextLoader,
        '.rtf': TextLoader,
    }

    def __init__(self, loader_kwargs: Optional[Dict[str, Any]] = None):
        self.loader_kwargs = loader_kwargs or {}
        self.logger = AppLogger1().get_logger()

    def _get_loader_class(self, file_path: str) -> Any:
        """Get appropriate loader for file extension."""
        ext = Path(file_path).suffix.lower()
        if ext in self.SUPPORTED_EXTENSIONS:
            return self.SUPPORTED_EXTENSIONS[ext]
        raise ValueError(f"Unsupported file type: {ext}")
    
    def _enrich_metadata(self, docs: List[Document], file_path: str):
        """Add consistent metadata to all documents."""
        file_path_obj = Path(file_path)
        file_id = file_path_obj.stem
        file_type = file_path_obj.suffix.lower()
        
        for doc in docs:
            doc.metadata.update({
                'file_id': file_id,
                'file_name': file_path_obj.name,
                'file_type': file_type,
                'file_size': file_path_obj.stat().st_size,
                'file_dir': str(file_path_obj.parent)
            })

    def load_file(self, file_path: str) -> List[Document]:
        """Load single file with proper loader."""
        loader_class = self._get_loader_class(file_path)
        
        # Special handling for JSONL
        if Path(file_path).suffix.lower() == '.jsonl':
            loader = loader_class(file_path, **self.loader_kwargs)
        else:
            loader = loader_class(file_path, **self.loader_kwargs)
        
        docs = loader.load()
        self._enrich_metadata(docs, file_path)
        return docs
    

    def load_directory(self, directory_path: str, glob_pattern: str = "**/*") -> List[Document]:
        """Load all supported files from directory."""
        all_docs = []
        data_dir = Path(directory_path)
        self.logger.info(" Loading files from directory")
        for file_path in data_dir.glob(glob_pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    print(f"Loading {file_path.name}...")
                    docs = self.load_file(str(file_path))
                    all_docs.extend(docs)
                except Exception as e:
                    print(f"Failed {file_path.name}: {e}")
        
        return all_docs
    
    def analyze_load(self, docs: List[Document]) -> Dict[str, Any]:
        """Analyze loaded documents with stats."""
        file_stats = defaultdict(list)
        self.logger.info("Analyzing the loaded documents")
        for doc in docs:
            file_id = doc.metadata.get('file_id', 'unknown')
            file_type = doc.metadata.get('file_type', 'unknown')
            file_stats[file_type].append(doc)
        
        return {
            'total_docs': len(docs),
            'total_files': len(set(d.metadata['file_id'] for d in docs)),
            'file_types': dict(Counter(d.metadata['file_type'] for d in docs)),
            'avg_content_length': sum(len(d.page_content) for d in docs) / len(docs),
            'content_length_range': (min(len(d.page_content) for d in docs),
                                   max(len(d.page_content) for d in docs))
        }
    

