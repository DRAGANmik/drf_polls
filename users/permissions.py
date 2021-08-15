from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_staff
            or request.method == "PATCH"
            and request.user.id
        )

    def has_object_permission(self, request, view, obj):

        return obj == request.user or request.user and request.user.is_staff
