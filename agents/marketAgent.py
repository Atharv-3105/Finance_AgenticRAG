from agents.baseAgent import BaseAgent
from agents.context import AgentContext
from utils.market_data import fetch_market_data, compute_signals
from utils.symbol_resolver import resolve_symbol
from utils.logger import AgentTimer


class MarketAgent(BaseAgent):
    async def run(self, context: AgentContext)->AgentContext:
        with AgentTimer("MarketAgent"):
            query_info = context.get("query_understanding", {})
            asset = query_info.get("asset")
            
            if not asset:
                context["market_data"] = {}
                return context

            # symbol = SYMBOL_MAP.get(asset.upper())
            # if not symbol:
            #     context["market_data"] = {"error" : "Unknown asset symbol"}
            #     return context
            
            # df = fetch_market_data(symbol)
            # signals = compute_signals(df)
            
            # context["market_data"] = {
            #     "symbol" : symbol,
            #     "signals" : signals
            # }
            
            #Multiple Assets Approach 
            assets = asset if isinstance(asset, list) else [asset]
            
            market_results = {}
            
            for a in assets:
                symbol = resolve_symbol(a)
                
                if not symbol:
                    market_results[a] = {
                        "error": "Unable to resolve asset symbol"
                    }
                    continue
                
                df = fetch_market_data(symbol)
                signals = compute_signals(df)
                market_results[a] = {
                    "symbol":symbol,
                    "signals":signals
                }
            
            context["market_data"] = market_results
            return context
         