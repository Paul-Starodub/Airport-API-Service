from typing import Type, Optional

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer
from airplanes.models import Airplane, AirplaneType
from rest_framework.permissions import IsAdminUser
from airplanes.permissions import IsAdminOrIfAuthenticatedReadOnly
from airplanes.serializers import (
    AirplaneDetailSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    AirplaneSerializer,
    AirplaneImageSerializer,
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

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
        serializer_class=AirplaneImageSerializer,
    )
    def upload_image(
        self, request: Request, pk: Optional[int] = None
    ) -> Response:
        """Endpoint to uploading image to specific airplane"""

        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
