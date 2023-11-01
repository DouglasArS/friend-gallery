from django.http import FileResponse, HttpResponse, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Gallery, Picture
from .serializers import PictureResponseSerializer, PictureSerializer


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureResponseSerializer
    serializers_dict = {
        "list": PictureResponseSerializer,
        "create": PictureSerializer,
        "retrieve": PictureResponseSerializer,
        "update": PictureSerializer,
    }
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        serializer = self.serializers_dict.get(self.action, None)
        if serializer is None:
            return super().get_serializer_class()
        return serializer

    @swagger_auto_schema(
        operation_summary="List registered pictures by gallery id",
        operation_description="List registered pictures by gallery id",
        responses={
            200: "pictures_list",
            204: "empty_list",
            404: "gallery_not_found",
        },
    )
    def list(self, request, gallery_id):
        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except:
            return Response(
                {"message": "gallery_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        pictures = Picture.objects.filter(gallery=gallery)
        pictures_data = PictureResponseSerializer(pictures, many=True).data

        if pictures_data:
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_204_NO_CONTENT

        return Response(pictures_data, status=status_code)

    @swagger_auto_schema(
        operation_summary="Upload a new picture",
        operation_description="Upload a new picture",
        manual_parameters=[
            openapi.Parameter(
                name="data",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="The picture file to upload",
            ),
            openapi.Parameter(
                name="privacy",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Privacy setting for the picture",
            ),
        ],
        responses={
            201: "Picture uploaded successfully",
            400: "Validation error occurred",
            404: "Gallery not found",
        },
    )
    def create(self, request, gallery_id):
        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except:
            return Response(
                {"message": "gallery_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PictureSerializer(data=request.data)
        data = str(request.FILES["data"]).split(".")

        if serializer.is_valid():
            picture = Picture(
                gallery=gallery,
                name=data[0],
                format=data[1],
                bytes=request.FILES.get("data").read(),
                privacy=request.POST.get("privacy"),
            )
            picture.save()
            return Response(
                {"message": "picture_uploaded"}, status=status.HTTP_201_CREATED
            )

        return Response(
            {"message": "validation_error_occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_summary="Get picture by id",
        operation_description="Get picture by id",
        responses={
            200: "picture_info",
            404: "picture_not_found",
        },
    )
    def retrieve(self, request, id=None):
        try:
            picture = Picture.objects.get(id=id)
        except:
            return Response(
                {"message": "picture_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        return HttpResponse(picture.bytes, content_type=f"image/{picture.format}")

    @swagger_auto_schema(
        operation_description="Delete a picture",
        responses={
            200: "picture_deleted",
            404: "picture_not_found",
        },
    )
    def destroy(self, request, id=None):
        try:
            picture = Picture.objects.get(pk=id)
        except:
            return Response(
                {"message": "picture_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        picture.delete()
        return Response({"message": "picture_deleted"}, status=status.HTTP_200_OK)
