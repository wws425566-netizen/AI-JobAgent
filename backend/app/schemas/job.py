from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class JobPostingRead(BaseModel):
    id: int
    title: str
    role_category: str
    company_name: str
    company_type: str
    location: str
    industry: str
    required_skills: list[str]
    preferred_skills: Optional[list[str]] = None
    japanese_level: Optional[str] = None
    experience_requirement: str
    initial_salary: int
    job_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
