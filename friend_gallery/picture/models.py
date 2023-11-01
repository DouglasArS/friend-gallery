from django.db import models
from gallery.models import Gallery
from user.models import User


class Picture(models.Model):
    PRIVACY_CHOICES = (
        ("public", "Public"),
        ("private", "Private"),
    )

    name = models.CharField(max_length=255, null=False, blank=False)
    format = models.CharField(max_length=255, null=False, blank=False)
    data = models.ImageField(default=None)
    bytes = models.BinaryField(null=False, blank=False)
    privacy = models.CharField(max_length=7, choices=PRIVACY_CHOICES, default="private")
    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name="pictures"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Name: {self.data} | Gallery: {self.gallery.name}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.picture.data}"
