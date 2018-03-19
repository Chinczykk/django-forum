from django.shortcuts import render
from .. import services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def section_list(request):
    searchValue = request.GET.get('search', '')
    if request.method == 'GET' and searchValue:
        object_list = services.find_sections(searchValue)
    else:
        object_list = ()
    paginator = Paginator(object_list, 7)
    page = request.GET.get('page')
    try:
        sections = paginator.page(page)
    except PageNotAnInteger:
        sections = paginator.page(1)
    except EmptyPage:
        sections = paginator.page(paginator.num_pages)

    if request.POST.get('checker_if_add', '') == "True" or request.POST.get('first_checker', '') == "True":
        check_add = add_section(request)
        return render(request, 'forum/section/list.html', {'sections': sections,
                                                       'page': page,
                                                       'add': 'True',
                                                       'errors': check_add['errors'],
                                                       'valid': check_add['valid']})
    else:
        return render(request, 'forum/section/list.html', {'sections': sections,
                                                       'page': page})

def add_section(request):
    errors = {'name': '', 'description': '', 'isError': False}
    valid = {'name': '', 'description': ''}
    if request.method == 'POST' and request.POST.get('checker_if_add', '') != 'True':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if not name:
            errors['name'] = 'Please tell us name of section'
        elif len(name) < 3:
            errors['name'] = 'Name of section should have atleast 3 characters'
        elif services.check_if_section_name_exists(name):
            errors['name'] = 'This name of section is already taken!'
        if not description:
            errors['description'] = 'Every section should have description'

        if errors['name'] != '' or errors['description'] != '':
            errors['isError'] = True

            if errors['name'] == '':
                valid['name'] = name
            if errors['description'] == '':
                valid['description'] = description
        else:
            if request.session['user']:
                user = request.session['user']
                services.add_section(name, description, user)

    return {'errors': errors, 'valid': valid}