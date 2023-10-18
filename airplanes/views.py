from rest_framework.viewsets import ModelViewSet
from airplanes.models import Airplane, AirplaneType
from airplanes.serializers import AirplaneSerializer, AirplaneTypeSerializer


class AirplaneTypeViewSet(ModelViewSet):
    """AirplaneType CRUD endpoints"""

    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    """Airplane CRUD endpoints"""

    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
