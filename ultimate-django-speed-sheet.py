"""
Database setup
"""
DBNAME = ""
DBPASSWORD = ""
DBUSER = "django"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DBNAME,
        'USER': DBUSER,
        'PASSWORD': DBPASSWORD,

        'HOST': 'localhost',
        'PORT': 5432,
    }
}




"""
Base Account model
"""
class Account(AbstractBaseUser):

	email 			= models.EmailField(unique=True, verbose_name="email", max_length=60, blank=False, null=False)
	username 		= models.CharField(unique=True, verbose_name="username", max_length=255, blank=False, null=False)

    # My fields
    name            = models.CharField(unique=False, verbose_name="name", max_length=255, null=False, blank=False)
    surname         = models.CharField(unique=False, verbose_name="surname", max_length=255, null=False, blank=False)
    gender          = models.CharField(choices=genders, verbose_name="gender", max_length=10, blank=False, null=False, default="Female")
    dob             = models.DateField(unique=False, verbose_name="dob", auto_now_add=False, null=False, blank=False)
    phone_no        = models.IntegerField(unique=True, verbose_name="phone_no", null=False, blank=False)

    # Default fields
	date_joined  	= models.DateTimeField(auto_now_add=True, verbose_name="date_joined")
	last_login  	= models.DateTimeField(auto_now_add=True, verbose_name="last_login")
	hide_email 		= models.BooleanField(default=True, verbose_name="hide_email")
	is_active 		= models.BooleanField(default=True, verbose_name="is_active")
	is_superuser  	= models.BooleanField(default=False, verbose_name="is_superuser")
	is_staff  		= models.BooleanField(default=False, verbose_name="is_staff")
	is_admin  		= models.BooleanField(default=False, verbose_name="is_admin")

	objects = BaseAccountManager()

	USERNAME_FIELD = ['email']
	REQUIRED_FIELDS = ['username', 'name', 'surname', 'gender', 'dob', 'phone_no']

	def __str__(self):
		return self.name

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True



