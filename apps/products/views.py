from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Category


class ProductGalleryView(ListView):
    model = Product
    template_name = 'products/gallery.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        queryset = Product.objects.filter(active=True).select_related('category').prefetch_related('gallery_images')
        
        # Search filter
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'all':
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(active=True)
        context['selected_category'] = self.request.GET.get('category', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(active=True).select_related('category').prefetch_related('gallery_images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related products in same category
        context['related_products'] = Product.objects.filter(
            category=self.object.category, 
            active=True
        ).exclude(pk=self.object.pk)[:4]
        return context


class ProductModalApiView(View):
    """
    JSON API endpoint for lightbox / Quick View modal in gallery page.
    """
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, active=True)
        gallery_urls = [img.image.url for img in product.gallery_images.all()]
        if not gallery_urls and product.image:
            gallery_urls = [product.image.url]

        data = {
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
            'description': product.description,
            'price': str(product.price) if product.price else 'Custom Quote',
            'is_available': product.is_available,
            'image_url': product.image.url if product.image else '',
            'gallery_urls': gallery_urls,
            'url': product.get_absolute_url()
        }
        return JsonResponse(data)
