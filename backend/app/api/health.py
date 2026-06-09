from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """返回服务健康状态，方便确认后端已经启动。"""
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "database": settings.database_url,
    }

