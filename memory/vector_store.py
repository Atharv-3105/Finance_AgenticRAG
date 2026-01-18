import faiss
import numpy as np 
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        
    def add_documents(self, docs: list[str]):
        embeddings = self.model.encode(docs)
        self.index.add(np.array(embeddings).astype("float32"))
        self.documents.extend(docs)
    
    def search(self, query: str, top_k:int = 3)-> list[str]:
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"), top_k
        )
        
        return [self.documents[i] for i in indices[0]]