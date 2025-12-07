
from app.services.inventory_service import InventoryService

class WorkflowService:
    def __init__(self, db, inventory_repo):
        self.db = db
        self.inventory_repo = inventory_repo

    def on_invoice_paid(self, invoice_id: int, product_id: int, qty: int):
        """Trigger when invoice is fully paid."""
        inv_svc = InventoryService(self.db, self.inventory_repo)
        inv_svc.reserve_stock(product_id, qty)
        print(f"[Inventory] Reserved {qty} units for invoice {invoice_id}")
        return True
