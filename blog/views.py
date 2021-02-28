from django.shortcuts import render, get_object_or_404
from main.views import paginate

from . import models

def blog_page(request):
    q_tag = request.GET.get('tag')
    tag   = None
    #
    posts = models.Post.objects.filter(is_publicated=True)
    if q_tag:
        try:
            tag = models.Tag.objects.get(pk=q_tag)
        except:
            pass
        else:
            posts = posts.filter(tags=tag)
    #
    page = paginate(request, posts)

    context = {
        'page': page,
        'tag': tag,
    }

    return render(request, "blog.html", context=context)

def view_post(request, pk):
    context = {
        'post': get_object_or_404(models.Post, pk=pk)
    }
    return render(request, "blog_post.html", context=context)
