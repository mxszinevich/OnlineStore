from rest_framework import routers

from login.views import UserProfileView


router = routers.SimpleRouter()
router.register('', UserProfileView)

urlpatterns = []
urlpatterns += router.urls
