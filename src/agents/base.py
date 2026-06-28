from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """
    Abstract base class defining the contract and workflow lifecycle for all AI Agents.
    
    Every domain-specific agent (Problem Analysis, Research, etc.) must subclass
    BaseAgent and implement prompt construction and output parsing.
    """
    
    def __init__(self, name: str):
        """
        Initializes the base agent.

        Args:
            name: Human-readable name of the agent.
        """
        self.name = name

    @abstractmethod
    def build_system_prompt(self, *args, **kwargs) -> str:
        """
        Constructs the system instructions or behavior persona for the agent.
        """
        pass

    @abstractmethod
    def build_user_prompt(self, *args, **kwargs) -> str:
        """
        Constructs the user query or inputs context for the agent.
        """
        pass

    @abstractmethod
    def parse_response(self, response_text: str, *args, **kwargs) -> Any:
        """
        Parses and structures the raw LLM response text into a standard result model.
        """
        pass

    def run(self, inputs: Dict[str, Any], llm_service: Any, *args, **kwargs) -> Any:
        """
        Executes the template method lifecycle for the agent run.

        1. Build system instructions.
        2. Build user input context.
        3. Invoke the LLM service wrapper.
        4. Parse and structure the response.

        Args:
            inputs: Raw context, variables, or data files for the agent.
            llm_service: The LLMService wrapper to query the LLM.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments (e.g., json_mode).

        Returns:
            The structured/parsed result of the agent execution.
        """
        system_prompt = self.build_system_prompt(inputs, *args, **kwargs)
        user_prompt = self.build_user_prompt(inputs, *args, **kwargs)
        
        json_mode = kwargs.get("json_mode", False)
        
        response_text = llm_service.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            json_mode=json_mode
        )
        
        return self.parse_response(response_text, *args, **kwargs)
