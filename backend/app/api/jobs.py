from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.job import JobPostingRead
from app.services.job_service import list_jobs

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("", response_model=list[JobPostingRead])
def get_jobs(db: Session = Depends(get_db)) -> list[JobPostingRead]:
    """Return all seeded job postings."""
    return list_jobs(db)

