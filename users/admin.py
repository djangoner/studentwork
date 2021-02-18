from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'email', 'last_login', 'balance')
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = (
        ('Общая информация', {
            'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'balance')
        }),
        ('Права', {
            'fields': ('user_permissions', 'groups', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Дополнительная информация', {
            'fields': ('last_login', 'date_joined')
        })
    )
