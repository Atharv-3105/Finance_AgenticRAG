#Agent which will Retrieve Asset Related Documents from Vector_Store

from agents.baseAgent import BaseAgent
from agents.context import AgentContext
# from memory.init_store import vector_store
from utils.vector_store import get_vector_store
from utils.embeddings import embed
from utils.logger import AgentTimer

vector_store = get_vector_store(dim=384)

class RetrievalAgent(BaseAgent):
    async def run(self, context: AgentContext)->AgentContext:
        with AgentTimer("RetrievalAgent"):
            query_info = context.get("query_understanding", {})
            asset = query_info.get("asset")
            intent = query_info.get("intent")
            
            if not asset or not intent:
                context["retrieval"] = []
                return context
            
            search_query = f"{asset} {intent}"
            query_embedding = embed(search_query)
            retrieved_docs = vector_store.search(query_embedding, k = 3)
            
            context["retrieval"] = retrieved_docs
            return context
       