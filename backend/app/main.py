from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.jobs import router as jobs_router
from app.api.recommendations import router as recommendations_router
from app.core.database import Base, engine
from app.models import job_posting  # noqa: F401


app = FastAPI(
    title="JobAgent API",
    description="Backend service for the JobAgent recommendation project.",
    version="0.1.0",
)

# 浏览器会限制不同端口之间的请求。开发阶段允许 Vite 默认地址访问后端 API。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables() -> None:
    """Create SQLite tables during the beginner phase."""
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(jobs_router)
app.include_router(recommendations_router)
