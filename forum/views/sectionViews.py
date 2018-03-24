from django.shortcuts import render, redirect
from .. import services
from ..forms import SectionForm, EditSectionForm
from .. import methods

def section_list(request):
    edit = ''
    searchValue = request.GET.get('search', '')
    if request.method == 'GET' and searchValue:
        object_list = services.find_sections(searchValue)
    else:
        object_list = ()
    page = request.GET.get('page')
    sections = methods.make_pagination(page, object_list, 7)
    if request.method == 'POST':
        if request.POST.get('edit', '') == 'True':
            id = request.POST.get('id', '')
            request.session['edit_id'] = id
            section = services.section_by_id(id)
            form = EditSectionForm(initial={'name': section.name, 'description': section.description})
            edit = 'True'
        elif request.POST.get('edit_checker', '') == 'True':
            form = EditSectionForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                id = request.session.get('edit_id', False)
                services.update_section(id, cd['name'], cd['description'])
                section = services.section_by_id(id)
                del request.session['edit_id']
                return redirect('forum:topic_list', section.name)
            else:
                edit = 'True'
        else:
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
                                                                    'form_up': 'True',
                                                                    'edit': edit})
    else:
        return render(request, 'forum/section/list.html', {'sections': sections,
                                                       'page': page})

def delete_section(request, id):
    services.delete_section(id)
    return redirect('forum:section_list')