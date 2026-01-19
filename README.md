---
title: Financial Agentic RAG
emoji: 💹
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Financial Agentic RAG System

A multi-agent financial reasoning system that combines:
- LLM-based query understanding
- Retrieval-Augmented Generation (RAG)
- Market data and news analysis
- Risk-aware reasoning
- Structured report generation

## API Usage

Visit `/docs` to access the FastAPI Swagger UI.

Example query:
```json
POST /api/query
{
  "query": "Compare NVIDIA and AMD for 3 months"
}
