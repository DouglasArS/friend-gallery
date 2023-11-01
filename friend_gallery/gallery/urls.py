from django.urls import path

from .views import GalleryViewSet

urlpatterns = [
    path(
        "",
        GalleryViewSet.as_view({"post": "create"}),
        name="gallery-list",
    ),
    path(
        "user/<int:user_id>",
        GalleryViewSet.as_view({"get": "list"}),
        name="gallery-list",
    ),
    path(
        "<int:id>",
        GalleryViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="gallery-detail",
    ),
]
