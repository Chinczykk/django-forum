from django.shortcuts import render, redirect
from .. import services
from .. import methods
from django.contrib.auth.decorators import login_required


@login_required
def subscribtion_list(request):
    if request.user:
        subs = services.subscribtions_by_user(request.user)
        object_list = ([sub.section for sub in subs])
    else:
        object_list = ()
    page = request.GET.get('page')
    sections = methods.make_pagination(page, object_list, 8)
    return render(request, 'forum/subscribtion/list.html', {'sections': sections,
                                                            'page': page})

@login_required
def subscribe_section(request, id):
    section = services.section_by_id(id)
    services.subscribe(request.user, section)
    return redirect('forum:topic_list', section.name)

@login_required
def unsubscribe_section(request, id):
    section = services.section_by_id(id)
    services.unsubscribe(request.user, section)
    if request.POST.get('top_list', '') == "True":
        return redirect('forum:topic_list', section.name)
    else:
        return redirect('forum:subscribtion_list')