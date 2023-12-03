from django.urls import path

from .views import UserDetail, UserList

urlpatterns = [
    path("", UserList.as_view(), name="list-create"),
    path("<int:pk>/", UserDetail.as_view(), name="get-update-delete"),
]
