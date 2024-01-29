from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
import os
from .utils import genders

from friend.models import FriendList

admin_no_encoded = 1010
class BaseAccountManager(BaseUserManager):
	def create_user(self, email, username, name, surname, gender, dob, admin_no, phone_no, is_learner=True, password=None):
		if not (email, username, name, surname, gender, dob, admin_no, phone_no, is_learner):
			raise ValueError('User must have all and valid information')
		
		if admin_no == 1010:
			is_learner = False

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			name=name,
			surname=surname,
			gender=gender,
			dob=dob,
			admin_no=admin_no,
			phone_no=phone_no,
			is_learner=is_learner,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, name, surname, gender, dob, admin_no, phone_no, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			name=name,
			surname=surname,
			gender=gender,
			dob=dob,
			admin_no=admin_no,
			phone_no=phone_no,
			is_learner=False,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user




class BaseAccount(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(verbose_name="username", max_length=30, unique=True)
	name 					= models.CharField(verbose_name="name", max_length=255, unique=False, null=False, blank=False, default="None")
	surname					= models.CharField(verbose_name="surname", max_length=255, unique=False, null=False, blank=False, default="None")
	gender          		= models.CharField(choices=genders, verbose_name="gender", max_length=10, blank=False, null=False, default="Female")
	dob            			= models.DateField(verbose_name="dob", unique=False , auto_now_add=False, blank=False, null=False, default=2000-1-1)
	admin_no				= models.IntegerField(verbose_name="admin_no", unique=True, null=False, blank=False, default=0)
	phone_no        		= models.IntegerField(verbose_name="phone_no", unique=True, null=False, blank=False, default=0)

	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	is_learner 				= models.BooleanField(verbose_name="is_learner", default=True)
	hide_email				= models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'name', 'surname', 'gender', 'dob', 'admin_no', 'phone_no']

	objects = BaseAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

