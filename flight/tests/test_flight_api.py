from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


from rest_framework import status
from rest_framework.test import APIClient

from airplanes.models import Airplane, AirplaneType
from flight.models import Crew, Flight
from flight.serializers import FlightDetailSerializer
from locations.models import Route, Airport

FLIGHT_URL = reverse("travelings:flight-list")


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(FLIGHT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client1 = APIClient()
        self.crew = Crew.objects.create(first_name="Paul", last_name="Star")
        self.airport1 = Airport.objects.create(
            name="Airport1", closest_big_city="City1"
        )
        self.airport2 = Airport.objects.create(
            name="Airport2", closest_big_city="City2"
        )
        self.route = Route.objects.create(
            source=self.airport1, destination=self.airport2, distance=1200
        )
        self.airplane_type = AirplaneType.objects.create(name="Test_type")
        self.airplane = Airplane.objects.create(
            name="Test_name",
            seats_in_row=10,
            rows=3,
            airplane_type=self.airplane_type,
        )
        self.flight1 = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now(),
        )
        self.flight2 = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=3),
        )
        self.flight3 = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=3),
        )
        # Associate crew with the flights
        self.flight1.crews.add(self.crew)
        self.flight2.crews.add(self.crew)
        self.flight3.crews.add(self.crew)
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test_password"
        )
        self.client.force_authenticate(self.user)
        self.staff = get_user_model().objects.create_superuser(
            "test_admin@test.com", "test1_password", is_staff=True
        )
        self.client1.force_authenticate(self.staff)

    def test_str_method(self) -> None:
        self.assertEqual(str(self.flight1), f"Flight #{self.flight1.id}")

    def test_retrieve_flight_detail(self) -> None:
        url = reverse(
            "travelings:flight-detail", kwargs={"pk": self.flight1.id}
        )
        response = self.client.get(url)
        serializer = FlightDetailSerializer(self.flight1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(serializer.data, response.data)

    def test_create_flight(self) -> None:
        data = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": timezone.now(),
        }

        response = self.client.post(FLIGHT_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client1.post(FLIGHT_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_queryset_with_crew_name_filter(self) -> None:
        response = self.client.get(FLIGHT_URL, data={"first_name": "Paul"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_queryset_with_crew_last_name_filter(self) -> None:
        response = self.client.get(FLIGHT_URL, data={"last_name": "Star"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_queryset_with_combined_filters(self) -> None:
        response = self.client.get(
            FLIGHT_URL, data={"first_name": "Paul", "last_name": "Star"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
