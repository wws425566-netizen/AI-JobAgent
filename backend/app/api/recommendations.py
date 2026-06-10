from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.recommendation import RecommendationResponse, UserProfileInput
from app.services.recommendation_service import recommend_jobs

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("", response_model=RecommendationResponse)
def create_recommendations(
    profile: UserProfileInput,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    """Return the five highest-scoring jobs for the submitted profile."""
    return recommend_jobs(db, profile)
