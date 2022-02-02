from rest_framework.permissions import BasePermission

from login.models import UserProfile


class AccessUserProfilePermissions(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.type_user == UserProfile.TYPE_BOOKKEEPER
        )
