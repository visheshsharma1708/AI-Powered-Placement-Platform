from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeAnalysisResponse(BaseModel):
    id: int
    resume_id: int
    raw_text: str
    skills: list
    education: list
    projects: list
    experience: list
    certifications: list
    achievements: list
    technologies: list
    parser_version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)