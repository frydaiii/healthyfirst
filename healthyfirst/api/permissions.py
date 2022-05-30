from rest_framework import permissions


class PersonPermission(permissions.BasePermission):
    """
    Custom permissions
    """

    def has_object_permission(self, request, view, obj):

        # Manager permissions
        if request.user.is_manager:
            if obj.is_manager and request.user.username != obj.username:
                return False
            return True

        # Staff permissions
        if view.action == 'delete' or request.user.username != obj.username:
            return False
        if view.action in ('update', 'partial_update'):
            if any(k in request.data for k in ('username', 'id_area', 'is_manager')):
                return False
        return True
