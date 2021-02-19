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
    path("", views.index_page, name="index"),
    path("catalog/<str:discipline>", views.catalog_page, name="discipline"),
    path("catalog", views.catalog_page, name="catalog"),
    path("file/<int:id>", views.document_page, name="document"),

    #-- Cabinet
    path("cabinet", views.cabinet, name="cabinet"),

    ##
    path("secure_media/document/<path:path>", views.secure_document, name="secure_document"),
]
