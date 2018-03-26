from django.conf.urls import url
from views import sectionViews
from views import topicViews
from views import accountViews

urlpatterns = [ 
    #url(r'^$', views.subscriptions_topics, name='subscriptions_topics')
    #url(r'^/', sectionViews.section_list, name='default'),
    url(r'^find_section/', sectionViews.section_list, name='section_list'),
    url(r'^register/', accountViews.register, name='register'), 
    url(r'^login/', accountViews.login, name='login'),
    url(r'^logout/', accountViews.logout, name='logout'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/delete_topic/(?P<id>[\w\- ]+)/', topicViews.delete_topic, name='delete_topic'),
    url(r'^delete_section/(?P<id>[\w\- ]+)/', sectionViews.delete_section, name='delete_section'),
    url(r'^subscribe/(?P<id>[\w\- ]+)/', sectionViews.subscribe_section, name='subscribe'),    
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/(?P<topic_name>[\w\-\:\?\! ]+)/delete_comment/(?P<id>[\w\- ]+)/', topicViews.delete_comment, name='delete_comment'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/$', topicViews.topic_list, name='topic_list'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/(?P<topic_name>[\w\-\:\?\! ]+)/', topicViews.topic_view, name='topic_view'),
    #url(r'^(.*)', sectionViews.section_list, name='default')
]