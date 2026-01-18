from agents.baseAgent import BaseAgent
from agents.context import AgentContext
from agents.facts_rules import detect_contradictions
from utils.logger import AgentTimer

class FactCheckerAgent(BaseAgent):
    async def run(self, context: AgentContext)->AgentContext:
        with AgentTimer("FactCheckerAgent"):
        
            risk_analysis = context.get("risk_analysis", {})
            market_data = context.get("market_data", {})
            news_sentiment = context.get("news_sentiment", {})
            retrieval_docs = context.get("retrieval", {})
            
            contradictions = detect_contradictions(risk_analysis, market_data, news_sentiment)
            
            warnings = []
            
            if not retrieval_docs:
                warnings.append("No supporting documents found")
            
            #Adjust confidence based on the contradictions
            confidence_adjustment = "none"
            if contradictions:
                confidence_adjustment = "decrease"
            
            context["fact_check"] = {
                "is_consistent": len(contradictions) == 0,
                "contradictions": contradictions,
                "confidence_adjustment":confidence_adjustment,
                "warnings": warnings
            }
            
            return context