import datetime

from factory import (
    Sequence,
    SubFactory,
    LazyAttribute,
    Faker
)
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyDate

from login.tests.factories import UserProfileFactory
from products.models import (
    Product,
    UserCart
)


class ProductFactory(DjangoModelFactory):
    """
    Фабрика продукта
    """

    name = Sequence(lambda n: f'Продукт {n}')
    price = FuzzyInteger(10000, 100000)
    creation_date = FuzzyDate(
        start_date=datetime.date.today(), end_date=datetime.date.today() + datetime.timedelta(days=100)
    )

    class Meta:
        model = Product


class UserCartFactory(DjangoModelFactory):
    """
    Фабрика пользовательской корзины с идентифицированным пользователем
    """
    product = SubFactory(ProductFactory)
    creation_date = LazyAttribute(
        lambda obj: FuzzyDate(
            start_date=obj.product.creation_date, end_date=obj.product.creation_date + datetime.timedelta(days=100))
    )
    session_key = Faker("bban")
    customer = SubFactory(UserProfileFactory)

    class Meta:
        model = UserCart



