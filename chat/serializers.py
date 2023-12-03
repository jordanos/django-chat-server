import channels.layers
from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.utils import get_mime_type
from users.models import UserChannel

from .models import Message, Room

User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
            "id",
            "owner",
            "users",
        ]

    def validate_max_users(self, value):
        max_u = settings.MAX_USERS_IN_ROOM
        if value > max_u:
            raise serializers.ValidationError(
                f"System max users limit is {max_u}", code=400
            )
        return value

    def create(self, validated_data):
        owner = self.context["request"].user
        obj = Room.objects.create(**validated_data, owner=owner)
        return obj

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class JoinRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
            "id",
            "owner",
            "max_users",
            "users",
            "name",
            "type",
        ]

    def update(self, instance, validated_data):
        # check for room users limit
        room = instance
        if room.users.count() >= room.max_users:
            raise serializers.ValidationError(
                "Max users limit for group reached.", code=400
            )
        user = self.context["request"].user
        room.users.add(user)
        room.save()
        # add current user channel to group
        try:
            channel = UserChannel.objects.get(owner=user)
            if channel.is_active:
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_add)(
                    f"room_{room.id}",
                    channel.channel_name,
                )
        except UserChannel.DoesNotExist:
            pass
        return room


class LeaveRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "updated_at",
            "id",
            "owner",
            "max_users",
            "users",
            "name",
            "type",
        ]

    def update(self, instance, validated_data):
        user = self.context["request"].user
        room = instance
        room.users.remove(user)
        room.save()
        # remove current user channel from group
        try:
            channel = UserChannel.objects.get(owner=user)
            if channel.is_active:
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_discard)(
                    f"room_{room.id}",
                    channel.channel_name,
                )
        except UserChannel.DoesNotExist:
            pass
        return room


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "id", "file_type", "owner"]

    def validate_room(self, room):
        user = self.context["request"].user
        if not room.users.filter(pk=user.pk).exists():
            raise serializers.ValidationError(
                "You're not authorized to perform any actions in this room", code=403
            )
        return room

    def create(self, validated_data):
        # add file_type for a file
        if "file" in validated_data:
            file = validated_data["file"]
            mime = get_mime_type(file)
            validated_data["file_type"] = mime
        owner = self.context["request"].user
        obj = Message.objects.create(**validated_data, owner=owner)
        return obj
