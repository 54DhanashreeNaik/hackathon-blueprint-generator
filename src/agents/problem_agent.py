import streamlit as st
from typing import Any, Dict, List
import json
import logging

from src.agents.base import BaseAgent
from src.models.agent_models import ProblemAnalysisResult
from src.prompts.problem_prompt import build_problem_system_prompt, build_problem_user_prompt
from src.services.file_processing_service import FileProcessingService
from src.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class ProblemUnderstandingAgent(BaseAgent):
    """Agent that extracts problem analysis from uploaded documents.

    It uses :class:`FileProcessingService` to extract clean text from supported files,
    builds prompts via :mod:`src.prompts.problem_prompt`, and queries the LLM via
    :class:`LLMService`. The LLM response is parsed into a
    :class:`ProblemAnalysisResult` model.
    """

    def __init__(self) -> None:
        super().__init__("Problem Understanding Agent")
        self.file_service = FileProcessingService()
        self.llm_service = LLMService()

    def build_system_prompt(self) -> str:
        """Return the system prompt for the problem analysis."""
        return build_problem_system_prompt()

    def build_user_prompt(self, document_text: str) -> str:
        """Return the user prompt containing the combined document text."""
        return build_problem_user_prompt(document_text)

    def parse_response(self, response) -> ProblemAnalysisResult:
        """Parse LLM response into a ProblemAnalysisResult.

        Accepts a dict or JSON string.
        """
        if isinstance(response, str):
            try:
                data = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error("Failed to decode LLM JSON response: %s", e)
                data = {}
        elif isinstance(response, dict):
            data = response
        else:
            logger.error("Unexpected response type: %s", type(response))
            data = {}

        raw_output = response if isinstance(response, str) else json.dumps(response)

        return ProblemAnalysisResult(
            extracted_problems=data.get("extracted_problems", []),
            technical_constraints=data.get("technical_constraints", []),
            target_audiences=data.get("target_audiences", []),
            assumptions=data.get("assumptions", []),
            risks=data.get("risks", []),
            raw_output=raw_output,
        )

    def _extract_documents(self, uploaded_files: List[Any]) -> List[str]:
        """
        Extract clean text from uploaded files.

        The Home page stores UploadedFileMetadata objects in AppState,
        so we reopen the saved files from disk using local_path.
        """

        texts: List[str] = []

        for file_meta in uploaded_files:
            try:
                logger.info(f"Processing {file_meta.local_path}")

                result = self.file_service.process_file(
                    file_source=file_meta.local_path
                )

                if result.clean_text.strip():
                    texts.append(result.clean_text)

            except Exception as e:
                logger.warning(
                    "Failed to process %s: %s",
                    file_meta.name,
                    e,
                )

        return texts

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent workflow.

        Expected ``inputs`` structure:
            {"uploaded_files": List[UploadedFile]}

        Returns a dictionary produced by ``ProblemAnalysisResult.model_dump()``.
        """
        uploaded_files = inputs.get("uploaded_files", [])
        if not uploaded_files:
            empty_result = ProblemAnalysisResult(
                extracted_problems=[],
                technical_constraints=[],
                target_audiences=[],
                assumptions=[],
                risks=[],
                raw_output="",
            )
            return empty_result.model_dump()

        document_texts = self._extract_documents(uploaded_files)
        combined_text = "\n\n".join(document_texts)

        system_prompt = self.build_system_prompt()
        user_prompt = self.build_user_prompt(combined_text)

        llm_response = self.llm_service.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            json_mode=True,
        )

        result = self.parse_response(llm_response)
        return result.model_dump()
