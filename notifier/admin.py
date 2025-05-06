from django.contrib import admin
from .models import TelegramSubscriber


@admin.register(TelegramSubscriber)
class TelegramSubscriberAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'created_at')
    search_fields = ('chat_id',)
