from rest_framework import serializers

from .models import Picture


class PictureResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ("id", "name", "format", "privacy", "created_at")


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = (
            "data",
            "privacy",
        )

    data = serializers.FileField(required=True)
    privacy = serializers.ChoiceField(choices=Picture.PRIVACY_CHOICES, required=False)

    def validate_privacy(self, value):
        if value is not None and value not in dict(Picture.PRIVACY_CHOICES).keys():
            raise serializers.ValidationError("invalid_privacy_value")
        return value
