from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ('image', 'image_preview', 'caption')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 70px; height: 70px; object-fit: cover; border-radius: 8px; border: 1px solid #00E5FF;" />',
                obj.image.url
            )
        return format_html('<span style="color: #888;">No Preview</span>')
    image_preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category_image_preview', 'active', 'ordering')
    list_editable = ('active', 'ordering')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('category_image_preview',)

    def category_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #00E5FF;" />',
                obj.image.url
            )
        return format_html('<span style="color: #666;">No Image</span>')
    category_image_preview.short_description = "Image Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'price_display', 'is_available', 
        'featured', 'active', 'product_thumbnail', 'created_at'
    )
    list_filter = ('category', 'featured', 'is_available', 'active', 'created_at')
    search_fields = ('title', 'description', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('product_thumbnail', 'created_at', 'updated_at')
    inlines = [GalleryImageInline]

    fieldsets = (
        ('Product Identification', {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Media & Display', {
            'fields': ('image', 'product_thumbnail')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available', 'featured', 'active')
        }),
        ('System Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        if obj.price:
            return f"${obj.price}"
        return "Custom Quote"
    price_display.short_description = "Price"

    def product_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #00E5FF;" />',
                obj.image.url
            )
        return format_html('<span style="color: #666;">No Image</span>')
    product_thumbnail.short_description = "Thumbnail"

    actions = ['make_featured', 'remove_featured', 'make_active', 'make_inactive']

    @admin.action(description="Mark selected items as Featured")
    def make_featured(self, request, queryset):
        queryset.update(featured=True)

    @admin.action(description="Remove selected items from Featured")
    def remove_featured(self, request, queryset):
        queryset.update(featured=False)

    @admin.action(description="Mark selected items as Active")
    def make_active(self, request, queryset):
        queryset.update(active=True)

    @admin.action(description="Mark selected items as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(active=False)
