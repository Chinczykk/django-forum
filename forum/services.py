from .models import Section, Topic, Comment

def find_sections(search):
    return Section.objects.filter(name__contains=search)

def topics_by_section_name(name):
    return Topic.objects.filter(section__name=name)

def topic_by_title(title, section_name):
    return Topic.objects.filter(title=title, section__name=section_name)[0]

def section_by_name(name):
    return Section.objects.filter(name=name)[0]

def comments_for_topic(topic_name):
    return Comment.objects.filter(topic__title=topic_name)