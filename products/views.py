from django.db.models import Q

from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from login.models import UserProfile
from products.exceptions import ServiceUnavailable
from products.filters import ProductFilter, OrderFilter
from products.mixins import ChoiceSerializerMixin
from products.models import (
    Product,
    Order,
    UserCart,
    Score,
    OrderPayments
)
from products.permissions import (
    CustomerOrderPermissions,
    EmployeeOrderPermissions,
    CheckerScorePermissions,
    OrderPaymentsPermissions
)
from products.serializers import (
    ProductSerializer,
    CustomerCartCreateSerializer,
    CustomerOrderCreateSerializer,
    OrderSerializer,
    OrderUpdateEmployeeSerializer,
    ScoreViewSerializer,
    ScoreCreateSerializer,
    OrderPaymentsSerializer
)
from products.utils import is_sessionid


class ProductsView(viewsets.ModelViewSet):
    """
    Представление товара магазина
    """
    http_method_names = ['get']
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


class OrderView(ChoiceSerializerMixin, viewsets.ModelViewSet):
    """
    Представление заказа для сотрудников
    """
    serializer_class = OrderSerializer
    permission_classes = [EmployeeOrderPermissions]

    serializer_classes_by_action = {
        'update': OrderUpdateEmployeeSerializer
    }
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        user = self.request.user.type_user
        datetime_filter = self.get_order_on_date_filter(self.request.query_params)
        if user == UserProfile.TYPE_SELLER:
            return Order.objects.filter(status=Order.STATUS_GENERATED).filter(datetime_filter)
        elif user == UserProfile.TYPE_CHECKER:
            return Order.objects.filter(status__in=(Order.STATUS_DONE, Order.STATUS_PAY)).filter(datetime_filter)
        elif user == UserProfile.TYPE_BOOKKEEPER:
            return Order.objects.filter(datetime_filter)

        return []

    def get_order_on_date_filter(self, query_params):
        """
        Метод возвращающий фильтр по временным параметрам запроса
        """
        from_ = query_params.get('from')
        to_ = query_params.get('to')
        from_filter = Q(creation_date__date__gte=from_) if from_ else Q()
        to_filter = Q(creation_date__date__lte=to_) if to_ else Q()
        return from_filter & to_filter


class CustomerOrderView(ChoiceSerializerMixin, viewsets.ModelViewSet):
    """
    Представление заказа для покупателя
    """
    serializer_class = OrderSerializer
    permission_classes = [CustomerOrderPermissions]
    serializer_classes_by_action = {
        'create': CustomerOrderCreateSerializer
    }
    http_method_names = ['get', 'post', 'delete']

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class CartView(ChoiceSerializerMixin, viewsets.ModelViewSet):
    """
    Представления корзины покупателя
    """
    http_method_names = ['get', 'post', 'delete']

    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAuthenticated]
    }
    serializer_classes_by_action = {
        'create': CustomerCartCreateSerializer,
        'list': CustomerCartCreateSerializer
    }

    def get_queryset(self):

        user_cart_filter = Q(session_key=self.request.session._get_session_key())

        if not self.request.user.is_anonymous:
            user_cart_filter |= Q(customer=self.request.user)

        return UserCart.objects.filter(user_cart_filter)

    def perform_create(self, serializer):
        #  Определяем наличие продукта
        product_id = self.request.data.get('product')
        if product_id is not None:
            product = Product.objects.get(id=product_id)
            if product.quantity:
                product.quantity -= 1
                product.save(update_fields=['quantity'])
            else:
                raise ServiceUnavailable()

        #  Определяем покупателя
        if self.request.user.is_anonymous:  #  Если пользователь анонимный - сохраняем сессию
            if not is_sessionid(self.request):  # Если на клиенте нет сессии возвращаем созданную сессию
                self.request.session.cycle_key()
            user_params = {'session_key': self.request.session._get_session_key()}
        else:
            user_params = {'customer': self.request.user}
        serializer.save(**user_params)

    def perform_destroy(self, instance):
        instance.product.quantity += 1  # При прямом удалении корзины - увеличиваем кол-во товара
        instance.product.save(update_fields=['quantity'])
        super().destroy()


class ScoreView(ChoiceSerializerMixin, viewsets.ModelViewSet):
    """
    Представление для счета
    """
    serializer_class = ScoreViewSerializer
    permission_classes = [CheckerScorePermissions]
    serializer_classes_by_action = {
        'create': ScoreCreateSerializer
    }
    http_method_names = ['get', 'post']

    def get_queryset(self):
        user = self.request.user
        queryset = []

        if self.request.user.type_user == UserProfile.TYPE_SHOPPER:
            queryset = Score.objects.select_related('order').filter(order__user=user)
        elif self.request.user.type_user == UserProfile.TYPE_CHECKER:
            queryset = Score.objects.select_related('order').all()

        return queryset


class OrderPaymentsView(viewsets.ModelViewSet):
    """
    Представление для оплаты заказа клиентом
    """
    serializer_class = OrderPaymentsSerializer
    permission_classes = [OrderPaymentsPermissions]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):

        if self.request.user.type_user in (UserProfile.TYPE_CHECKER, UserProfile.TYPE_BOOKKEEPER):
            order_filter = Q()
        else:
            order_filter = Q(customer=self.request.user)

        return OrderPayments.objects.select_related('score', 'customer').filter(order_filter)






























