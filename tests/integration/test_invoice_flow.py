from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

def setup_function():
    Base.metadata.create_all(bind=engine)

def test_invoice_and_payment():
    # create invoice
    r = client.post("/invoices/", json={"customer_id": 1, "total_cents": 5000})
    assert r.status_code == 200
    invoice = r.json()

    # pay invoice
    r2 = client.post(f"/invoices/{invoice['id']}/pay", json={"amount_cents": 5000})
    assert r2.status_code == 200
    assert r2.json()["status"] == "paid"
