from rest_framework import serializers

from .models import Picture


class PictureResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ("id", "name", "format", "privacy", "created_at")


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ("data",)

    data = serializers.FileField(required=True)


class PicturePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ("privacy",)

    privacy = serializers.CharField(required=True)
