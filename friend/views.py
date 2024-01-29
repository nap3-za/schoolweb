from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required

from account.models import BaseAccount
from friend.models import FriendRequest, FriendList

# Optimized
@login_required(login_url="login")
def friends_list_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')
	
	elif auth_user.is_authenticated:

		subject_user_id = kwargs.get("subject_user_id")
		if subject_user_id:
			context['id'] = subject_user_id
			try:
				subject_account = BaseAccount.objects.get(pk=subject_user_id)
				context['subject_account'] = subject_account
			except BaseAccount.DoesNotExist:
				return render(request, template_name="errors/does_not_exist.html")
			
			# Fried list
			try:
				friend_list = FriendList.objects.get(user=subject_account)
			except FriendList.DoesNotExist:
				friend_list = FriendList(user=subject_account)
				friend_list.save()
			
			
			# Must be friends to view a friends list
			if auth_user != subject_account:
				if not auth_user in friend_list.friends.all():
					return render(request, template_name="errors/be_friends.html")
			
			# [(friend1, True), (friend2, False), ...]		
			friends = [] 

			auth_user_friend_list = FriendList.objects.get(user=auth_user)

			# Checking any subject's friends are friends with us
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
			context['friends'] = friends
		else:
			return render(request, template_name="errors/does_not_exist.html")
	else:
		return redirect('login')

	return render(request, "friend/friend_list.html", context)

# Optimized
@login_required(login_url="login")
def friend_requests_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	if auth_user.is_authenticated:
		friend_requests = FriendRequest.objects.filter(receiver=auth_user, is_active=True).order_by('-timestamp')
		context['friend_requests'] = friend_requests
	else:
		return render(request, template_name="errors/not_allowed.html")

	return render(request, "friend/friend_requests.html", context)

# Optimized
@login_required(login_url="login")
def send_friend_request_view(request, *args, **kwargs):

	auth_user = request.user
	payload = {}

	if not auth_user.is_authenticated:
		return redirect('login')

	if request.method == "POST" and auth_user.is_authenticated:
		receiver_user_id = request.POST.get("receiver_user_id")
		print(receiver_user_id)
		if receiver_user_id:
			receiver = BaseAccount.objects.get(pk=receiver_user_id)
			auth_account = BaseAccount.objects.get(id=auth_user.id)
			try:
				# All friend requests
				friend_requests = FriendRequest.objects.filter(sender=auth_account, receiver=receiver)
				
				try:
					# If there are any past friend requests
					if friend_requests:
						for request in friend_requests:
							if request.is_active:
								payload['response'] = "Friend request already sent"
								return render(request, template_name="errors/done.html")
							else:
								request.is_active = True 
								request.save()
								friend_request = request
								payload['reponse'] = "Friend request sent"
								return redirect('account', subject_user_id=receiver_user_id)
		
					# If there are no past friend requests
					else:
						friend_request = FriendRequest(sender=auth_account, receiver=receiver)
						friend_request.save()	
						payload['response'] = "Friend request sent"
				except:
					return render(request, template_name="errors/try_again.html")

			except Exception as e:
				print("[-] Errors : "+str(e))
				payload['response'] = str(e)

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			return render(request, template_name="errors/does_not_exist.html")
		if payload['response'] == None:
			payload['response'] = "Placeholder"

	return HttpResponse(json.dumps(payload), content_type="application/json")

# Optimized
@login_required(login_url="login")
def accept_friend_request_view(request, *args, **kwargs):
	auth_user = request.user
	payload = {}

	if not auth_user.is_authenticated:
		return redirect('login')

	if request.method == "GET" and auth_user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			
			# Found it , Accept it 
			if friend_request and friend_request.receiver == auth_user:
				friend_request.accept()
				payload['response'] = "Friend request accepted."
			else:
				payload['response'] = "That is not your request to accept."
		else:
			payload['response'] = "Unable to accept that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to accept a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

# Optimized
@login_required(login_url="login")
def unfriend_view(request, *args, **kwargs):
	auth_user = request.user
	payload = {}

	if not auth_user.is_authenticated:
		return redirect('login')

	if request.method == "POST" and auth_user.is_authenticated:
		subject_user_id = request.POST.get("receiver_user_id")
		if subject_user_id:
			try:
				print("[+] In the try block")
				removee = BaseAccount.objects.get(pk=subject_user_id)
				friend_list = FriendList.objects.get(user=auth_user)
				friend_list.unfriend(removee)
				payload['response'] = "Successfully removed that friend."
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove that friend."

	return HttpResponse(json.dumps(payload), content_type="application/json")

# Optimized
@login_required(login_url="login")
def decline_friend_request_view(request, *args, **kwargs):
	auth_user = request.user
	payload = {}

	if not auth_user.is_authenticated:
		return redirect('login')

	if request.method == "GET" and auth_user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			
			# confirm that is the correct request
			if friend_request and friend_request.receiver == auth_user:
				# found the request. Now decline it
				friend_request.decline()
				payload['response'] = "Friend request declined."
			else:
				payload['response'] = "That is not your friend request to decline."
		else:
			payload['response'] = "Unable to decline that friend request."

	return HttpResponse(json.dumps(payload), content_type="application/json")

# Optimized
@login_required(login_url="login")
def cancel_friend_request_view(request, *args, **kwargs):
	auth_user = request.user
	payload = {}

	if not auth_user.is_authenticated:
		return redirect('login')

	if request.method == "POST" and auth_user.is_authenticated:
		receiver_id = request.POST.get("receiver_user_id")
		
		if receiver_id:
			receiver = BaseAccount.objects.get(pk=receiver_id)
			
			try:
				friend_requests = FriendRequest.objects.filter(sender=auth_user, receiver=receiver, is_active=True)
			except FriendRequest.DoesNotExist:
				payload['response'] = "Nothing to cancel. Friend request does not exist."

			# If there are many friend request, cancel them all
			if len(friend_requests) > 1:
				for request in friend_requests:
					request.cance()
				payload['response'] = "Friend request canceled."
			else:
				friend_requests.first().cancel()
				payload['response'] = "Friend request canceled."
		else:
			payload['response'] = "Unable to cancel that friend request."

	return HttpResponse(json.dumps(payload), content_type="application/json")

