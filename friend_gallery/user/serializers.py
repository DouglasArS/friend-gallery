from rest_framework import serializers

from .models import User


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "created_at")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    username = serializers.CharField(required=True, min_length=1, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, max_length=255)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username_in_use")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email_in_use")
        return value
