from django.urls import path
from .views import (
    learner_registration_view,
    learner_account_update,
)

urlpatterns = [
    path('learner/register/', learner_registration_view, name="learner_account_reg"),
    path('learner/account/update/', learner_account_update, name="learner_account_update")
	
]
