from django.urls import path

from .views import PictureViewSet

urlpatterns = [
    path(
        "<int:id>",
        PictureViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="picture_by_id",
    ),
    path(
        "gallery/<int:gallery_id>",
        PictureViewSet.as_view({"get": "list", "post": "create"}),
        name="picture_by_gallery_id",
    ),
]
