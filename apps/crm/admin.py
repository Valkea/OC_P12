from django.contrib import admin

from .models import Client, Contract, Event

# admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Define the 'Client' admin section behaviors & displays. """

    # inlines = [UserContribInline, UserIssuesInline]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "compagny_name",
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

    list_display = (
        "compagny_name",
        "status",
        "sales_contact",
    )

    list_filter = ("status", "sales_contact")
