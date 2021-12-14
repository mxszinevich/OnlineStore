from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from login.models import UserProfile
from login.permissions import AccessUserProfilePermissions
from login.serializers import UserProfileSerializer, CustomTokenObtainPairSerializer


class UserProfileView(viewsets.ReadOnlyModelViewSet):
    """
    Представление для отображения пользователей
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AccessUserProfilePermissions]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Представление для получение токена
    """
    serializer_class = CustomTokenObtainPairSerializer