from django.conf.urls import url
from views import sectionViews
from views import topicViews

urlpatterns = [ 
    #url(r'^$', views.subscriptions_topics, name='subscriptions_topics')
    url(r'^find_section/', sectionViews.section_list, name='section_list'),
    url(r'^(?P<section_name>[\w\-]+)/$', topicViews.topic_list, name='topic_list'),
    url(r'^(?P<section_name>[\w\-]+)/(?P<topic_name>[\w\-]+)/', topicViews.topic_view, name='topic_view'),
]