from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, routers

from login.views import CustomTokenObtainPairView

schema_view = get_schema_view(
   openapi.Info(
      title="OnlineStore API",
      default_version='v1',
      description="API тестового задания OnlineStore",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/users/', include('login.urls')),
    path('api/store/', include('products.urls')),
    path('auth/jwt/create', CustomTokenObtainPairView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

