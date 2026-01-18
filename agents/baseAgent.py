from abc import ABC, abstractmethod
from agents.context import AgentContext


class BaseAgent(ABC):
    def __init__(self, name:str):
        self.name = name
    
    @abstractmethod
    async def run(self, context:AgentContext)->AgentContext:
        pass