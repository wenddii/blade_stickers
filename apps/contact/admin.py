from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status_badge', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('name', 'phone', 'email', 'message', 'created_at')
    
    def status_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color: #666; font-weight: bold;">✔ Read</span>')
        return format_html('<span style="background-color: #00E5FF; color: #090909; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">NEW MESSAGE</span>')
    status_badge.short_description = "Status"

    actions = ['mark_as_read', 'mark_as_unread']

    @admin.action(description="Mark selected messages as Read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as Unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
