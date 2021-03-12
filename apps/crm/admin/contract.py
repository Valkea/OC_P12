from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import messages

from apps.crm.models import Client, Contract, Event
from apps.users.models import EpicMember
from apps.crm.permissions import CheckContractPermissions

# admin.site.register(Contract)


class ContractEventsInline(admin.TabularInline):
    """
    Inline for displaying the events of the contract directly on it's admin page.
    """

    model = Event
    fk_name = "contract"

    extra = 0

    verbose_name = "Event"
    verbose_name_plural = "Events"

    readonly_fields = [
        "name",
        "support_contact",
        "status",
        "attendees",
        "notes",
        "start_date",
        "close_date",
        "created_time",
        "updated_time",
    ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_view_permission(self, request, obj=None):
        return True


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """ Define the 'Contract' admin section behaviors & displays. """

    inlines = [ContractEventsInline]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "client",
                    "sales_contact",
                    "status",
                    "amount",
                ]
            },
        ),
        (
            "Dates",
            {
                "fields": ["payment_date", "created_time", "updated_time"],
            },
        ),
    ]

    readonly_fields = ["created_time", "updated_time"]

    list_display = (
        "get_contract",
        "get_client",
        "status",
        "sales_contact",
    )

    list_filter = ("status", "sales_contact")

    search_fields = ["id", "client__company_name"]

    def get_contract(self, obj):
        return obj

    def get_client(self, obj):
        path = "admin:crm_client_change"
        url = reverse(path, args=(obj.client.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.client.company_name))

    get_client.admin_order_field = "client"  # Allows column order sorting
    get_client.short_description = "Associated Client"  # Renames column head

    # --- CUSTOM methods ---

    def get_readonly_fields(self, request, obj=None):
        """ Apply readonly on some fields in regards to the current user """

        if request.user.team in [EpicMember.Team.SELL, EpicMember.Team.SUPPORT]:
            return self.readonly_fields + ["sales_contact"]
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Restict the selectbox values in regards to the current user """

        if request.user.team == EpicMember.Team.SELL:
            if db_field.name == "client":
                t = Client.objects.filter(sales_contact=request.user)
                kwargs["queryset"] = t
            if db_field.name == "sales_contact":
                t = EpicMember.objects.filter(id=request.user.id)
                kwargs["queryset"] = t

        return super(ContractAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def save_model(self, request, obj, form, change):
        if request.user.team == EpicMember.Team.SELL:
            client = Client.objects.get(id=obj.client.id)
            if not client.sales_contact == request.user:
                return messages.error(request, "This is not your client")
            obj.sales_contact = request.user
        obj.save()

    # --- CONTRACT ADMIN Permissions ---

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):

        if not hasattr(request.user, "team"):
            return False

        return CheckContractPermissions.has_permission_static(request, is_admin=True)

    def has_change_delete_permission(self, request, obj=None):

        if not hasattr(request.user, "team"):
            return False

        if request.user.is_superuser:
            return True
        elif request.user.team == EpicMember.Team.MANAGE:
            return True
        elif request.user.team == EpicMember.Team.SELL:
            if obj is None:
                return False
            return obj.sales_contact == request.user
        elif request.user.team == EpicMember.Team.SUPPORT:
            return False

        return False

        # if obj is None:
        #     return False

        # return CheckContractPermissions.has_object_permission_static(
        #     request, obj, is_admin=True
        # )

    def has_change_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)
