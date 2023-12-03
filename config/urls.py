from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import parsers
from rest_framework.authtoken.views import ObtainAuthToken


class CustomAuthView(ObtainAuthToken):
    parser_classes = (parsers.JSONParser,)


API_PATH = "api/v1"

urlpatterns = [
    # SCHEMA
    path(f"{API_PATH}/schema/", SpectacularAPIView.as_view(), name="schema"),
    # SWAGGER
    path("", lambda request: redirect(f"{API_PATH}/")),
    path(
        f"{API_PATH}/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"{API_PATH}/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # ENDPOINTS
    path(f"{API_PATH}/auth/login/", CustomAuthView.as_view(), name="auth"),
    path(f"{API_PATH}/users/", include("users.urls"), name="user"),
    path(f"{API_PATH}/chats/", include("chat.urls"), name="chat"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
