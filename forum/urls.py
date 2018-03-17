from django.conf.urls import url
from views import sectionViews
from views import topicViews
from views import accountViews

urlpatterns = [ 
    #url(r'^$', views.subscriptions_topics, name='subscriptions_topics')
    url(r'^find_section/', sectionViews.section_list, name='section_list'),
    url(r'^add_section/',    sectionViews.add_section, name='add_section'),
    url(r'^register/', accountViews.register, name='register'),
    url(r'^login/', accountViews.login, name='login'),
    url(r'^logout/', accountViews.logout, name='logout'),
    url(r'^(?P<section_name>[\w\-]+)/$', topicViews.topic_list, name='topic_list'),
    url(r'^(?P<section_name>[\w\-]+)/(?P<topic_name>[\w\-]+)/', topicViews.topic_view, name='topic_view'),
]