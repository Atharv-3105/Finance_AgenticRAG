from agents.baseAgent import BaseAgent
from agents.context import AgentContext
from utils.news import fetch_news
# from utils.sentiment import analyze_sentiment
from utils.logger import AgentTimer

POSITIVE_WORDS = ["growth", "strong", "record", "beat", "surge"]
NEGATIVE_WORDS = ["decline", "weak", "fall", "risk", "lawsuit"]

def score_sentiment(text: str) ->int:
    score = 0
    t = text.lower()
    for w in POSITIVE_WORDS:
        if w in t:
            score+=1
    for w in NEGATIVE_WORDS:
        if w in t:
            score -= 1
    
    return score

class NewsAgent(BaseAgent):
    async def run(self, context: AgentContext)->AgentContext:
        with AgentTimer("NewsAgent"):
            query_info = context.get("query_understanding", {})
            asset = query_info.get("asset")
            
            if not asset:
                context["news_sentiment"] = {}
                return context
            
            assets = asset if isinstance(asset, list)else [asset]
            
            sentiment_results = {}
            for a in assets:
                try:
                    articles = fetch_news(a)
                except Exception:
                    sentiment_results[a] = {
                        "overall_sentiment":"unknown",
                        "headlines": [],
                        "error":"News fetch failed"
                    }
                    continue
                
                if not articles:
                    sentiment_results[a] = {
                        "overall_sentiment":"neutral",
                        "headlines":[]
                    }
                    continue
            # articles = fetch_news(asset)
            
            # sentiments = []
            # headlines = []
                total_score = 0
                headlines = []
                
                for art in articles:
                    title = art.get("title", "")
                    desc = art.get("description", "")
                    combined = f"{title} {desc}"
                    total_score += score_sentiment(combined)
                    headlines.append(title)

                if total_score > 0:
                    overall = "positive"
                elif total_score < 0:
                    overall = "negative"
                else:
                    overall = "neutral"
                
                sentiment_results[a] = {
                    "overall_sentiment": overall,
                    "headlines": headlines[:5]
                }
            
            # for article in articles:
            #     title = article.get("title", "")
            #     description = article.get("description", "")
            #     combined_text = f"{title}. {description}"
                
            #     sentiment_result = analyze_sentiment(combined_text)
            #     sentiments.append(sentiment_result["polarity"])
            #     headlines.append({
            #         "title":title,
            #         "sentiment": sentiment_result["sentiment"]
            #     })
            
            # avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            
            # context["news_sentiment"] = {
            #     "average_polarity" : avg_sentiment,
            #     "overall_sentiment": (
            #         "positive" if avg_sentiment > 0.1 else "negaitve" if avg_sentiment < 0.1 else "neutral"
            #     ),
            #     "headlines": headlines
            # }
            context["news_sentiment"] = sentiment_results
            return context
            
        