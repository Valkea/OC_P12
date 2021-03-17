from django_filters import rest_framework as filters

from apps.crm.models import Client


class ClientFilter(filters.FilterSet):
    """
    This is a filter for the :model:`crm.Client` model lists
    """

    company_name_contains = filters.CharFilter(
        field_name="company_name", lookup_expr="icontains"
    )

    contact_first_name_contains = filters.CharFilter(
        field_name="contact_first_name", lookup_expr="icontains"
    )
    contact_last_name_contains = filters.CharFilter(
        field_name="contact_last_name", lookup_expr="icontains"
    )
    contact_email_contains = filters.CharFilter(
        field_name="contact_email", lookup_expr="icontains"
    )

    min_created = filters.DateFilter(field_name="created_time", lookup_expr="gte")
    max_created = filters.DateFilter(field_name="created_time", lookup_expr="lte")

    sort_by = filters.CharFilter(
        method="filter_sort_by",
        label="Sort by a given value (company_name, -status, etc.)",
    )

    def filter_sort_by(self, queryset, name, value):
        values = value.lower().split(",")
        return queryset.order_by(*values)

    class Meta:
        model = Client
        fields = [
            "id",
            "company_name",
            "company_name_contains",
            "status",
            "sales_contact",
            "contact_first_name",
            "contact_first_name_contains",
            "contact_last_name",
            "contact_last_name_contains",
            "contact_email",
            "contact_email_contains",
            "contact_mobile",
            "company_phone",
            "created_time",
            "min_created",
            "max_created",
            "sort_by",
        ]
