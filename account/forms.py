from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import BaseAccount


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = BaseAccount
		fields = ('email', 'username', 'name', 'surname', 'gender', 'dob', 'admin_no', 'phone_no', 'password1', 'password2')

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = BaseAccount.objects.exclude(pk=self.instance.pk).get(email=email)
		except BaseAccount.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = BaseAccount.objects.exclude(pk=self.instance.pk).get(username=username)
		except BaseAccount.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)
	
	def clean_admin_no(self):
		admin_no = self.cleaned_data['admin_no']
		try:
			account = BaseAccount.objects.exclude(pk=self.instance.pk).get(admin_no=admin_no)
		except BaseAccount.DoesNotExist:
			return admin_no
		raise forms.ValidationError('Invalid admin number')

	def clean_dob(self):
		dob = self.cleaned_data['dob']
		if dob == None:
			raise forms.ValidationError('Invalid date of birth')
		return dob

class AuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = BaseAccount
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class UpdateForm(forms.ModelForm):

	class Meta:
		model = BaseAccount
		fields = ('username', 'email', 'name', 'surname', 'phone_no', 'hide_email' )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = BaseAccount.objects.exclude(pk=self.instance.pk).get(email=email)
		except BaseAccount.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = BaseAccount.objects.exclude(pk=self.instance.pk).get(username=username)
		except BaseAccount.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)

	def clean_phone_no(self):
		phone_no = self.cleaned_data['phone_no']
		try:
			account = BaseAccount.objects.exclude(pk=self.instance.pk).get(phone_no=phone_no)
		except BaseAccount.DoesNotExist:
			return phone_no
		raise forms.ValidationError('Phone number "%s" is already in use.' % phone_number)

	def save(self, commit=True):
		account = super(UpdateForm, self).save(commit=False)
		account.username = self.cleaned_data['username']
		account.email = self.cleaned_data['email'].lower()
		account.name = self.cleaned_data['name']
		account.surname = self.cleaned_data['surname']
		account.phone_no = self.cleaned_data['phone_no']
		account.hide_email = self.cleaned_data['hide_email']
		if commit:
			account.save()
		return account


