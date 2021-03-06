from rest_framework import serializers

from .models import Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):
    """ This serializer returns a translation of the Client model. """

    class Meta:
        model = Client
        fields = [
            "id",
            "company_name",
            "status",
            "sales_contact",
            "contact_first_name",
            "contact_last_name",
            "contact_email",
            "contact_mobile",
            "company_phone",
            "created_time",
            "updated_time",
        ]
