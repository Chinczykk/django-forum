from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.subscriptions_topics, name='subscriptions_topics')
    url(r'^find_section/', views.section_list, name='section_list')
]