from .models import Section, Topic, Comment
from django.contrib.auth.models import User

def find_sections(search):
    return Section.objects.filter(name__contains=search)

def topics_by_section_name(name):
    return Topic.objects.filter(section__name=name)

def topic_by_title(title, section_name):
    if Topic.objects.filter(title=title, section__name=section_name):
        return Topic.objects.filter(title=title, section__name=section_name)[0]

def section_by_name(name):
    if Section.objects.filter(name=name):
        return Section.objects.filter(name=name)[0]

def comments_for_topic(topic_name):
    return Comment.objects.filter(topic__title=topic_name)

def check_if_login_exists(login):
    if len(User.objects.filter(username=login)) > 0:
        return True
    else:
        return False

def check_if_email_exists(email):
    if len(User.objects.filter(email=email)) > 0:
        return True
    else:
        return False
    
def add_user(login, password, email):
    user = User.objects.create(username=login, password=password, email=email)
    user.set_password(password)
    user.save()

def check_login_and_password(login, password):
    if len(User.objects.filter(username=login)) > 0:
        user = User.objects.filter(username=login)[0]
        if user.check_password(password):
            return False
    return True

def get_user_by_login(name):
    return User.objects.get(username=name)
    
#TODO: Prepare one method to get user by any attribute 

def get_user_by_id(id):
    return User.objects.get(id=id)

def check_if_section_name_exists(name):
    if len(Section.objects.filter(name=name)) > 0:
        return True
    else:
        return False

def add_section(name, description, userId):
    user = get_user_by_id(userId)
    section = Section.objects.create(name=name, description=description, owner=user)
    section.save()

def add_topic(title, body, section, userId):
    user = get_user_by_id(userId)
    topic = Topic.objects.create(title=title, body=body, section=section, owner=user)
    topic.save()
    return topic

def add_comment(body, userId, topic):
    user = get_user_by_id(userId)
    comment = Comment.objects.create(body=body, owner=user, topic=topic)