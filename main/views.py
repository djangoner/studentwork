import logging
import os
import json
from itertools import chain
import jsonlines

from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, FileResponse, HttpResponseForbidden, \
            HttpResponseNotFound, JsonResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# from django.core import serializers
from django.db.models import Q

from . import models, forms, search_engine

BASE_PRICE = models.BASE_PRICE

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("users:login") + "?next=" + request.path)

        ##-- If logged in
        return func(request, *args, **kwargs)

    return wrapper

def paginate(request, objects):
    paginator = Paginator(objects, per_page=20)
    page_num = request.GET.get('page', '1')
    try:
        page = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)
    except:
        page = paginator.page(1)

    return page


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

    context = {
        "discipline": discipline_search if discipline else discipline,
        "page": paginate(request, objects)
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
    # Owning if document buyed or current user is author
    owning = document in request.user.buyed_documents.all() or request.user == document.author
    user = request.user
    #
    if not request.user.is_authenticated: # If not logged in return to document
        return HttpResponseRedirect(document.get_absolute_url() )

    # If not owning buy
    if not owning:
        if request.user.balance < price:
            messages.add_message(request, messages.WARNING, "Недостаточно баллов для загрузки файла! <a href='/faq'>Как пополнить баланс</a>")
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


def document_upload(request):
    #
    docs_on_moderation = models.Document.objects.filter(author=request.user, approved=None).count()
    can_upload = docs_on_moderation < 5
    #
    if request.POST and can_upload:
        form = forms.DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            #
            doc = form.save(commit=False)
            doc.approved = None
            doc.author = request.user
            #
            doc.save()
            messages.add_message(request, messages.SUCCESS, "Документ отправлен на модерацию")
            return HttpResponseRedirect(reverse("main:cabinet") + "#files")
    else:
        form = forms.DocumentUploadForm()
    #
    context = {
        "form": form,
        "can_upload": can_upload
    }
    return render(request, "cabinet/document_upload.html", context=context)


def secure_document(request, path):
    base_path = "media/secure/documents"
    file      = os.path.join(base_path, path)
    relpath   = os.path.relpath(file, "media")
    logging.info("Secure document handling %s" % file)
    if not os.path.exists(file):
        return HttpResponseNotFound("not_exists")
    ## If exists
    doc = get_object_or_404(models.Document, file=relpath) # If no doc found return 404
    #
    if request.user.is_superuser or (request.user.is_authenticated and doc in request.user.buyed_documents.all()):
        return FileResponse(open(file, "rb"), as_attachment=True)
    #
    return HttpResponseForbidden("access_denied")

def search_page(request):
    return render(request, "search_page.html")


def search_results(request):
    max_pages = 10
    per_page  = 10
    #-- Args check
    query = request.GET.get("search")
    # if query is None:
        # return redirect("main:index")
        # return HttpResponse("no_query", status=422)

    try:
        page  = int(request.GET.get("page", "1"))
    except ValueError:
        page = 1
        # return HttpResponse("invalid_page_number", status=422)
    #-- Call search engine
    try:
        search = search_engine.search_queryset(query, per_page=per_page, page=page, max_pages = max_pages).filter(approved=True)
    except Exception as e:
        logging.exception("SearchEngine search exception ", exc_info=e)
        search = False

    light_search = False
    if search == False:
        search = models.Document.objects.filter(Q(title__icontains=query) | Q(annotation__icontains=query)).filter(approved=True)[per_page * (page-1):per_page * page]
        light_search = True
    ##
    print("Search results:", search)
    context = {
        'iframe': True,
        'docs': search,
        'page': paginate(request, search),
        'light_search': light_search,
        'search_query': query,
    }
    return render(request, "search_results.html", context=context)


def order_work(request):
    def send_work(data):
        message = render_to_string("emails/form_order_work.html", {
            "data": data,
        })
        email = EmailMessage(
            'Форма \"Заказать работу\"',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ORDER_WORK_EMAIL],
            # html_message=message
        )
        if request.FILES:
            attachment = request.FILES['attachment']
            email.attach(attachment.name, attachment.read(), attachment.content_type)
        email.content_subtype = "html"
        email.send()
    def form_label(form, name):
        fields = form.fields
        if name in fields:
            f = fields[name]
            if hasattr(f, 'label'):
                return f.label
        return name

    if request.POST:
        form = forms.OrderWorkForm(request.POST, request.FILES)
    else:
        form = forms.OrderWorkForm()
    #
    if form.is_valid():
        data = form.cleaned_data
        data_f = data.copy()
        data_f.pop('attachment')
        logging.info(f"Order work form filled! Data: {data}")

        with jsonlines.open("order_work.jl", "a") as writer:
            writer.write(data_f)
        ##
        try:
            send_work({ form_label(form, k):v for k,v in data_f.items()})
        except Exception as e:
            logging.exception("Form request work sending failed", exc_info=e)

        return HttpResponse("ok", status=200)
    else:
        print(form.errors)
        return JsonResponse(dict(form.errors.as_json()), status=422)

#-- Cabinet and users

@login_required
def cabinet(request):
    docs_buyed   = request.user.buyed_documents.all()
    docs_uploaded= models.Document.objects.filter(author=request.user)
    docs = list(chain(docs_uploaded, docs_buyed))
    can_download_files = int(request.user.balance / BASE_PRICE)
    #
    context = {
        "page": paginate(request, docs),
        "docs_saved": docs_buyed.count(),
        "docs_uploaded": docs_uploaded.count(),
        "BASE_PRICE": BASE_PRICE,
        "can_download_files": can_download_files,
    }
    return render(request, "cabinet/cabinet.html", context=context)
