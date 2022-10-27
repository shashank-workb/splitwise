from django.urls import path
from split.views import ExpenseCreate, ExpenseRUD

app_name = 'split'

urlpatterns = [
    path(
        "",
        ExpenseCreate.as_view(),
        name='expense_create',
    ),
    path(
        "<str:pk>/",
        ExpenseRUD.as_view(),
        name='expense_rud',
    ),
]