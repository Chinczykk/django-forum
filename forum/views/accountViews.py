from django.shortcuts import render
from .. import services
from ..forms import RegisterForm
from .. import services
import re

def register(request):
    errors = {'login': '', 'password': '', 'confirmPassword': '', 'email': '', 'isError': False}
    valid = {'login': '', 'password': '', 'confirmPassword': '', 'email': ''}
    if request.method == 'POST':
        login = request.POST.get("login", "")
        password = request.POST.get("password", "")
        confirmPassword = request.POST.get("confirmPassword", "")
        email = request.POST.get("email", "")
        if not login:
            errors['login'] = 'Please tell us your login'
        elif len(login) < 5:
            errors['login'] = 'Login should have atleast 5 characters'
        elif services.check_login(login):
            errors['login'] = 'This login is already taken!'
        if not password:
            errors['password'] = 'Please tell us your password'
        elif len(password) < 8:
            errors['password'] = 'Password should have atleast 8 characters'
        if not confirmPassword:
            errors['confirmPassword'] = 'Please confirm your password'
        elif confirmPassword != password:
            errors['confirmPassword'] = 'Passwords are not equal'
        if not email:
            errors['email'] = 'Please tell us your email'
        elif not re.search('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
            errors['email'] = 'This is not correct email!'

        if errors['login'] != '' or errors['password'] != '' or errors['confirmPassword'] != '' or errors['email'] != '':
            errors['isError'] = True

            if errors['login'] == '':
                valid['login'] = login
            if errors['password'] == '':
                valid['password'] = password
            if errors['confirmPassword'] == '':
                valid['confirmPassword'] = confirmPassword
            if errors['email'] == '':
                valid['email'] = email
        
        else:
            services.add_user(login, password, email)
            return render(request, 'forum/account/register.html', {'errors': errors, 'valid': valid})
            #TODO: Call a login.html with a message 'You are registered. You can log in now'

    return render(request, 'forum/account/register.html', {'errors': errors,
                                                           'valid': valid})