from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUserOrReadOnly(BasePermission):
    """
    Allows read-only access to any user (authenticated or not).
    Allows full access only to admin users (is_staff=True).
    """

    def has_permission(self, request, view):
        # Allow all GET, HEAD, OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff
