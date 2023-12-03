import os
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from common.utils import get_mime_type

User = get_user_model()


def upload(instance, filename):
    file_type = "all"
    mime = get_mime_type(instance)
    types = mime.split("/")
    if len(types) > 1:
        file_type = types[0]
    return "/".join([f"{file_type}", f"{str(uuid4())}{os.path.splitext(filename)[1]}"])


class Room(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    users = models.ManyToManyField(
        User,
        related_name="thread_second_person",
    )
    max_users = models.IntegerField(default=10, null=False, blank=False)
    type = models.CharField(
        max_length=10,
        choices=[["PRIVATE", "PRIVATE"], ["GROUP", "GROUP"]],
        default="GROUP",
        null=False,
        blank=False,
    )
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room", null=False, blank=False
    )
    text = models.TextField(null=False, blank=True)
    file = models.FileField(blank=False, null=True, upload_to=upload)
    file_type = models.CharField(max_length=20, blank=False, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
