from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import EpicMember

# admin.site.register(EpicMember)
admin.site.unregister(Group)


@admin.register(EpicMember)
class UserAdmin(UserAdmin):
    """ Define the 'EpicMember' admin section behaviors & displays. """

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "email",
                    "team",
                ]
            },
        ),
        (
            "Status",
            {
                "classes": [
                    "collapse",
                ],
                "fields": ["is_active", "is_staff", "is_superuser"],
            },
        ),
        (
            "Dates",
            {
                "fields": ["date_joined", "last_login"],
            },
        ),
    ]
    readonly_fields = ["date_joined", "last_login"]

    list_display = (
        "username",
        "email",
        "team",
    )
    list_filter = (
        "is_active",
        "team",
    )
    # --- CUSTOM methods ---

    def get_readonly_fields(self, request, obj=None):
        """ Apply readonly on some fields in regards to the current user """

        if request.user.team == EpicMember.Team.MANAGE:
            return self.readonly_fields + ["is_superuser", "is_staff"]
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or request.user.team == EpicMember.Team.MANAGE:
            obj.is_staff = True
            obj.save()

    # --- EPIC MEMBER ADMIN Permissions ---

    def has_add_change_delete_permission(self, request, obj=None):

        if not hasattr(request.user, "team"):
            return False

        if request.user.is_superuser or request.user.team == EpicMember.Team.MANAGE:
            return True

        return False

    def has_view_permission(self, request, obj=None):
        return self.has_add_change_delete_permission(request, obj)

    def has_module_permission(self, request):
        return self.has_add_change_delete_permission(request)

    def has_add_permission(self, request):
        return self.has_add_change_delete_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_add_change_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_add_change_delete_permission(request, obj)
