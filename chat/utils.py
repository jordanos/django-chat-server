from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from users.models import UserChannel

from .models import Message, Room

User = get_user_model()


@database_sync_to_async
def get_rooms(user: User):
    rooms = Room.objects.filter(users__in=[user])
    return list(rooms)


@database_sync_to_async
def create_chat_message(user: User, text: str, room_id: int):
    room = Room.objects.get(pk=room_id)
    message = Message.objects.create(owner=user, text=text, room=room)
    return message


@database_sync_to_async
def update_user_channel(user: User, channel_name: str):
    if not UserChannel.objects.filter(owner=user).exists():
        user_channel = UserChannel.objects.create(
            owner=user, channel_name=channel_name, is_active=True
        )
        return
    user_channel = UserChannel.objects.get(owner=user)
    user_channel.channel_name = channel_name
    user_channel.is_active = True
    user_channel.save()


@database_sync_to_async
def deactivate_user_channel(user: User):
    try:
        user_channel = UserChannel.objects.get(owner=user)
        user_channel.is_active = False
        user_channel.save()
    except UserChannel.DoesNotExist:
        pass
