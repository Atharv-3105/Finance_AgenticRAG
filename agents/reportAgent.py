from agents.baseAgent import BaseAgent
from agents.context import AgentContext
from utils.prompts import REPORT_AGENT_PROMPT
from utils.llm import call_llm
from utils.logger import AgentTimer
import json

class ReportAgent(BaseAgent):
    async def run(self, context: AgentContext)->AgentContext:
        with AgentTimer("ReportAgent"):
            report_input = {
                "intent":context.get("query_understanding", {}).get("intent"),
                "market_data": context.get("market_data"),
                "news_sentiment": context.get("news_sentiment"),
                "risk_analysis": context.get("risk_analysis"),
                "fact_check":context.get("fact_check")
            }
            
            prompt = REPORT_AGENT_PROMPT.format(data = json.dumps(report_input, indent=2))
            
            report_text = await call_llm(prompt, temperature=0.2)
            
            context["final_report"] = {
                "text":report_text.strip(),
                "confidence_note": report_input["fact_check"].get("confidence_adjustment"),
                "is_consistent": report_input["fact_check"].get("is_consistent")
            }
            return context