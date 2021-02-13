from django.contrib import admin
from .models import UsersEmail


@admin.register(UsersEmail)
class UserEmailAdmin(admin.ModelAdmin):
    """Электронные адреса пользователей"""
    list_display = ('email', 'date')



