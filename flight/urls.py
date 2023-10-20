from django.urls import path, include
from rest_framework import routers

from flight.views import CrewViewSet, FlightViewSet

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "travelings"
