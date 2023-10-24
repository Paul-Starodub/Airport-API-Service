from typing import Type

from django.db.models import QuerySet

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

    queryset = Crew.objects.prefetch_related("flights")
    serializer_class = CrewSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return CrewDetailSerializer

        return super().get_serializer_class()


class FlightViewSet(ModelViewSet):
    """Flight CRUD endpoints"""

    queryset = Flight.objects.prefetch_related("crews").select_related(
        "route__source",
        "route__destination",
        "airplane__airplane_type",
    )
    serializer_class = FlightSerializer

    def get_queryset(self) -> QuerySet[Flight]:
        queryset = self.queryset

        # filtering
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if first_name:
            queryset = queryset.filter(crews__first_name__iexact=first_name)

        if last_name:
            queryset = queryset.filter(crews__last_name__iexact=last_name)
        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return super().get_serializer_class()
