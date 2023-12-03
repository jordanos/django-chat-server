from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}"


class UserChannel(models.Model):
    channel_name = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}_{self.channel_name}"
