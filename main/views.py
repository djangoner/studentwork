from django.shortcuts import render, get_object_or_404, reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, FileResponse, Http404, HttpResponseForbidden
from django.contrib import messages
import logging
import os

from . import models

BASE_PRICE = 10

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("users:login") + "?next=" + request.path)

        ##-- If logged in
        return func(request, *args, **kwargs)

    return wrapper


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
        discipline_search = get_object_or_404(models.Discipline, slug=discipline)
        objects = discipline_search.visible_documents # Only visible
    else:
        discipline_search = None
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
        "discipline": discipline_search if discipline else discipline,
        "page": page
    }
    template = "catalog_discipline.html" if discipline else "catalog.html"
    return render(request, template, context=context)

def document_page(request, id):
    document = get_object_or_404(models.Document, pk=id)

    context = {
        "doc": document,
        # "price": price,
        # "can_buy": can_buy,
        "file_link": reverse("main:document_download", args=[document.id]),
    }
    return render(request, "document.html", context=context)


def document_download(request, id):
    document = get_object_or_404(models.Document, pk=id)
    price = BASE_PRICE
    owning = document in request.user.buyed_documents.all()
    user = request.user
    #
    if not request.user.is_authenticated: # If not logged in return to document
        return HttpResponseRedirect(document.get_absolute_url() )

    # If not owning buy
    if not owning:
        if request.user.balance < price:
            messages.add_message(request, messages.WARNING, "Недостаточно баллов для загрузки файла!")
            return HttpResponseRedirect(document.get_absolute_url())
        logging.info(f"Processing payment: user ({user}), price ({price}), balance({user.balance} => {user.balance - price})")
        user.balance = user.balance - price
        user.buyed_documents.add(document)
        user.save()
        logging.info(f"Payment of user {user} processed.")
        # messages.add_message(request, messages.SUCCESS, "Работа успешно куплена!")
        # return HttpResponseRedirect("?#buyed")
    else:
        logging.info(f"User {user} is already owning file")
    #
    # can_buy = (request.user.balance >= BASE_PRICE) if request.user.is_authenticated else None
    context = {
        "document": document,
        "price": price,
        "download_link": document.file_download_url,
    }
    return render(request, "document_download.html", context=context)


def secure_document(request, path):
    base_path = "media/secure/documents"
    file      = os.path.join(base_path, path)
    relpath   = os.path.relpath(file, "media")
    if not os.path.exists(file):
        return Http404("not_exists")
    ## If exists
    doc = get_object_or_404(models.Document, file=relpath) # If no doc found return 404
    #
    if request.user.is_authenticated and doc in request.user.buyed_documents.all():
        return FileResponse(open(file, "rb"), as_attachment=True)
    #
    return HttpResponseForbidden("access_denied")

#-- Cabinet and users

@login_required
def cabinet(request):
    return render(request, "cabinet/cabinet.html")
