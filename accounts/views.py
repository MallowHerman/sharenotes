from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from base.models import Document

# Create your views here.

def loginView(request):
	page = 'login'
	if request.method == 'POST':
		user_email = request.POST.get('user_email').lower()
		user_password = request.POST.get('user_password')
		print(user_email)
		print(user_password)
		try:
			user = User.objects.get(email=user_email)
		except:
			messages.error(request, "O usuário não existe")

		user = authenticate(request, username=user.username, password=user_password)

		if user is not None:
			 login(request, user)
			 return redirect('dashboard')
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
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
			messages.success(request, "Cadastro realizado com sucesso!")

			return redirect('login')
	else:
		form = UserRegisterForm()

	context = {
	'page': page,
	'form': form
	}
	return render(request, 'accounts/login-register.html', context)



def logoutView(request):
	logout(request)
	return redirect('base:index')



def profile(request, username):
	user = User.objects.get(username=username)
	documents = user.document_set.all()
	context = {
		'user': user,
		'documents': documents
	}
	return render(request, 'accounts/profile.html', context)

@login_required
def dashboard(request):
	user = User.objects.get(username=request.user)
	documents = user.document_set.all()
	context = {
		'user': user,
		'documents': documents
	}
	return render(request, 'accounts/dashboard.html', context)