from django.urls import path

from .views import AuthorizationViewSet

urlpatterns = [
    path(
        "",
        AuthorizationViewSet.as_view({"post": "login"}),
        name="login",
    ),
]
