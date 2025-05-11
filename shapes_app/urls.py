from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserShapeViewSet

router = DefaultRouter()
router.register(r'shapes', UserShapeViewSet, basename='shape') # 'shapes' will be the URL prefix

urlpatterns = [
    path('', include(router.urls)),
]
