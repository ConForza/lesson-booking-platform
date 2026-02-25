from fastapi import APIRouter
from app.services.invoice_preview_service import InvoicePreviewService
from app.schemas.invoice import InvoicePreviewRequest, InvoicePreviewResponse

invoice_router = APIRouter(tags=["invoices"])
service = InvoicePreviewService()

@invoice_router.post("/invoices/preview", response_model=InvoicePreviewResponse)
async def preview_invoice(body: InvoicePreviewRequest):
    return service.preview_invoice(body)