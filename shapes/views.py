from rest_framework import viewsets
from .models import Shape
from .serializers import ShapeSerializer
from .permissions import IsAdminOrReadOnly

class ShapeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shapes to be:
    - Listed and retrieved by anyone.
    - Created, updated, and deleted only by admin users.
    """

    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer
    permission_classes = [IsAdminOrReadOnly]
