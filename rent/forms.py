from django import forms

from django.contrib.auth.models import User
from rent.models import *

MAX_UPLOAD_SIZE = 2500000

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		username = cleaned_data['username']
		if User.objects.filter(username__exact=username):
			pass
		else:
			raise forms.ValidationError('Username does not exist.')
		return cleaned_data

class RegistrationForm(forms.Form):
	username   = forms.CharField(max_length = 20)
	first_name = forms.CharField(max_length=20)
	last_name  = forms.CharField(max_length=20)
	#email      = forms.CharField(max_length=50,
                                 #widget = forms.EmailInput(), required=False)
	password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
	password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())
	#short_bio = forms.CharField(max_length=430,required=False)


	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")
		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")
		return username

class OfferNewItem(forms.ModelForm):
	class Meta:
		model = OfferingItem
		fields = ['name','picture','description','reward']