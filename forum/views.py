from django.shortcuts import render
from . import services
# Create your views here.

def section_list(request):
    searchValue = request.GET.get('search', '')
    if request.method == 'GET' and searchValue:
        sections = services.find_sections(searchValue)
    else:
        sections = ()
    return render(request, 'forum/section/list.html', {'sections': sections})

def topic_list(request, name):
    topics = services.topics_by_section_name(name)
    if topics:
        sectionName = topics[0].section.name
    return render(request, 'forum/topic/list.html', {'topics': topics,
                                                     'sectionName': sectionName})