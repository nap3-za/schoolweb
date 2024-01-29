from django.urls import path
from .views import (
    teacher_registration_view,
    teacher_account_update,
)

urlpatterns = [
    path('teacher/register/', teacher_registration_view, name="teacher_account_reg"),
    path('teacher/account/update/', teacher_account_update, name="teacher_account_update")
	
]
