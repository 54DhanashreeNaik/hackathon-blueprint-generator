from typing import Any, Dict
from src.agents.base import BaseAgent
from src.prompts.research_prompt import RESEARCH_SYSTEM_PROMPT

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("Research Agent")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success",
            "search_queries": [
                "Streamlit multipage modern templates",
                "Pydantic state schemas in Streamlit session state",
                "Automated software architecture layout generators"
            ],
            "recommended_apis": [
                {"name": "Gemini API", "use_case": "Orchestrating agent workflows and writing documents"},
                {"name": "Tavily Search API", "use_case": "Finding up-to-date repository formats and tutorials"}
            ],
            "raw_output": "System Prompt configured: " + RESEARCH_SYSTEM_PROMPT[:50] + "..."
        }
