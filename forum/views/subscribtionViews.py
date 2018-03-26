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