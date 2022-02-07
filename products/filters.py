from django_filters import rest_framework as filters

from products.models import (
    Product,
    Order
)


class ProductFilter(filters.FilterSet):
    """
    Фильтр продуктов
    """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    price = filters.RangeFilter(field_name='price')
    date = filters.DateFilter(field_name='creation_date', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['name', 'price']


class OrderFilter(filters.FilterSet):
    """
    Фильтр заказов для покупателей
    """
    product = filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    status = filters.ChoiceFilter(field_name='status', choices=Order.STATUSES)

    class Meta:
        model = Order
        fields = ['product', 'status']

