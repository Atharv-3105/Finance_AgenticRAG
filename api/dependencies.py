from agents.orchestrator import AgentOrchestrator
from agents.queryAgent import QueryAgent
from agents.retrievalAgent import RetrievalAgent
from agents.marketAgent import MarketAgent
from agents.newsAgent import NewsAgent
from agents.riskAgent import RiskAgent
from agents.factCheckerAgent import FactCheckerAgent
from agents.reportAgent import ReportAgent


orchestrator = AgentOrchestrator()

orchestrator.register_agents(QueryAgent("query"))
orchestrator.register_agents(RetrievalAgent("retrieval"))
orchestrator.register_agents(MarketAgent("market"))
orchestrator.register_agents(NewsAgent("news"))
orchestrator.register_agents(RiskAgent("risk"))
orchestrator.register_agents(FactCheckerAgent("fact_check"))
orchestrator.register_agents(ReportAgent("report"))

'''
    We create this for Single Orchestrator Instance
'''