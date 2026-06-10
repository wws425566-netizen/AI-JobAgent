import unittest

from pydantic import ValidationError

from app.models.job_posting import JobPosting
from app.schemas.recommendation import UserProfileInput
from app.services.recommendation_service import evaluate_job


def make_job(**overrides) -> JobPosting:
    values = {
        "id": 1,
        "title": "Backend Engineer",
        "role_category": "backend",
        "company_name": "Example Company",
        "company_type": "自社开发",
        "location": "东京",
        "industry": "互联网",
        "required_skills": ["Python", "FastAPI", "SQL"],
        "preferred_skills": ["AWS", "Docker"],
        "japanese_level": "N2",
        "experience_requirement": "1年以上",
        "initial_salary": 300000,
        "job_url": "https://example.com/job",
    }
    values.update(overrides)
    return JobPosting(**values)


class RecommendationServiceTests(unittest.TestCase):
    def test_full_match_receives_full_score(self) -> None:
        profile = UserProfileInput(
            skills=["Python", "FastAPI", "SQL", "AWS", "Docker"],
            experience_years=1,
            japanese_level="N2",
            desired_role="backend",
            preferred_locations=["东京"],
            expected_salary=300000,
        )

        details = evaluate_job(profile, make_job())

        self.assertEqual(sum(details.breakdown.model_dump().values()), 100.0)
        self.assertEqual(details.missing_skills, [])

    def test_skill_matching_ignores_letter_case(self) -> None:
        profile = UserProfileInput(skills=["python", "FASTAPI"], experience_years=1)

        details = evaluate_job(profile, make_job(japanese_level=None))

        self.assertAlmostEqual(details.breakdown.required_skills, 23.33, places=2)
        self.assertEqual(details.missing_skills, ["SQL"])

    def test_missing_japanese_level_does_not_break_recommendation(self) -> None:
        profile = UserProfileInput(skills=["Python"], experience_years=0)

        details = evaluate_job(profile, make_job(japanese_level="N2"))

        self.assertEqual(details.breakdown.japanese, 0.0)
        self.assertIn("确认日语能力是否达到 N2", details.next_steps)

    def test_profile_rejects_empty_skills(self) -> None:
        with self.assertRaises(ValidationError):
            UserProfileInput(skills=[], experience_years=0)


if __name__ == "__main__":
    unittest.main()
