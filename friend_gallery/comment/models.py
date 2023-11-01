from django.db import models
from picture.models import Picture
from user.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.picture.data}"
