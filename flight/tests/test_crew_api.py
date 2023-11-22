from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from flight.models import Crew
from flight.serializers import CrewDetailSerializer

CREW_URL = reverse("travelings:crew-list")


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(CREW_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client1 = APIClient()
        self.crew = Crew.objects.create(first_name="Paul", last_name="Star")
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test_password"
        )
        self.client.force_authenticate(self.user)
        self.user = get_user_model().objects.create_user(
            "test_admin@test.com", "test_password", is_staff=True
        )
        self.client1.force_authenticate(self.user)

    def test_str_method(self) -> None:
        self.assertEqual(str(self.crew), "Person: Paul Star")

    def test_retrieve_crew_detail(self) -> None:
        url = reverse("travelings:crew-detail", kwargs={"pk": self.crew.id})
        response = self.client.get(url)
        serializer = CrewDetailSerializer(self.crew)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(serializer.data, response.data)

    def test_create_crew(self) -> None:
        data = {"first_name": "Cat", "last_name": "Red"}

        response = self.client.post(CREW_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client1.post(CREW_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
