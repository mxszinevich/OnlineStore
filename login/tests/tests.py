import pytest

from django.urls import reverse

from login.tests.factories import UserProfileFactory


class TestCustomTokenObtainPairView:
    """
    Тестирование получение токена
    """

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'full_name, email, password, status_code', [
            ('user_name', 'user@example.com', '123456', 400),
            ('user_name', 'user@example.com', '12pass456', 201),
            ('', 'user@example.com', '12pass456', 400),
            ('user_name', 'email', '12pass456', 400),
        ]
    )
    def test_user_registration(self, full_name, email, password, status_code, api_client):
        """
        Тестирование регистрации пользователя
        """
        url = '/auth/users/'
        data = {
            'full_name': full_name,
            'email': email,
            'password': password,
        }
        response = api_client.post(url, data=data)
        assert response.status_code == status_code

    @pytest.mark.django_db
    def test_get_jwt_token(self, api_client):
        """
        Тестирование получение jwt-токена
        """
        url = reverse('jwt-create')
        user = UserProfileFactory()
        data = {
            'email': user.email,
            'password': 'password'
        }
        response = api_client.post(url, data=data)

        assert response.status_code == 200
        assert 'refresh' in response.data
        assert 'access' in response.data






