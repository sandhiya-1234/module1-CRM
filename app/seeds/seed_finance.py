from app.database import SessionLocal
from app.models import Invoice

def run():
    db = SessionLocal()
    invoices = [
        Invoice(customer_id=1, total_cents=10000, status="sent"),
        Invoice(customer_id=2, total_cents=25000, status="sent"),
        Invoice(customer_id=3, total_cents=15000, status="paid"),
    ]
    db.add_all(invoices)
    db.commit()
    db.close()
    print("✅ Seeded finance data successfully!")

if __name__ == "__main__":
    run()
