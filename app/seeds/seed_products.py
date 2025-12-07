from app.database import SessionLocal
from app.models import Product

def run():
    db = SessionLocal()
    try:
        products = [
            {"name": "Bluetooth Speaker", "sku": "SPK-001", "stock": 50},
            {"name": "Wireless Headphones", "sku": "HPH-001", "stock": 30},
            {"name": "Smartwatch", "sku": "WTCH-001", "stock": 20},
        ]

        for p in products:
            existing = db.query(Product).filter(Product.sku == p["sku"]).first()
            if existing:
                print(f"⚠️  Skipped existing product: {p['sku']}")
                continue

            prod = Product(**p)
            db.add(prod)

        db.commit()
        print("✅  Seeded products successfully (skipping duplicates).")

    except Exception as e:
        db.rollback()
        print(f"❌  Seeding failed: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    run()
