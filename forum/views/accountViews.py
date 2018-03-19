from django.shortcuts import render
from .. import services
from .. import services
from ..forms import RegisterForm
import re

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            services.add_user(cd["login"], cd["password"], cd["email"])
            info = 'Your account is ready. You can log in now.'
            return render(request, 'forum/account/login.html', {'info': info})
    else :
        form = RegisterForm()
    return render(request, 'forum/account/register.html', {'form': form})

def login(request):
    errors = {'login': '', 'password': '', 'bad_login_or_password': '', 'isError': False}
    valid = {'login': ''}
    if request.method == 'POST':
        login = request.POST.get("login", "")
        password = request.POST.get("password", "")
        
        if not login:
            errors['login'] = 'Please tell us your login'
        if not password:
            errors['password'] = 'Please tell us your password'
        if errors['login'] == '' and errors['password'] == '' and services.check_login_and_password(login, password):
            errors['bad_login_or_password'] = 'Bad login or password!'
    
        if errors['login'] != '' or errors['password'] != '' or errors['bad_login_or_password']:
            errors['isError'] = True

            if errors['login'] == '':
                valid['login'] = login

        else:
            request.session['user'] = services.get_user_by_login(login).id
            return render(request, 'forum/section/list.html', {})

    return render(request, 'forum/account/login.html', {'errors': errors, 'valid': valid})

def logout(request):
    try:
        del request.session['user']
    except:
        pass
    return render(request, 'forum/section/list.html', {})