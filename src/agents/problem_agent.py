from typing import Any, Dict
from src.agents.base import BaseAgent
from src.prompts.problem_prompt import PROBLEM_UNDERSTANDING_SYSTEM_PROMPT

class ProblemUnderstandingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Problem Understanding Agent")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder simulation of agent's execution
        uploaded_files = inputs.get("uploaded_files", [])
        files_summary = ", ".join([f.name for f in uploaded_files]) if uploaded_files else "No files uploaded"
        
        return {
            "status": "success",
            "extracted_problems": [
                "Address the core problem outlined in: " + files_summary,
                "Integrate user workflow expectations.",
                "Ensure scalability and microservices boundary mapping."
            ],
            "technical_constraints": [
                "Supported format compliance.",
                "Environment variable dependencies (dotenv).",
                "UI navigation integrity."
            ],
            "target_audiences": [
                "Hackathon developers looking for rapid scaffolds.",
                "Evaluators searching for clean structural blueprints."
            ],
            "raw_output": "System Prompt configured: " + PROBLEM_UNDERSTANDING_SYSTEM_PROMPT[:50] + "..."
        }
