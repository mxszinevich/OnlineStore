from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import F

from config.celery import app
from products.models import Product, UserCart


@app.task
def check_discounts_products() -> int:
    """
    Метод начисления скидок за товар
    Если дата создания продукта > одного месяца то скидка 20%.
    """
    number_of_months_discount = 1
    discount = 0.2
    products = Product.objects.filter(
        creation_date__lte=datetime.now() + relativedelta(months=-number_of_months_discount)
    )
    products.update(price=F('price') * (1 - discount), discount=discount)

    return products.count()

@app.task
def delete_user_carts() -> int:
    """
    Метод удаления корзин анонимных пользователей с временем жизни > 30 мин
    """
    users_cart = UserCart.objects.filter(customer=None)
    Product.objects.filter(cart__in=users_cart).update(quantity=F('quantity') + 1)
    users_cart_count = users_cart.count()
    users_cart.delete()

    return users_cart_count
