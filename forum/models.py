from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='sections')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='topics')
    body = models.TextField()
    votes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    body = models.TextField()
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body

class Subscribtion(models.Model):
    user = models.ForeignKey(User, related_name='user')
    section = models.ForeignKey(Section, related_name='section')

class Vote(models.Model):
    user = models.ForeignKey(User, related_name='vote_user')
    topic = models.ForeignKey(Topic, related_name='topic')