import pytest
from django.urls import reverse
from rest_framework import status

from products.tests.factories import ProductFactory

from products.models import UserCart

from products.models import Product


class TestProductsView:
    """
    Тестирование API продуктов
    """

    @pytest.mark.django_db
    def test_products_view(self, api_client):
        """
        Тестирование просмотра списка продуктов
        """
        url = reverse('products-list')
        product_count = 5
        for _ in range(product_count):
            ProductFactory()

        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == product_count

    @pytest.mark.django_db
    def test_add_product_in_user_cart(self, api_client):
        """
        Тестирование создания корзины пользователя по сессии
        """
        url = reverse('cart-list')
        product = ProductFactory()

        assert Product.objects.first().quantity == product.quantity

        data = {"product": product.id}
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert UserCart.objects.count() == 1
        user_cart = UserCart.objects.first()
        assert user_cart.session_key == api_client.session._get_session_key()
        assert user_cart.product == product
        assert Product.objects.first().quantity == product.quantity - 1



















