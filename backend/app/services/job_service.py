from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_posting import JobPosting


def list_jobs(db: Session) -> list[JobPosting]:
    """List all job postings ordered by id."""
    statement = select(JobPosting).order_by(JobPosting.id)
    return list(db.scalars(statement).all())

