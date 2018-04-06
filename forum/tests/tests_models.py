from django.test import TestCase
from ..models import User, Section, Topic

class TopicModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='logged', password='logged')
        self.section = Section.objects.create(name='test123', description='test', owner=self.user)
        self.topic = Topic.objects.create(title='test132', body='test', section=self.section, owner=self.user)

    def test_create_topic(self):
        self.assertEqual(self.topic.votes, 0)