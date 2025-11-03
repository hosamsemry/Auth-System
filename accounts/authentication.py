from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import Token

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token_key = request.headers.get("Authorization")
        if not token_key:
            return None

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token")

        if token.is_expired():
            raise exceptions.AuthenticationFailed("Token expired")

        return (token.user, token)
