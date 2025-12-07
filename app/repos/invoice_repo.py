from app.models import Invoice

class InvoiceRepo:
    def __init__(self, db): self.db = db
    def get(self, inv_id): return self.db.query(Invoice).get(inv_id)
    def create(self, invoice):
         with self.db.begin():
            self.db.add(invoice)
            self.db.flush()      # ensure PK is assigned inside the open transaction
            self.db.refresh(invoice)
         return invoice
