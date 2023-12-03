import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .utils import (
    create_chat_message,
    deactivate_user_channel,
    get_rooms,
    update_user_channel,
)

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """Websocket instance for each connection

    Args:
        AsyncWebsocketConsumer (_type_): _description_
    """

    async def connect(self):
        # get user from the scope using the auth middleware
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close(401)
            return
        # track current user channel in database
        await update_user_channel(user, self.channel_name)
        # register the channel/consumer on all chat rooms the user has access to
        # we can then listen to all incoming data from this channel and
        # update the other channels residing in the same group
        self.rooms = [f"room_{room.id}" for room in await get_rooms(user)]
        for room in self.rooms:
            await self.channel_layer.group_add(room, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        # validate the request and create a message
        user = self.scope["user"]
        text = data.get("text", None)
        room = data.get("room", None)
        # since creating a message triggers a signal for broadcasting the message to all channels in the message_room
        # we are certain the other users will recieve the message instantly
        if text is None or room is None:
            # todo: handdle errors
            await self.send(text_data=json.dumps({"error": "validation error"}))
        else:
            await create_chat_message(user, text, room)

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if not user.is_anonymous:
            # deactivate user channel on database
            await deactivate_user_channel(user)
            # unregister the channel from group to save resources
            for room in self.rooms:
                await self.channel_layer.group_discard(room, self.channel_name)

    async def send_message(self, event):
        message = event["data"]
        await self.send(text_data=json.dumps(message))
