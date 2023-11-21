from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.db.models import Count

from rest_framework import status
from rest_framework.test import APIClient

from locations.models import Airport
from locations.serializers import AirportListSerializer

AIRPORT_URL = reverse("locations:airport-list")


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(AIRPORT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client1 = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "testpass"
        )
        self.staff = get_user_model().objects.create_superuser(
            "testq@gmail.com", "testqpass", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.client1.force_authenticate(self.staff)

    def test_str_method(self) -> None:
        airport = Airport.objects.create(
            name="Germany", closest_big_city="Berlin"
        )

        self.assertEqual(str(airport), "Germany")

    def test_list_airports(self) -> None:
        Airport.objects.create(name="Germany", closest_big_city="Berlin")
        Airport.objects.create(name="Poland", closest_big_city="Warshaw")
        res = self.client.get(AIRPORT_URL)
        airports = Airport.objects.annotate(total_likes=Count("likes"))
        serializer = AirportListSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_airport_create(self) -> None:
        data = {"name": "Ukraine", "closest_big_city": "Lviv"}
        res = self.client1.post(AIRPORT_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 1)

    def test_update_like_view(self) -> None:
        self.client.force_login(self.user)
        self.airport = Airport.objects.create(
            name="Germany", closest_big_city="Berlin"
        )
        url = reverse(
            "locations:airport-evaluate", kwargs={"pk": self.airport.pk}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user in self.airport.likes.all())

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user in self.airport.likes.all())
