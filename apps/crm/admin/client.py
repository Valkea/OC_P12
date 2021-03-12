from django.contrib import admin

from apps.crm.models import Client, Contract
from apps.users.models import EpicMember
from apps.crm.permissions import CheckClientPermissions

# admin.site.register(Client)


class ClientContractsInline(admin.TabularInline):
    """
    Inline for displaying the contracts of the client directly on it's admin page.
    """

    model = Contract
    fk_name = "client"

    extra = 0

    verbose_name = "Contract"
    verbose_name_plural = "Contracts"

    readonly_fields = [
        "sales_contact",
        "status",
        "amount",
        "payment_date",
        "created_time",
        "updated_time",
    ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_view_permission(self, request, obj=None):
        return True


# class ClientEventsInline(admin.TabularInline):
#     """
#     Inline for displaying the events of the company directly on it's admin page.
#     """
#
#     model = Event
#     fk_name = "contract__client"
#
#     extra = 0
#
#     verbose_name = "Event"
#     verbose_name_plural = "Events"
#
#     readonly_fields = [
#         "name",
#         "contract",
#         "support_contact",
#         "status",
#         "attendees",
#         "notes",
#         "start_date",
#         "close_date",
#         "created_time",
#         "updated_time",
#     ]
#
#     def has_add_permission(self, *args, **kwargs):
#         return True
#
#     def has_delete_permission(self, *args, **kwargs):
#         return True


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Define the 'Client' admin section behaviors & displays. """

    inlines = [ClientContractsInline]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "company_name",
                    "status",
                    "sales_contact",
                    "contact_first_name",
                    "contact_last_name",
                    "contact_email",
                    "contact_mobile",
                    "company_phone",
                ]
            },
        ),
        (
            "Dates",
            {
                "fields": ["created_time", "updated_time"],
            },
        ),
    ]

    readonly_fields = ["created_time", "updated_time"]

    search_fields = [
        "company_name",
        "contact_first_name",
        "contact_last_name",
        "contact_email",
        "contact_mobile",
        "company_phone",
    ]

    list_display = (
        "company_name",
        "status",
        "sales_contact",
    )

    list_filter = ("status", "sales_contact")

    # --- CUSTOM methods ---

    def get_readonly_fields(self, request, obj=None):
        """ Apply readonly on some fields in regards to the current user """

        if request.user.team in [EpicMember.Team.SELL, EpicMember.Team.SUPPORT]:
            return self.readonly_fields + ["sales_contact"]
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Restict the selectbox values in regards to the current user """

        if request.user.team == EpicMember.Team.SELL:
            if db_field.name == "sales_contact":
                t = EpicMember.objects.filter(id=request.user.id)
                kwargs["queryset"] = t

        return super(ClientAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def save_model(self, request, obj, form, change):

        if request.user.team == EpicMember.Team.SELL:
            obj.sales_contact = request.user

        obj.save()

    # --- CLIENT ADMIN Permissions ---

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):

        if not hasattr(request.user, "team"):
            return False

        return CheckClientPermissions.has_permission_static(request, is_admin=True)

    def has_change_delete_permission(self, request, obj=None):

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

        # return CheckClientPermissions.has_object_permission_static(
        #     request, obj, is_admin=True
        # )

    def has_change_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)

        

