from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.schemas.job import JobPostingRead


RoleCategory = Literal[
    "backend",
    "frontend",
    "fullstack",
    "infra",
    "ai",
    "data",
    "qa",
    "security",
    "embedded",
    "mobile",
    "enterprise",
]


class UserProfileInput(BaseModel):
    skills: list[str] = Field(min_length=1, examples=[["Python", "Linux", "SQL"]])
    experience_years: int = Field(ge=0, le=50, examples=[1])
    japanese_level: Optional[Literal["N1", "N2", "N3"]] = None
    desired_role: Optional[RoleCategory] = None
    preferred_locations: Optional[list[str]] = Field(default=None, examples=[["东京", "大阪"]])
    expected_salary: Optional[int] = Field(default=None, ge=0, examples=[300000])
    project_summary: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("skills", "preferred_locations")
    @classmethod
    def remove_empty_values(cls, values: Optional[list[str]]) -> Optional[list[str]]:
        if values is None:
            return None
        cleaned = [value.strip() for value in values if value.strip()]
        if not cleaned:
            raise ValueError("列表中至少需要一个有效值")
        return cleaned


class ScoreBreakdown(BaseModel):
    required_skills: float
    preferred_skills: float
    experience: float
    japanese: float
    role: float
    location: float
    salary: float


class RecommendationItem(BaseModel):
    job: JobPostingRead
    match_score: float
    score_breakdown: ScoreBreakdown
    reasons: list[str]
    missing_skills: list[str]
    next_steps: list[str]


class RecommendationResponse(BaseModel):
    total_jobs_evaluated: int
    recommendations: list[RecommendationItem]
