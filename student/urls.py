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
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler403, handler500
from django.contrib.sitemaps.views import sitemap 

from main.sitemaps import StaticViewSitemap, DisciplinesSitemap, DocumentsSitemap
from blog.sitemaps import PostsSitemap
import main.views


sitemaps = {
    'static': StaticViewSitemap,
    'disciplines': DisciplinesSitemap,
    'documents': DocumentsSitemap,
    'blog_posts': PostsSitemap,
}

handler404 = 'main.views.handler_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    ##
    path('', include(('users.urls', 'users'), namespace="users")),
    path('', include(('main.urls', 'main'), namespace="main")),
    # path('', include(('chat.urls', 'chat'), namespace="chat")),
    path('', include(('blog.urls', 'blog'), namespace="blog")),
    ## CMS After custom urls
    re_path(r'^', include('cms.urls')),
    #
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #
    path("<str:discipline>", main.views.catalog_page, name="discipline"),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
