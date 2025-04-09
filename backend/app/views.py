from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ninja import NinjaAPI
from .auth import JWTAuth
from .schemas import UserCreate, TokenResponse
from pydantic import EmailStr

User = get_user_model()

api = NinjaAPI(title="Mocklingo API", version="1.0", docs_url="/docs")

# -------------------- Signup --------------------
@api.post("/signup", auth=None, tags=["auth"])
def signup(request, user: UserCreate):
    if User.objects.filter(email__iexact=user.email).exists():
        return JsonResponse({"error": "User already exists"}, status=400)

    user_obj = User.objects.create_user(
        email=user.email,
        username=user.username,
        password=user.password,
    )

    return JsonResponse({"success": True, "user_id": user_obj.id, "user_email": user_obj.email})



# -------------------- Login --------------------
@api.post("/login", response=TokenResponse, auth=None, tags=["auth"])
def login(request, email: EmailStr, password: str):
    user = authenticate(request, email=email, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    
    if not user.is_active:
        return JsonResponse({"error": "User account is disabled"}, status=403)


    refresh = RefreshToken.for_user(user)

    response = JsonResponse({
        "access": str(refresh.access_token),
    })

    response.set_cookie(
        key="refresh",
        value=str(refresh),
        httponly=True,
        secure=True,
        samesite="Strict",
    )

    return response


# -------------------- Logout --------------------
@api.post("/logout", auth=JWTAuth(), tags=["auth"])
def logout(request):
    refresh_token = request.COOKIES.get("refresh")

    if refresh_token is None:
        return JsonResponse({"error": "No refresh token found"}, status=400)

    if not refresh_token:
        return JsonResponse({"error": "Refresh token missing"}, status=400)


    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    response = JsonResponse({"success": True})
    response.delete_cookie("refresh", path="/", samesite="Strict")

    return response
