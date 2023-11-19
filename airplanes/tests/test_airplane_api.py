import io

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APIClient

from PIL import Image

from airplanes.models import Airplane, AirplaneType
from airplanes.serializers import (
    AirplaneListSerializer,
    AirplaneDetailSerializer,
)

AIRPLANE_URL = reverse("transport:airplane-list")


def detail_airplane_url(airplane_id: int) -> str:
    return reverse("transport:airplane-detail", kwargs={"pk": airplane_id})


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(AIRPLANE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client1 = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "testpass"
        )
        self.staff = get_user_model().objects.create_superuser(
            "staff@test.com", "test!pass", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.client1.force_authenticate(self.staff)
        self.type1 = AirplaneType.objects.create(name="airplane_type1")
        self.airplane = Airplane.objects.create(
            name="test1", rows=3, seats_in_row=7, airplane_type=self.type1
        )

    def test_str_method(self) -> None:
        self.assertEqual(str(self.airplane), "test1")

    def test_list_airplane(self) -> None:
        Airplane.objects.create(
            name="test4", rows=3, seats_in_row=7, airplane_type=self.type1
        )
        Airplane.objects.create(
            name="test2", rows=6, seats_in_row=8, airplane_type=self.type1
        )
        res = self.client.get(AIRPLANE_URL)
        airplanes = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplanes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_airplane_detail(self) -> None:
        url = detail_airplane_url(self.airplane.id)
        response = self.client.get(url)
        serializer = AirplaneDetailSerializer(self.airplane)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(serializer.data, response.data)

    def test_upload_image(self) -> None:
        image_stream = io.BytesIO()
        image = Image.new("RGB", (100, 100), "white")
        image.save(image_stream, format="JPEG")
        self.image_file = SimpleUploadedFile(
            "test_image.jpg", image_stream.getvalue()
        )
        self.upload_image_url = reverse(
            "transport:airplane-upload-image", kwargs={"pk": self.airplane.id}
        )
        image_data = {"image": self.image_file}

        response = self.client1.post(
            self.upload_image_url, image_data, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("image", response.data)

        self.airplane.refresh_from_db()
        self.assertIsNotNone(self.airplane.image)
