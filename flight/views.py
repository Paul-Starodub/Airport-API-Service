from typing import Type

from django.db.models import Count, QuerySet, F

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from airplanes.permissions import IsAdminOrIfAuthenticatedReadOnly
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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return CrewDetailSerializer

        return super().get_serializer_class()


class FlightViewSet(ModelViewSet):
    """Flight CRUD endpoints"""

    queryset = Flight.objects.prefetch_related(
        "crews__flights",
    ).select_related(
        "route__source",
        "route__destination",
        "airplane__airplane_type",
    )
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self) -> QuerySet[Flight]:
        queryset = self.queryset

        # filtering
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if first_name:
            queryset = queryset.filter(crews__first_name__iexact=first_name)

        if last_name:
            queryset = queryset.filter(crews__last_name__iexact=last_name)

        # adding available tickets
        queryset = queryset.annotate(
            tickets_available=F("airplane__rows") * F("airplane__seats_in_row")
            - Count("tickets")
        )

        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.STR,
                description="Filtering by first name (ex. ?first_name=paul)",
            ),
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.STR,
                description="Filtering by last name (ex. ?last_name=Starodub)",
            ),
        ]
    )
    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().list(request, *args, **kwargs)
