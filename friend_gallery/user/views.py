import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from werkzeug.security import generate_password_hash

from .models import User
from .serializers import UserResponseSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserResponseSerializer
    serializers_dict = {
        "list": UserResponseSerializer,
        "create": UserSerializer,
        "retrieve": UserResponseSerializer,
        "update": UserSerializer,
    }

    def get_serializer_class(self):
        serializer = self.serializers_dict.get(self.action, None)
        if serializer is None:
            return super().get_serializer_class()
        return serializer

    @swagger_auto_schema(
        operation_summary="List registered users",
        operation_description="List registered users",
        responses={
            200: "user_list",
            204: "empty_list",
        },
    )
    def list(self, request):
        users = self.filter_queryset(self.get_queryset())
        users_data = UserResponseSerializer(users, many=True).data

        if users_data:
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_204_NO_CONTENT

        return Response(users_data, status=status_code)

    @swagger_auto_schema(
        operation_summary="Create new user",
        operation_description="Create new user",
        request_body=UserSerializer,
        responses={
            200: "user_created",
            400: "validation_error_occurred",
        },
    )
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            user = User(
                username=data.get("username"),
                email=data.get("email"),
                password=generate_password_hash(password=data.get("password")),
            )
            user.save()
            return Response({"message": "user_created"}, status=status.HTTP_201_CREATED)

        return Response(
            {"message": "validation_error_occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_summary="Get user by id",
        operation_description="Get user by id",
        responses={
            200: "user_info",
            404: "user_not_found",
        },
    )
    def retrieve(self, request, id=None):
        try:
            user = User.objects.get(id=id)
        except:
            return Response(
                {"message": "user_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserResponseSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a user",
        operation_description="Update a user",
        request_body=UserSerializer,
        responses={
            200: "user_updated",
            400: "validation_error_occurred",
            404: "user_not_found",
        },
    )
    def update(self, request, id=None):
        try:
            user = User.objects.get(id=id)
        except:
            return Response(
                {"message": "user_not_found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user_updated"}, status=status.HTTP_200_OK)

        return Response(
            {"message": "validation_error_occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )
