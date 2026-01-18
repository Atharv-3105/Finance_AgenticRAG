from newsapi import NewsApiClient
import os 
from utils.cache import get_cache, set_cache

POSITIVE_TTL = 1800 #30 minutes
NEGATIVE_TTL = 300  #5 minutes

def fetch_news(query: str, page_size: int = 5):
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        raise RuntimeError("NEWS_API_KEY not found.")
    
    client = NewsApiClient(api_key=api_key)
    response = client.get_everything(
        q = query,
        language="en",
        sort_by="relevancy",
        page_size=page_size
    )
    
    return response.get("articles", [])