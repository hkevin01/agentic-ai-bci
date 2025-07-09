"""
Base agent class for all BCI research agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAgent(ABC):
    """Base class for all research agents."""
    
    def __init__(self, llm, tools: List[Any], name: Optional[str] = None):
        """Initialize the base agent.
        
        Args:
            llm: Language model instance
            tools: List of tools available to the agent
            name: Optional name for the agent
        """
        self.llm = llm
        self.tools = tools
        self.name = name or self.__class__.__name__
        self.executor = self._create_executor()
    
    @abstractmethod
    def _create_executor(self) -> Any:
        """Create the agent executor.
        
        Returns:
            Configured executor instance
        """
        raise NotImplementedError
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with input data.
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Formatted results from the agent execution
        """
        try:
            result = await self.executor.arun(input_data)
            return self._format_output(result)
        except Exception as e:
            return {
                "error": str(e),
                "agent": self.name,
                "status": "failed"
            }
    
    @abstractmethod
    def _format_output(self, result: Any) -> Dict[str, Any]:
        """Format the agent output.
        
        Args:
            result: Raw result from agent execution
            
        Returns:
            Formatted output dictionary
        """
        raise NotImplementedError
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities.
        
        Returns:
            List of capability descriptions
        """
        return [getattr(tool, 'name', str(tool)) for tool in self.tools]
