from factory import (
    Faker,
    LazyAttribute,
    PostGenerationMethodCall
)
from factory.django import DjangoModelFactory

from login.models import UserProfile


class UserProfileFactory(DjangoModelFactory):
    """
    Фабрика модели пользователя
    """
    full_name = Faker('name')
    is_active = True
    is_admin = False
    type_user = UserProfile.TYPE_SHOPPER
    email = LazyAttribute(lambda obj: f'{obj.full_name.replace(" ", "_").lower()}@email.com')
    password = PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = UserProfile
