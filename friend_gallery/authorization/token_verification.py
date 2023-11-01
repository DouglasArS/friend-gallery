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

from friend_gallery.settings import SECRET_KEY


def token_required(load_user=False):
    def wrapper(f):
        @wraps(f)
        def decorator(self, *args, **kwargs):
            token = None
            if "Authorization" not in self.request.headers:
                return Response(
                    {"message": "user_unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            token = self.request.headers["Authorization"]
            if not token or token[:7] != "Bearer ":
                return Response(
                    {"message": "user_unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            token = token[7:]

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except:
                return Response(
                    {"message": "user_unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if load_user:
                try:
                    user = User.objects.get(id=data["sub"])
                except:
                    return Response(
                        {"message": "user_not_found"}, status=status.HTTP_404_NOT_FOUND
                    )

                kwargs["logged_user"] = user

            return f(request=self.request, *args, **kwargs)

        return decorator

    return wrapper
