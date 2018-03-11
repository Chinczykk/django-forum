from django.shortcuts import render
from .models import Section, Topic, Comment
# Create your views here.

def section_list(request):  
    sections = Section.objects.all()
    return render(request, 'forum/section/list.html', {'sections': sections})