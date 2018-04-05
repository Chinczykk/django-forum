from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate

# Create your tests here.

class RegisterFormTest(TestCase):

    def test_register_from(self):
        form = RegisterForm({
            'username': 'test1234',
            'password': 'test1234',
            'confirm_password': 'test1234',
            'email': 'test@wp.pl'
        })
        self.assertTrue(form.is_valid())
        register = form.save()
        self.assertEqual(register.username, 'test1234')
        self.assertEqual(register.password, 'test1234')
        self.assertEqual(register.email, 'test@wp.pl')

    def test_blank_data(self):
        form = RegisterForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
            'confirm_password': ['This field is required.'],
            'email': ['This field is required.']
        })

    def test_different_passwords(self):
        form = RegisterForm({
            'username': 'test1234',
            'password': 'test1234',
            'confirm_password': 'test12345',
            'email': 'test@wp.pl'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'confirm_password': ['Passwords are not equal']
        })

    # Bad email and too short username and password
    def test_bad_email_and_too_short_username_and_password(self):
        form = RegisterForm({
            'username': 'test',
            'password': 'test',
            'confirm_password': 'test',
            'email': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field should have atleast 5 characters'],
            'password': ['This field should have atleast 8 characters'],
            'email': ['Enter a valid email address.']
        })

