from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Return True if the request method is safe or the request user is
        the owner of the object.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
