from django.urls import path

from .views import CommentViewSet

urlpatterns = [
    path(
        "comment/<int:id>",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="comment-detail",
    ),
    path(
        "<int:picture_id>/comment",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comment_by_picture",
    ),
]
