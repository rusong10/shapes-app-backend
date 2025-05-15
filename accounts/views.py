from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import UserSerializer

def set_refresh_cookies(response, refresh_token):
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=getattr(settings, 'SIMPLE_JWT', {}).get('AUTH_COOKIE_SECURE'),
        samesite='Lax',
        path='/api/accounts/',
        max_age=getattr(settings, 'SIMPLE_JWT', {}).get('REFRESH_TOKEN_LIFETIME').total_seconds()
    )
    return response

class LoginView(APIView):
    """
    Login view. Issues access token in response body and refresh token in HttpOnly cookie.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            refresh = RefreshToken.for_user(user)
            response = Response({
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'is_staff': user.is_staff,
                },
                'detail': 'Login successful.'
            }, status=status.HTTP_200_OK)

            set_refresh_cookies(response, refresh)
            return response
        
        return Response(
            {'detail': 'Invalid credentials.'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    """
    Logout view. Blacklists refresh token and deletes the refresh token cookie.
    """
    
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'detail': 'No refresh token provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(
                {'detail': 'Logged out successfully.'},
                status=status.HTTP_200_OK
            )
        except Exception:
            response = Response(
                {'detail': 'Invalid or already blacklisted token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        response.delete_cookie('refresh_token', '/api/accounts/')
        return response

class CustomTokenRefreshView(TokenRefreshView):
    """
    Refreshes access token using HttpOnly refresh token cookie. 
    A new refresh token replaces the old cookie.
    """
     
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'detail': 'No refresh token provided.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            # DRF ValidationError detail is a dict
            detail = exc.detail
            if isinstance(detail, dict):
                detail = " ".join(
                    f"{k}: {' '.join(map(str, v)) if isinstance(v, list) else v}"
                    for k, v in detail.items()
                )

            return Response(
                {'detail': detail or 'Invalid refresh token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = serializer.validated_data
        access = data.get('access')
        new_refresh = data.get('refresh')

        response = Response({'access': access})

        if new_refresh:
            set_refresh_cookies(response, new_refresh)

        return response

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
