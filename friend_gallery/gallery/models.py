from django.db import models
from user.models import User


class Gallery(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    owners = models.ManyToManyField(User, related_name="gallery_owners")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Gallery {self.username} | Owners: {self.owners} "
