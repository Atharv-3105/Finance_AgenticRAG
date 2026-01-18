import yfinance as yf 
import pandas as pd 
from utils.cache import get_cache,set_cache

POSITIVE_TTL = 600
NEGATIVE_TTL = 120

def fetch_market_data(symbol: str, period: str = "6mo") ->pd.DataFrame:
    if not symbol:
        return None
    
    #Normalize Cache Key
    cache_key = f"market:{symbol.upper()}:{period}"
    
    #Cache Look-Up
    cached = get_cache(cache_key)
    if cached is not None:
        print("[MARKET CACHE_HIT]", cache_key)
        return cached
    
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period = period)
        
        if df is None or df.empty:
            set_cache(cache_key, None, NEGATIVE_TTL)
            return None

        set_cache(cache_key, df, POSITIVE_TTL)
        return df

    except Exception as e:
        print("Market Data error:", e)
        set_cache(cache_key, None, NEGATIVE_TTL)
        return None
    
    
    
    # ticker = yf.Ticker(symbol)
    # df = ticker.history(period = period)
    # return df


def compute_signals(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {}
    
    close = df["Close"]
    
    return {
        "current_price" : float(close.iloc[-1]),
        "mean_price" : float(close.mean()),
        "volatility": float(close.std()),
        "trend": "bullish" if close.iloc[-1] > close.mean() else "bearish"
    }