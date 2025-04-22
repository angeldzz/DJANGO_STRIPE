# base/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Verifica si el modelo tiene un campo 'user' o 'user_profile' para determinar el propietario
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'user_profile'):
            return obj.user_profile.user == request.user
        return False