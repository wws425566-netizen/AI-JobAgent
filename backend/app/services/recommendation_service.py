from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.job_posting import JobPosting
from app.schemas.recommendation import (
    RecommendationItem,
    RecommendationResponse,
    ScoreBreakdown,
    UserProfileInput,
)
from app.services.job_service import list_jobs


SCORE_WEIGHTS = {
    "required_skills": 35.0,
    "preferred_skills": 10.0,
    "experience": 15.0,
    "japanese": 15.0,
    "role": 10.0,
    "location": 10.0,
    "salary": 5.0,
}

JAPANESE_RANK = {"N3": 1, "N2": 2, "N1": 3}
EXPERIENCE_YEARS = {"新卒": 0, "1年以上": 1, "3年以上": 3}


@dataclass
class EvaluationDetails:
    breakdown: ScoreBreakdown
    reasons: list[str]
    missing_skills: list[str]
    next_steps: list[str]


def normalize(value: str) -> str:
    return value.strip().casefold()


def overlap(user_skills: set[str], job_skills: list[str] | None) -> list[str]:
    if not job_skills:
        return []
    return [skill for skill in job_skills if normalize(skill) in user_skills]


def ratio_score(matched_count: int, total_count: int, weight: float) -> float:
    if total_count == 0:
        return weight
    return weight * matched_count / total_count


def evaluate_job(profile: UserProfileInput, job: JobPosting) -> EvaluationDetails:
    user_skills = {normalize(skill) for skill in profile.skills}
    matched_required = overlap(user_skills, job.required_skills)
    matched_preferred = overlap(user_skills, job.preferred_skills)
    missing_skills = [
        skill for skill in job.required_skills if normalize(skill) not in user_skills
    ]

    required_score = ratio_score(
        len(matched_required), len(job.required_skills), SCORE_WEIGHTS["required_skills"]
    )
    preferred_score = ratio_score(
        len(matched_preferred),
        len(job.preferred_skills or []),
        SCORE_WEIGHTS["preferred_skills"],
    )

    required_years = EXPERIENCE_YEARS.get(job.experience_requirement, 0)
    if required_years == 0 or profile.experience_years >= required_years:
        experience_score = SCORE_WEIGHTS["experience"]
    else:
        experience_score = SCORE_WEIGHTS["experience"] * profile.experience_years / required_years

    if job.japanese_level is None:
        japanese_score = SCORE_WEIGHTS["japanese"]
    elif profile.japanese_level is None:
        japanese_score = 0.0
    elif JAPANESE_RANK[profile.japanese_level] >= JAPANESE_RANK[job.japanese_level]:
        japanese_score = SCORE_WEIGHTS["japanese"]
    else:
        japanese_score = (
            SCORE_WEIGHTS["japanese"]
            * JAPANESE_RANK[profile.japanese_level]
            / JAPANESE_RANK[job.japanese_level]
        )

    role_score = (
        SCORE_WEIGHTS["role"]
        if profile.desired_role is None or profile.desired_role == job.role_category
        else 0.0
    )

    normalized_locations = {
        normalize(location) for location in profile.preferred_locations or []
    }
    location_score = (
        SCORE_WEIGHTS["location"]
        if not normalized_locations or normalize(job.location) in normalized_locations
        else 0.0
    )

    if profile.expected_salary is None or job.initial_salary >= profile.expected_salary:
        salary_score = SCORE_WEIGHTS["salary"]
    else:
        salary_score = SCORE_WEIGHTS["salary"] * job.initial_salary / profile.expected_salary

    reasons = []
    if matched_required:
        reasons.append(f"匹配必备技能：{', '.join(matched_required)}")
    if matched_preferred:
        reasons.append(f"匹配加分技能：{', '.join(matched_preferred)}")
    if profile.desired_role == job.role_category:
        reasons.append("岗位方向符合期望")
    if normalized_locations and normalize(job.location) in normalized_locations:
        reasons.append("工作地点符合期望")
    if profile.expected_salary is not None and job.initial_salary >= profile.expected_salary:
        reasons.append("新人起薪达到期望")
    if not reasons:
        reasons.append("该岗位在当前候选岗位中综合匹配度较高")

    next_steps = []
    if missing_skills:
        next_steps.append(f"优先补充必备技能：{', '.join(missing_skills)}")
    if job.japanese_level and profile.japanese_level is None:
        next_steps.append(f"确认日语能力是否达到 {job.japanese_level}")
    elif job.japanese_level and japanese_score < SCORE_WEIGHTS["japanese"]:
        next_steps.append(f"继续提升日语至 {job.japanese_level}")
    if profile.experience_years < required_years:
        next_steps.append(f"通过项目经历补充岗位要求的 {required_years} 年经验差距")
    if not next_steps:
        next_steps.append("根据岗位技能关键词调整简历并准备投递")

    breakdown = ScoreBreakdown(
        required_skills=round(required_score, 2),
        preferred_skills=round(preferred_score, 2),
        experience=round(experience_score, 2),
        japanese=round(japanese_score, 2),
        role=round(role_score, 2),
        location=round(location_score, 2),
        salary=round(salary_score, 2),
    )
    return EvaluationDetails(breakdown, reasons, missing_skills, next_steps)


def recommend_jobs(
    db: Session, profile: UserProfileInput, limit: int = 5
) -> RecommendationResponse:
    jobs = list_jobs(db)
    recommendations = []

    for job in jobs:
        details = evaluate_job(profile, job)
        total_score = round(sum(details.breakdown.model_dump().values()), 2)
        recommendations.append(
            RecommendationItem(
                job=job,
                match_score=total_score,
                score_breakdown=details.breakdown,
                reasons=details.reasons,
                missing_skills=details.missing_skills,
                next_steps=details.next_steps,
            )
        )

    recommendations.sort(key=lambda item: (-item.match_score, item.job.id))
    return RecommendationResponse(
        total_jobs_evaluated=len(jobs),
        recommendations=recommendations[:limit],
    )
