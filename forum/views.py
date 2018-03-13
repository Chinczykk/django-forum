from django.shortcuts import render
from . import services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def section_list(request):
    searchValue = request.GET.get('search', '')
    if request.method == 'GET' and searchValue:
        object_list = services.find_sections(searchValue)
    else:
        object_list = ()
    paginator = Paginator(object_list, 7)
    page = request.GET.get('page')
    try:
        sections = paginator.page(page)
    except PageNotAnInteger:
        sections = paginator.page(1)
    except EmptyPage:
        sections = paginator.page(paginator.num_pages)
    return render(request, 'forum/section/list.html', {'sections': sections,
                                                       'page': page})

def topic_list(request, name):
    if name:
        object_list = services.topics_by_section_name(name)
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
    sectionName = name
    return render(request, 'forum/topic/list.html', {'topics': topics,
                                                     'sectionName': sectionName,
                                                     'page': page})