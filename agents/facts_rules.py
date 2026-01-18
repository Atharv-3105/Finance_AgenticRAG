def detect_contradictions(risk_analysis, market_data, news_sentiment):
    contradictions = []
    
    overall = risk_analysis.get("overall_signal")
    market_trend = market_data.get("signals", {}).get("trend")
    news = news_sentiment.get("overall_sentiment")
    
    if overall == "bullish" and market_trend == "bearish":
        contradictions.append("Overall signal is bullish but market trend is bearish")
    
    if overall == "bullish" and news == "negative":
        contradictions.append("Overall signal is bullish but news sentiment is negative")
    
    if overall == "bearish" and news == "positive":
        contradictions.append("Overall signal is bearish but news sentiment is positive")
    
    return contradictions