from rest_framework import permissions

# from rest_framework.exceptions import NotFound, PermissionDenied

from apps.crm.admin.event import EventAdmin
from apps.users.models import EpicMember


class CheckClientPermissions(permissions.BasePermission):
    """This permission class check whether or not the current user is allowed
    to act on the provided HTTP verb (request.method), and act accondingly.
    """

    def has_permission(self, request, view):
        """ Define the Client's admins permissions on views """
        return self.has_permission_static(request)

    def has_object_permission(self, request, view, obj):
        """ Define the Client's admins permissions on object level """
        return self.has_object_permission_static(request, obj)

    # For ADMIN menus

    @staticmethod
    def has_permission_static(request, is_admin=False):
        """ Define the Client's admins permissions on views """

        if request.user.is_superuser:
            return True

        # SAFE METHODS
        if request.method in permissions.SAFE_METHODS:
            return True

        # OTHER METHODS
        if request.user.team == EpicMember.Team.MANAGE:
            return True
        elif request.user.team == EpicMember.Team.SELL:
            return True

        return False

    @staticmethod
    def has_object_permission_static(request, obj, is_admin=False):
        """ Define the Client's admins permissions on object level """

        if request.user.is_superuser:
            return True

        # SAFE METHODS
        if request.method in permissions.SAFE_METHODS:
            if is_admin and request.user.team == EpicMember.Team.SELL:
                return obj.sales_contact == request.user
            return True

        # OTHER METHODS
        if request.user.team == EpicMember.Team.MANAGE:
            return True
        elif request.user.team == EpicMember.Team.SELL:
            return obj.sales_contact == request.user

        return False


class CheckContractPermissions(permissions.BasePermission):
    """This permission class check whether or not the current user is allowed
    to act on the provided HTTP verb (request.method), and act accondingly.
    """

    def has_permission(self, request, view):
        """ Define the Contract's admins permissions on views """
        return self.has_permission_static(request)

    def has_object_permission(self, request, view, obj):
        """ Define the Contract's admins permissions on object level """
        return self.has_object_permission_static(request, obj)

    # For ADMIN menus

    @staticmethod
    def has_permission_static(request, is_admin=False):
        """ Define the Contract's admins permissions on views """

        if request.user.is_superuser:
            return True

        # SAFE METHODS
        if request.method in permissions.SAFE_METHODS:
            return True

        # OTHER METHODS
        if request.user.team == EpicMember.Team.MANAGE:
            return True
        elif request.user.team == EpicMember.Team.SELL:
            return True

        return False

    @staticmethod
    def has_object_permission_static(request, obj, is_admin=False):
        """ Define the Contract's admins permissions on object level """

        if request.user.is_superuser:
            return True

        # SAFE METHODS
        if request.method in permissions.SAFE_METHODS:
            if is_admin and request.user.team == EpicMember.Team.SELL:
                return obj.sales_contact == request.user
            return True

        # OTHER METHODS
        if request.user.team == EpicMember.Team.MANAGE:
            return True
        elif request.user.team == EpicMember.Team.SELL:
            return obj.sales_contact == request.user

        return False


class CheckEventPermissions(permissions.BasePermission):
    """This permission class check whether or not the current user is allowed
    to act on the provided HTTP verb (request.method), and act accondingly.
    """

    def has_permission(self, request, view):
        """ Define the Event's admins permissions on views """

        # print("Event :: METHOD has_permission:", request.method)

        if request.method == "POST":
            return EventAdmin.has_add_permission(self, request)

        return True

    def has_object_permission(self, request, view, obj):
        """ Define the Event's admins permissions on object level """

        # print("Event :: METHOD has_object_permission:", request.method)

        if request.method == "POST":
            return EventAdmin.has_add_permission(self, request)
        elif request.method == "DELETE" or request.method == "PUT":
            return EventAdmin.has_change_delete_permission(self, request, obj)

        return True
