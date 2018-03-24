from django.shortcuts import render, redirect
from .. import services
from ..forms import SectionForm
from .. import methods

def section_list(request):
    searchValue = request.GET.get('search', '')
    if request.method == 'GET' and searchValue:
        object_list = services.find_sections(searchValue)
    else:
        object_list = ()
    page = request.GET.get('page')
    sections = methods.make_pagination(page, object_list, 7)
    if request.method == 'POST':
        form = SectionForm()
        if request.POST.get('checker', '') == "True":
            form = SectionForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                userId = request.session.get('_auth_user_id', False)
                services.add_section(cd["name"], cd["description"], userId)
                return redirect('forum:topic_list', cd["name"])

        return render(request, 'forum/section/list.html', {'sections': sections,
                                                                    'page': page,
                                                                    'form': form,
                                                                    'add': 'True'})
    else:
        return render(request, 'forum/section/list.html', {'sections': sections,
                                                       'page': page})