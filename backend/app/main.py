from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.jobs import router as jobs_router
from app.core.database import Base, engine
from app.models import job_posting  # noqa: F401


app = FastAPI(
    title="JobAgent API",
    description="Backend service for the JobAgent recommendation project.",
    version="0.1.0",
)


@app.on_event("startup")
def create_tables() -> None:
    """Create SQLite tables during the beginner phase."""
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(jobs_router)
