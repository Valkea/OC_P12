from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import messages

from .models import Client, Contract, Event
from apps.users.models import EpicMember

# admin.site.register(Client)
# admin.site.register(Contract)
# admin.site.register(Event)


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

        if request.user.is_superuser:
            return True

        if request.user.team == EpicMember.Team.MANAGE:
            return True

        elif request.user.team == EpicMember.Team.SELL:
            return True

        return False

    def has_change_delete_permission(self, request, obj=None):

        if obj is None:
            return False

        if request.user.is_superuser:
            return True

        if request.user.team == EpicMember.Team.MANAGE:
            return True

        elif request.user.team == EpicMember.Team.SELL:
            return obj.sales_contact == request.user

        return False

    def has_change_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)


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
                return messages.error(request, "You can only contracts to your clients")
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

        if request.user.is_superuser:
            return True

        if request.user.team == EpicMember.Team.MANAGE:
            return True

        elif request.user.team == EpicMember.Team.SELL:
            return True

        return False

    def has_change_delete_permission(self, request, obj=None):

        if obj is None:
            return False

        if request.user.is_superuser:
            return True

        if request.user.team == EpicMember.Team.MANAGE:
            return True

        elif request.user.team == EpicMember.Team.SELL:
            return obj.sales_contact == request.user

        return False

    def has_change_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """ Define the 'Event' admin section behaviors & displays. """

    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         queryset = Event.objects.all()
    #     else:
    #         # queryset = Event.objects.filter(venue__admin_group__in=request.user.groups.all())
    #         queryset = Event.objects.filter(support_contact=request.user)
    #     return queryset

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

        if request.user.is_superuser:
            return True

        if request.user.team == EpicMember.Team.MANAGE:
            return True

        if request.user.team == EpicMember.Team.SELL:
            return True

        return False

    def has_change_delete_permission(self, request, obj=None):

        if obj is None:
            return False

        if request.user.is_superuser:
            return True

        if request.user.team == EpicMember.Team.MANAGE:
            return True

        if request.user.team == EpicMember.Team.SELL:
            contract = Contract.objects.get(id=obj.contract.id)
            return contract.sales_contact == request.user

        if request.user.team == EpicMember.Team.SUPPORT:
            return obj.support_contact == request.user

        return False

    def has_change_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_delete_permission(request, obj)
