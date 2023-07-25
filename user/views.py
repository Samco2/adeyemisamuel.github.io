from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from base.decorators import *

from .forms import UserUpdateForm, ProfileUpdateForm
from base.forms import *
from base.filters import PostFilter

from base.models import *



def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		email = request.POST.get('email')
		password =request.POST.get('password')

		#Little Hack to work around re-building the usermodel
		try:
			user = User.objects.get(email=email)
			user = authenticate(request, username=user.username, password=password)
		except:
			messages.error(request, 'User with this email does not exists')
			return redirect('login')

		if user is not None:
			login(request, user)
			messages.success(request, 'You are loggedin!')
			return redirect('home')

		else:
			messages.error(request, 'Email OR password is incorrect')

	context = {}
	return render(request, 'base/login.html', context)

def registerPage(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			messages.success(request, 'Account successfuly created!')

			user = authenticate(request, username=user.username, password=request.POST['password1'])

			if user is not None:
				login(request, user)


			next_url = request.GET.get('next')
			if next_url == '' or next_url == None:
				next_url = 'home'
			return redirect(next_url)
		else:
			messages.error(request, 'An error has occured with registration')
	context = {'form':form}
	return render(request, 'base/register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home')

@login_required(login_url="home")
def updateProfile(request):
	user = request.user
	profile = user.profile
	form = ProfileUpdateForm(instance=profile)
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=user)
		if user_form.is_valid():
			user_form.save()

		form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('home')


	context = {'form':form}
	return render(request, 'base/profile_form.html', context)
