import json 
from agents.baseAgent import BaseAgent
from agents.context import AgentContext
from utils.llm import call_llm
from utils.prompts import QUERY_AGENT_PROMPT
from utils.logger import AgentTimer


def infer_intent_from_txt(text: str):
    t = text.lower()
    
    if any(w in t for w in ["comparison", "vs", "difference"]):
        return "comparison"
    if any(w in t for w in ["invest", "buy", "hold"]):
        return "investment_analysis"
    return None

def clean_llm_response(raw: str)-> str:
        raw = raw.strip()
        
        if raw.startswith("```"):
            raw = raw.split("```")[1].strip()
        
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
        return raw
    
class QueryAgent(BaseAgent):
    async def run(self, context: AgentContext)->AgentContext:
        with AgentTimer("QueryAgent"):
            user_query = context.get("user_query")
            
            prompt = QUERY_AGENT_PROMPT.format(query = user_query)
            raw = await call_llm(prompt)
            raw = clean_llm_response(raw)
            
            print("RAW LLM OUTPUT:", repr(raw))
            
            parsed = {
                "intent":None,
                "asset": None,
                "time_horizon": None,
                "risk_profile": None,
                "confidence": "low"
            }
            
            try:
                llm_data = json.loads(raw)
                if isinstance(llm_data, dict):
                    parsed.update(llm_data)
            except Exception:
                pass
            
            #Normalize Empty strings
            if parsed.get("assest") == "":
                parsed["asset"] = None
            
            rule_intent = infer_intent_from_txt(user_query)
            
            if parsed["intent"] is None and rule_intent:
                parsed["intent"] = rule_intent
                parsed["confidence"] = "low"
            
            elif parsed["intent"] != rule_intent and rule_intent:
                parsed["confidence"] = "low"
            
            if parsed["intent"] and parsed["asset"] and parsed["time_horizon"]:
                parsed["confidence"] = "high"
            
            context["query_understanding"] = parsed        
            return context
            