from rest_framework import serializers

from .models import Client, Contract, Event, Status


class StatusSerializer(serializers.ModelSerializer):
    """ This serializer returns a translation of the Status model. """

    class Meta:
        model = Status
        fields = [
            "id",
            "table",
            "value",
            "label",
        ]


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


class ContractSerializer(serializers.ModelSerializer):
    """ This serializer returns a translation of the Contract model. """

    class Meta:
        model = Contract
        fields = [
            "id",
            "client",
            "sales_contact",
            "status",
            "amount",
            "payment_date",
            "created_time",
            "updated_time",
        ]


class EventSerializer(serializers.ModelSerializer):
    """ This serializer returns a translation of the Event model. """

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "contract",
            "support_contact",
            "status",
            "attendees",
            "notes",
            "start_date",
            "close_date",
            "created_time",
            "updated_time",
        ]
