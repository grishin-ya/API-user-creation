from rest_framework.permissions import BasePermission

class IsAdminExtended(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or getattr(user, "is_admin", False))
        )

class IsAuthenticatedOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
