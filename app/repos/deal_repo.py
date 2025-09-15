# app/repos/deal_repo.py
from app.models import Deal

class DealRepo:
    def __init__(self, db):
        self.db = db

    def create(self, lead_id: int, value_cents: int, seller_id: int = None):
        deal = Deal(lead_id=lead_id, value_cents=value_cents, seller_id=seller_id)
        self.db.add(deal)
        self.db.commit()
        self.db.refresh(deal)
        return deal
