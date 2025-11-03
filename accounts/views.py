from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User, Token
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                "message": f"User {user.email} registered successfully",
                "token": token.key
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

            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "message": "Login successful",
                    "token": token.key
                })
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
