
from app.models import Payment

class PaymentRepo:
    def __init__(self, db): self.db = db

    def create(self, payment):
        # if caller already started a transaction, don't begin another
        if self.db.in_transaction():
            self.db.add(payment)
            self.db.flush()
            self.db.refresh(payment)
            return payment

        # repo manages its own transaction when needed
        with self.db.begin():
            self.db.add(payment)
            self.db.flush()      # ensure PK is assigned inside the open transaction
            self.db.refresh(payment)
        return payment