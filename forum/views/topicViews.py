from django.shortcuts import render
from .. import services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def topic_list(request, section_name):
    if section_name:
        object_list = services.topics_by_section_name(section_name)
    else:
        object_list = ()
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    section = services.section_by_name(section_name)
    return render(request, 'forum/topic/list.html', {'topics': topics,
                                                     'section': section,
                                                     'page': page})

def topic_view(request, section_name, topic_name):
    topic = services.topic_by_title(topic_name, section_name)
    if topic_name:
        object_list = services.comments_for_topic(topic_name)
    else:
        object_list = ()
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, 'forum/topic/view.html', {'topic': topic,
                                                     'comments': comments,
                                                     'page': page})