from django.urls import path, include
from rest_framework import routers

from locations.views import RouteViewSet, AirportViewSet

router = routers.DefaultRouter()
router.register("routes", RouteViewSet)
router.register("airports", AirportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "locations"
