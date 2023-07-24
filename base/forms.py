from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from user.models import Profile




class PostForm(ModelForm):

	class Meta:
		model = Post
		fields = '__all__'

		widgets = {
			'tags':forms.CheckboxSelectMultiple(),
		}
class CustomUserCreationForm(UserCreationForm):
	discipline = forms.CharField()
	

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'discipline', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']
		

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['profl_pic']
	
   