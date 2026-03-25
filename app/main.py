import logging

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
import time

from app.api.v1.auth import auth_router
from app.api.v1.health import health_router
from app.api.v1.invoice import invoice_router
from app.api.v1.lessons import lessons_router
from app.api.v1.students import students_router
from app.core.exceptions import DomainError
from app.core.config import get_settings, Settings
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

settings = get_settings()

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    force=True
)
logging.getLogger("httpx").setLevel(logging.ERROR)

tags_metadata = [
    {"name": "system",
     "description": "System-level endpoints such as health checks."},
    {"name": "students",
     "description": "Endpoints related to student lesson tracking and calculations."},
    {"name": "invoices",
     "description": "Endpoints for invoice preview and generation logic."},
    {"name": "lessons",
     "description": "Endpoints related to creating and fetching lessons."}
]

app = FastAPI(
    title=settings.app_name,
    description="Backend API for managing student lessons and invoice tracking for a music school",
    version=settings.version,
    openapi_tags=tags_metadata
)
app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(invoice_router, prefix=settings.api_v1_prefix)
app.include_router(students_router, prefix=settings.api_v1_prefix)
app.include_router(auth_router, prefix=settings.api_v1_prefix)

app.include_router(lessons_router, prefix=settings.api_v1_prefix)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    if response.status_code >= 400:
        logger.warning(
            "%s %s -> %s (%.3fs)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
    else:
        logger.info(
            "%s %s -> %s (%.3fs)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

    return response

@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {
        "message": "Hello World",
        "environment": settings.environment,
        "version": settings.version,
    }

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
