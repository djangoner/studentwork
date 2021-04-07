from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from . import models

class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'blog:blog',
        ]

    def location(self, item):
        return reverse(item)


class PostsSitemap(Sitemap):
    def items(self):
        return models.Post.objects.all()
