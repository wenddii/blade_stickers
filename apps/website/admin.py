from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, Testimonial


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Branding & General', {
            'fields': ('site_name', 'logo', 'favicon', 'footer_text')
        }),
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle')
        }),
        ('About & Mission Story', {
            'fields': ('about_story', 'about_mission')
        }),
        ('Live Counters', {
            'fields': ('stats_stickers_count', 'stats_customers_count', 'stats_designs_count', 'stats_rating')
        }),
        ('Contact Info & Direct Messaging', {
            'fields': ('phone_number', 'telegram_username', 'whatsapp_number', 'email', 'address', 'map_embed_url')
        }),
        ('Social Links & Handles', {
            'fields': ('tiktok_handle', 'instagram_handle', 'facebook_link')
        }),
    )

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'role', 'rating_stars', 'avatar_preview', 'active', 'ordering', 'created_at')
    list_editable = ('active', 'ordering')
    list_filter = ('active', 'rating')
    search_fields = ('customer_name', 'role', 'message')
    readonly_fields = ('avatar_preview', 'created_at')

    def rating_stars(self, obj):
        return "★" * obj.rating
    rating_stars.short_description = "Rating"

    def avatar_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 2px solid #00E5FF;" />',
                obj.image.url
            )
        return format_html('<span style="color: #666;">No Image</span>')
    avatar_preview.short_description = "Avatar"
