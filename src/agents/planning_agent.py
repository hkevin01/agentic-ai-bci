"""
Planning Agent for experiment design and protocol generation.
"""

from typing import Any, Dict, List

from .base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    """Agent specialized in experiment planning and design."""
    
    def __init__(self, llm, tools: List[Any]):
        """Initialize the Planning Agent."""
        super().__init__(llm, tools, "PlanningAgent")
    
    def _create_executor(self) -> Any:
        """Create the agent executor for planning tasks."""
        return MockPlanningExecutor()
    
    def _format_output(self, result: Any) -> Dict[str, Any]:
        """Format the planning results."""
        return {
            "status": "success",
            "agent": self.name,
            "experiment_plan": result.get("experiment_plan", {}),
            "timeline": result.get("timeline", {}),
            "budget_estimate": result.get("budget_estimate", {})
        }


class MockPlanningExecutor:
    """Mock planning executor for development."""
    
    async def arun(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock planning execution."""
        return {
            "experiment_plan": {
                "title": "Mock BCI Study",
                "participants": 20,
                "sessions": 10,
                "duration": "8 weeks"
            },
            "timeline": {
                "recruitment": "2 weeks",
                "data_collection": "8 weeks",
                "analysis": "4 weeks"
            },
            "budget_estimate": {
                "total": "$10,000",
                "personnel": "$6,000",
                "equipment": "$4,000"
            }
        }
