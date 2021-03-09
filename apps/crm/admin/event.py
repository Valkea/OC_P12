from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from apps.crm.models import Contract, Event
from apps.users.models import EpicMember
from apps.crm.permissions import CheckEventPermissions

# admin.site.register(Event)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """ Define the 'Event' admin section behaviors & displays. """

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "contract",
                    "support_contact",
                    "status",
                    "attendees",
                    "notes",
                ]
            },
        ),
        (
            "Dates",
            {
                "fields": ["start_date", "close_date", "created_time", "updated_time"],
            },
        ),
    ]

    readonly_fields = ["created_time", "updated_time"]

    list_display = (
        "name",
        "get_contract",
        "get_client",
        "status",
        "support_contact",
    )

    list_filter = ("status", "support_contact")

    search_fields = ["name", "contract__id", "contract__client__company_name"]

    def get_contract(self, obj):
        path = "admin:crm_contract_change"
        url = reverse(path, args=(obj.contract.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.contract))

    get_contract.admin_order_field = "contract"  # Allows column order sorting
    get_contract.short_description = "Associated Contract"  # Renames column head

    def get_client(self, obj):
        path = "admin:crm_client_change"
        url = reverse(path, args=(obj.contract.client.id,))
        return mark_safe(
            "<a href='{}'>{}</a>".format(url, obj.contract.client.company_name)
        )

    get_client.admin_order_field = "client"  # Allows column order sorting
    get_client.short_description = "Associated Client"  # Renames column head

    # --- CUSTOM methods ---

    def get_readonly_fields(self, request, obj=None):
        """ Apply readonly on some fields in regards to the current user """

        if request.user.team == EpicMember.Team.SELL:
            return self.readonly_fields + ["support_contact"]
        if request.user.team == EpicMember.Team.SUPPORT:
            return self.readonly_fields + ["support_contact", "contract"]
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Restict the selectbox values in regards to the current user """

        if request.user.team == EpicMember.Team.SELL:
            if db_field.name == "contract":
                kwargs["queryset"] = Contract.objects.filter(sales_contact=request.user)

        return super(EventAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    # --- EVENT ADMIN Permissions ---

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):

        if not hasattr(request.user, "team"):
            return False

        return CheckEventPermissions.has_permission_static(request, is_admin=True)

        # if request.user.is_superuser:
        #     return True

        # if request.user.team == EpicMember.Team.MANAGE:
        #     return True

        # if request.user.team == EpicMember.Team.SELL:
        #     return True

        # return False

    def has_change_delete_permission(self, request, obj=None):

        if obj is None:
            return False

        return CheckEventPermissions.has_object_permission_static(
            request, obj, is_admin=True
        )

        # if request.user.is_superuser:
        #     return True

        # if request.user.team == EpicMember.Team.MANAGE:
        #     return True

        # if request.user.team == EpicMember.Team.SELL:
        #     contract = Contract.objects.get(id=obj.contract.id)
        #     return contract.sales_contact == request.user

        # if request.user.team == EpicMember.Team.SUPPORT:
        #     return obj.support_contact == request.user

        # return False

    def has_change_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)
