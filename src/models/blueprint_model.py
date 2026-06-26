from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TechStackItem(BaseModel):
    category: str
    technology: str
    reason: str

class Milestone(BaseModel):
    title: str
    duration: str
    deliverables: List[str]

class ArchitectureModule(BaseModel):
    name: str
    description: str
    dependencies: List[str]

class BlueprintSchema(BaseModel):
    project_name: str
    one_liner: str
    target_audience: str
    problem_statement: str
    proposed_solution: str
    architecture: List[ArchitectureModule] = Field(default_factory=list)
    tech_stack: List[TechStackItem] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    risks_and_mitigations: Dict[str, str] = Field(default_factory=dict)
