from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repos.audit_repo import AuditRepo, ActivityRepo
from app.services.audit_service import AuditService
from app.schemas import AuditOut

router = APIRouter(prefix="/audit", tags=["audit"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[AuditOut])
def get_audit_logs(entity: str = None, db: Session = Depends(get_db)):
    svc = AuditService(db, AuditRepo, ActivityRepo)
    return svc.audit_repo(db).list_logs(entity)
