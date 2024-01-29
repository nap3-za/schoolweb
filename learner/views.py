from django.shortcuts import render, redirect
from .models import LearnerAccount
from account.models import BaseAccount
from .forms import LearnerAccountRegistration, LearnerAccountEdit
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required(login_url="login")
# def learner_registration_view(request, *args, **kwargs):
#     context = {}
#     auth_user = request.user

#     if not auth_user.is_authenticated:
#         return redirect('login')

#     elif auth_user.is_authenticated:
#         subject_user_id = kwargs.get("subject_user_id")
#         if subject_user_id:
#             account = BaseAccount.objects.get(id=subject_user_id)

#             if account and account.is_learner:
#                 context['form'] = LearnerAccountEdit()

#                 if request.method == "POST" and request.POST:
#                     form = LearnerAccountRegistration(request.POST)
#                     if form.is_valid():
#                         try:
#                             learner = LearnerAccount.objects.get(user=auth_user)
#                         except LearnerAccount.DoesNotExist:
#                             learner_account = form.save(commit=False)
#                             learner_account.user = auth_user
#                             learner_account.save()
#                             return redirect('home')
#                         return HttpResponse("You already have a learner account")

#                     else:
#                         form = LearnerAccountRegistration(request.POST)
#                         context['form'] = form
#             else:
#                 return render(request, "errors/not_allowed.html")

#     return render(request, "learner/reg.html", context)

# @login_required(login_url="login")
# def learner_account_update(request, *args, **kwargs):
#     context = {}
#     auth_user = request.user

#     if not auth_user.is_authenticated:
#         return redirect('login')
#     elif auth_user.is_authenticated:
#         subject_user_id = 
#         auth_user = BaseAccount.objects.get(id=subject_user_id)
#         if auth_user and auth_user.is_learner:
#             try:
#                 learner_account = LearnerAccount.objects.get(user=auth_user)
#                 context['learner_account'] = learner_account
#             except:
#                 return render(request, template_name="errors/does_not_exist.html")
#             if request.method == "POST" and request.POST:
#                     form = LearnerAccountEdit(request.POST)
#                     if form.is_valid():
#                         try:
#                             grade = form.cleaned_data['grade']
#                             stream = form.cleaned_data['stream']
#                             club = form.cleaned_data['club']
#                             sport = form.cleaned_data['sport']

#                             learner_account.grade = grade
#                             learner_account.stream = stream
#                             learner_account.club = club
#                             learner_account.sport = sport
#                             learner_account.save()
#                             return redirect('account', subject_user_id=auth_subject_user_id)
                            
#                         except:
#                             form = LearnerAccountRegistration(request.POST)
#                             context['form'] = form

#                         return HttpResponse("You already have a learner account")
#                     else:
#                         form = LearnerAccountEdit(request.POST)
#                         context['form'] = form
#         else:
#             return render(request, "errors/not_allowed.html")
#     return render(request, "learner/edit.html", context)
    
@login_required(login_url="login")
def learner_registration_view(request, *args, **kwargs):
    context = {}
    auth_user = request.user
    if not auth_user.is_authenticated:
        return redirect("login")

    if auth_user.is_authenticated:

        if auth_user.is_learner:
            
            if request.method == "POST" and request.POST:
                form = LearnerAccountRegistration(request.POST)

                if form.is_valid():
                    try:
                        learner_account = LearnerAccount.objects.get(user=auth_user)
                        return render(request, template_name="errors/done.html")
                    except LearnerAccount.DoesNotExist:
                        learner_account = form.save(commit=False)
                        learner_account.user = auth_user
                        learner_account.save()
                        return redirect('account', subject_user_id=auth_user.id)
                    
                    else:
                        form  = LearnerAccountRegistration(request.POST)
                        context['form'] = form
            else:
                return render(request, "errors/not_allowed.html")

    return render(request, "learner/reg.html", context)

@login_required(login_url="login")
def learner_account_update(request, *args, **kwargs):
    context = {}
    auth_user = request.user

    if not auth_user.is_authenticated:
        return redirect('login')

    elif auth_user.is_authenticated:
        subject_user_id = kwargs.get("subject_user_id")
        auth_user = BaseAccount.objects.get(id=auth_user.id)
        if auth_user and auth_user.is_learner:
            try:
                learner_account = LearnerAccount.objects.get(user=auth_user)
                context['learner_account'] = learner_account
            except:
                return redirect("reg_complete")

            if request.method == "POST" and request.POST:
                form = LearnerAccountEdit(request.POST)
                if form.is_valid():
                    try:
                        grade = form.cleaned_data['grade']
                        stream = form.cleaned_data['stream']
                        club = form.cleaned_data['club']
                        sport = form.cleaned_data['sport']

                        learner_account.grade = grade
                        learner_account.stream = stream
                        learner_account.club = club
                        learner_account.sport = sport
                        learner_account.save()
                        return redirect('account', subject_user_id=auth_user.id)
                    except Exception as e:
                        form = LearnerAccountEdit(request.POST)
                        context['form'] = form
                else:
                    form = LearnerAccountEdit(request.POST)
                    context['form'] = form
            else:
                pass
        else:
            return render(request, "errors/not_allowed.html")

    return render(request, "learner/edit.html", context)
    
     

