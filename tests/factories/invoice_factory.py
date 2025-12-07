import factory
from app.models import Invoice

class InvoiceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Invoice
        sqlalchemy_session = None   # dynamic assignment
        sqlalchemy_session_persistence = "flush"

    customer_id = factory.Sequence(lambda n: n + 1)
    total_cents = factory.Iterator([1000, 2000, 5000])
    status = factory.Iterator(["sent", "paid"])
