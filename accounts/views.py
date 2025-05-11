from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializers import CustomTokenObtainPairSerializer

def set_refresh_cookies(response, refresh_token):
    if refresh_token:
        response.set_cookie(
            key=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
            value=refresh_token,
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
            httponly=settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True),
            samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
            domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None),
        )
    return response

def clear_refresh_cookies(response):
    response.delete_cookie(
        key=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
        path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
        domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None),
        samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax') # Match samesite for deletion
    )
    # CSRF token is managed by Django, usually not cleared manually here
    return response

@method_decorator(ensure_csrf_cookie, "dispatch")
class LoginView(TokenObtainPairView):
    """
    Login view. Issues access token in response body and refresh token in HttpOnly cookie.
    Also ensures CSRF cookie is available.
    """

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # Basic presence check
        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Type check
        if not isinstance(username, str) or not isinstance(password, str):
            return Response({"detail": "Username and password must be strings."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")
        username = serializer.validated_data.get("username")

        response_data = {
            "access": access_token,
            "username": username
        }

        response = Response(response_data, status=status.HTTP_200_OK)
        set_refresh_cookies(response, refresh_token)

        return response
    
@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    """
    Logout view. Blacklists refresh token and clears the refresh token cookie.
    Requires CSRF token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH"))

        if not refresh_token:
            return Response({"detail": "Refresh token not found in cookie."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            if settings.SIMPLE_JWT.get('BLACKLIST_AFTER_ROTATION'):
                token.blacklist()
                response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
                clear_refresh_cookies(response)
                return response
        except TokenError:
            # Token might be invalid or already blacklisted
            response = Response({"detail": "Invalid refresh token or already logged out."}, status=status.HTTP_400_BAD_REQUEST)
            clear_refresh_cookies(response) # Still try to clear cookie
            return response
        except Exception as e:
            # Catch any other exceptions during token processing
            response = Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            clear_refresh_cookies(response)
            return response
        
@method_decorator(csrf_protect, name="dispatch")
class CustomTokenRefreshView(TokenRefreshView):
    """
    Refreshes access token using HttpOnly refresh token cookie.
    Requires CSRF token.
    If rotation is enabled, a new refresh token is also set as a cookie.
    """

    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token_from_cookie = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH'))

        if not refresh_token_from_cookie:
            return Response({"detail": "Refresh token cookie not found."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer_data = {'refresh': refresh_token_from_cookie}
        serializer = self.serializer_class(data=serializer_data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # If the original refresh token was invalid
            response = Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            clear_refresh_cookies(response)
            return response
        except Exception as e:
            return Response({"detail": "An error occurred during token refresh."}, status=status.HTTP_400_BAD_REQUEST)

        access_token = serializer.validated_data.get('access')
        new_refresh_token = serializer.validated_data.get('refresh') # If ROTATE_REFRESH_TOKENS is True

        # Prepare response data without the refresh token in the body
        response_data = {'access': access_token}

        response = Response(response_data, status=status.HTTP_200_OK)
        set_refresh_cookies(response, new_refresh_token)

        return response
    
class CustomTokenVerifyView(TokenVerifyView):
    permission_classes = [AllowAny]