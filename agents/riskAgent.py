from agents.baseAgent import BaseAgent
from agents.context import AgentContext
from agents.risk_rules import (
    score_market_trend, score_retrieval, score_sentiment
)
from utils.logger import AgentTimer

class RiskAgent(BaseAgent):
    async def run(self, context: AgentContext)->AgentContext:
        with AgentTimer("RiskAgent"):
            market_data = context.get("market_data", {})
            news_sentiment = context.get("news_sentiment", {})
            intent = context.get("query_understanding", {}).get("intent")
            retrieval_docs = context.get("retrieval", [])
            
            per_asset = {}
            
            for asset, mdata in market_data.items():
                signals = mdata.get("signals", {})
                sentiment = news_sentiment.get(asset, {})
                
                market_score = score_market_trend(signals)
                sentiment_score = score_sentiment(sentiment)
                total = market_score + sentiment_score
                
                if total >= 2:
                    outlook = "bullish"
                    confidence = "high"
                elif total <= -2:
                    outlook = "bearish"
                    confidence = "high"
                else:
                    outlook = "neutral"
                    confidence = "medium"
                
                risks = []
                if market_score < 0:
                    risks.append("Negative market trend")
                if sentiment_score < 0:
                    risks.append("Negative sentiment")
                if not sentiment:
                    risks.append("No recent news data")
                
                per_asset[asset] = {
                    "market_score":market_score,
                    "sentiment_score":sentiment_score,
                    "total_score":total,
                    "outlook":outlook,
                    "confidence":confidence,
                    "risks":risks
                }
            
            comparison = None
            if intent == "comparison" and len(per_asset) >= 2:
                sorted_asset = sorted(
                    per_asset.items(),
                    key = lambda x : x[1]["total_score"],
                    reverse = True
                )
                best, worst = sorted_asset[0], sorted_asset[-1]
                
                comparison = {
                    "stronger_asset": best[0],
                    "weaker_asset": worst[0],
                    "reason":"Relative strength based on combined market sentiment score"
                }
                
            context["risk_analysis"] = {
                "per_asset": per_asset,
                "comparison":comparison
            }
            
            return context
                
                    
            # market_score = score_market_trend(market_data)
            # sentiment_score = score_sentiment(news_sentiment)
            # retrieval_score = score_retrieval(retrieval_docs)
            
            # total_score = market_score + sentiment_score + retrieval_score
            
            # if total_score >= 3:
            #     overall = "bullish"
            #     confidence = "high"
            # elif total_score >= 1:
            #     overall = "slightly_bullish"
            #     confidence = "medium"
            # elif total_score <= -2:
            #     overall = "bearish"
            #     confidence = "high"
            # else:
            #     overall = "neutral"
            #     confidence = "low"
            
            # risks = []
            # if market_score < 0:
            #     risks.append("Negative Market Trend")
            # if sentiment_score < 0:
            #     risks.append("Negative news sentiment")
            # if retrieval_score == 0:
            #     risks.append("Weak Evidence")
            
            # context["risk_analysis"] = {
            #     "market_score": market_score,
            #     "sentiment_score":sentiment_score,
            #     "retrieval_score":retrieval_score,
            #     "total_score": total_score,
            #     "overall_signal":overall,
            #     "confidence": confidence,
            #     "key_risks": risks
            # }
            
            # return context