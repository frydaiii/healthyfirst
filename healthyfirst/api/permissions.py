from rest_framework import permissions


class PersonPermission(permissions.BasePermission):
    """
    Custom permissions for Person table
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


class PremisePermission(permissions.BasePermission):
    """
    Custom permissions for Premise table
    """

    def has_permission(self, request, view):
        if any(k in view.action for k in ('list', 'retrieve')):
            return True
        return request.user.is_manager


class CertificatePermission(permissions.BasePermission):
    """
    Custom permissions for Certificate table
    """

    def has_permission(self, request, view):
        return request.user.is_manager


class BusinessTypePermission(permissions.BasePermission):
    """
    Custom permissions for Certificate table
    """

    def has_permission(self, request, view):
        return request.user.is_manager


class InspectionPlanPermission(permissions.BasePermission):
    """
    Custom permissions for InspectionPlan table
    """

    def has_permission(self, request, view):
        return True


class SamplePermission(permissions.BasePermission):
    """
    Custom permissions for Sample table
    """

    def has_permission(self, request, view):
        return True


class AreaPermission(permissions.BasePermission):
    """
    Custom permissions for Certificate table
    """

    def has_permission(self, request, view):
        return request.user.is_manager

