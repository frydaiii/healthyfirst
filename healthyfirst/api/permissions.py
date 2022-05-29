from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager()


class ViewOwnResource(permissions.BasePermission):
    """
    Permission class to check that a user can view his own resource only
    """

    def has_permission(self, request, view):
        if view.action == 'retrieve' and view.kwargs['username'] != request.user.username:
            return False  # not grant access
        return True  # grant access otherwise
