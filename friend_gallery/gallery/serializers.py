from rest_framework import serializers

from .models import Gallery


class GalleryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ("id", "name", "description", "owners", "created_at")


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = (
            "name",
            "description",
        )

    name = serializers.CharField(required=True, min_length=1, max_length=255)
    description = serializers.CharField(required=False, min_length=1, max_length=255)

    def validate_name(self, value):
        if Gallery.objects.filter(name=value).exists():
            raise serializers.ValidationError("name_in_use")
        return value
