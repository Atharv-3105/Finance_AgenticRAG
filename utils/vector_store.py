import os 
import faiss
import pickle 

DATA_DIR = "data"
INDEX_PATH = os.path.join(DATA_DIR, "vector.index")
META_PATH = os.path.join(DATA_DIR, "vector_meta.pkl")

os.makedirs(DATA_DIR, exist_ok=True)

_vector_store = None

def get_vector_store(dim: int = 384):
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore(dim)
    return _vector_store

class VectorStore:
    def __init__(self, dim:int):
        self.dim = dim
        self.index = None 
        self.metadata = []
        
        self._load_or_create()
    
    def _load_or_create(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(META_PATH, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.metadata = []
        
    def add(self, embeddings, docs):
        if len(embeddings) != len(docs):
            raise ValueError(
                f"Embedding count: ({len(embeddings)}) "
                f"!= doc count: ({len(docs)})"
            )
            
        self.index.add(embeddings)
        self.metadata.extend(docs)
        self._persist()
        
        if self.index.ntotal != len(self.metadata):
            raise RuntimeError(
                f"FAISS Index ({self.index.ntotal}) "
                f"!= metadata: ({len(self.metadata)})"
            )
    
    def search(self, query_embedding, k = 5):
        if self.index.ntotal == 0:
            return []
        
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        return results
    
    def _persist(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)