from django import forms

from django.contrib.auth import (
	authenticate, 
	get_user_model, 
	login,
	logout,
	)

from .models import Product, UserProfile, TransactionItem

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

User = get_user_model()



class UserLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}), max_length=30, required=True, label='')
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), max_length=30, required=True, label='')


	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username=username, password=password)

			if not user or not user.is_active:
				raise forms.ValidationError("Sorry invalid login details. Try again")

			if not user.userprofile.is_verified:
				raise forms.ValidationError("Not yet Verified")

		return super(UserLoginForm, self).clean(*args, **kwargs)
			


	def login(self, request):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		user = authenticate(username=username, password=password)

		return user


class UserRegistrationForm(forms.ModelForm):

	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}), max_length=30, required=True, label='')
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}), max_length=30, required=True, label='')
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}), max_length=120, required=True, label='')
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}), max_length=30, required=True, label='')
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), max_length=30, required=True, label='')
	password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}), max_length=30, required=True, label='')
	
	class Meta:
		model = User
		fields = ['first_name','last_name', 'email', 'username', 'password', 'password_confirm']

	def clean_password_confirm(self):

		password = self.cleaned_data.get("password")
		password_confirm = self.cleaned_data.get("password_confirm")

		if password != password_confirm:
			raise forms.ValidationError("Passwords Must Much")
		return password

	def clean_username(self):
		username = self.cleaned_data.get("username")
		username_qs = User.objects.filter(username=username)

		if username_qs.exists():
			raise forms.ValidationError("This username already exists")

		return username

	def clean_email(self):

		email = self.cleaned_data.get("email")
		email_qs = User.objects.filter(email=email)

		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")

		return email



class UserProfileForm(forms.ModelForm):
	
	class Meta:
		model = UserProfile
		fields = ['profile_pic']



class VerificationForm(forms.Form):

	email = forms.EmailField(label='Enter your Email', required=True, max_length=120)
	verification_code = forms.CharField(label='Enter the verification code', required=True, max_length=10)

	def clean(self, *args, **kwargs):

		email = self.cleaned_data.get("email")
		verification_code = self.cleaned_data.get("verification_code")

		user_obj = User.objects.get(email=email)
		profile_obj = UserProfile.objects.get(user=user_obj)

		if profile_obj.pin != verification_code:
			raise forms.ValidationError("Incorrect Verification Code")
		else:
			print(profile_obj.pin)
			profile_obj.is_verified = True
			profile_obj.save()


		return super(VerificationForm, self).clean(*args, **kwargs)


class UserEditForm(forms.ModelForm):

	first_name = forms.CharField(label='First Name', required=True, max_length=120)
	last_name = forms.CharField(label='Last Name', required=True, max_length=120)
	username = forms.CharField(label='Username', required=True, max_length=120)
	email = forms.EmailField(label='Email', required=True, max_length=120)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email']



class UserProfileEditForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ['profile_pic']



class ProductForm(forms.ModelForm):

	title = forms.CharField(label='Title', required=True, max_length=120)
	description = forms.CharField(widget=forms.Textarea(), max_length=512, required=True, label='Description')

	class Meta:
		model = Product
		fields = ['title', 'description', 'image1', 'videofile']


class TransactionForm(forms.ModelForm):

	is_available = forms.BooleanField(required=False)
	is_active = forms.BooleanField(required=False)

	def __init__(self, request, *args, **kwargs):
		self.page_request_var = request
		self.helper = FormHelper()
		self.helper.form_id = 'js-confirm-request-form'
		self.helper.form_method = 'post'
		self.helper.form_action = 'mainapp:confirm-request'

		self.helper.add_input(Submit('submit', 'Confirm Request'))


		super(TransactionForm, self).__init__(*args, **kwargs)


	class Meta:
		model = Product
		fields = ['is_available','is_active']


class RevokeForm(forms.ModelForm):

	is_available = forms.BooleanField(required=False)
	is_active = forms.BooleanField(required=False)

	def __init__(self, request, *args, **kwargs):
		self.page_request_var = request
		self.helper = FormHelper()
		self.helper.form_id = 'js-revoke-request-form'
		self.helper.form_method = 'post'
		self.helper.form_action = 'mainapp:revoke-request'

		self.helper.add_input(Submit('submit', 'Revoke'))


		super(RevokeForm, self).__init__(*args, **kwargs)


	class Meta:
		model = Product
		fields = ['is_available','is_active']
