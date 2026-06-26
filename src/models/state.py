from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class UploadedFileMetadata(BaseModel):
    name: str
    size_bytes: int
    content_type: str
    local_path: str

class AppState(BaseModel):
    uploaded_files: List[UploadedFileMetadata] = Field(default_factory=list)
    problem_analysis_results: Optional[Dict[str, Any]] = None
    research_results: Optional[List[Dict[str, Any]]] = None
    evidence_items: Optional[List[Dict[str, Any]]] = None
    intelligence_insights: Optional[Dict[str, Any]] = None
    generated_blueprint: Optional[Dict[str, Any]] = None
