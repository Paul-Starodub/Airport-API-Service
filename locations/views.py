from typing import Type

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer

from locations.models import Route, Airport
from locations.serializers import (
    RouteDetailSerializer,
    RouteListSerializer,
    AirportSerializer,
)


class RouteViewSet(ModelViewSet):
    """Route CRUD endpoints"""

    queryset = Route.objects.all()
    serializer_class = RouteDetailSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return RouteListSerializer

        return super().get_serializer_class()


class AirportViewSet(ModelViewSet):
    """Airport CRUD endpoints"""

    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
