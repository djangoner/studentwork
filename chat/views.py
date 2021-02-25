from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import consumers, models, forms

def chat_page(request):
    context = {
        'iframe': True,
    }
    return render(request, "chat.html", context=context)


@csrf_exempt
def send_file(request):
    if not request.POST:
        return HttpResponse('no_data', status=422)
    #
    chat_id = request.POST.get('chat_id')
    form = forms.FileForm(request.POST, request.FILES)
    #
    if form.is_valid():
        data = form.cleaned_data
        try:
            chat = models.Chat.objects.get(pk=chat_id)
            if not(models.is_admin(request.user) or request.user == chat.user):
                print("Not in chat")
                raise ValueError('not_in_chat')
        except Exception as e:
            print("Chat id invalid:", e)
            return HttpResponse('chat_id_invalid', status=422)
        #
        msg = form.save(commit=False)
        msg.text = ""
        msg.chat = chat
        msg.author = "user" if chat.user == request.user else "admin"
        #
        if not msg.attachment:
            return HttpResponse('no_attachment', status=422)
        msg.save()
        consumers.ChatConsumer.handle_new_message(msg)
    else:
        return HttpResponse('invalid_data', status=422)
    return HttpResponse('ok')