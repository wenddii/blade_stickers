from django.views.generic import TemplateView
from django.http import HttpResponse
from django.urls import reverse
from apps.products.models import Product, Category
from .models import Testimonial, SiteSettings


class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Featured Products
        context['featured_stickers'] = Product.objects.filter(
            active=True, featured=True
        ).select_related('category').prefetch_related('gallery_images')[:8]

        context['featured_posters'] = Product.objects.filter(
            active=True, category__slug__icontains='poster'
        ).select_related('category')[:6]

        context['categories'] = Category.objects.filter(active=True)
        context['testimonials'] = Testimonial.objects.filter(active=True)
        context['latest_products'] = Product.objects.filter(active=True).order_by('-created_at')[:6]

        return context


class AboutView(TemplateView):
    template_name = 'website/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(active=True)[:4]
        return context


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    domain = request.build_absolute_uri('/')[:-1]
    
    urls = [
        {'loc': domain + reverse('website:home'), 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': domain + reverse('website:about'), 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': domain + reverse('products:gallery'), 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': domain + reverse('contact:contact'), 'priority': '0.8', 'changefreq': 'monthly'},
    ]

    # Add active product URLs
    products = Product.objects.filter(active=True)
    for prod in products:
        urls.append({
            'loc': domain + prod.get_absolute_url(),
            'priority': '0.7',
            'changefreq': 'weekly'
        })

    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{u["loc"]}</loc>')
        xml_content.append(f'    <changefreq>{u["changefreq"]}</changefreq>')
        xml_content.append(f'    <priority>{u["priority"]}</priority>')
        xml_content.append('  </url>')
    xml_content.append('</urlset>')

    return HttpResponse("\n".join(xml_content), content_type="application/xml")
