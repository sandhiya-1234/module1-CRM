# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

# -------------------
# Leads & Deals (Module 1)
# -------------------
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True, index=True)
    status = Column(String, default="new")  # new, contacted, qualified, converted
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    value_cents = Column(Integer, nullable=False)
    seller_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    lead = relationship("Lead")

# -------------------
# Finance (Module 2)
# -------------------
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    total_cents = Column(Integer, nullable=False)
    status = Column(String, default="draft")  # draft, sent, paid, cancelled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    amount_cents = Column(Integer, nullable=False)
    received_at = Column(DateTime, default=datetime.datetime.utcnow)

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    debit_cents = Column(Integer, default=0)
    credit_cents = Column(Integer, default=0)
    reference = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# -------------------
# Audit (Module 3)
# -------------------

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, nullable=True)
    entity = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    changes = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ActivityFeed(Base):
    __tablename__ = "activity_feed"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# -------------------
# Audit (Module 4)
# -------------------

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # admin, manager, staff
    description = Column(String)

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("dummy_users.id"))  # For now; change to "users.id" later
    role_id = Column(Integer, ForeignKey("roles.id"))

from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "dummy_users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    role = Column(String, default="staff")  # simple placeholder

# -------------------
# inventory (Module 5)
# -------------------

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
import datetime
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class StockTransaction(Base):
    __tablename__ = "stock_transactions"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    qty_change = Column(Integer, nullable=False)  # +10 add, -3 reduce
    reason = Column(String, nullable=True)        # sale, return, manual
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# -------------------
# message (Module 8)
# -------------------

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base  # adjust import to your project

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)         # optional
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True, nullable=False)
    sender_id = Column(Integer, nullable=False)        # user id
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", backref="messages")
