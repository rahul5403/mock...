from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
User = get_user_model()

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_auth = JWTAuthentication()
        try:
            # print(f"Received token: {token}")
            validated_token = jwt_auth.get_validated_token(token)
            # print(f"Validated token: {validated_token}")

            user = jwt_auth.get_user(validated_token)
            # print(f"Authenticated user: {user}, is_authenticated: {user.is_authenticated}")

            # ✅ Explicitly set request.user and request.auth
            request.user = user
            request.auth = validated_token

            return user, validated_token
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            raise AuthenticationFailed("Invalid token or expired")



        