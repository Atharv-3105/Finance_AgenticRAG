from memory.vector_store import VectorStore
from data.financial_docs import FINANCIAL_DOCS

vector_store = VectorStore()
vector_store.add_documents(FINANCIAL_DOCS)