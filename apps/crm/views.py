from rest_framework import viewsets, permissions  # , status
from rest_framework.exceptions import NotFound, PermissionDenied
from django_filters import rest_framework as filters

from apps.users.models import EpicMember
from .models import Client, Contract, Event, Status
from .serializers import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
    StatusSerializer,
)
from .permissions import (
    CheckClientPermissions,
    CheckContractPermissions,
    CheckEventPermissions,
)

from .filters import ClientFilter, ContractFilter, EventFilter


class StatusViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ["id", "table", "value", "label"]


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.IsAuthenticated & CheckClientPermissions)]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ClientFilter
    # filterset_fields = ['company_name', 'status']

    def create_or_update(self, request):
        """ Custom method used to setup the Client's Foreign-keys (sales_contact) """

        if request.user.team == EpicMember.Team.SELL:
            if hasattr(request.data, "_mutable"):
                request.data._mutable = True
            request.data.update({"sales_contact": request.user.id})

        elif request.user.team in ["", EpicMember.Team.SUPPORT]:
            raise PermissionDenied("You aren't allowed to do that")

        return request

    def create(self, request, *args, **kwargs):
        new_request = self.create_or_update(request)
        return super().create(new_request, args, kwargs)

    def update(self, request, *args, **kwargs):
        new_request = self.create_or_update(request)
        return super().update(new_request, args, kwargs)


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.IsAuthenticated & CheckContractPermissions)]
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContractFilter

    def get_queryset(self, *args, **kwargs):
        """ Handle nested Client's 'pk' in the URI """
        try:
            client_id = self.kwargs.get("client_pk")
            client = Client.objects.get(id=client_id)

            return self.queryset.filter(client=client)

        except Client.DoesNotExist:
            raise NotFound(f"Client (id:{client_id}) does not exist")

    def create_or_update(self, request):
        """ Custom method used to setup the Contract's Foreign-keys (sales_contact) """

        if request.user.team == EpicMember.Team.SELL:

            try:
                # client_id = request.data['client']
                client_id = self.kwargs.get("client_pk")
                client = Client.objects.get(id=client_id)

                if client.sales_contact != request.user:
                    raise ValueError("This is not your client")

                if hasattr(request.data, "_mutable"):
                    request.data._mutable = True
                request.data.update({"client": client_id})
                request.data.update({"sales_contact": request.user.id})

            except Client.DoesNotExist:
                raise NotFound(f"A Client with id {client_id} does not exist")
            except ValueError as e:
                raise PermissionDenied(e)

        elif request.user.team in ["", EpicMember.Team.SUPPORT]:
            raise PermissionDenied("You aren't allowed to do that")

        return request

    def create(self, request, *args, **kwargs):
        new_request = self.create_or_update(request)
        return super().create(new_request, args, kwargs)

    def update(self, request, *args, **kwargs):
        new_request = self.create_or_update(request)
        return super().update(new_request, args, kwargs)


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.IsAuthenticated & CheckEventPermissions)]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    def get_queryset(self, *args, **kwargs):
        """ Handle nested Client's and Contract's 'pk' in the URI """
        try:
            client_id = self.kwargs.get("client_pk")
            Client.objects.get(id=client_id)

            contract_id = self.kwargs.get("contract_pk")
            contract = Contract.objects.get(id=contract_id, client=client_id)

            return self.queryset.filter(contract=contract)

        except Client.DoesNotExist:
            raise NotFound(f"Client (id:{client_id}) does not exist")
        except Contract.DoesNotExist:
            raise NotFound(
                f"Contract (id:{contract_id}) does not exist for Client (id:{client_id})"
            )

    def create_or_update(self, request):
        """ Custom method used to setup the Event's Foreign-keys (sales_contact) """

        if request.user.team == EpicMember.Team.SELL:

            if hasattr(request.data, "_mutable"):
                request.data._mutable = True
            request.data.pop("support_contact", None)

        elif request.user.team == EpicMember.Team.SUPPORT:

            if hasattr(request.data, "_mutable"):
                request.data._mutable = True
            request.data.pop("support_contact", None)
            event = Event.objects.get(id=self.kwargs.get("pk"))
            request.data.update({"contract": event.contract.id})

        elif request.user.team == "":
            raise PermissionDenied("You aren't allowed to do that")

        return request

    def create(self, request, *args, **kwargs):
        new_request = self.create_or_update(request)
        return super().create(new_request, args, kwargs)

    def update(self, request, *args, **kwargs):
        new_request = self.create_or_update(request)
        return super().update(new_request, args, kwargs)
