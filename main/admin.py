from django.contrib import admin
from django.http import HttpResponseRedirect

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

    readonly_fields = ('file_type', 'file_size', 'document_pages', 'uploaded', 'author', 'approved')
    fieldsets = (
        ('Общая информация', {
            'fields': ('title', 'annotation', 'type', 'discipline', 'language')
            }),
        ('Файл', {
            'fields': ('file', 'file_type', 'file_size', 'document_pages', 'approved', 'uploaded', 'author')
            }),
    )
    change_form_template = "admin/change_document.html"

    def response_change(self, request, obj):
        if "_document_accept" in request.POST:
            obj.approved = True
            obj.save()
            self.message_user(request, "Вы проверили документ, бонус автору будет отправлен,")
            return HttpResponseRedirect(".")
        elif "_document_recheck" in request.POST:
            obj.approved = None
            obj.save()
            self.message_user(request, "Вы пометили документ для модерации.")
            return HttpResponseRedirect(".")
        elif "_document_decline" in request.POST:
            obj.approved = False
            obj.save()
            self.message_user(request, "Вы отклонили документ, он будет удален.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
