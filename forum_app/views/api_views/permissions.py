from rest_framework import permissions
from forum_app.models import CustomUser


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, CustomUser):
            if request.method == 'DELETE':
                return obj == request.user or bool(request.user and request.user.is_staff)

            return obj == request.user

        if request.method == 'DELETE':
            return obj.user == request.user or bool(request.user and request.user.is_staff)

        return obj.user == request.user
