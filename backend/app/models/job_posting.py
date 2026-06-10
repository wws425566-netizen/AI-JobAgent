from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class JobPosting(Base):
    """Job posting data used by the recommendation system."""

    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    company_name: Mapped[str] = mapped_column(String(120), nullable=False)
    company_type: Mapped[str] = mapped_column(String(40), nullable=False)
    location: Mapped[str] = mapped_column(String(80), nullable=False)
    industry: Mapped[str] = mapped_column(String(80), nullable=False)
    required_skills: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    preferred_skills: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    japanese_level: Mapped[str] = mapped_column(String(20), nullable=True)
    experience_requirement: Mapped[str] = mapped_column(String(40), nullable=False)
    initial_salary: Mapped[int] = mapped_column(Integer, nullable=False)
    job_url: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
