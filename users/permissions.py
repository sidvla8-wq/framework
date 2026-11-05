# from rest_framework import permissions
#
#
# class IsModer(permissions.BasePermission):
#     """Пользователь — модератор (состоит в группе 'moderators')"""
#
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
#         return request.user.groups.filter(name="moderators").exists()
#
#
# class IsOwner(permissions.BasePermission):
#     """Объект принадлежит пользователю (owner поле)"""
#
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


# Модератор — участник группы "moderators"
def is_moderator(user):
    return user.is_authenticated and user.groups.filter(name='moderators').exists()


class IsModer(permissions.BasePermission):
    """Разрешает доступ только модераторам"""
    def has_permission(self, request, view):
        return is_moderator(request.user)


class IsOwner(permissions.BasePermission):
    """Разрешает доступ только владельцу объекта"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerOrOwner(BasePermission):
    """Модератор ИЛИ владелец объекта — заменяет IsModer() | IsOwner()"""
    def has_permission(self, request, view):
        # на уровне списка достаточно быть авторизованным
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if is_moderator(request.user):
            return True
        return getattr(obj, 'owner', None) == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Чтение всем, изменение — только владельцу"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, 'owner', None) == request.user
