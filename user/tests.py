from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.create_user_url = reverse("user:create")
        self.manage_user_url = reverse("user:manage")

        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }

    def test_create_user(self) -> None:
        response = self.client.post(
            self.create_user_url,
            data=self.user_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

        user = get_user_model().objects.first()

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_create_user_invalid_password(self) -> None:
        user_data = {"email": "test@example.com", "password": "test"}
        response = self.client.post(self.create_user_url, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_manage_user(self) -> None:
        user = get_user_model().objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        updated_data = {"email": "newemail@example.com"}
        response = self.client.patch(self.manage_user_url, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, updated_data["email"])

    def test_manage_user_unauthenticated(self) -> None:
        response = self.client.get(self.manage_user_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
