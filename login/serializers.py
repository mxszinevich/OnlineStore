from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from login.models import UserProfile
from products.models import UserCart


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя
    """
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'full_name', 'type_user')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для получени jwt токенов.
    Добавлен только вызов функции binding_user_to_user_cart(self.user, self.context['request'])
    Нужен для привязки анонимных корзин к пользователю
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        binding_user_to_user_cart(self.user, self.context['request'])

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


def binding_user_to_user_cart(user, request):
    """
    Функция привязки анонимной корзины к пользователю
    """
    session_key = request.session._get_session_key()
    if session_key:
        user_cart = UserCart.objects.select_related('customer').filter(session_key=session_key, customer=None)
        if user_cart.exists():
            for cart in user_cart:
                cart.customer = user

            UserCart.objects.bulk_update(user_cart, ['customer'])

