from fastapi import FastAPI
from api.routes.query import router as query_router
from dotenv import load_dotenv
import os
load_dotenv()
print("NEWS_API_KEY loaded:", bool(os.getenv("NEWS_API_KEY")))

app = FastAPI(
    title="Fin_AgenticRAG",
    description="Financial Multi-Agent RAG System",
    version="1.0.0", 
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(query_router, prefix = "/api")

@app.get("/")
def health_check():
    return {
        "status":"ok",
        "service": "Financial Agentic RAG"}