from django.urls import path, include
from rest_framework import routers

from airplanes.views import AirplaneTypeViewSet, AirplaneViewSet

router = routers.DefaultRouter()
router.register("types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "transport"
