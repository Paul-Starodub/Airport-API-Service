from django.views import View
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request


class IsAuthenticatedOrAnonymous(BasePermission):
    """Permissions for authorized/unauthorized users"""

    def has_permission(self, request: Request, view: View) -> bool:
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        ) or (
            request.user
            and request.user.is_authenticated
            and request.method == "POST"
            and view.action == "evaluate"
        )
