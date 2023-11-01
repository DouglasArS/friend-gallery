from django.urls import path

from .views import AuthorizationViewSet

urlpatterns = [
    path(
        "login",
        AuthorizationViewSet.as_view({"post": "login"}),
        name="login",
    ),
]
