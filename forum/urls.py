from django.conf.urls import url
from views import sectionViews
from views import topicViews
from views import accountViews
from views import subscribtionViews

urlpatterns = [ 
    #url(r'^$', views.subscriptions_topics, name='subscriptions_topics')
    #url(r'^/', sectionViews.section_list, name='default'),
    url(r'^$', topicViews.new_topic_list, name="default"),
    url(r'^find_section/', sectionViews.section_list, name='section_list'),
    url(r'^subscribtions/', subscribtionViews.subscribtion_list, name='subscribtion_list'),
    url(r'^register/', accountViews.register, name='register'), 
    url(r'^login/', accountViews.login, name='login'),
    url(r'^logout/', accountViews.logout, name='logout'),
    url(r'^new_topics/', topicViews.new_topic_list, name='new_topic_list'),
    url(r'^profile/(?P<name>[\w\-\:\?\! ]+)/', accountViews.profile, name='profile'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/delete_topic/(?P<id>[\w\- ]+)/', topicViews.delete_topic, name='delete_topic'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/upvote/(?P<id>[\w\- ]+)/', topicViews.upvote, name='upvote'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/downvote/(?P<id>[\w\- ]+)/', topicViews.downvote, name='downvote'),
    url(r'^delete_section/(?P<id>[\w\- ]+)/', sectionViews.delete_section, name='delete_section'),
    url(r'^subscribe/(?P<id>[\w\- ]+)/', subscribtionViews.subscribe_section, name='subscribe'),    
    url(r'^unsubscribe/(?P<id>[\w\- ]+)/', subscribtionViews.unsubscribe_section, name='unsubscribe'),    
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/(?P<topic_name>[\w\-\:\?\! ]+)/delete_comment/(?P<id>[\w\- ]+)/', topicViews.delete_comment, name='delete_comment'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/$', topicViews.topic_list, name='topic_list'),
    url(r'^(?P<section_name>[\w\-\:\?\! ]+)/(?P<topic_name>[\w\-\:\?\! ]+)/', topicViews.topic_view, name='topic_view'),
    #url(r'^(.*)', sectionViews.section_list, name='default')
]