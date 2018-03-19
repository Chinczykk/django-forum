from django.shortcuts import render
from .. import services
from .. import services
from .. import forms
import re
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            services.add_user(cd["login"], cd["password"], cd["email"])
            info = 'Your account is ready. You can log in now.'
            return render(request, 'forum/account/login.html', {'info': info}) # TODO: MAKE REDIRECT BECOUSE IT DOESNT WORK
    else :
        form = forms.RegisterForm()
    return render(request, 'forum/account/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['login'], password=cd['password'])
            if user is not None:
                auth_login(request, user)
                return render(request, 'forum/section/list.html', {})
            else:
                error = 'Bad login or password'
                return render(request, 'forum/account/login.html', {'form': form, 'error': error})
    else:
        form = forms.LoginForm()
    return render(request, 'forum/account/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return render(request, 'forum/section/list.html', {})