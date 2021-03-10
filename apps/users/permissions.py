from rest_framework import permissions

from apps.users.models import EpicMember


class CheckEpicMemberPermissions(permissions.BasePermission):
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

        if request.user.is_superuser or request.user.team == EpicMember.Team.MANAGE:
            return True

        if request.method == "POST":
            return False

        return True

    @staticmethod
    def has_object_permission_static(request, obj, is_admin=False):
        """ Define the Client's admins permissions on object level """

        if request.user.is_superuser or request.user.team == EpicMember.Team.MANAGE:
            return True

        if request.method == "DELETE":
            return False

        return request.user == obj
