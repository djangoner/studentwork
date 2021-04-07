from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from main.views import paginate
from django.contrib import messages

from . import models, forms

def blog_page(request):
    q_tag = request.GET.get('tag')
    tag   = None
    #
    posts = models.Post.get_available()
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
    post = get_object_or_404(models.Post, pk=pk)
    #
    delcomment = request.GET.get("delcomm")
    if delcomment and request.user.is_superuser:
        try:
            com = models.PostComment.objects.get(id=delcomment)
            com.delete()
        except:
            pass
        return HttpResponseRedirect("?#comments")
    #
    if request.POST:
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            comment = form.save(commit=False)

            comment.author = request.user
            comment.post   = post
            comment.save()

            messages.add_message(request, messages.SUCCESS, "Комментарий успешно опубликован")
            return HttpResponseRedirect('#comments')
    else:
        form = forms.CommentForm(request.GET)

    #
    context = {
        'post': post,
    }
    return render(request, "blog_post.html", context=context)
