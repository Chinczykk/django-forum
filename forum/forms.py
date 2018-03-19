from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

class RegisterForm(forms.ModelForm):
    login = forms.CharField(max_length=20,
                            min_length=5,
                            error_messages={'min_length': 'This field should have atleast 5 characters'},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=8,
                            error_messages={'min_length': 'This field should have atleast 8  characters'},
                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(error_messages={'min_length': 'This field should have atleast 5 characters'},
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('login', 'password', 'confirm_password', 'email')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                {"confirm_password": ["Passwords are not equal",]}
            )

class LoginForm(forms.ModelForm):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('login', 'password')