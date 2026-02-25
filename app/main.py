from fastapi import FastAPI
from app.api.v1.health import health_router
from app.api.v1.invoice import invoice_router

app = FastAPI()
app.include_router(health_router, prefix="/api/v1")
app.include_router(invoice_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}
