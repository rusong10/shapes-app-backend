from rest_framework import viewsets
from .models import UserShape
from .serializers import UserShapeSerializer
from .permissions import IsAdminUserOrReadOnly # Import your custom permission

class UserShapeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user shapes to be:
    - Listed and retrieved by anyone.
    - Created, updated, and deleted only by admin users.
    """
    queryset = UserShape.objects.all().order_by('-created_at')
    serializer_class = UserShapeSerializer
    permission_classes = [IsAdminUserOrReadOnly] # Use the custom permission
