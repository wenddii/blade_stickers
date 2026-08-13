from django.urls import path
from .views import ProductGalleryView, ProductDetailView, ProductModalApiView

app_name = 'products'

urlpatterns = [
    path('', ProductGalleryView.as_view(), name='gallery'),
    path('api/<int:pk>/modal/', ProductModalApiView.as_view(), name='product_modal_api'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
