from typing import Type

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer
from airplanes.models import Airplane, AirplaneType
from airplanes.permissions import IsAdminOrIfAuthenticatedReadOnly
from airplanes.serializers import (
    AirplaneDetailSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    AirplaneSerializer,
)


class AirplaneTypeViewSet(ModelViewSet):
    """AirplaneType CRUD endpoints"""

    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(ModelViewSet):
    """Airplane CRUD endpoints"""

    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return AirplaneListSerializer

        if self.action == "retrieve":
            return AirplaneDetailSerializer

        return super().get_serializer_class()
