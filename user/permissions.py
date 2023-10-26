from django.views import View
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request


class IsAuthenticatedOrAnonymous(BasePermission):
    """Permissions for authorized/unauthorized users"""

    def has_permission(self, request: Request, view: View) -> bool:
        if request.user.is_anonymous and request.method not in SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
