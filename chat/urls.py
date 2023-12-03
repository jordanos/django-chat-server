from django.urls import path

from .views import JoinRoom, LeaveRoom, MessageDetail, MessageList, RoomDetail, RoomList

urlpatterns = [
    path("messages/", MessageList.as_view(), name="list-create"),
    path("messages/<int:pk>/", MessageDetail.as_view(), name="get-update-delete"),
    path("rooms/", RoomList.as_view(), name="list-create"),
    path("rooms/<int:pk>/", RoomDetail.as_view(), name="get-update-delete"),
    path("rooms/<int:pk>/join/", JoinRoom.as_view(), name="join"),
    path("rooms/<int:pk>/leave/", LeaveRoom.as_view(), name="leave"),
]
