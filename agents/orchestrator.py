from agents.context import AgentContext

class AgentOrchestrator:
    def __init__(self):
        self.pipeline = []
        
    def register_agents(self, agent):
        self.pipeline.append(agent)
    
    async def run(self, initital_input: dict) -> dict:
        
        context = AgentContext()
        context.update(initital_input)
        
        for agent in self.pipeline:
            context = await agent.run(context)
        
        return context