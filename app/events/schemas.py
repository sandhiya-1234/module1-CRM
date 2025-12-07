from pydantic import BaseModel
from datetime import datetime

class InvoicePaid(BaseModel):
    invoice_id: int
    customer_id: int
    amount_cents: int
    paid_at: datetime
