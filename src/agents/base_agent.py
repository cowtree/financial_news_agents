from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main task.
        
        Args:
            input_data: Dictionary containing input data for the agent
            
        Returns:
            Dictionary containing the agent's output
        """
        pass
    
    def __str__(self) -> str:
        return f"{self.name} Agent" 