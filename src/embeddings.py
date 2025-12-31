from typing import List, Any
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import OllamaEmbeddings


# class EmbeddingModel:
    
#     def __init__(self,model_name):
#         self.model_name = model_name
#         self.model = SentenceTransformer(model_name)

#     def embed_documents(self, texts):

#         embeddings = self.model.encode(
#             texts,
#             batch_size=32,
#             normalize_embeddings=True,
#             show_progress_bar=True,
#             convert_to_numpy=True
#         )
#         return embeddings
    
#     def embed_query(self, text):
#         embedding = self.model.encode(
#             [text],
#             normalize_embeddings=True,
#             convert_to_numpy=True
#         )
#         return embedding[0].tolist()
    
#     @property
#     def embed_dim(self):
#         return self.model.get_sentence_embedding_dimension()
    
#     def get_model_info(self):
#         return {
#             "model_name": self.model_name,
#             "embed_dim": self.embed_dim
#         }

class EmbeddingModel:

    def __init__(self, model_name):
        self.model_name = model_name

    def load_model(self):
        # Use single-process mode to avoid multiprocessing "spawn" pickling issues
        # when running under Streamlit or other spawn-based environments.
        embedding_model = HuggingFaceEmbeddings(
            model_name=self.model_name,
            multi_process=False,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
        )
        return embedding_model
    
# class EmbeddingModel:

#     def __init__(self, model_name):
#         self.model_name = model_name

#     def load_model(self):
#         embedding_model = HuggingFaceEmbeddings(
#             model_name=self.model_name,
#             multi_process=True,
#             model_kwargs={"device": "cpu"},
#             encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
#         )
#         return embedding_model