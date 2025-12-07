import asyncio
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.finance_service import FinanceService
from app.repos.invoice_repo import InvoiceRepo
from app.repos.payment_repo import PaymentRepo
from app.repos.ledger_repo import LedgerRepo
from app.schemas import InvoiceCreate, InvoiceOut, PaymentCreate, PaymentOut
from app.models import Invoice, Payment
from app.api.security import require_roles
from app.utils.cache import redis_client, make_key
from app.schemas import InvoiceOut 



router = APIRouter(prefix="/invoices", tags=["finance"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/", response_model=InvoiceOut)
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin", "manager"))  # ✅ RBAC added here
):
    svc = FinanceService(db, InvoiceRepo, PaymentRepo, LedgerRepo)
    return svc.create_invoice(payload.customer_id, payload.total_cents)

@router.post("/{invoice_id}/pay")
async def pay_invoice(
    invoice_id: int,
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin", "manager"))
):
    svc = FinanceService(db, InvoiceRepo, PaymentRepo, LedgerRepo)

    try:
        # Run synchronous DB operation in a separate thread
        inv = await asyncio.to_thread(svc.record_payment, invoice_id, payload.amount_cents)
        return {"invoice_id": inv.id, "status": inv.status}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.get(Invoice, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv

@router.get("/{invoice_id}/payments", response_model=List[PaymentOut])
def list_payments(invoice_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter_by(invoice_id=invoice_id).all()
    return payments

@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    key = make_key("invoice", "get", invoice_id)
    raw = redis_client.get(key)
    if raw:
        return json.loads(raw)
    inv = InvoiceRepo(db).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    payload = InvoiceOut.from_orm(inv).dict()
    redis_client.setex(key, 30, json.dumps(payload))
    return payload