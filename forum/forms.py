from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms import ValidationError
from . import services

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
        login = cleaned_data.get("login")

        if password != confirm_password:
            raise forms.ValidationError(
                {"confirm_password": ["Passwords are not equal",]}
            )
            
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError(
                {"login": ["Login is already taken",]}
            )

class LoginForm(forms.ModelForm):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('login', 'password')

class SectionForm(forms.ModelForm):
    name = forms.CharField(min_length=5,
                            max_length=50,
                            error_messages={'min_length': 'This field should have atleast 5 characters'},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = models.Section
        fields = ('name', 'description')
    def clean(self):
        cleaned_data = super(SectionForm, self).clean()
        name = cleaned_data.get("name")
        if services.check_if_section_name_exists(name):
            raise forms.ValidationError(
                {"name": ["Section with this name already exists",]}
            )

class EditSectionForm(forms.ModelForm):
    name = forms.CharField(min_length=5,
                            max_length=50,
                            error_messages={'min_length': 'This field should have atleast 5 characters'},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = models.Section
        fields = ('name', 'description')
    def clean(self):
        cleaned_data = super(EditSectionForm, self).clean()
        name = cleaned_data.get("name")
        last_name = cleaned_data.get("last_name")
        if name != last_name:
            if services.check_if_section_name_exists(name):
                raise forms.ValidationError(
                    {"name": ["Section with this name already exists",]}
                )

class TopicForm(forms.ModelForm):
    title = forms.CharField(min_length=5,
                            max_length=50,
                            error_messages={'min_length': 'This field should have atleast 5 characters'},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = models.Topic
        fields = ('title', 'body')

class CommentForm(forms.ModelForm):
    body = forms.CharField(min_length=1,
                            max_length=50,
                            error_messages={'min_length': 'This field should have atleast 5 characters'},
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = models.Comment
        fields = ('body',)

class UserProfileForm(forms.ModelForm):
    firstname = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = models.User
        fields = ('firstname', 'lastname')
                            
                            