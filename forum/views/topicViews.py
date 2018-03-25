from django.shortcuts import render, redirect
from .. import services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from ..forms import TopicForm, CommentForm
from .. import methods

def topic_list(request, section_name):
    section = services.section_by_name(section_name)
    task = ''
    form = None
    form_up = False
    if request.session.get('_auth_user_id', False):
        userLogged = request.session.get('_auth_user_id', False)

    if section_name:
        object_list = services.topics_by_section_name(section_name)
    else:
        object_list = ()
    page = request.GET.get('page')
    topics = methods.make_pagination(page, object_list, 4)
    
    if request.method == 'POST':
        if request.POST.get('edit_topic', '') == 'True':
            id = request.POST.get('edit_id', '')
            request.session['edit_id'] = id
            topic = services.topic_by_id(id)
            form = TopicForm(initial={'title': topic.title, 'body': topic.body})
            task = 'edit'
            form_up = 'True'
        elif request.POST.get('cancel', '') == 'True':
            task = ''
        elif request.POST.get('edit_checker', '') == 'True':
            form_up = 'True'
            task = 'edit'
            form = TopicForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                id = request.session.get('edit_id', False)
                services.update_topic(id, cd['title'], cd['body'])
                del request.session['edit_id']
                form_up = ''
                task = ''
        else:
            form = TopicForm()
            task = 'add'
            form_up = 'True'
            if request.POST.get('add_checker', '') == 'True':
                form = TopicForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    userId = request.session.get('_auth_user_id', False)
                    services.add_topic(cd["title"], cd["body"], section, userId)
                    return redirect('forum:topic_view', section_name, cd["title"])
        
    return render(request, 'forum/topic/list.html', {'topics': topics,
                                                     'section': section,
                                                     'task': task,
                                                     'page': page,
                                                     'form': form,
                                                     'form_up': form_up})

def topic_view(request, section_name, topic_name):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            topic = services.topic_by_title(topic_name, section_name)
            userId = request.session.get('_auth_user_id', False)
            services.add_comment(cd["body"], userId, topic)
            form = CommentForm()
    topic = services.topic_by_title(topic_name, section_name)
    if topic_name:
        object_list = services.comments_for_topic(topic_name)
    else:
        object_list = ()
    page = request.GET.get('page')
    comments = methods.make_pagination(page, object_list, 4)
    return render(request, 'forum/topic/view.html', {'topic': topic,
                                                     'sectionName': section_name,
                                                     'comments': comments,
                                                     'form': form,
                                                     'page': page})

@login_required
def delete_topic(request, section_name, id):
    topic_owner_id = services.topic_by_id(id).owner.id
    logged_user_id = request.session.get("_auth_user_id", False)
    if int(topic_owner_id) == int(logged_user_id):
        services.delete_topic(id)
    return redirect('forum:topic_list', section_name)

@login_required
def delete_comment(request, section_name, topic_name, id):
    comment_owner_id = services.comment_by_id(id).owner.id
    logged_user_id = request.session.get("_auth_user_id", False)
    if int(comment_owner_id) == int(logged_user_id):
        services.delete_comment(id)
    return redirect('forum:topic_view', section_name, topic_name)