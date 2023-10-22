from django.urls import path, include
from rest_framework import routers

from orders.views import OrderViewSet

router = routers.DefaultRouter()
router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "orders"
