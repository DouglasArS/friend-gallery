from datetime import datetime, timedelta
from functools import wraps

import jwt
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from user.models import User
from werkzeug.security import check_password_hash

from friend_gallery.settings import JWT_EXP, SECRET_KEY

from .serializers import AuthorizationSerializer


class AuthorizationViewSet(viewsets.ViewSet):
    serializer_class = AuthorizationSerializer

    @swagger_auto_schema(
        operation_summary="User login",
        operation_description="User login",
        request_body=AuthorizationSerializer,
        responses={
            200: "user_logged",
            401: "user_unauthorized",
            404: "user_not_found",
        },
    )
    @permission_classes([])
    @action(detail=False, methods=["POST"])
    def login(self, request):
        serializer = AuthorizationSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data

            try:
                user = User.objects.get(email=data.get("email"))
            except:
                return Response(
                    {"message": "user_not_found"}, status=status.HTTP_404_NOT_FOUND
                )

            login_pwd = data.get("password")
            user_pwd = user.password

            if not check_password_hash(user_pwd, login_pwd):
                return Response(
                    {"message": "user_unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            token = self._create_jwt(user.id)
            return Response(
                {"acess_token": token, "message": "user_logged"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "user_unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
        )

    def _create_jwt(self, sub: int) -> str:
        return jwt.encode(
            {"sub": sub, "exp": datetime.utcnow() + timedelta(hours=JWT_EXP)},
            SECRET_KEY,
        )
