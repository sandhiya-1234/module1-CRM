from app.database import SessionLocal
from app.models import User

db = SessionLocal()

if not db.query(User).first():
    db.add_all([
        User(name="Admin User", email="admin@crm.com", role="admin"),
        User(name="Manager User", email="manager@crm.com", role="manager"),
        User(name="Staff User", email="staff@crm.com", role="staff")
    ])
    db.commit()
    print("✅ Dummy users added!")
else:
    print("Dummy users already exist.")
