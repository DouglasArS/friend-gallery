from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Username: {self.username}"
