from django.contrib import admin

from . import models

# class DisciplineInline(admin.TabularInline):
#     model = models.Discipline
#     extra = 0

@admin.register(models.Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', )
    readonly_fields = ('slug', )
    fieldsets = (
        ('Общая информация', {
            'fields': (('title', 'slug'))
            }),
    )
    # inlines = [
    #     DisciplineInline
    # ]

@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploaded', 'approved')
    list_filter = ('file_type', 'approved', 'language')
    search_fields = ('title', 'annotation', 'file', 'author')

    readonly_fields = ('file_type', 'file_size', 'document_pages', 'uploaded', 'author')
    fieldsets = (
        ('Общая информация', {
            'fields': ('title', 'annotation', 'type', 'discipline', 'language')
            }),
        ('Файл', {
            'fields': ('file', 'file_type', 'file_size', 'document_pages', 'approved', 'uploaded', 'author')
            }),
    )
