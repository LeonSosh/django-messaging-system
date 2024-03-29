from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "receiver", "creation_date", "is_read")
    list_filter = ("is_read", "creation_date")
    search_fields = ("subject", "message", "sender__username", "receiver__username")
