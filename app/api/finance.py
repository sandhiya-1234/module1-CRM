from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.finance_service import FinanceService
from app.repos.invoice_repo import InvoiceRepo
from app.repos.payment_repo import PaymentRepo
from app.repos.ledger_repo import LedgerRepo
from app.api.security import require_roles

router = APIRouter(prefix="/finance", tags=["finance"])

@router.post("/invoice")
def create_invoice(
    customer_id: int,
    total_cents: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin", "manager"))  # 👈 Only admin/manager allowed
):
    svc = FinanceService(db, InvoiceRepo, PaymentRepo, LedgerRepo)
    return svc.create_invoice(customer_id, total_cents)

from fastapi import HTTPException, status

@router.post("/payment")
def record_payment(
    invoice_id: int,
    amount_cents: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin", "manager"))
):
    svc = FinanceService(db, InvoiceRepo, PaymentRepo, LedgerRepo)
    try:
        return svc.record_payment(invoice_id, amount_cents)
    except ValueError as e:
        # Catch business logic errors and send clean message
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)  # e.g. "Invoice not payable"
        )
