from typing import Type

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer
from airplanes.models import Airplane, AirplaneType
from airplanes.serializers import (
    AirplaneDetailSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
)


class AirplaneTypeViewSet(ModelViewSet):
    """AirplaneType CRUD endpoints"""

    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    """Airplane CRUD endpoints"""

    queryset = Airplane.objects.all()
    serializer_class = AirplaneDetailSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return AirplaneListSerializer

        return super().get_serializer_class()
