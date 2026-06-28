from pydantic import BaseModel, Field
from typing import List

class ProblemAnalysisResult(BaseModel):
    """
    Structured model representing the output of the Problem Analysis Agent.
    Contains clean lists of problems, constraints, target audiences, assumptions,
    risks, and the raw text output.
    """
    extracted_problems: List[str] = Field(
        default_factory=list,
        description="List of key problems extracted from the input materials."
    )
    technical_constraints: List[str] = Field(
        default_factory=list,
        description="Technical limitations, constraints, or environment requirements."
    )
    target_audiences: List[str] = Field(
        default_factory=list,
        description="Primary and secondary target audiences or user personas."
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description="Key assumptions made during analysis."
    )
    risks: List[str] = Field(
        default_factory=list,
        description="Potential risks, trade-offs, or blockers identified."
    )
    raw_output: str = Field(
        ...,
        description="The raw text response from the language model."
    )
