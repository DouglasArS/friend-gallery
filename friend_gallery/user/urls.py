from django.urls import path

from .views import UserViewSet

urlpatterns = [
    path(
        "",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user-list",
    ),
    path(
        "<int:id>",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
            }
        ),
        name="user-detail",
    ),
]