"""
Account manager
"""
class BaseAccountManager(BaseUserManager):

    def create_user(self, email, username, name, surname, gender, dob, phone_no, password=None):
        if not (username,email):
            return ValueError('User must have all and valid info')

        user = self.model(email=self.normalize_email(email), username=username, name=name, surname=surname, gender=gender, dob=dob, phone_no=phone_no)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, surname, gender, dob, phone_no, password=None):
        user = self.create_user(email=self.normalize_email(email), username=username,, name=name, surname=surname, gender=gender, dob=dob, phone_no=phone_no, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


"""
Admin for the model
"""
class Admin(admin.ModelAdmin):

    list_display = ()

    readonly_fields = ()
    search_fields = ()

    fieldsets = ()
    list_filter = ()
    filter_horizontal = ()

    class Meta:
        model = 

admin.site.register()

""" 
Model backend
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CaseInsensitiveModelBackend(ModelBackend):
    # Default = None
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_m = get_user_model()
        if username == None:
            # Getting it from the USERNAME_FIELD specified in models.py
            username = kwargs.get(user_m.USERNAME_FIELD)       
        try:
            case_insensetive_username_field = '{}__iexact'.format(user_m.USERNAME_FIELD)
            # Getting the user using the case_insensetive_username_field72
            user = user_m._default_manager.get(**{case_insensetive_username_field: username})
        except user_m.DoesNotExist:
            # Create a new one
            user_m().set_password(password)        
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


"""
Model setup
"""
AUTH_USER_MODEL = 'account.Account'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'account.backends.CaseInsensitiveModelBackend',
)



"""
Statiffiles setup
"""
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = 'static_cdn'
MEDIA_ROOT = 'media_cdn'

STATICFILES_DIRS = [
    Path.joinpath(BASE_DIR, 'static'),
    Path.joinpath(BASE_DIR, 'media'),
]

BASE_URL = "http://127.0.0.1:800/"
"""
Staticfiles urls setup
"""
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    


""" 
Raising field and non-field errors
"""
{% for field in form %}
	<p>
	{% for error in field.errors %}
		<p style="color: red">{{ error }}</p>
	{% endfor %}
	</p>
{% endfor %}


{% if form.non_field_errors %}
	<div style="color: red">
		<p>{{ form.non_field_errors }}</p>
	</div>
{% endif %}


"""
Account views
"""
def register_view(request, *args, **kwrgs):
    user = request.user
    context = {}

    if user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if not user.is_authenticated:
                form.save()
                email = form.cleaned_data['email']
                raw_password = form.cleaned_data['password1']
                account = authenticate(email=email, password=raw_password)
                login(request, account)
                return redirect('home')
            elif user.is_authenticated:
                return redirect('Home')
        else:
            form = RegisterForm(request.POST)
            context['registerForm'] = form            
    return render(request, "account/register.html", context)

def login_view(request, *args, **kwrgs):
    user = request.user
    context = {}
    if user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            raw_password = request.POST['password']
            account = authenticate(email=email, password=raw_password)
            if account:
                login(request, account)
                return redirect('home')
        else:
            form = LoginForm(request.POST)
            context['loginForm'] = form
    return render(request, "account/login.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='http://127.0.0.1:8000/login/')
def account_view(request, *args, **kwargs):
    context = {}
    user = request.user
    # Template variables
    is_friend = None
    request_sent = None
    is_self = None

    them_to_you = FriendRequestStatus.THEM_SENT_TO_YOU.value
    you_to_them = FriendRequestStatus.YOU_SENT_TO_THEM.value
    no_request = FriendRequestStatus.NO_REQUEST_SENT.value

    if not user.is_authenticated:
        return render(request, "errors/not_auth.html")


    elif user.is_authenticated:
        account_id = kwargs.get("user_id")
        if account_id:

            # Account we are viewing
            try:
                account = BaseAccount.objects.get(id=account_id)
            except:
                account = False
            if account:
                context['account'] = account
                if account == user:
                    is_self = True
                    context['is_self'] = is_self
                    context['user'] = account
                    try:
                        friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
                        context['friend_requests'] = friend_requests
                        try:
                            friends = FriendList.objects.get(user=user)
                        except FriendList.DoesNotExist:
                            friend_list = FriendList.objects.create(user=user)
                            friend_list.save()
                            friends = friend_list
                            context['friends'] = friends.friends.all()
                        context['friends'] = friends.friends.all()
                    except FriendRequest.DoesNotExist:
                        friend_requests = 0
                        context['friend_requests'] = friend_requests

                elif account != user:
                    is_self = False
                    context['is_self'] = is_self
                    account_friend_list = None
                    user_friend_list = None
                    try:
                        user_friend_list = FriendList.objects.get(user=user)
                        account_friend_list = FriendList.objects.get(user=account)

                    except FriendList.DoesNotExist:
                        account_friend_list = FriendList.objects.create(user=account)
                        account_friend_list.save()  
                        user_friend_list = FriendList.objects.create(user=user)                      
                        user_friend_list.save()

                    if user_friend_list and account_friend_list:
                        if are_friends(user, account):
                            is_friend = True
                            context['is_friend'] = is_friend
                        else:
                            if get_friend_request(sender=user, receiver=account) != False:
                                request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                                context['request_sent'] = request_sent
                                context['friend_request_id'] =  get_friend_request(sender=user, receiver=account).pk 
                                print(f"[+] {request_sent} ")

                            if get_friend_request(sender=account, receiver=user) != False:
                                request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                                context['request_sent'] = request_sent

                                print(f"[+] {request_sent} ")
                            
                            elif request_sent != FriendRequestStatus.YOU_SENT_TO_THEM.value and request_sent != FriendRequestStatus.THEM_SENT_TO_YOU.value:
                                print("[+] Else case is executing")
                                request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                                context['request_sent'] = request_sent
                    else:
                        return render(request, template_name='errors/does_not_exist.html')
                else:
                    return render(request, template_name='errors/not_allowed.html')
            else:
                return render(request, template_name="errors/does_not_exist.html")
        else:
            return render(request, template_name="errors/does_not_exist.html")
    else:
        is_self = False
        context['is_self'] = is_self
        return render(request, template_name="errors/not_auth.html")

    context['is_friend'] = is_friend
    context['request_sent'] = request_sent
    context['is_self'] = is_self
    return render(request, "account/account.html", context)

@login_required(login_url='http://127.0.0.1:8000/login/')
def delete_view(request, *args, **kwargs):
    user = request.user
    context = {}
    context['form'] = DeleteForm
    if not user.is_authenticated:
        return redirect('login')

    elif user.is_authenticated:
        account_id = kwargs.get("user_id")
        if account_id:
            account = BaseAccount.objects.get(id=account_id)
            if account:
                context['user'] = user
                if request.method == "POST":
                    form = DeleteForm(request.POST)
                    if form.is_valid():
                        email = form.cleaned_data['email1']
                        password = form.cleaned_data['password1']
                        try:
                            account = authenticate(email=email, password=password)
                            account.delete()
                        except:
                            return render("errors/cannot_auth.html")
                        return HttpResponse("Account deleted successfully")
                    else:
                        form = DeleteForm(request.POST)
                        context['deleteForm'] = form                        
                else:
                    form = DeleteForm(request.POST)
                    context['deleteForm'] = form
            else:
                return render("errors/does_not_exist.html")
        else:
            return render("errors/not_auth.html")
    else:
        return render("errors/not_auth.html")

    return render(request, "account/delete.html", context)

   
    return render(request, "account/delete.html", context)

@login_required(login_url='http://127.0.0.1:8000/login/')
def update_view(request, *args, **kwargs):
    user = request.user
    context = {}
    context['form'] = UpdateAccountForm
    if not user.is_authenticated:
        return redirect('login')
    
    elif user.is_authenticated:
        account_id = kwargs.get("user_id")
        if account_id:
            account = BaseAccount.objects.get(id=account_id)
            if account:
                context['user'] = account
                if request.method == "POST":
                    if request.POST:
                        form = UpdateAccountForm(request.POST, instance=request.user)
                        context['form'] = form
                        if form.is_valid():
                            if user == account:
                                form.save()
                                return redirect('account',user_id=account_id)
                            else:
                                return HttpResponse("This is not your account")
                        else:
                            form = UpdateAccountForm(request.POST)
                            context['updateForm'] = form
                    else:
                        return render("errors/not_post.html")
            else:
                return render("errors/does_not_exist.html")
        else:
            return render("errors/does_not_exist.html")
    else:
        return render("errors/not_auth.html")
    return render(request, "account/update.html", context)

# This is basically almost exactly the same as friends/friend_list_view
@login_required(login_url='http://127.0.0.1:8000/login/')
def account_search(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = BaseAccount.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
            user = request.user
            accounts = [] # [(account1, True), (account2, False), ...]
            if user.is_authenticated:
                # get the authenticated users friend list
                try:
                    auth_user_friend_list = FriendList.objects.get(user=user)
                except FriendList.DoesNotExist:
                    auth_user_friend_list = FriendList.objects.create(user=user)
                    auth_user_friend_list.save()
                for account in search_results:
                    accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
                context['accounts'] = accounts
            else:
                for account in search_results:
                    accounts.append((account, False))
                context['accounts'] = accounts
                
    return render(request, "account/account_search.html", context)

"""
Account forms
"""
class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, required=True)
    phone_no = forms.IntegerField(required=True)
    
    class Meta:
        model = BaseAccount
        fields = ('email', 'username', 'name', 'surname', 'gender', 'dob', 'phone_no')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = BaseAccount.objects.exclude(pk=self.instance.pk).get(email=email)
        except BaseAccount.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email "{email}" is already in use.')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = BaseAccount.objects.exclude(pk=self.instance.pk).get(username=username)
        except BaseAccount.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username "{username}" is already in use.')

class LoginForm(forms.ModelForm):
    password    = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = BaseAccount
        fields = ('email', 'password')
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

class UpdateAccountForm(forms.ModelForm):

    class Meta:
        model = BaseAccount
        fields = ('email', 'username', 'name', 'surname', 'phone_no', 'hide_email', 'hide_sensetive_data')

    def save(self, commit=True):
        account = super(UpdateAccountForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.name = self.cleaned_data['name']
        account.surname = self.cleaned_data['surname']
        account.phone_no = self.cleaned_data['phone_no']
        account.email = self.cleaned_data['email'].lower()
        account.hide_email = self.cleaned_data['hide_email']
        account.hide_sensetive_data = self.cleaned_data['hide_sensetive_data']
        if commit:
            account.save()
        return account

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            accounts = BaseAccount.objects.filter(email=email)
            if len(accounts) >1:
                raise forms.ValidationError(f"Email {email} already in use")
            elif len(accounts) == 1:
                return email
        except Exception as e:
            raise forms.ValidationError(str(e))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            accounts = BaseAccount.objects.filter(username=username)
            if len(accounts) > 1:
                raise forms.ValidationError(f"Username {username} already in use")
            elif len(accounts) == 1:
                return username
        except Exception as e:
            raise forms.ValidationError(str(e))

class DeleteForm(forms.Form):

    email1          = forms.EmailField(max_length=60, required=False)
    email2          = forms.EmailField(max_length=60, required=False)

    password1       = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False)
    password2       = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False)

    def clean_all(self):
        email1 = self.cleaned_data['email1']
        email2 = self.cleaned_data['email2']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if email1 != email2:
            raise forms.ValidationError("Emails do not match")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
              
        try:
            account = BaseAccount.objects.get(email=email1, password=password1)
        except BaseAccount.DoesNotExist:
            raise forms.ValidationError("Invalid email or password")

  
"""
Friend           


"""
Html template
"""
{% load static %}
{% extends 'base.html' %}

{% block title %}

{% endblock title %}

{% block css %}

{% endblock css %}

{% block content %}
<div class="container-fluid">
	<div class="row justify-content-center">
		<div class="col-md-7">
			<div class="card my-4 border border-dark ">
				<div class="card-body">
					<h2 class="card-title card-h"></h2>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}


