from django.contrib import admin

from apps.crm.models import Status
from apps.users.models import EpicMember

# admin.site.register(Status)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """ Define the 'Status' admin section behaviors & displays. """

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "table",
                    "value",
                    "label",
                ]
            },
        ),
    ]

    list_display = (
        "get_list_label",
        "value",
        "table",
    )

    list_filter = ("table",)

    # --- CUSTOM methods ---

    def get_list_label(self, obj):
        return f"{obj.table}::{obj.label}"

    # --- STATUS ADMIN Permissions ---

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
