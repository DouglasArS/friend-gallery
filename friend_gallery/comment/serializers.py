from rest_framework import serializers

from .models import Comment


class CommentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text", "created_at")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text",)
