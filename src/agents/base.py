from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """Abstract base class for all AI Agents."""
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the agent logic."""
        pass
