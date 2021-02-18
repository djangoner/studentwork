from django.shortcuts import render

from . import models


def index_page(request):
    disciplines_groups   = models.Discipline.objects.filter(subdisciplines__isnull=False)
    disciplines_nogroups = models.Discipline.objects.filter(subdisciplines__isnull=True, parent__isnull=True)
    context = {
        "disciplines_groups": disciplines_groups,
        "disciplines_nogroups": disciplines_nogroups,
    }
    return render(request, 'index.html', context=context)

def cabinet(request):
    return render(request, "cabinet/cabinet.html")
