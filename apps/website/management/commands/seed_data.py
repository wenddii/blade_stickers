from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.website.models import SiteSettings, Testimonial
from apps.products.models import Category, Product, GalleryImage


class Command(BaseCommand):
    help = 'Seeds initial sample data for Blade Stickers showcase site.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding Blade Stickers database...'))

        # 1. Site Settings
        site_settings = SiteSettings.get_settings()
        site_settings.site_name = "Blade Stickers"
        site_settings.hero_title = "High-Impact Custom Stickers & Electric Wall Posters"
        site_settings.hero_subtitle = "Designed and printed in high definition. Waterproof vinyl laptop decals, phone stickers, anime collections, Ethiopian legend posters, and custom room decor."
        site_settings.phone_number = "+251 91 234 5678"
        site_settings.telegram_username = "bladestickers"
        site_settings.whatsapp_number = "251912345678"
        site_settings.tiktok_handle = "@bladestickers"
        site_settings.instagram_handle = "@blade_stickers"
        site_settings.email = "info@bladestickers.com"
        site_settings.address = "Bole Medhanialem, Addis Ababa, Ethiopia"
        site_settings.stats_stickers_count = 18500
        site_settings.stats_customers_count = 4200
        site_settings.stats_designs_count = 620
        site_settings.save()
        self.stdout.write(self.style.SUCCESS('[OK] SiteSettings configured.'))

        # 2. Categories
        categories_data = [
            {
                'name': 'Laptop Stickers',
                'description': 'Heavy-duty waterproof matte & holographic vinyl stickers for laptops and MacBooks.',
                'ordering': 1,
            },
            {
                'name': 'Phone Stickers',
                'description': 'Precision die-cut micro stickers for iPhone and Android cases.',
                'ordering': 2,
            },
            {
                'name': 'Anime Stickers',
                'description': 'Vibrant anime collection featuring iconic characters and vibrant aesthetic prints.',
                'ordering': 3,
            },
            {
                'name': 'Ethiopian Musician Posters',
                'description': 'Tribute wall posters honoring legendary Ethiopian music icons and modern stars.',
                'ordering': 4,
            },
            {
                'name': 'International Artist Posters',
                'description': 'High resolution aesthetic music album and movie poster art.',
                'ordering': 5,
            },
            {
                'name': 'Wall Posters & Room Decor',
                'description': 'Large format aesthetic room art on heavy premium textured paper.',
                'ordering': 6,
            },
            {
                'name': 'Custom Sticker Printing',
                'description': 'Upload your custom design or logo for tailored die-cut production.',
                'ordering': 7,
            },
        ]

        cat_objs = {}
        for cat in categories_data:
            obj, _ = Category.objects.get_or_create(
                name=cat['name'],
                defaults={
                    'slug': slugify(cat['name']),
                    'description': cat['description'],
                    'ordering': cat['ordering'],
                    'active': True
                }
            )
            cat_objs[cat['name']] = obj
        self.stdout.write(self.style.SUCCESS('[OK] Categories created.'))

        # 3. Sample Products (using Unsplash high-res image URLs for demonstration)
        products_data = [
            {
                'title': 'Cyberpunk Holographic Laptop Sticker Set',
                'category': cat_objs['Laptop Stickers'],
                'description': 'Ultra-durable waterproof vinyl sticker pack with iridescent chrome holographic accents. Designed to resist scratch, UV exposure, and wear.',
                'price': 15.00,
                'featured': True,
                'is_available': True,
                'img_url': 'https://images.unsplash.com/photo-1572375992501-4b0892d50c69?q=80&w=800&auto=format&fit=crop',
            },
            {
                'title': 'Ethiopian Music Icon Tilahun Gessesse Poster',
                'category': cat_objs['Ethiopian Musician Posters'],
                'description': 'Vintage retro art print honoring the legendary voice of Ethiopia, Tilahun Gessesse. Printed on 300GSM heavy matte poster paper.',
                'price': 25.00,
                'featured': True,
                'is_available': True,
                'img_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=800&auto=format&fit=crop',
            },
            {
                'title': 'Neon Katana Cyber Anime Decal',
                'category': cat_objs['Anime Stickers'],
                'description': 'Electric cyan and magenta anime warrior die-cut vinyl sticker. Perfect for gaming rigs, laptops, and skateboards.',
                'price': 12.00,
                'featured': True,
                'is_available': True,
                'img_url': 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=800&auto=format&fit=crop',
            },
            {
                'title': 'Aster Aweke Soul Diva Vintage Poster',
                'category': cat_objs['Ethiopian Musician Posters'],
                'description': 'Sleek graphic illustration of Ethiopian music legend Aster Aweke. Rich colors and dark modern room decor aesthetic.',
                'price': 25.00,
                'featured': True,
                'is_available': True,
                'img_url': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=800&auto=format&fit=crop',
            },
            {
                'title': 'Minimalist Retro Camera Phone Decal',
                'category': cat_objs['Phone Stickers'],
                'description': 'Precision laser-cut camera lens decal for iPhone and Android cases. Scratch resistant, anti-bubble application.',
                'price': 8.00,
                'featured': False,
                'is_available': True,
                'img_url': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?q=80&w=800&auto=format&fit=crop',
            },
            {
                'title': 'Teddy Afro Ethiopian Culture Wall Art',
                'category': cat_objs['Ethiopian Musician Posters'],
                'description': 'Iconic artwork representing unity, Ethiopian culture, and reggae soul fusion. A centerpiece wall poster for studio or home.',
                'price': 30.00,
                'featured': True,
                'is_available': True,
                'img_url': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=800&auto=format&fit=crop',
            },
            {
                'title': 'Synthwave International Artist Album Poster',
                'category': cat_objs['International Artist Posters'],
                'description': 'Dark aesthetic retrowave album cover art print with vibrant neon glowing gradients.',
                'price': 22.00,
                'featured': False,
                'is_available': True,
                'img_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=800&auto=format&fit=crop',
            },
            {
                'title': 'Custom Die-Cut Brand & Business Sticker Pack',
                'category': cat_objs['Custom Sticker Printing'],
                'description': 'Turn your personal logo, vector art, or artwork into premium vinyl sticker bundles. Fast turn-around and custom shapes.',
                'price': None,
                'featured': True,
                'is_available': True,
                'img_url': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b675?q=80&w=800&auto=format&fit=crop',
            },
        ]

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                title=p_data['title'],
                defaults={
                    'slug': slugify(p_data['title']),
                    'category': p_data['category'],
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'featured': p_data['featured'],
                    'is_available': p_data['is_available'],
                    'active': True
                }
            )

        self.stdout.write(self.style.SUCCESS('[OK] Sample Products created.'))

        # 4. Testimonials
        testimonials_data = [
            {
                'customer_name': 'Dawit Alemu',
                'role': 'Graphic Designer & Gamer',
                'message': 'Blade Stickers are insane quality! The waterproof vinyl on my laptop looks as fresh as day one after 6 months of heavy travel.',
                'rating': 5,
                'ordering': 1,
            },
            {
                'customer_name': 'Selam Kassa',
                'role': 'Interior Decor Enthusiast',
                'message': 'Ordered the Ethiopian Musician posters for my living room wall. The print resolution and paper texture blew me away. 10/10 recommendation!',
                'rating': 5,
                'ordering': 2,
            },
            {
                'customer_name': 'Michael T.',
                'role': 'Anime & Music Collector',
                'message': 'Fast Telegram communication and instant response. Custom die-cut stickers came out crisp and vivid.',
                'rating': 5,
                'ordering': 3,
            },
        ]

        for t_data in testimonials_data:
            Testimonial.objects.get_or_create(
                customer_name=t_data['customer_name'],
                defaults={
                    'role': t_data['role'],
                    'message': t_data['message'],
                    'rating': t_data['rating'],
                    'ordering': t_data['ordering'],
                    'active': True
                }
            )
        self.stdout.write(self.style.SUCCESS('[OK] Testimonials created.'))

        self.stdout.write(self.style.SUCCESS('Database successfully seeded with Blade Stickers data!'))
