from app.models import Product, StockTransaction

class InventoryRepo:
    def __init__(self, db):
        self.db = db

    def get_product(self, pid: int):
        return self.db.query(Product).filter(Product.id == pid).first()

    def add_transaction(self, trx: StockTransaction):
        self.db.add(trx)
        self.db.commit()
        self.db.refresh(trx)
        return trx

    def adjust_stock(self, pid: int, qty: int):
        product = self.get_product(pid)
        if not product:
            raise ValueError("Product not found")
        product.stock += qty
        self.db.commit()
        self.db.refresh(product)
        return product
