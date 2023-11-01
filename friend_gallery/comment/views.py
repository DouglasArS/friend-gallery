from authorization.token_verification import token_required
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Comment, Picture, User
from .serializers import CommentResponseSerializer, CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentResponseSerializer
    serializers_dict = {
        "list": CommentResponseSerializer,
        "create": CommentSerializer,
        "retrieve": CommentResponseSerializer,
        "update": CommentSerializer,
    }

    def get_serializer_class(self):
        serializer = self.serializers_dict.get(self.action, None)
        if serializer is None:
            return super().get_serializer_class()
        return serializer

    @swagger_auto_schema(
        operation_summary="List registered comments ",
        operation_description="List registered comments ",
        responses={
            200: "comment_list",
            204: "empty_list",
            404: "picture_not_found",
        },
    )
    def list(self, request, picture_id):
        try:
            picture = Picture.objects.get(id=picture_id)
        except:
            return Response(
                {"message": "picture_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        comments = Comment.objects.filter(picture=picture)
        comments_data = CommentResponseSerializer(comments, many=True).data

        if comments_data:
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_204_NO_CONTENT

        return Response(comments_data, status=status_code)

    @swagger_auto_schema(
        operation_summary="Create a new comment",
        operation_description="Create a new comment",
        request_body=CommentSerializer,
        responses={
            200: "comment_created",
            400: "validation_error_occurred",
            404: "user_not_found",
        },
    )
    @token_required(load_user=True)
    def create(self, request, logged_user, picture_id):
        try:
            picture = Picture.objects.get(id=picture_id)
        except:
            return Response(
                {"message": "picture_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            comment = Comment(user=logged_user, picture=picture, text=data.get("text"))
            comment.save()

            return Response(
                {"message": "comment_created"}, status=status.HTTP_201_CREATED
            )

        return Response(
            {"message": "validation_error_occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_summary="Get comment by id",
        operation_description="Get comment by id",
        responses={
            200: "comment_info",
            404: "comment_not_found",
        },
    )
    def retrieve(self, request, id=None):
        try:
            comment = Comment.objects.get(id=id)
        except:
            return Response(
                {"message": "comment_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentResponseSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a user",
        operation_description="Update a user",
        request_body=CommentSerializer,
        responses={
            200: "comment_updated",
            400: "validation_error_occurred",
            404: "comment_not_found",
        },
    )
    @token_required(load_user=True)
    def update(self, request, logged_user, id=None):
        try:
            comment = Comment.objects.get(id=id)
        except:
            return Response(
                {"message": "comment_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        if logged_user != comment.user:
            return Response(
                {"message": "user_unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            comment.text = data.get("text")
            comment.save()
            return Response({"message": "comment_updated"}, status=status.HTTP_200_OK)

        return Response(
            {"message": "validation_error_occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_summary="Delete a comment",
        operation_description="Delete a comment",
        responses={
            200: "comment_deleted",
            404: "comment_not_found",
        },
    )
    @token_required(load_user=True)
    def destroy(self, request, logged_user, id=None):
        try:
            comment = Comment.objects.get(id=id)
        except:
            return Response(
                {"message": "comment_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        if logged_user != comment.user:
            return Response(
                {"message": "user_unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        comment.delete()
        return Response({"message": "gallery_deleted"}, status=status.HTTP_200_OK)
