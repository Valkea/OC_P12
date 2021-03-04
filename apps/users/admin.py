from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EpicMember

# admin.site.register(EpicMember)


@admin.register(EpicMember)
class UserAdmin(UserAdmin):
    """ Define the 'EpicMember' admin section behaviors & displays. """

    # inlines = [
    #     UserContribInline,
    # ]

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
