
from app.models import Deal

class DealRepo:
    def __init__(self, db):
        self.db = db

    def create(self, lead_id: int, value_cents: int, seller_id: int = None):
        deal = Deal(lead_id=lead_id, value_cents=value_cents, seller_id=seller_id)

        if self.db.in_transaction():
            # already in a transaction started by the caller — don't begin another
            self.db.add(deal)
            self.db.flush()
            self.db.refresh(deal)
            return deal

        # repo manages its own transaction when caller hasn't started one
        with self.db.begin():
            self.db.add(deal)
            self.db.flush()      # ensure PK is assigned inside the open transaction
            self.db.refresh(deal)
        return deal
