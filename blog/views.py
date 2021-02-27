from django.shortcuts import render
from main.views import paginate

from . import models

def blog_page(request):
    posts = models.Post.objects.filter(is_publicated=True)
    page = paginate(request, posts)

    context = {
        'page': page,
    }

    return render(request, "blog.html", context=context)
