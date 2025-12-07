# app/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# -------------------
# Leads / Deals (Module 1)
# -------------------
class LeadCreate(BaseModel):
    name: str
    email: EmailStr | None = None

class LeadOut(BaseModel):
    id: int
    name: str
    email: EmailStr | None
    status: str
    class Config:
        orm_mode = True

class PromoteRequest(BaseModel):
    value_cents: int
    seller_id: int | None = None

# -------------------
# Finance (Module 2)
# -------------------
class InvoiceCreate(BaseModel):
    customer_id: int
    total_cents: int

class InvoiceOut(BaseModel):
    id: int
    customer_id: int
    total_cents: int
    status: str
    class Config:
        orm_mode = True

class PaymentCreate(BaseModel):
    amount_cents: int

class PaymentOut(BaseModel):
    id: int
    invoice_id: int
    amount_cents: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

# pydantic v2: use `from_attributes`; if you're on v1 use `orm_mode = True`
model_config = {"from_attributes": True}

# -------------------
# Finance (Module 3)
# -------------------

from pydantic import BaseModel
from datetime import datetime

class AuditOut(BaseModel):
    id: int
    entity: str
    entity_id: int
    action: str
    changes: dict
    created_at: datetime
    class Config:
        orm_mode = True

# -------------------
# inventory (Module 5)
# -------------------

from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    sku: str
    opening_stock: int = 0

class ProductOut(BaseModel):
    id: int
    name: str
    sku: str
    stock: int
    class Config:
        orm_mode = True

# -------------------
# message (Module 8)
# -------------------

# app/schemas/message_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    conversation_id: int
    sender_id: int
    content: str

class MessageOut(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str
    is_read: bool
    created_at: datetime
    class Config:
        orm_mode = True

class ConversationOut(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True
