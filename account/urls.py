from django.urls import path

from account.views import (
	register_view,
	reg_complete_view,

	login_view,
	logout_view,

	account_view,
	search_view,

	update_view,
	delete_view,
)
from django.contrib.auth import views as auth_views

urlpatterns = [

	path('register/', register_view, name="register"),
	path('user/complete-registration/', reg_complete_view, name="reg_complete"),

	path('login/', login_view, name="login"),
	path('logout/', logout_view, name="logout"),

	path('user/<subject_user_id>/details/', account_view, name="account"),
	path('search/', search_view, name="search"),

	path('user/update/', update_view, name="update"),	
	path('user/delete/564646546584646465/6546584/635465/64654/', delete_view, name="delete_account"),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_reset/password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_reset/password_change.html'), 
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset/password_reset_done.html'),
     name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
]
