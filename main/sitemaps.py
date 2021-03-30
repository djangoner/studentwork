from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from . import models

class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'main:search',
        ]

    def location(self, item):
        return reverse(item)


class DisciplinesSitemap(Sitemap):
    def items(self):
        return models.Discipline.objects.all()

class DocumentsSitemap(Sitemap):
    def items(self):
        return models.Document.objects.filter(approved=True)
