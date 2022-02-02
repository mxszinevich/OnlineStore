from rest_framework.permissions import BasePermission

from login.models import UserProfile
from products.models import Order, Score


class CustomerOrderPermissions(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        if view.action == 'destroy':
            # Пользователю нельзя удалить уже обработанные заказы
            if obj.status != Order.STATUS_GENERATED:
                return False
        return obj.user == request.user


class EmployeeOrderPermissions(BasePermission):
    """
    Permissions доступа сотрудников к заказу
    """
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_store_employee
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        update: Обновить могут только сотрудники определенной категории
        destroy: Можно удалить только заказы со статусом "Создан"
        """
        if view.action in 'update':
            if all([status in obj.is_allowed_change_of_status(request.user.type_user) for status in (obj.status, request.data['status'])]):
                return True
            return False
        if view.action in 'destroy':
            return obj.status == Order.STATUS_GENERATED

        return True


class CheckerScorePermissions(BasePermission):

    def has_permission(self, request, view) -> bool:
        if view.action == 'create':
            return bool(request.user.type_user == UserProfile.TYPE_CHECKER)

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        action = view.action
        if action in ('list', 'retrieve'):
            return (
                    bool(request.user.type_user == UserProfile.TYPE_CHECKER)
                    or (hasattr(obj, 'order') and obj.order.user == request.user)
            )

        return False


class OrderPaymentsPermissions(BasePermission):
    """
    Permissions оплаты заказа
    """
    FULL_ACCESS_USERS_TYPES = (UserProfile.TYPE_CHECKER, UserProfile.TYPE_BOOKKEEPER)

    def has_permission(self, request, view) -> bool:
        user = request.user
        permission_list = [
            user,
            user.is_authenticated
        ]
        return all(permission_list)

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.order.user == request.user or self.is_access_users_types(request.user)

    @staticmethod
    def is_access_users_types(user):
        return bool(user.type_user in OrderPaymentsPermissions.FULL_ACCESS_USERS_TYPES)
