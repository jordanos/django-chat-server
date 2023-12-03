import channels.layers
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message
from .serializers import MessageSerializer


@receiver(post_save, sender=Message)
def message_group_channels(sender, instance, **kwargs):
    """
    Sends created message instance to channels in the group
    or users in the room
    """
    channel_layer = channels.layers.get_channel_layer()
    obj = MessageSerializer(instance)
    async_to_sync(channel_layer.group_send)(
        f"room_{instance.room.id}",
        {"type": "send.message", "data": obj.data},
    )
