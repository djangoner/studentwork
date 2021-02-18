from django.contrib import admin

from . import models


@admin.register(models.Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )

@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploaded', 'approved')
    list_filter = ('file_type', 'approved', 'language')

    readonly_fields = ('file_type', 'document_pages', 'uploaded', 'author')
    fieldsets = (
        ('Общая информация', {
            'fields': ('title', 'annotation', 'type', 'discipline', 'language')
            }),
        ('Файл', {
            'fields': ('file', 'file_type', 'document_pages', 'approved', 'uploaded', 'author')
            }),
    )
