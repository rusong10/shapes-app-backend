from rest_framework.routers import DefaultRouter
from .views import ShapeViewSet

router = DefaultRouter()
router.register(r'', ShapeViewSet, basename='shape')

urlpatterns = router.urls
