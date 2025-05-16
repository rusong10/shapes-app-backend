from django.urls import path
from .views import LoginView, LogoutView, CustomTokenRefreshView, CustomTokenVerifyView, MeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('me/', MeView.as_view(), name='me'),
]
