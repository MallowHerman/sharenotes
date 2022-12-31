from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def loginView(request):
	page = 'login'
	if request.method == 'POST':
		user_username = request.POST.get('user_username')
		user_password = request.POST.get('user_password')
		user = authenticate(request, username=user_username, password=user_password)
		if user is not None:
			 login(request, user)
			 return redirect('base:index')
		else:
			messages.error(request, 'Email e senha estão incorretos')


	context = {
	'page': page
	}
	return render(request, 'accounts/login-register.html', context)


def registerView(request):
	page = 'register'

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('base:index')
	else:
		form = UserRegisterForm()

	context = {
	'page': page,
	'form': form
	}
	return render(request, 'accounts/login-register.html', context)



def logoutView(request):
	logout(request)
	return redirect('login')