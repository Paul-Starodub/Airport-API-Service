from typing import Type

from django.db.models import QuerySet

from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import Serializer
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination

from orders.models import Order
from orders.serializers import OrderSerializer, OrderListSerializer


class OrderPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route__destination",
        "tickets__flight__route__source",
        "tickets__flight__airplane__airplane_type",
        "tickets__flight__crews",
    )

    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get_queryset(self) -> QuerySet[Order]:
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return OrderListSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)
