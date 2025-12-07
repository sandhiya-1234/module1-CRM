import factory
from app.models import Product

class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = None   # we’ll assign this dynamically in the test
        sqlalchemy_session_persistence = "flush"

    name = factory.Sequence(lambda n: f"Product {n}")
    sku = factory.Sequence(lambda n: f"SKU-{n}")
    stock = 10
