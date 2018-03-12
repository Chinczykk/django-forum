from .models import Section, Topic, Comment

def find_sections(search):
    return Section.objects.filter(name__contains=search)

def topics_by_section_name(name):
    return Topic.objects.filter(section__name=name)