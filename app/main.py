from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.auth import auth_router
from app.api.v1.health import health_router
from app.api.v1.invoice import invoice_router
from app.api.v1.students import students_router
from app.core.exceptions import DomainError
from app.core.config import get_settings, Settings
from app.db.database import Base, engine
from fastapi import Depends

Base.metadata.create_all(bind=engine)

settings = get_settings()

tags_metadata = [
    {"name": "system",
     "description": "System-level endpoints such as health checks."},
    {"name": "students",
     "description": "Endpoints related to student lesson tracking and calculations."},
    {"name": "invoices",
     "description": "Endpoints for invoice preview and generation logic."}
]

app = FastAPI(
    title=settings.app_name,
    description="Backend API for managing student lessons and invoice tracking for a music school",
    version=settings.version,
    openapi_tags=tags_metadata,
)
app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(invoice_router, prefix=settings.api_v1_prefix)
app.include_router(students_router, prefix=settings.api_v1_prefix)
app.include_router(auth_router, prefix=settings.api_v1_prefix)

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
