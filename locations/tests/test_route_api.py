from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError as Django_error

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError

from locations.models import Airport, Route
from locations.serializers import RouteListSerializer, RouteSerializer

ROUTE_URL = reverse("locations:route-list")


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(ROUTE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test_password"
        )
        self.client.force_authenticate(self.user)
        self.route_source = Airport.objects.create(
            name="Germany", closest_big_city="Berlin"
        )
        self.route_destination = Airport.objects.create(
            name="Poland", closest_big_city="Warshaw"
        )

    def test_str_method(self) -> None:
        route = Route.objects.create(
            source=self.route_source,
            destination=self.route_destination,
            distance=1270,
        )

        self.assertEqual(str(route), "Route #1")

    def test_list_routes(self) -> None:
        res = self.client.get(ROUTE_URL)
        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_clean_method_with_same_source_and_destination(self) -> None:
        route = Route(
            source=self.route_source,
            destination=self.route_source,
            distance=100,
        )

        with self.assertRaises(Django_error) as context:
            route.clean()

        self.assertEqual(
            context.exception.messages,
            ["Source and destination cannot be the same"],
        )

    def test_validate_method_with_same_source_and_destination(self) -> None:
        data = {
            "source": self.route_destination.id,
            "destination": self.route_destination.id,
            "distance": 100,
        }

        serializer = RouteSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            "Source and destination cannot be the same.",
            str(context.exception),
        )
