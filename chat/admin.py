from django.contrib import admin

from . import models

@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')

@admin.register(models.ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'author', 'text', 'sended', 'readed', 'created')