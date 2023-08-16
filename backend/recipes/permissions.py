from rest_framework.permissions import (BasePermission)


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ('GET',)
            or request.user.is_authenticated
            and request.user.is_admin
        )


class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET',)
            or (obj.author == request.user)
        )
