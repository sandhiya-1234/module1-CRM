from app.database import SessionLocal
from app.repos.inventory_repo import InventoryRepo
from app.services.inventory_service import InventoryService

class WorkflowHandlers:
    @staticmethod
    async def on_invoice_paid(data: dict):
        """Triggered when an invoice is paid; updates inventory."""
        db = None
        try:
            invoice_id = data.get("invoice_id")
            product_id = data.get("product_id", 1)
            qty = data.get("qty", 1)

            print(f"⚙️ Workflow Triggered: Invoice {invoice_id}, Product {product_id}, Qty {qty}")

            # ✅ Create DB session manually
            db = SessionLocal()

            # ✅ Initialize service with repo
            inv_service = InventoryService(db, InventoryRepo)

            # ✅ Reserve stock (reduce inventory)
            inv_service.reserve_stock(product_id, qty)
            db.commit()

            # 🟢 INSERT THESE LINES HERE (debug confirmation)
            updated = inv_service.repo(db).get_product(product_id)
            print(f"📦 Inventory Updated: {updated.name} (ID {product_id}) now has {updated.stock} units left.")

            print(f"✅ Stock reduced for Product {product_id} after Invoice {invoice_id} payment.")

        except Exception as e:
            print(f"❌ Workflow Handler Error: {e}")
            if db:
                db.rollback()
        finally:
            if db:
                db.close()
