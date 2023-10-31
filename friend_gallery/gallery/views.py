from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Gallery, User
from .serializers import GalleryResponseSerializer, GallerySerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GalleryResponseSerializer
    serializers_dict = {
        "list": GalleryResponseSerializer,
        "create": GallerySerializer,
        "retrieve": GalleryResponseSerializer,
        "update": GallerySerializer,
    }

    def get_serializer_class(self):
        serializer = self.serializers_dict.get(self.action, None)
        if serializer is None:
            return super().get_serializer_class()
        return serializer

    @swagger_auto_schema(
        operation_summary="List registered galleries",
        operation_description="List registered galleries",
        responses={
            200: "user_list",
            204: "empty_list",
            404: "user_not_found",
        },
    )
    def list(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response(
                {"message": "user_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        galleries = Gallery.objects.filter(owners=user)
        galleries_data = GalleryResponseSerializer(galleries, many=True).data

        if galleries_data:
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_204_NO_CONTENT

        return Response(galleries_data, status=status_code)

    @swagger_auto_schema(
        operation_summary="Create a new gallery",
        operation_description="Create a new gallery",
        request_body=GallerySerializer,
        responses={
            200: "gallery_created",
            400: "validation_error_occurred",
            404: "user_not_found",
        },
    )
    def create(self, request, user_id):
        try:
            owner = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "user_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = GallerySerializer(data=request.data)

        if serializer.is_valid():
            gallery = serializer.save()
            gallery.owners.add(owner)
            return Response(
                {"message": "gallery_created"}, status=status.HTTP_201_CREATED
            )

        return Response(
            {"message": "validation_error_occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_summary="Get gallery by id",
        operation_description="Get gallery by id",
        responses={
            200: "gallery_info",
            404: "gallery_not_found",
        },
    )
    def retrieve(self, request, id=None):
        try:
            gallery = Gallery.objects.get(id=id)
        except:
            return Response(
                {"message": "gallery_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = GalleryResponseSerializer(gallery)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a user",
        operation_description="Update a user",
        request_body=GallerySerializer,
        responses={
            200: "gallery_updated",
            400: "validation_error_occurred",
            404: "gallery_not_found",
        },
    )
    def update(self, request, id=None):
        try:
            gallery = Gallery.objects.get(id=id)
        except:
            return Response(
                {"message": "gallery_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = GallerySerializer(gallery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "gallery_updated"}, status=status.HTTP_200_OK)

        return Response(
            {"message": "validation_error_occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_summary="Delete a gallery",
        operation_description="Delete a gallery",
        responses={
            200: "gallery_deleted",
            404: "gallery_not_found",
        },
    )
    def destroy(self, request, id=None):
        try:
            gallery = Gallery.objects.get(pk=id)
        except:
            return Response(
                {"message": "gallery_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        gallery.delete()
        return Response({"message": "gallery_deleted"}, status=status.HTTP_200_OK)
