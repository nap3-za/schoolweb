from django.urls import path
from friend.views import(
	send_friend_request_view,
	friend_requests_view,
	accept_friend_request_view,
	unfriend_view,
	decline_friend_request_view,
	cancel_friend_request_view,
	friends_list_view,
)


urlpatterns = [
	path('list/<int:subject_user_id>', friends_list_view, name='friend_list'),
	path('unfriend/', unfriend_view, name='unfriend'),
    path('send-friend-request/', send_friend_request_view, name='send_request'),
    path('cancel_friend_request/', cancel_friend_request_view, name='cancel_request'),
    path('friend_requests/', friend_requests_view, name='friend_requests'),
    path('friend_request_accept/<friend_request_id>/', accept_friend_request_view, name='accept_request'),
    path('friend_request_decline/<friend_request_id>/', decline_friend_request_view, name='decline_request'),
]