# app/api/leads.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import LeadCreate, LeadOut, PromoteRequest
from app.repos.lead_repo import LeadRepo
from app.repos.deal_repo import DealRepo
from app.services.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["leads"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LeadOut)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    svc = LeadService(LeadRepo, DealRepo, db)
    return svc.create_lead(payload.name, payload.email)

@router.post("/{lead_id}/promote")
def promote(lead_id: int, payload: PromoteRequest, db: Session = Depends(get_db)):
    svc = LeadService(LeadRepo, DealRepo, db)
    try:
        deal = svc.promote_to_deal(lead_id, payload.value_cents, payload.seller_id)
        return {"deal_id": deal.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
