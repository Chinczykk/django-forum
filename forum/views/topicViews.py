from django.shortcuts import render, redirect
from .. import services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import TopicForm, CommentForm

def topic_list(request, section_name):
    section = services.section_by_name(section_name)
    add = False
    form = None
    #if request.POST.get('checker', '') == "True":
    #    check_add = add_topic(request, section)

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
    
    if request.method == 'POST':
        form = TopicForm()
        add = 'True'
        if request.POST.get('checker', '') == 'True':
            form = TopicForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                userId = request.session.get('_auth_user_id', False)
                services.add_topic(cd["title"], cd["body"], section, userId)
                return redirect('forum:topic_view', section_name, cd["title"])
    
    return render(request, 'forum/topic/list.html', {'topics': topics,
                                                     'section': section,
                                                     'add': add,
                                                     'page': page,
                                                     'form': form})

def topic_view(request, section_name, topic_name):
    form = CommentForm()
    if request.method == 'POST':
        if request.POST.get('delete', '') == 'True':
            commentId = request.POST.get('delete_id', '')
            services.delete_comment(commentId)
        else:
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
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, 'forum/topic/view.html', {'topic': topic,
                                                     'sectionName': section_name,
                                                     'comments': comments,
                                                     'form': form,
                                                     'page': page})