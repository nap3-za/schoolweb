from django.shortcuts import render, redirect
from .forms import TeacherAccountRegistration, TeacherAccountEdit
from account.models import BaseAccount
from django.http import HttpResponse
from .models import TeacherAccount

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
def teacher_registration_view(request, *args, **kwargs):
    context = {}
    auth_user = request.user
    if not auth_user.is_authenticated:
        return redirect("login")

    if auth_user.is_authenticated:

        if not auth_user.is_learner:
            
            if request.method == "POST" and request.POST:
                form = TeacherAccountRegistration(request.POST)

                if form.is_valid():
                    try:
                        teacher_account = TeacherAccount.objects.get(user=auth_user)
                        return render(request, template_name="errors/done.html")
                    except TeacherAccount.DoesNotExist:
                        teacher_account = form.save(commit=False)
                        teacher_account.user = auth_user
                        teacher_account.save()
                        return redirect('account', subject_user_id=auth_user.id)
                    
                    else:
                        form  = TeacherAccountRegistration(request.POST)
                        context['form'] = form
            # else:
            #     return render(request, "errors/not_allowed.html")

    return render(request, "teacher/reg.html", context)

@login_required(login_url="login")
def teacher_account_update(request, *args, **kwargs):
    context = {}
    auth_user = request.user

    if not auth_user.is_authenticated:
        return redirect('login')

    elif auth_user.is_authenticated:
        subject_user_id = kwargs.get("subject_user_id")
        auth_user = BaseAccount.objects.get(id=auth_user.id)
        if auth_user and not auth_user.is_learner:
            try:
                teacher_account = TeacherAccount.objects.get(user=auth_user)
                context['teacher_account'] = teacher_account
            except:
                return redirect("reg_complete")

            if request.method == "POST" and request.POST:
                form = TeacherAccountEdit(request.POST)
                if form.is_valid():
                    try:
                        sport = form.cleaned_data['sport']
                        sub1 = form.cleaned_data['sub1']
                        sub2 = form.cleaned_data['sub2']
                        sub3 = form.cleaned_data['sub3']
                        stream1 = form.cleaned_data['stream1']
                        stream2 = form.cleaned_data['stream2']

                        teacher_account.sport = sport
                        teacher_account.sub1 = sub1
                        teacher_account.sub2 = sub2
                        teacher_account.stream1 = stream1
                        teacher_account.stream2 = stream2
                        teacher_account.save()
                        return redirect('account', subject_user_id=auth_user.id)
                    except Exception as e:
                        form = TeacherAccountEdit(request.POST)
                        context['form'] = form
                else:
                    form = TeacherAccountEdit(request.POST)
                    context['form'] = form
            else:
                pass
        else:
            return render(request, "errors/not_allowed.html")

    return render(request, "teacher/edit.html", context)
    
    
