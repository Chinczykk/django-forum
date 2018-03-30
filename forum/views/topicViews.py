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
    if services.check_if_user_is_subscribing(request.user, section):
        is_user_sub = True
    else:
        is_user_sub = False

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
                    services.add_topic(cd["title"], cd["body"], section, request.user)
                    return redirect('forum:topic_view', section_name, cd["title"])
        
    return render(request, 'forum/topic/list.html', {'topics': topics,
                                                     'section': section,
                                                     'task': task,
                                                     'page': page,
                                                     'form': form,
                                                     'form_up': form_up,
                                                     'is_user_sub': is_user_sub})

def topic_view(request, section_name, topic_name):
    form = CommentForm()
    section = services.section_by_name(section_name)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            topic = services.topic_by_title(topic_name, section_name)
            services.add_comment(cd["body"], request.user, topic)
            form = CommentForm()
    topic = services.topic_by_title(topic_name, section_name)
    vote = services.get_vote(request.user, topic)
    if vote:
        vote_type = vote.vote_type
    else:
        vote_type = ''
    if topic_name:
        object_list = services.comments_for_topic(topic_name)
    else:
        object_list = ()
    page = request.GET.get('page')
    comments = methods.make_pagination(page, object_list, 4)
    return render(request, 'forum/topic/view.html', {'topic': topic,
                                                     'section': section,
                                                     'comments': comments,
                                                     'form': form,
                                                     'page': page,
                                                     'vote_type': vote_type})

def new_topic_list(request):
    if not request.user.is_authenticated():
        return redirect('forum:section_list')

    object_list = services.topics_for_subscribtions(request.user)
    page = request.GET.get('page')
    topics = methods.make_pagination(page, object_list, 4)
    return render(request, 'forum/topic/new_list.html', {'page': page,
                                                         'topics': topics})

@login_required
def delete_topic(request, section_name, id):
    topic_owner_id = services.topic_by_id(id).owner.id
    section_owner_id = services.section_by_name(section_name).owner.id
    logged_user_id = request.user.id
    if int(topic_owner_id) == int(logged_user_id) or int(section_owner_id) == int(logged_user_id):
        services.delete_topic(id)
    return redirect('forum:topic_list', section_name)

@login_required
def delete_comment(request, section_name, topic_name, id):
    comment_owner_id = services.comment_by_id(id).owner.id
    section_owner_id = services.section_by_name(section_name).owner.id
    logged_user_id = request.user.id
    if int(comment_owner_id) == int(logged_user_id) or int(section_owner_id) == int(logged_user_id):
        services.delete_comment(id)
    return redirect('forum:topic_view', section_name, topic_name)

@login_required
def upvote(request, section_name, id):
    topic = services.topic_by_id(id)
    services.upvote(request.user, topic)
    return redirect('forum:topic_view', section_name, topic.title)

@login_required
def downvote(request, section_name, id):
    topic = services.topic_by_id(id)
    services.downvote(request.user, topic)
    return redirect('forum:topic_view', section_name, topic.title)