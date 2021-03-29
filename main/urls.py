"""student URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index_page, name="index"),
    path("search", views.search_page, name="search"),
    path("search/results", views.search_results, name="search_results"),
    # path("catalog", views.catalog_page, name="catalog"),

    path("file/<int:id>", views.document_page, name="document"),
    path("file/<int:id>/download", views.document_download, name="document_download"),

    path("order_work", views.order_work, name="order_work"),

    #-- Cabinet
    path("cabinet", views.cabinet, name="cabinet"),
    path("cabinet/document_upload", views.document_upload, name="document_upload"),

    ##
    path("secure_media/document/<path:path>", views.secure_document, name="secure_document"),
    path("media/secure/documents/<path:path>", views.secure_document, name="secure_document2"),

    #
    # path("<str:discipline>", views.catalog_page, name="discipline"),
    # path("api/search", views.api_search, name="api_search"),
]
