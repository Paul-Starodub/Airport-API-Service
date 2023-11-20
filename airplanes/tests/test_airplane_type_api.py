from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from airplanes.models import AirplaneType
from airplanes.serializers import AirplaneTypeSerializer

AIRPLANE_TYPE_URL = reverse("transport:airplanetype-list")


class UnauthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_list_airplane_type(self) -> None:
        AirplaneType.objects.create(name="airplane_type1")
        AirplaneType.objects.create(name="airplane_type2")
        res = self.client.get(AIRPLANE_TYPE_URL)
        airplane_types = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_types, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_str_method(self) -> None:
        airplane_type = AirplaneType.objects.create(name="airplane_type1")

        self.assertEqual(str(airplane_type), "airplane_type1")
