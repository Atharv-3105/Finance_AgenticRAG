def score_market_trend(signals: dict)-> int:
    trend =signals.get("trend")
    if trend == "bullish":
        return 2
    if trend == "bearish":
        return -2
    return 0

def score_sentiment(news_sentiment: dict)->int:
    sentiment = news_sentiment.get("overall_sentiment")
    if sentiment == "positive":
        return 1
    if sentiment == "negative":
        return -1
    return 0


def score_retrieval(docs: list[str])->int:
    if not docs:
        return 0
    positive_keywords = ["growth", "leading", "demand"]
    score = 0
    for doc in docs:
        if any(k in doc.lower() for k in positive_keywords):
            score += 1
    return min(score, 2)
