# coding=utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (authenticate, login as auth_login,
	logout as auth_logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from accounts.forms import LoginForm, AddUserForm
from annoying.functions import get_config


def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	next_uri = request.REQUEST.get('next', get_config('LOGIN_REDIRECT_URL',
		reverse('home')))
	# rescuing poor users from infinite redirection loop
	if next_uri == get_config('LOGIN_URL', reverse('login')):
		next_uri = get_config('LOGIN_REDIRECT_URL', reverse('home'))

	form = LoginForm()

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid() and form.user:
			auth_login(request, form.user)
			messages.success(request, "Hello, {0}.".format(form.user))
			return redirect(next_uri)

	return TemplateResponse(request, 'accounts/login.html', {
		'form': form,
		'next': next_uri,
	})


@login_required
def logout(request):
	next_uri = request.REQUEST.get('next', reverse('home'))
	auth_logout(request)
	messages.success(request, "Bye bye.")
	return redirect(next_uri)


@login_required
def add_user(request):
	if not request.user.is_superuser:
		return redirect(reverse('index'))

	form = AddUserForm()

	if request.method == 'POST':
		form = AddUserForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,
				"Successfully created a new user.")
			return redirect(reverse('index'))

	return TemplateResponse(request, 'accounts/add_user.html', {
		'form': form,
	})


def profile(request, user_id):
	user = get_object_or_404(User.objects.select_related(), pk=user_id)
	return TemplateResponse(request, 'accounts/profile.html', {
		'profile_user': user,
	})


def userlist(request):
	return TemplateResponse(request, 'accounts/list.html', {
		'users': User.objects.all().select_related(),
	})
