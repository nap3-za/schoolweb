from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
import json
from django.contrib.auth.decorators import login_required

from teacher.models import TeacherAccount
from learner.models import LearnerAccount
from account.models import BaseAccount

from account.forms import RegistrationForm, AuthenticationForm, UpdateForm

from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest

# Optimized
def register_view(request, *args, **kwargs):
	auth_user = request.user
	context = {}

	if auth_user.is_authenticated: 
		return render(request, template_name="auth.html", context={'email':auth_user.email})

	elif not auth_user.is_authenticated:
		# If the form is being submited
		if request.method == "POST" and request.POST:
			form = RegistrationForm(request.POST)
			if form.is_valid():
				form.save()

				# Authenticating the user
				email = form.cleaned_data.get('email').lower()
				admin_no = form.cleaned_data.get('admin_no')
				raw_password = form.cleaned_data.get('password1')
				auth_user_account = authenticate(email=email, password=raw_password)
				
				if admin_no == 1010:
					auth_user_account.is_learner = False
					auth_user_account.save()
					return redirect('reg_complete')

				login(request, auth_user_account)
				destination = kwargs.get("next")
				if destination:
					return redirect(destination)
				return redirect('reg_complete')
			else:
				form = RegistrationForm(request.POST)
				context['form'] = form

	else:
		return redirect("login")
	return render(request, 'account/register.html', context)

# Optimized
@login_required(login_url="login")
def reg_complete_view(request, *args, **kwargs):
	auth_user = request.user
	context = {}
	
	if not auth_user.is_authenticated:
		return redirect('login')

	elif auth_user.is_authenticated:
		""" 
		The authenticated user's base account
		"""
		auth_user_account = BaseAccount.objects.get(id=auth_user.id)
		
		if auth_user_account:
			"""
			Redirection based on the is_learner field
			"""
			if auth_user_account.is_learner:
				is_learner = auth_user_account.is_learner
				return redirect('learner_account_reg')
			elif not auth_user_account.is_learner:
				return redirect('teacher_account_reg')
			else:
				return render(request, template_name="errors/does_not_exist.html")
	
	else:
		return redirect('login')

# Optimized
@login_required(login_url="login")
def logout_view(request):
	logout(request)
	return redirect("login")

# Optimized
def login_view(request, *args, **kwargs):
	auth_user = request.user
	context = {}

	if not auth_user.is_authenticated:

		# If the form is being submitted
		if request.method == 'POST' and request.POST:
			form = AuthenticationForm(request.POST)
			if form.is_valid():
				email = form.cleaned_data['email']
				password = form.cleaned_data['password']

				#  A try block just to be safe
				try:
					auth_user_account = authenticate(email=email, password=password)
				except:
					return render(request, template_name="errors/try_again.html")
				"""
				If the account is active , login
				"""
				if auth_user_account.is_active:
					login(request, auth_user_account)
					return redirect('home')

				elif not auth_user_account.is_active:
					return render(request, template_name="errors/deleted.html", context={'email': email})
			else:
				form = AuthenticationForm(request.POST)
				context['login_form'] = form				
		
	else:
		return redirect('login')

	return render(request, "account/login.html", context)

# Optimized
@login_required(login_url="login")
def search_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	elif auth_user.is_authenticated:

		if request.method == "GET":
			search_query = request.GET.get("q")
			if len(search_query) > 0:
				search_results = BaseAccount.objects.filter(username__icontains=search_query).filter(name__icontains=search_query, is_active=True).filter(surname__icontains=search_query).distinct()
				
				# [(account1, True), (account2, False), ...]
				# Boolean value for 'is_friend'
				accounts = []
				auth_user_friend_list = FriendList.objects.get(user=auth_user)
				for account in search_results:
					accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
				context['accounts'] = accounts
				
			else:
				pass
	else:
		return redirect('login')
	return render(request, "account/search_results.html", context)

