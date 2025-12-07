from tests.factories.product_factory import ProductFactory
from tests.factories.invoice_factory import InvoiceFactory

def test_factories_create_data(db_session):
    # ✅ Link pytest DB session to factory
    ProductFactory._meta.sqlalchemy_session = db_session
    InvoiceFactory._meta.sqlalchemy_session = db_session

    # ✅ Create fake objects (auto-added to db_session)
    p1 = ProductFactory(stock=15)
    i1 = InvoiceFactory()

    db_session.commit()

    assert p1.stock == 15
    assert i1.status in ["sent", "paid"]
