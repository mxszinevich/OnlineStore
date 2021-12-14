from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import Order, UserCart, Score, OrderPayments


class ProductSerializer(serializers.Serializer):
    """
    Сериализатор товара
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.IntegerField()
    creation_date = serializers.DateTimeField()
    quantity = serializers.IntegerField()


class CustomerOrderCreateSerializer(serializers.Serializer):
    """
    Сериализатор создания заказа покупателем
    """
    cart = serializers.IntegerField(required=True)

    def validate(self, attrs):
        user = self.context['request'].user
        session_key = self.context['request'].session._get_session_key()
        user_cart_filter = Q(id=attrs['cart']) & (Q(customer=user) | Q(session_key=session_key))
        carts = UserCart.objects.filter(user_cart_filter)
        if not carts.exists():
            raise ValidationError('Ваша корзина пуста')
        else:
            carts_with_unknown_user = carts.filter(customer=None)  # Обновляем все корзины текущего пользователя
            for cart in carts_with_unknown_user:
                cart.customer = user
            UserCart.objects.bulk_update(carts_with_unknown_user, ['customer'])

        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        user_cart = UserCart.objects.get(id=validated_data['cart'])
        product = user_cart.product
        user_cart.delete()
        return Order.objects.create(
            product=product,
            user=self.context['request'].user
        )


class CustomerCartCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания корзины заказа
    """
    class Meta:
        model = UserCart
        fields = ('id', 'product')
        extra_kwargs = {
            'product': {'required': True},
            'id': {'read_only': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation_data = {
            'product': instance.product.name,
            'price': instance.product.price,
        }
        representation.update(representation_data)
        return representation


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор заказов (используется только для просмотра заказов)
    """
    class Meta:
        model = Order
        exclude = ('session_key',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation_data = {
            'user': instance.user.email,
            'product': instance.product.name,
            'status': instance.get_status_display()
        }
        representation.update(representation_data)
        return representation


class OrderUpdateEmployeeSerializer(serializers.ModelSerializer):
    """
    Сериализатор заказов для сотрудников магазина
    """
    class Meta:
        model = Order
        fields = ('status', )
        extra_kwargs = {
            'status': {'required': True},
            'id': {'read_only': True}
        }


class ScoreViewSerializer(serializers.ModelSerializer):
    """
    Сериализатор просмотра счета
    """
    order = OrderSerializer(many=False)
    class Meta:
        model = Score
        fields = ('id', 'creation_date', 'order')


class ScoreCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для генерации счета кассиром
    """
    class Meta:
        model = Score
        fields = ('order',)
        extra_kwargs = {
            'order': {'required': True}
        }


class OrderPaymentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор оплаты заказа
    """
    class Meta:
        model = OrderPayments
        fields = ('score', 'payment')

        extra_kwargs = {
            'score': {'required': True},
            'payment': {'required': True}
        }






