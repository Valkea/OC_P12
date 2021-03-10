from django_filters import rest_framework as filters

from apps.users.models import EpicMember


class EpicMemberFilter(filters.FilterSet):

    username_contains = filters.CharFilter(
        field_name="username", lookup_expr="icontains"
    )

    first_name_contains = filters.CharFilter(
        field_name="first_name", lookup_expr="icontains"
    )

    last_name_contains = filters.CharFilter(
        field_name="last_name", lookup_expr="icontains"
    )

    email_contains = filters.CharFilter(
        field_name="email", lookup_expr="icontains"
    )

    min_last_login = filters.DateFilter(field_name="last_login", lookup_expr="gte")
    max_last_login = filters.DateFilter(field_name="last_login", lookup_expr="lte")

    min_created = filters.DateFilter(field_name="created_time", lookup_expr="gte")
    max_created = filters.DateFilter(field_name="created_time", lookup_expr="lte")

    sort_by = filters.CharFilter(
        method="filter_sort_by",
        label="Sort by a given value (username, -team, etc.)",
    )

    def filter_sort_by(self, queryset, name, value):
        values = value.lower().split(",")
        return queryset.order_by(*values)

    class Meta:
        model = EpicMember
        fields = [
            "id",
            "team",
            "username",
            "username_contains",
            "first_name",
            "first_name_contains",
            "last_name",
            "last_name_contains",
            "email",
            "email_contains",
            "is_active",
            "last_login",
            "min_last_login",
            "max_last_login",
            "created_time",
            "min_created",
            "max_created",
            "sort_by",
        ]
