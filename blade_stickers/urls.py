from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom Admin Site Branding
admin.site.site_header = "Blade Stickers Admin"
admin.site.site_title = "Blade Stickers Admin Portal"
admin.site.index_title = "Manage Products, Gallery, Testimonials & Site Settings"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.website.urls', namespace='website')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('contact/', include('apps.contact.urls', namespace='contact')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
