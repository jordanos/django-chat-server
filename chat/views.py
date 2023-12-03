from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsOwner

from .models import Message, Room
from .serializers import (
    JoinRoomSerializer,
    LeaveRoomSerializer,
    MessageSerializer,
    RoomSerializer,
)


class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by("-updated_at")
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # filter rooms by the logged in user
        user = self.request.user
        queryset = self.queryset.filter(users__in=[user])
        return queryset


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class JoinRoom(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = JoinRoomSerializer
    permission_classes = [IsAuthenticated]


class LeaveRoom(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = LeaveRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # filter rooms by the logged in user
        if not self.request.user.is_authenticated:
            return self.queryset
        user = self.request.user
        queryset = self.queryset.filter(users__in=[user])
        return queryset


class MessageList(generics.ListCreateAPIView):
    # filter_backends = [MessagesFilterBackend]
    filterset_fields = ["room"]
    parser_classes = [MultiPartParser]
    queryset = Message.objects.all().order_by("-created_at")
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # filter messages by the logged in user
        user = self.request.user
        queryset = self.queryset.filter(room__users__in=[user])
        return queryset


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]
