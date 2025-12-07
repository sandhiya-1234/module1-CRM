from http.client import HTTPException
from app.models import Product, StockTransaction
from app.repos.inventory_repo import InventoryRepo

class InventoryService:
    def __init__(self, db, repo):
        self.db = db
        self.repo = repo or InventoryRepo

    def create_product(self, name: str, sku: str, opening_stock: int = 0):
        # ✅ 1. Check if SKU already exists before inserting
        existing = self.db.query(Product).filter(Product.sku == sku).first()
        if existing:
            raise HTTPException(status_code=400, detail="SKU already exists")

        # ✅ 2. Safe to create new product now
        product = Product(name=name, sku=sku, stock=opening_stock)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def reserve_stock(self, pid: int, qty: int):
        product = self.repo(self.db).get_product(pid)
        if not product:
            raise ValueError("Product not found")
        if product.stock < qty:
            raise ValueError("Insufficient stock")

        trx = StockTransaction(product_id=pid, qty_change=-qty, reason="reserve")
        product.stock -= qty
        self.db.add(trx)
        self.db.commit()
        self.db.refresh(product)
        return product
