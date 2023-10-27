from typing import Type, Optional

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from django.db.models import Count

from locations.models import Route, Airport
from locations.permissions import IsAuthenticatedOrAnonymous
from airplanes.permissions import IsAdminOrIfAuthenticatedReadOnly
from locations.serializers import (
    RouteDetailSerializer,
    RouteListSerializer,
    AirportSerializer,
    RouteSerializer,
    AirportListSerializer,
    AirportLikeSerializer,
)


class RouteViewSet(ModelViewSet):
    """Route CRUD endpoints"""

    queryset = Route.objects.select_related("destination", "source")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return super().get_serializer_class()


class AirportViewSet(ModelViewSet):
    """Airport CRUD endpoints"""

    queryset = Airport.objects.annotate(total_likes=Count("likes")).values(
        "id", "name", "closest_big_city", "total_likes"
    )
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticatedOrAnonymous,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return AirportListSerializer

        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="change-like",
        serializer_class=AirportLikeSerializer,
    )
    def evaluate(self, request: Request, pk: Optional[int] = None) -> Response:
        """Endpoint to evaluate an airport"""

        airplane = self.get_object()
        user = self.request.user
        if user not in airplane.likes.all():
            airplane.likes.add(user)
            return Response(
                "You liked this airport", status=status.HTTP_200_OK
            )
        airplane.likes.remove(user)
        return Response("You disliked this airport", status=status.HTTP_200_OK)
