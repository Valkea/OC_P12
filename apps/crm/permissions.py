from rest_framework import permissions

# from rest_framework.exceptions import NotFound, PermissionDenied

from apps.users.models import EpicMember
from apps.crm.models import Contract


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
        return self.has_permission_static(request)

    def has_object_permission(self, request, view, obj):
        """ Define the Event's admins permissions on object level """
        return self.has_object_permission_static(request, obj)

    # For ADMIN menus

    @staticmethod
    def has_permission_static(request, is_admin=False):
        """ Define the Event's admins permissions on views """

        if request.user.is_superuser:
            return True

        # SAFE METHODS
        if request.method in permissions.SAFE_METHODS:
            return True

        # OTHER METHODS
        if request.user.team == EpicMember.Team.MANAGE:
            return True

        elif request.user.team == EpicMember.Team.SELL:

            if request.method == "DELETE":
                return True

            contract = Contract.objects.get(id=request.data["contract"])
            return contract.sales_contact == request.user

        elif request.user.team == EpicMember.Team.SUPPORT:
            return not request.method == "POST"

        return False

    @staticmethod
    def has_object_permission_static(request, obj, is_admin=False):
        """ Define the Event's admins permissions on object level """

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

            return obj.contract.sales_contact == request.user

        elif request.user.team == EpicMember.Team.SUPPORT:

            if request.method == "DELETE":
                return False

            return obj.support_contact == request.user

        return False
