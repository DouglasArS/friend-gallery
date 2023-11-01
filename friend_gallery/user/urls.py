from django.urls import path

from .views import UserFileViewSet, UserViewSet

urlpatterns = [
    path(
        "",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user-list",
    ),
    path(
        "file",
        UserFileViewSet.as_view({"post": "load"}),
        name="user-file",
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
