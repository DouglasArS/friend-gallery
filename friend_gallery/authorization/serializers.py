from rest_framework import serializers


class AuthorizationSerializer(serializers.Serializer):
    class Meta:
        fields = ("email", "password")

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8)
