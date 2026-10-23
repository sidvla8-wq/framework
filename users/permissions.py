from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Пользователь — модератор (состоит в группе 'moderators')"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    """Объект принадлежит пользователю (owner поле)"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Владелец может всё, остальные — только чтение"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
