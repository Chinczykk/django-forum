from django.conf.urls import url
from views import sectionViews
from views import topicViews
from views import accountViews
from views import subscribtionViews

urlpatterns = [ 
    #url(r'^$', views.subscriptions_topics, name='subscriptions_topics')
    #url(r'^/', sectionViews.section_list, name='default'),
    url(r'^find_section/', sectionViews.section_list, name='section_list'),
    url(r'^subscribtions/', subscribtionViews.subscribtion_list, name='subscribtion_list'),
    url(r'^register/', accountViews.register, name='register'), 
    url(r'^login/', accountViews.login, name='login'),
    url(r'^logout/', accountViews.logout, name='logout'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/delete_topic/(?P<id>[\w\- ]+)/', topicViews.delete_topic, name='delete_topic'),
    url(r'^delete_section/(?P<id>[\w\- ]+)/', sectionViews.delete_section, name='delete_section'),
    url(r'^subscribe/(?P<id>[\w\- ]+)/', sectionViews.subscribe_section, name='subscribe'),    
    url(r'^unsubscribe/(?P<id>[\w\- ]+)/', sectionViews.unsubscribe_section, name='unsubscribe'),    
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/(?P<topic_name>[\w\-\:\?\! ]+)/delete_comment/(?P<id>[\w\- ]+)/', topicViews.delete_comment, name='delete_comment'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/$', topicViews.topic_list, name='topic_list'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/(?P<topic_name>[\w\-\:\?\! ]+)/', topicViews.topic_view, name='topic_view'),
    #url(r'^(.*)', sectionViews.section_list, name='default')
]