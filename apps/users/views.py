from rest_framework import permissions, viewsets
from django_filters import rest_framework as filters

from .models import EpicMember
from .serializers import EpicMember_Serializer, EpicMember_DETAILS_Serializer
from .permissions import CheckEpicMemberPermissions
from .filters import EpicMemberFilter


class EpicMember_ViewSet(viewsets.ModelViewSet):
    """
    Display :model:`users.User` instances using the EpicMemberSerializer

    These are the PARTIAL (light) user views
    """

    permission_classes = [permissions.IsAuthenticated & CheckEpicMemberPermissions]
    serializer_class = EpicMember_Serializer
    queryset = EpicMember.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EpicMemberFilter


class EpicMember_Detailed_ViewSet(viewsets.ModelViewSet):
    """
    Display :model:`users.User` instances using the EpicMember_DETAILS_Serializer

    These are the DETAILED (not full) user views
    """

    permission_classes = [permissions.IsAuthenticated & CheckEpicMemberPermissions]
    serializer_class = EpicMember_DETAILS_Serializer
    queryset = EpicMember.objects.all()
