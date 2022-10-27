from re import M
from django.urls import path
from user.views import GroupCreate, GroupRUD

app_name = 'group'

urlpatterns = [
    path(
        "",
        GroupCreate.as_view(),
        name='group_create',
    ),
    path(
        "<str:pk>/",
        GroupRUD.as_view(),
        name='group_RUD',
    )
]