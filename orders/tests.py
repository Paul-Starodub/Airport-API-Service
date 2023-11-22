from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone


from rest_framework import status
from rest_framework.test import APIClient

from airplanes.models import AirplaneType, Airplane
from flight.models import Flight
from locations.models import Airport, Route
from orders.models import Order, Ticket
from orders.serializers import OrderSerializer, TicketSerializer

ORDER_URL = reverse("orders:order-list")


class OrderAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@gmail.com",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)

        self.airport1 = Airport.objects.create(
            name="Airport_", closest_big_city="City1"
        )
        self.airport2 = Airport.objects.create(
            name="Airport2_", closest_big_city="City2"
        )
        self.route = Route.objects.create(
            source=self.airport1, destination=self.airport2, distance=100
        )
        self.airplane_type = AirplaneType.objects.create(name="Test_type_")
        self.airplane = Airplane.objects.create(
            name="Test_name",
            seats_in_row=10,
            rows=3,
            airplane_type=self.airplane_type,
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now(),
        )
        self.order_data = {
            "tickets": [{"row": 1, "seat": 1, "flight": self.flight.id}]
        }

    def test_create_order(self) -> None:
        response = self.client.post(
            ORDER_URL, data=self.order_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(
            Ticket.objects.count(), len(self.order_data["tickets"])
        )

    def test_create_order_with_invalid_ticket_data(self) -> None:
        self.order_data["tickets"][0]["row"] = 0

        response = self.client.post(
            ORDER_URL, data=self.order_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Ticket.objects.count(), 0)


class OrderSerializerTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@gmail.com",
            password="test_password",
        )
        self.client.force_authenticate(user=self.user)
        self.airport1 = Airport.objects.create(
            name="Airport_", closest_big_city="City1"
        )
        self.airport2 = Airport.objects.create(
            name="Airport2_", closest_big_city="City2"
        )
        self.route = Route.objects.create(
            source=self.airport1, destination=self.airport2, distance=100
        )
        self.airplane_type = AirplaneType.objects.create(name="Test_type_")
        self.airplane = Airplane.objects.create(
            name="Test_name",
            seats_in_row=10,
            rows=3,
            airplane_type=self.airplane_type,
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now(),
        )
        self.order_data = {
            "tickets": [{"row": 1, "seat": 1, "flight": self.flight.id}]
        }

    def test_order_serializer_with_valid_data(self) -> None:
        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())

    def test_order_serializer_with_invalid_ticket_data(self) -> None:
        ticket_data = [{"row": 0, "seat": 1, "flight": self.flight}]
        order_data = {"tickets": ticket_data}

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("tickets", serializer.errors)


class TicketSerializerTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@gmail.com",
            password="test_password",
        )
        self.client.force_authenticate(user=self.user)
        self.airport1 = Airport.objects.create(
            name="Airport_", closest_big_city="City1"
        )
        self.airport2 = Airport.objects.create(
            name="Airport2_", closest_big_city="City2"
        )
        self.route = Route.objects.create(
            source=self.airport1, destination=self.airport2, distance=100
        )
        self.airplane_type = AirplaneType.objects.create(name="Test_type_")
        self.airplane = Airplane.objects.create(
            name="Test_name",
            seats_in_row=10,
            rows=3,
            airplane_type=self.airplane_type,
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now(),
        )
        self.order_data = {
            "tickets": [{"row": 1, "seat": 1, "flight": self.flight.id}]
        }

    def test_ticket_serializer_with_valid_data(self) -> None:
        ticket_data = {"row": 1, "seat": 1, "flight": self.flight.id}

        serializer = TicketSerializer(data=ticket_data)
        self.assertTrue(serializer.is_valid())

    def test_ticket_serializer_with_invalid_data(self) -> None:
        ticket_data = {"row": 0, "seat": 1, "flight": self.flight.id}

        serializer = TicketSerializer(data=ticket_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("row", serializer.errors)
