"""
Coordinator Agent for managing multi-agent interactions.
"""

from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    """Agent for coordinating multiple specialized agents."""
    
    def __init__(
        self,
        llm,
        tools: List[Any],
        agents: Optional[List[BaseAgent]] = None
    ):
        """Initialize the Coordinator Agent."""
        super().__init__(llm, tools, "CoordinatorAgent")
        self.agents = agents or []
    
    def _create_executor(self) -> Any:
        """Create the agent executor for coordination tasks."""
        return MockCoordinatorExecutor(self.agents)
    
    def _format_output(self, result: Any) -> Dict[str, Any]:
        """Format the coordination results."""
        return {
            "status": "success",
            "agent": self.name,
            "workflow": result.get("workflow", []),
            "results": result.get("results", {}),
            "agents_used": result.get("agents_used", [])
        }
    
    def add_agent(self, agent: BaseAgent) -> None:
        """Add an agent to the coordination pool."""
        if agent not in self.agents:
            self.agents.append(agent)
    
    def remove_agent(self, agent: BaseAgent) -> None:
        """Remove an agent from the coordination pool."""
        if agent in self.agents:
            self.agents.remove(agent)


class MockCoordinatorExecutor:
    """Mock coordinator executor for development."""
    
    def __init__(self, agents: List[BaseAgent]):
        """Initialize with available agents."""
        self.agents = agents
    
    async def arun(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock coordination execution."""
        task = input_data.get("task", "")
        return {
            "workflow": [
                f"Step 1: Route task '{task}' to appropriate agents",
                "Step 2: Execute agent tasks in sequence",
                "Step 3: Aggregate results"
            ],
            "results": {
                "task_completed": True,
                "execution_time": "2.5s"
            },
            "agents_used": [agent.name for agent in self.agents]
        }
