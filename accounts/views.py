from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User, Token
from .serializers import RegisterSerializer, LoginSerializer
from django.core.mail import send_mail
from django.core.cache import cache
import uuid

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                "message": "User registered successfully",
                "access_token": token.key,
                "refresh_token": token.refresh_key,
                "expires_at": token.expires_at
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            token, created = Token.objects.get_or_create(user=user)

            if token.is_expired():
                token.refresh()

            return Response({
                "message": "Login successful",
                "access_token": token.key,
                "refresh_token": token.refresh_key,
                "expires_at": token.expires_at
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        token_key = request.headers.get("Authorization")
        if not token_key:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            return Response({"message": "Logged out successfully"})
        except Token.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(refresh_key=refresh_token)
        except Token.DoesNotExist:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        token.refresh()
        return Response({
            "access_token": token.key,
            "refresh_token": token.refresh_key,
            "expires_at": token.expires_at
        })

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No user with this email"}, status=status.HTTP_400_BAD_REQUEST)

        reset_code = str(uuid.uuid4())[:8]  # short code
        cache.set(f"reset_{email}", reset_code, timeout=600)

        send_mail(
            "Password Reset Code",
            f"Your password reset code is: {reset_code}",
            "noreply@example.com",
            [email],
            fail_silently=True
        )

        return Response({"message": "Password reset code sent to email"})

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        new_password = request.data.get("new_password")

        saved_code = cache.get(f"reset_{email}")
        if saved_code != code:
            return Response({"error": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            cache.delete(f"reset_{email}")
            return Response({"message": "Password reset successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
 
class MeView(APIView):
    def get(self, request):
        token_key = request.headers.get("Authorization")
        if not token_key:
            return Response({"error": "No token provided"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            return Response({
                "email": user.email,
                "username": user.username
            })
        except Token.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)