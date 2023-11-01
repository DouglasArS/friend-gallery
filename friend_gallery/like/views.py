from authorization.token_verification import token_required
from django.http import HttpResponse, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Like, Picture, User


class LikeViewSet(viewsets.ViewSet):
    queryset = Like.objects.all()

    @swagger_auto_schema(
        operation_summary="Count likes of a picture",
        operation_description="Count likes of a picture",
        responses={
            200: "like_count",
            404: "picture_not_found",
        },
    )
    @action(detail=False, methods=["GET"])
    def count_likes(self, request, picture_id):
        try:
            picture = Picture.objects.get(id=picture_id)
        except:
            return Response(
                {"message": "picture_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        like_count = Like.objects.filter(picture=picture).count()
        return Response({"like_count": like_count}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Like a new picture",
        responses={
            200: "picture_uploaded",
            404: "user_not_found\npicture_not_found",
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

        existing_like = Like.objects.filter(
            picture_id=picture_id, user=logged_user
        ).first()
        if existing_like:
            return Response(
                {"message": "picture_already_liked"}, status=status.HTTP_400_BAD_REQUEST
            )

        like = Like(
            user=logged_user,
            picture=picture,
        )
        like.save()

        return Response({"message": "picture_liked"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Remove like of picture",
        responses={
            200: "like_deleted",
            404: "picture_not_found",
        },
    )
    @token_required(load_user=True)
    def destroy(self, request, logged_user, picture_id):
        try:
            like = Like.objects.filter(picture_id=picture_id, user=logged_user).first()
        except:
            return Response(
                {"message": "like_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        like.delete()
        return Response({"message": "like_deleted"}, status=status.HTTP_200_OK)
