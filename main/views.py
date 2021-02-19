from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from . import models


def index_page(request):
    slice_rows = 3
    disciplines   = models.Discipline.objects.all()
    rows = []
    ##-- Slice to rows
    for i in range(0, slice_rows):
        rows.append(disciplines[i::slice_rows]) # Append sliced

    context = {
        'disciplines': disciplines,
        'discipline_rows':rows,
    }
    return render(request, 'index.html', context=context)

def catalog_page(request, discipline= None):
    if discipline:
        objects = get_object_or_404(models.Discipline, slug=discipline).visible_documents # Only visible
    else:
        objects = models.Document.objects.all()
    #
    paginator = Paginator(objects, per_page=100)
    page_num = request.GET.get('page', '1')
    if page_num.isdigit(): # Validate that page is digit
        page_num = int(page_num)
    else:
        page_num = 1
    #
    page = paginator.page(page_num)

    context = {
        "discipline": discipline,
        'page': page
    }
    template = "discipline.html" if discipline else "catalog.html"
    return render(request, template, context=context)



#-- Cabinet and users

def cabinet(request):
    return render(request, "cabinet/cabinet.html")
