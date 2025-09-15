# app/schemas.py
from pydantic import BaseModel, EmailStr

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
