from fastapi import APIRouter

from app.api.controllers import health_check
from app.config import get_settings

settings = get_settings()

api_v1 = APIRouter(prefix=settings.prefix_api_v1)

api_v1.include_router(
    health_check.router, prefix="/healthcheck", tags=["Health Check"]
)
