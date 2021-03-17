from django_filters import rest_framework as filters

from apps.crm.models import Contract


class ContractFilter(filters.FilterSet):
    """
    This is a filter for the :model:`crm.Contract` model lists
    """

    min_amount = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr="lte")

    min_paydate = filters.DateFilter(field_name="payment_date", lookup_expr="gte")
    max_paydate = filters.DateFilter(field_name="payment_date", lookup_expr="lte")

    min_created = filters.DateFilter(field_name="created_time", lookup_expr="gte")
    max_created = filters.DateFilter(field_name="created_time", lookup_expr="lte")

    sort_by = filters.CharFilter(
        method="filter_sort_by",
        label="Sort by a given value (status, -amount, etc.)",
    )

    def filter_sort_by(self, queryset, name, value):
        values = value.lower().split(",")
        return queryset.order_by(*values)

    class Meta:
        model = Contract
        fields = [
            "id",
            # "client",
            "sales_contact",
            "status",
            "amount",
            "min_amount",
            "max_amount",
            "payment_date",
            "min_paydate",
            "max_paydate",
            "created_time",
            "min_created",
            "max_created",
            "sort_by",
        ]
