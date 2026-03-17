from fastapi import APIRouter, Depends

from app.core.deps import get_invoice_preview_service
from app.services.invoice_preview_service import InvoicePreviewService
from app.core.auth import get_current_user
from app.schemas.invoice import InvoicePreviewRequest, InvoicePreviewResponse

invoice_router = APIRouter(tags=["invoices"], dependencies=[Depends(get_current_user)])

@invoice_router.post(
    "/invoices/preview",
    response_model=InvoicePreviewResponse,
    summary="Preview invoice for staff member",
    description="Calculates invoice totals over a given period for a specific staff member (preview only). "
                "Dates are expected in DD-MM-YY format."
)
async def preview_invoice(
    body: InvoicePreviewRequest,
    service: InvoicePreviewService = Depends(get_invoice_preview_service)
):
    return service.preview_invoice(body)