from django.shortcuts import render
from .. import services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def topic_list(request, section_name):
    section = services.section_by_name(section_name)
    check_add = ''

    if request.POST.get('checker_if_add', '') == "True" or request.POST.get('first_checker', '') == "True":
        check_add = add_topic(request, section)

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
    
    if check_add != '':
        if check_add['is_added']:
            data = generate_data_for_view(request, check_add['is_added'], section_name)
            topic = services.topic_by_title(check_add['added_topic'], section_name)
            return render(request, 'forum/topic/view.html', {'topic': topic,
                                                             'comments': data['comments'],
                                                             'page': data['page']})
    
    if request.POST.get('checker_if_add', '') == "True" or request.POST.get('first_checker', '') == "True":
        return render(request, 'forum/topic/list.html', {'topics': topics,
                                                        'section': section,
                                                        'page': page,
                                                        'add': 'True',
                                                        'errors': check_add['errors'],
                                                        'valid': check_add['valid']})

    return render(request, 'forum/topic/list.html', {'topics': topics,
                                                     'section': section,
                                                     'page': page})

def add_topic(request, section):
    errors = {'title': '', 'body': '', 'isError': False}
    valid = {'title': '', 'body': ''}
    is_added = False
    added_topic = ''
    if request.method == 'POST' and request.POST.get('checker_if_add', '') != 'True':
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')

        if not title:
            errors['title'] = 'Please tell us title'
        elif len(title) < 3:
            errors['title'] = 'Title should have atleast 5 characters'
        if not body:
            errors['body'] = 'Body of your topic can not be empty'

        if errors['title'] != '' or errors['body'] != '':
            errors['isError'] = True

            if errors['title'] == '':
                valid['title'] = title
            if errors['body'] == '':
                valid['body'] = body
        else:
            if request.session['user']:
                user = request.session['user']
                added_topic = services.add_topic(title, body, section, user)
                is_added = True

    return {'errors': errors, 'valid': valid, 'is_added': is_added, 'added_topic': added_topic}

def topic_view(request, section_name, topic_name):
    data = generate_data_for_view(request, topic_name, section_name)
    return render(request, 'forum/topic/view.html', {'topic': data['topic'],
                                                     'comments': data['comments'],
                                                     'page': data['page']})

def generate_data_for_view(request, topic_name, section_name):
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
    return {'topic': topic, 'comments': comments, 'page': page}