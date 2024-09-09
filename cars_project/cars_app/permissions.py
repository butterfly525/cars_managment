from rest_framework import permissions


# Пользовательское ограничение: если текущий пользователь не является владельцем записи, то может только просматривать эту запись
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user