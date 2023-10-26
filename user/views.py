from rest_framework import generics

from user.models import User
from user.permissions import IsAuthenticatedOrAnonymous
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrAnonymous,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user
