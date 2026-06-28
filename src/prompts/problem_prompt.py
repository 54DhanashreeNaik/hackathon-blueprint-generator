"""
Prompt engineering module for the Problem Understanding Agent.
Provides structured system and user prompts to extract JSON data from hackathon briefs.
"""

def build_problem_system_prompt() -> str:
    """
    Constructs the system prompt instructing the model to behave as a senior
    Business Analyst, Solution Architect, Technical Consultant, and Hackathon Mentor.
    Enforces a strict JSON response format without markdown formatting or code fences.

    Returns:
        str: System prompt text.
    """
    return (
        "You are an expert Business Analyst, Solution Architect, Technical Consultant, and Hackathon Mentor.\n"
        "Your task is to perform a rigorous analysis of the provided hackathon document.\n\n"
        "INSTRUCTIONS FOR ANALYSIS:\n"
        "1. Extract the core problems, technical constraints, target audiences, assumptions, and risks.\n"
        "2. Only use facts explicitly mentioned or logically implied by the text. Never hallucinate or invent details.\n"
        "3. If a field cannot be derived from the document, leave the corresponding list empty.\n\n"
        "OUTPUT FORMAT REQUIREMENTS:\n"
        "- You must output a single, raw, valid JSON object matching the schema below.\n"
        "- Never wrap the JSON in markdown code blocks or code fences (e.g., do NOT use ```json or ```).\n"
        "- Never include introductory text, explanations, or notes before or after the JSON.\n"
        "- The response must contain only the raw JSON string starting with '{' and ending with '}'.\n\n"
        "REQUIRED JSON SCHEMA:\n"
        "{\n"
        "  \"extracted_problems\": [\n"
        "    \"Specific challenges, pain points, core objectives, or existing issues explicitly mentioned.\"\n"
        "  ],\n"
        "  \"technical_constraints\": [\n"
        "    \"Explicit technology requirements, programming language limits, cloud specifications, AI tools, hardware rules, or software requirements.\"\n"
        "  ],\n"
        "  \"target_audiences\": [\n"
        "    \"Primary end users, organizations, or beneficiaries of the solution.\"\n"
        "  ],\n"
        "  \"assumptions\": [\n"
        "    \"Implicit assumptions, environmental context, or resource limitations implied by the document.\"\n"
        "  ],\n"
        "  \"risks\": [\n"
        "    \"Technical risks, business risks, operational blockers, or missing crucial information that introduces project risk.\"\n"
        "  ]\n"
        "}"
    )

def build_problem_user_prompt(document_text: str) -> str:
    """
    Constructs the user prompt containing the delimited hackathon document text
    and reinforcing the strict output format instructions.

    Args:
        document_text: The extracted clean text content of the uploaded document.

    Returns:
        str: User prompt text.
    """
    return (
        "Analyze the following document and return the extracted details in the requested JSON structure.\n\n"
        "Uploaded Document\n"
        "------------------\n"
        f"{document_text}\n"
        "------------------\n\n"
        "Return strictly valid JSON only. Do not include markdown formatting, markdown code fences, or any explanation."
    )
