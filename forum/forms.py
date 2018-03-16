from django import forms

class RegisterForm(forms.Form):
    login = forms.CharField(max_length=15)
    password = forms.PasswordInput()
    confirmPassword = forms.PasswordInput()
    email = forms.EmailField()