from django.contrib import admin

from . import models

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publicated', 'publicated')
    list_filter = ('is_publicated',)
    search_fields = ('title', 'content')
    readonly_fields = ('created',)
    filter_horizontal = ('tags', )

    fieldsets = [
        ('Содержание', {
            'fields': ('title', 'content', 'image', 'tags'),
        }),
        ('Публикация', {
            'fields': ('is_publicated', 'publicated', 'created'),
        }),
    ]

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

    fieldsets = [
        ('Тег', {
            'fields': ('name', 'slug')
        })
    ]
