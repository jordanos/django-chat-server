from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "Access Denied: Owner user only"

    def has_object_permission(self, request, view, obj):
        return bool(obj.owner.id == request.user.id)
