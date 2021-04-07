from . import models

def unread_messages(request):
    unread_messages = 0
    is_admin = models.is_admin(request.user)
    #
    if request.user.is_authenticated:
        if is_admin:
            unread_messages = models.ChatMessage.objects.filter(~models.models.Q(author="admin"), readed=False).count()
        else:
            matching_chats = models.Chat.objects.filter(user=request.user)
            if matching_chats:
                chat = matching_chats.first()
                unread_messages = chat.get_unread_count(is_admin)
    return {
        "unread_messages": unread_messages
    }
