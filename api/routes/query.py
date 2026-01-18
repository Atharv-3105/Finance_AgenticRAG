from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.dependencies import orchestrator
from api.rate_limiter import rate_limiter


router = APIRouter()

class QueryRequest(BaseModel):
    query: str
 
@router.post("/analyze", dependencies=[Depends(rate_limiter)])   
async def analyze_query(request: QueryRequest):
    result = await orchestrator.run({
        "user_query": request.query
    })
    
    return{
        "status": "success",
        "data": result
    }