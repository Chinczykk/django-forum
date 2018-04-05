from django.shortcuts import render, redirect
from .. import services
from .. import services
from .. import forms
import re
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def register(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                services.add_user(cd["username"], cd["password"], cd["email"])
                request.session["info"] = 'True'
                return redirect('forum:login')
        else :
            form = forms.RegisterForm()
        return render(request, 'forum/account/register.html', {'form': form})
    else:
        return redirect('forum:section_list')

def login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            try:
                del request.session["info"]
            except:
                None
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=cd['username'], password=cd['password'])
                if user is not None:
                    auth_login(request, user)
                    return render(request, 'forum/section/list.html', {})
                else:
                    error = 'Bad login or password'
                    return render(request, 'forum/account/login.html', {'form': form, 'error': error})
        else:
            form = forms.LoginForm()
        return render(request, 'forum/account/login.html', {'form': form})
    else:
        return redirect('forum:section_list')

def logout(request):
    auth_logout(request)
    return redirect('forum:section_list')

def profile(request, name):
    user = services.get_user_by_login(name)
    form = ''
    top_topics = services.top_upvoted_posts(user)
    if request.method == 'POST':
        if request.POST.get('cancel', '') == 'True':
            form = ''
        elif request.POST.get('save', '') == 'True':
            form = forms.UserProfileForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                services.edit_user_details(user, cd["firstname"], cd["lastname"])
                form = ''
        else:
            form = forms.UserProfileForm(initial={'firstname': user.first_name, 'lastname': user.last_name})
    return render(request, 'forum/account/profile.html', {'user_to_edit': user,
                                                          'topics': top_topics,
                                                          'form': form})