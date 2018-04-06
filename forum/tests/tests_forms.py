from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import RegisterForm, LoginForm, SectionForm, TopicForm, CommentForm
from ..models import Section, Topic, Comment
from django.contrib.auth import authenticate
from .methods import *

# Create your tests here.

class RegisterFormTest(TestCase):

    def setUp(self):
        User.objects.create(username='test12345', password='test1234')

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
        check_form_for_errors(self, {}, {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
            'confirm_password': ['This field is required.'],
            'email': ['This field is required.']
        }, RegisterForm)

    def test_different_passwords(self):
        check_form_for_errors(self, {
            'username': 'test1234',
            'password': 'test1234',
            'confirm_password': 'test12345',
            'email': 'test@wp.pl'
        }, {
            'confirm_password': ['Passwords are not equal']
        }, RegisterForm)

    # Bad email and too short username and password
    def test_bad_email_and_too_short_username_and_password(self):
        check_form_for_errors(self, {
            'username': 'test',
            'password': 'test',
            'confirm_password': 'test',
            'email': 'test'
        }, {
            'username': ['This field should have atleast 5 characters'],
            'password': ['This field should have atleast 8 characters'],
            'email': ['Enter a valid email address.']
        }, RegisterForm)

    def test_taken_username(self):
        check_form_for_errors(self, {
            'username': 'test12345',
            'password': 'test1234',
            'confirm_password': 'test1234',
            'email': 'test@wp.pl'
        }, {
            'username': ['A user with that username already exists.']
        }, RegisterForm)

class SectionFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='logged', password='logged')
        self.section = Section.objects.create(name='taken', description='taken', owner=self.user)
    
    def test_good_credentials(self):
        form = SectionForm({
            'name': 'test123',
            'description': 'test'
        })
        self.assertTrue(form.is_valid())
        section = form.save(commit=False)
        section.owner = self.user
        section.save()
        self.assertEqual(section.name, 'test123')
        self.assertEqual(section.description, 'test')
        self.assertEqual(section.owner.username, 'logged')
        self.assertEqual(section.owner.id, 1)

    def test_empty_fields(self):
        check_form_for_errors(self, {}, {
            'name': ['This field is required.'],
            'description': ['This field is required.']
        }, SectionForm)

    def test_short_name(self):
        check_form_for_errors(self, {
            'name': 'te',
            'description': 'te'
        }, {
            'name': ['This field should have atleast 5 characters']
        }, SectionForm)

    def test_taken_name(self):
        check_form_for_errors(self, {
            'name': 'taken',
            'description': 't'
        }, {
            'name': ['Section with this name already exists']
        }, SectionForm)

class TopicFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='logged', password='logged')
        self.section = Section.objects.create(name='test12', description='test', owner=self.user)

    def test_good_credentials(self):
        form = TopicForm({
            'title': 'test123',
            'body': 'test'
        })
        self.assertTrue(form.is_valid())
        topic = form.save(commit=False)
        topic.owner = self.user
        topic.section = self.section
        topic.save()
        self.assertEqual(topic.title, 'test123')
        self.assertEqual(topic.body, 'test')
        self.assertEqual(topic.owner.id, 1)
        self.assertEqual(topic.owner.username, 'logged')
        self.assertEqual(topic.section.name, 'test12')
        self.assertEqual(topic.section.description, 'test')

    def test_empty_fields(self):
        check_form_for_errors(self, {}, {
            'title': ['This field is required.'],
            'body': ['This field is required.']
        }, TopicForm)

    def test_short_title(self):
        check_form_for_errors(self, {
            'title': 'te',
            'body': 'te'
        }, {
            'title': ['This field should have atleast 5 characters']
        }, TopicForm)

class CommentFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='logged', password='logged')
        self.section = Section.objects.create(name='test123', description='test', owner=self.user)
        self.topic = Topic.objects.create(title='test132', body='test', section=self.section, owner=self.user)

    def test_good_credentials(self):
        form = CommentForm({
            'body': 'test123'
        })
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.owner = self.user
        comment.topic = self.topic
        comment.save()
        self.assertEqual(comment.body, 'test123')
        self.assertEqual(comment.owner.id, 1)
        self.assertEqual(comment.owner.username, 'logged')
        self.assertEqual(comment.topic.title, 'test132')
        self.assertEqual(comment.topic.body, 'test')
        self.assertEqual(comment.topic.section.name, 'test123')
        self.assertEqual(comment.topic.section.description, 'test')

    def test_empty_fields(self):
        check_form_for_errors(self, {}, {
            'body': ['This field is required.']
        }, CommentForm)

class LoginFormTest(TestCase):

    def test_good_credentials(self):
        form = LoginForm({
            'username': 'test123',
            'password': 'test1234'
        })
        self.assertTrue(form.is_valid())

    def test_empty_fields(self):
        check_form_for_errors(self, {}, {
            'username': ['This field is required.'],
            'password': ['This field is required.']
        }, LoginForm)