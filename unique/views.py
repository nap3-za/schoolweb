from django.shortcuts import render, redirect
from django.conf import settings
from account.models import BaseAccount
from learner.models import LearnerAccount
from teacher.models import TeacherAccount
from django.contrib.auth.decorators import login_required

DEBUG = False

@login_required(login_url="login")
def home_view(request):
	auth_user = request.user
	auth_user_id = auth_user.id
	context = {}
	if auth_user.is_authenticated:
		try:
			auth_user_account = BaseAccount.objects.get(id=auth_user_id)
		except BaseAccount.DoesNotExist:
			return redirect('register')

		if auth_user_account.is_learner:
			try:
				auth_learner_account = LearnerAccount.objects.get(user=auth_user_account)
			except LearnerAccount.DoesNotExist:
				return redirect('reg_complete')
					
		elif not auth_user_account.is_learner:
			try:
				auth_teacher_account = TeacherAccount.objects.get(user=auth_user_account)
			except TeacherAccount.DoesNotExist:
				return redirect('reg_complete', subject_user_id=auth_user_id)
	else:
		return redirect('login')

	return render(request, "unique/home.html", context)





