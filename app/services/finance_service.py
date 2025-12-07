import asyncio
from datetime import datetime
from app.events.publisher import EventPublisher
from app.models import Invoice, Payment, LedgerEntry
from app.repos.audit_repo import ActivityRepo, AuditRepo
from app.repos.invoice_repo import InvoiceRepo
from app.repos.payment_repo import PaymentRepo
from app.repos.ledger_repo import LedgerRepo
from app.repos.inventory_repo import InventoryRepo
from app.services.audit_service import AuditService
from app.services.workflow_service import WorkflowService
from app.utils.cache import redis_client, make_key

class FinanceService:
    def __init__(self, db, invoice_repo, payment_repo, ledger_repo):
        self.db = db
        self.invoice_repo = invoice_repo
        self.payment_repo = payment_repo
        self.ledger_repo = ledger_repo

    def create_invoice(self, customer_id: int, total_cents: int):
        # 1️⃣ Create the invoice
        inv = Invoice(customer_id=customer_id, total_cents=total_cents, status="sent")
        saved = self.invoice_repo(self.db).create(inv)

        # 2️⃣ Log the action in AuditLog (append-only)
        AuditService(self.db, AuditRepo, ActivityRepo).log_event(
            actor_id=None,  # if user context exists later, replace None with user_id
            entity="Invoice",
            entity_id=saved.id,
            action="created",
            changes={"total_cents": total_cents, "status": "sent"}
        )

        # 3️⃣ Post an Activity Feed entry
        AuditService(self.db, AuditRepo, ActivityRepo).post_activity(
            user_id=None,
            message=f"Invoice #{saved.id} created for Customer {customer_id}"
        )

        return saved

    def record_payment(self, invoice_id: int, amount_cents: int):
        inv = self.invoice_repo(self.db).get(invoice_id)
        if not inv or inv.status not in ("sent", "partial"):
            raise ValueError("Invoice not payable")

        # ✅ Record payment
        pay = Payment(invoice_id=inv.id, amount_cents=amount_cents)
        self.payment_repo(self.db).create(pay)

        # ✅ Add ledger entry
        self.ledger_repo(self.db).create(
            LedgerEntry(
                description=f"Payment for invoice {inv.id}",
                debit_cents=0,
                credit_cents=amount_cents
            )
        )

        # ✅ Update invoice status
        if amount_cents >= inv.total_cents:
            inv.status = "paid"
        else:
            inv.status = "partial"

        self.db.commit()
        self.db.refresh(inv)

        # ✅ Trigger workflow and publish event asynchronously
        if inv.status == "paid":
            try:
                redis_client.delete(make_key("invoice", "get", invoice_id))
                # 1️⃣ Publish "invoice.paid" event to NATS
                event = {
                    "invoice_id": inv.id,
                    "customer_id": inv.customer_id,
                    "amount_cents": inv.total_cents,
                    "paid_at": datetime.utcnow().isoformat(),
                }
                asyncio.create_task(
                    EventPublisher().publish("invoice.paid", event)
                )
                print(f"[Event] Published invoice.paid for Invoice {inv.id}")

                # 2️⃣ Also trigger workflow immediately (optional for redundancy)
                WorkflowService(self.db, InventoryRepo).on_invoice_paid(
                    invoice_id=inv.id,
                    product_id=1,
                    qty=1
                )
                print(f"[Workflow Triggered] Invoice {inv.id} → stock reduced for product 1")

            except Exception as e:
                print(f"[Workflow/Event Error] {e}")
                print("Warning: cache invalidation failed")

        return inv