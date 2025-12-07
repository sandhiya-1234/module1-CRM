from app.models import LedgerEntry

class LedgerRepo:
    def __init__(self, db):
        self.db = db

    def create(self, description_or_entry, debit_cents: int = 0, credit_cents: int = 0, reference=None):
        # accept either a LedgerEntry instance or primitive args
        if isinstance(description_or_entry, LedgerEntry):
            entry = description_or_entry
            # allow caller-provided values to override only if primitives were supplied
            if debit_cents or credit_cents or reference is not None:
                entry.debit_cents = debit_cents
                entry.credit_cents = credit_cents
                entry.reference = reference
        else:
            entry = LedgerEntry(
                description=description_or_entry,
                debit_cents=debit_cents,
                credit_cents=credit_cents,
                reference=reference
            )

        # if caller already started a transaction, don't begin another
        if self.db.in_transaction():
            self.db.add(entry)
            self.db.flush()
            self.db.refresh(entry)
            return entry

        # repo manages its own transaction when needed
        with self.db.begin():
            self.db.add(entry)
            self.db.flush()      # ensure PK is assigned inside the open transaction
            self.db.refresh(entry)
        return entry