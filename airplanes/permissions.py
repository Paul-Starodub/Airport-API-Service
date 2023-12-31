from rest_framework.request import Request
from rest_framework.views import View
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as an admin user,
    or is a read-only for non-admin users request.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
