from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework import generics
from accounts.permissions import IsAdmin
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, GoogleLoginSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response




class RegisterView(generics.CreateAPIView):
    
    # User Registration API
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class MeView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    permission_classes = [
        IsAdmin
    ]

# Promote/demote users
class UpdateUserRoleView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        })
    
class GoogleLoginView(generics.GenericAPIView):

    # Serializer that accepts the Google ID token
    serializer_class = GoogleLoginSerializer

    def post(self, request):

        # Validate incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract Google ID token
        google_token = serializer.validated_data["id_token"]

        try:
            # Verify that the token really came from Google
            google_user = id_token.verify_oauth2_token(
                google_token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

        except ValueError:
            return Response(
                {
                    "error": "Invalid Google token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract user information from Google's response
        email = google_user["email"]
        first_name = google_user.get("given_name", "")
        last_name = google_user.get("family_name", "")

        # Create user if it doesn't already exist
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": first_name,
                "last_name": last_name,
                "role": "student",
            }
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Google login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )