from django_filters import rest_framework as filters

from apps.crm.models import Event


class EventFilter(filters.FilterSet):
    """
    This is a filter for the :model:`crm.Event` model lists
    """

    name_contains = filters.CharFilter(field_name="name", lookup_expr="icontains")

    notes_contains = filters.CharFilter(field_name="notes", lookup_expr="icontains")

    min_attendees = filters.NumberFilter(field_name="attendees", lookup_expr="gte")
    max_attendees = filters.NumberFilter(field_name="attendees", lookup_expr="lte")

    min_start = filters.DateFilter(field_name="start_date", lookup_expr="gte")
    max_start = filters.DateFilter(field_name="start_date", lookup_expr="lte")

    min_close = filters.DateFilter(field_name="close_date", lookup_expr="gte")
    max_close = filters.DateFilter(field_name="close_date", lookup_expr="lte")

    min_created = filters.DateFilter(field_name="created_time", lookup_expr="gte")
    max_created = filters.DateFilter(field_name="created_time", lookup_expr="lte")

    sort_by = filters.CharFilter(
        method="filter_sort_by",
        label="Sort by a given value (name, -attendees, etc.)",
    )

    def filter_sort_by(self, queryset, name, value):
        values = value.lower().split(",")
        return queryset.order_by(*values)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "name_contains",
            # "contract",
            "support_contact",
            "status",
            "attendees",
            "min_attendees",
            "max_attendees",
            "notes_contains",
            "start_date",
            "min_start",
            "max_start",
            "close_date",
            "min_close",
            "max_close",
            "created_time",
            "min_created",
            "max_created",
            "sort_by",
        ]
