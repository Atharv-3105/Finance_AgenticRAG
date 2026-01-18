import requests
from utils.cache import get_cache, set_cache

SEARCH_URL = "https://query2.finance.yahoo.com/v1/finance/search"

HEADERS = {
    "User-Agent":"Mozilla/5.0",
    "Accept": "application/json"
}

POSITIVE_TTL = 86400 #24 Hours
NEGATIVE_TTL = 1800  #30 Minutes

def resolve_symbol(asset_name: str)->str | None:
    if not asset_name:
        return None
    
    normalized = asset_name.strip().lower()
    cache_key = f"symbol:{normalized}"
    
    #Cache-LookUp
    cached = get_cache(cache_key)
    if cached is not None:
        print("[CACHE HIT]", cache_key)
        return cached
    
    try:
       params = {
           "q":asset_name,
           "quotesCount":5,
           "newsCount":0
       }
       r = requests.get(SEARCH_URL, params=params, headers=HEADERS ,timeout=5)
       r.raise_for_status()
       
       data = r.json()
       quotes = data.get("quotes", [])
       
       if  not quotes:
           set_cache(cache_key, None, NEGATIVE_TTL)
           return None
       
       for q in quotes:
           if q.get("quoteType") in ("EQUITY", "ETF"):
               symbol =  q.get("symbol")
               if symbol:
                   set_cache(cache_key, symbol, POSITIVE_TTL)
                   return symbol
       
       symbol = quotes[0].get("symbol")
       set_cache(cache_key, symbol, POSITIVE_TTL)
       return symbol
   
    except Exception as e:
        print("Symbol Resolution Error: ", e)
        set_cache(cache_key, None, NEGATIVE_TTL)
        return None
    