# Optimized
@login_required(login_url="login")
def account_view(request, *args, **kwargs):
	context = {}
	subject_user_id = kwargs.get("subject_user_id")
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	elif auth_user.is_authenticated:
		try:
			subject_account = BaseAccount.objects.get(pk=subject_user_id)
		except:
			return render(request, template_name="errors/does_not_exist.html")

		if subject_account:
			"""
			If the subject is a learner
			"""
			if subject_account.is_learner:
				context['base_account'] = subject_account
				try:
					learner_account = LearnerAccount.objects.get(user=subject_account)
					context['learner_account'] = learner_account
				except LearnerAccount.DoesNotExist:
					"""
					The account will be completed by the owner else , erro
					"""
					if auth_user == subject_account:
						return redirect('reg_complete')
					else:
						return render(request, template_name="errors/does_not_exist.html")

			"""
			If the subject is not a learner
			"""
			if not subject_account.is_learner:
				context['base_account'] = subject_account
				try:
					teacher_account = TeacherAccount.objects.get(user=subject_account)
					context['teacher_account'] = teacher_account
				except TeacherAccount.DoesNotExist:
					"""
					The account will be completed by the owner else , erro
					"""
					if auth_user == subject_account:
						return redirect('reg_complete')
					else:
						return render(request, template_name="errors/does_not_exist.html")

			"""
			Friend system related declarations
			"""

			# Friends
			try:
				friend_list = FriendList.objects.get(user=subject_account)
			except FriendList.DoesNotExist:
				friend_list = FriendList(user=subject_account)
				friend_list.save()
			friends = friend_list.friends.all()
			context['friends'] = friends
		
			# Some defeaults
			is_self = None
			is_friend = None
			friend_requests = None
			request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
			"""
			LOGIC 
			IS SELF : TRUE
				template					[1]
			
			IS SELF : FALSE
				IS FRIEND : TRUE
					template				[2]
				IS FRIEND : FALSE
					FRIEND REQUEST STATUS	
						YOU TO THEM			[3]
						NO REQUEST			[4]
						THEM TO YOU			[5]
			"""
			# Me or Someone else
			if auth_user == subject_account:
				is_self = True
				try:
					friend_requests = FriendRequest.objects.filter(receiver=auth_user, is_active=True)
				except:
					return render(request, "errors/does_not_exist.html")

			elif auth_user != subject_account:
				is_self = False

				# Friends
				if friends.filter(pk=auth_user.id):
					is_friend = True
				else:
					is_friend = False
					
					# Friend request
					if get_friend_request_or_false(sender=subject_account, receiver=auth_user) != False:
						request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
						context['pending_friend_request_id'] = get_friend_request_or_false(sender=subject_account, receiver=auth_user).pk
					elif get_friend_request_or_false(sender=auth_user, receiver=subject_account) != False:
						request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
					else:
						request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
			
		else:
			return render(request, template_name="errors/does_not_exist.html")
				
			# Set the template variables to the values

	else:
		return redirect('login')

	context['is_self'] = is_self
	context['is_friend'] = is_friend
	context['request_sent'] = request_sent
	context['friend_requests'] = friend_requests
	context['BASE_URL'] = settings.BASE_URL
	context['friends'] = friends
	print(friends)

	return render(request, "account/account.html", context)

# Optimized
@login_required(login_url="login")
def update_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	if auth_user.is_authenticated:	
		try:
			auth_user_account = BaseAccount.objects.get(id=auth_user.id)
			context['base_account'] = auth_user_account

		except BaseAccount.DoesNotExist:
			return render(request, template_name="errors/does_not_exist.html")

		# If the formis being submitted
		if request.method == "POST":
			if request.POST:
				form = UpdateForm(request.POST, instance=auth_user)
				if form.is_valid():
					form.save()
					return redirect("account", subject_user_id=auth_user.id)
				else:
					form = UpdateForm(request, instance=auth_user)
					context['form'] = form
			else:
				form = UpdateForm(request, instance=auth_user)
				context['form'] = form	

	return render(request, "account/edit_account.html", context)

# Optimized
@login_required(login_url="login")
def delete_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect("login")
	if auth_user.is_authenticated:
		auth_user_account = BaseAccount.objects.get(id=auth_user.id)

		if auth_user_account:
			
			# Should be subject user
			if auth_user != auth_user_account:
				return render(request, template_name="errors/not_allowed.html")

			elif auth_user == auth_user_account:

				if auth_user_account.is_learner:
					learner_account = LearnerAccount.objects.get(user=auth_user)
					learner_account.is_active = False
					learner_account.save()

				elif not auth_user_account.is_learner:
					teacher_account = TeacherAccount.objects.get(user=auth_user)
					teacher_account.is_active = False
					teacher_account.save()

				auth_user.is_active = False
				auth_user.save()
				logout(request)
				return redirect('register')
		else:
			return render(request, template_name="errors/does_not_exist.html")
	else:
		redirect('login')

