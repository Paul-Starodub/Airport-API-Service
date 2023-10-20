from typing import Type

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer

from flight.models import Crew, Flight
from flight.serializers import (
    CrewSerializer,
    FlightSerializer,
    FlightDetailSerializer,
    FlightListSerializer,
    CrewDetailSerializer,
)


class CrewViewSet(ModelViewSet):
    """Crew CRUD endpoints"""

    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return CrewDetailSerializer

        return super().get_serializer_class()


class FlightViewSet(ModelViewSet):
    """Flight CRUD endpoints"""

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return super().get_serializer_class()
