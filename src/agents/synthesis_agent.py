from typing import Any, Dict
from src.agents.base import BaseAgent
from src.prompts.synthesis_prompt import SYNTHESIS_SYSTEM_PROMPT

class SynthesisAgent(BaseAgent):
    def __init__(self):
        super().__init__("Evidence Synthesis Agent")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success",
            "evidence_sources": [
                {
                    "title": "Streamlit Documentation - st.navigation",
                    "category": "Official Docs",
                    "confidence_score": 0.98,
                    "relevance": "Direct solution for handling clean modular page routers in Streamlit applications."
                },
                {
                    "title": "Pydantic V2 State Management Guides",
                    "category": "Reference Library",
                    "confidence_score": 0.92,
                    "relevance": "Provides robust type-safety schemas for session states to avoid widget side effects."
                }
            ],
            "raw_output": "System Prompt configured: " + SYNTHESIS_SYSTEM_PROMPT[:50] + "..."
        }
