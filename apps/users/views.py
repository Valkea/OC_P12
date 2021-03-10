from rest_framework import permissions, viewsets

from .models import EpicMember
from .serializers import EpicMember_Serializer, EpicMember_DETAILS_Serializer
from .permissions import CheckEpicMemberPermissions


class EpicMember_ViewSet(viewsets.ModelViewSet):
    """
    Display :model:`users.User` instances using the EpicMemberSerializer

    These are the LIGHT user views
    """

    permission_classes = [permissions.IsAuthenticated & CheckEpicMemberPermissions]
    serializer_class = EpicMember_Serializer
    queryset = EpicMember.objects.all()


class EpicMember_Detailed_ViewSet(viewsets.ModelViewSet):
    """
    Display :model:`users.User` instances using the EpicMemberSerializer

    These are the LIGHT user views
    """

    permission_classes = [permissions.IsAuthenticated & CheckEpicMemberPermissions]
    serializer_class = EpicMember_DETAILS_Serializer
    queryset = EpicMember.objects.all()
