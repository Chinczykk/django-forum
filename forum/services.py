from .models import Section, Topic, Comment, Subscribtion
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

def add_section(name, description, user):
    section = Section.objects.create(name=name, description=description, owner=user)
    section.save()
    subscribe(user, section)

def add_topic(title, body, section, user):
    topic = Topic.objects.create(title=title, body=body, section=section, owner=user)
    topic.save()
    return topic

def section_by_id(id):
    return Section.objects.get(id=id)

def add_comment(body, user, topic):
    comment = Comment.objects.create(body=body, owner=user, topic=topic)

def comment_by_id(id):
    return Comment.objects.get(id=id)

def delete_comment(id):
    comment = comment_by_id(id)
    comment.delete()

def topic_by_id(id):
    return Topic.objects.get(id=id)

def delete_topic(id):
    topic = topic_by_id(id)
    topic.delete()

def update_topic(id, title, body):
    topic = Topic.objects.get(id=id)
    topic.title = title
    topic.body = body
    topic.save()

def update_section(id, name, description):
    section = Section.objects.get(id=id)
    section.name = name
    section.description = description
    section.save()

def delete_section(id):
    section = Section.objects.get(id=id)
    section.delete()

def subscribe(user, section):
    if not check_if_user_is_subscribing(user, section):
        Subscribtion.objects.create(user=user, section=section)

def unsubscribe(user, section):
    if check_if_user_is_subscribing(user, section):
        sub = Subscribtion.objects.filter(user=user, section=section)[0]
        sub.delete()

def check_if_user_is_subscribing(user, section):
    if len(Subscribtion.objects.filter(user=user, section=section)) > 0:
        return True
    else:
        return False

def subscribtions_by_user(user):
    return Subscribtion.objects.filter(user=user)

def topics_for_subscribtions(user):
    subs = Subscribtion.objects.filter(user=user)
    topics = []
    for sub in subs:
        topics += topics_by_section_name(sub.section.name)
    return topics