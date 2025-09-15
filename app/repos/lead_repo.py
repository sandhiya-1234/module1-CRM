# app/repos/lead_repo.py
from app.models import Lead

class LeadRepo:
    def __init__(self, db):
        self.db = db

    def get(self, lead_id: int):
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def create(self, name: str, email: str = None):
        lead = Lead(name=name, email=email)
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def list_all(self, limit=100):
        return self.db.query(Lead).order_by(Lead.created_at.desc()).limit(limit).all()
