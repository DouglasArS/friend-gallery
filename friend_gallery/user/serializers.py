from rest_framework import serializers

from .models import User


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "created_at")


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=1, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, max_length=255)

    class Meta:
        model = User
        fields = ("username", "email", "password")
