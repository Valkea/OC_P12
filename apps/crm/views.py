from rest_framework import viewsets, permissions  # , status
from rest_framework.exceptions import NotFound

from .models import Client, Contract
from .serializers import ClientSerializer, ContractSerializer


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    def get_queryset(self, *args, **kwargs):
        """ Handle nested client's 'pk' in the URI """
        try:
            client_id = self.kwargs.get("client_pk")
            client = Client.objects.get(id=client_id)

            return self.queryset.filter(client=client)

        except Client.DoesNotExist:
            raise NotFound(f"Client (id:{client_id}) does not exist")
