from unittest.mock import MagicMock
from app.services.finance_service import FinanceService

def test_record_payment_marks_paid():
    db = MagicMock()
    invoice_repo = MagicMock()
    payment_repo = MagicMock()
    ledger_repo = MagicMock()

    inv = MagicMock(id=1, total_cents=1000, status="sent")
    invoice_repo.return_value.get.return_value = inv

    svc = FinanceService(db, invoice_repo, payment_repo, ledger_repo)
    result = svc.record_payment(1, 1000)

    assert result.status == "paid"
    ledger_repo.return_value.create.assert_called_once()
