from fastapi import FastAPI

from app.api.health import router as health_router


app = FastAPI(
    title="JobAgent API",
    description="AI 求职岗位推荐 Agent 项目的后端服务",
    version="0.1.0",
)

app.include_router(health_router)

