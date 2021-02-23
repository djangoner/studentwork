from django.shortcuts import render


def chat_page(request):
    context = {
        'iframe': True,
    }
    return render(request, "chat.html", context=context)
