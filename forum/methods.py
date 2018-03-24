from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def make_pagination(page, object_list, objects_per_page):
    paginator = Paginator(object_list, objects_per_page)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)