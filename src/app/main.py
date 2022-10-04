import logging
from logging.config import dictConfig

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import api_v1
from app.config import LogConfig, get_settings

dictConfig(LogConfig().dict())
log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        openapi_url=f"{settings.prefix_api_v1}/openapi.json",
    )
    application.include_router(api_v1)

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    content = {"detail": []}
    for error in exc.errors():
        loc = error["loc"]
        msg = error["msg"]
        type_error = error["type"]
        content["detail"].append(
            {"field": list(loc)[-1], "message": msg, "type": type_error}
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=content
    )
