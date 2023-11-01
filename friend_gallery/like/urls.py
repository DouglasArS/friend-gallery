from django.urls import path

from .views import LikeViewSet

urlpatterns = [
    path(
        "<int:picture_id>/like/count",
        LikeViewSet.as_view({"get": "count_likes"}),
        name="Like_by_id",
    ),
    path(
        "<int:picture_id>/like",
        LikeViewSet.as_view({"post": "create", "delete": "destroy"}),
        name="Like_by_picture_id",
    ),
]
