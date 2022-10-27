from django.urls import path
from user.views import UserCreate, UserRUD

app_name = 'user'

urlpatterns = [
    path(
        "",
        UserCreate.as_view(),
        name='user_create',
    ),
    path(
        "<str:pk>/",
        UserRUD.as_view(),
        name='user_rud',
    ),
]