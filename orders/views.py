from typing import Type

from django.db.models import QuerySet

from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import Serializer
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializers import OrderSerializer, OrderListSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route",
        "tickets__flight__airplane",
        "tickets__flight__crews",
    )

    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Order]:
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return OrderListSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)
