from django.db import models
from django.core.exceptions import ValidationError


class SiteSettings(models.Model):
    """
    Singleton model for non-technical owner to edit all website dynamic settings,
    branding, contact info, social handles, and hero text from Django Admin.
    """
    site_name = models.CharField(max_length=100, default="Blade Stickers")
    logo = models.ImageField(upload_to="site/", blank=True, null=True, help_text="Website Brand Logo")
    favicon = models.ImageField(upload_to="site/", blank=True, null=True, help_text="Browser Favicon Icon")
    
    # Hero Section Content
    hero_title = models.CharField(
        max_length=200, 
        default="Custom Stickers & Wall Art Crafted to Elevate Your Style"
    )
    hero_subtitle = models.TextField(
        default="Express your personality with high-definition, waterproof vinyl stickers, anime decals, Ethiopian artist posters, and sleek room decorations."
    )
    
    # About Section Content
    about_story = models.TextField(
        default="Blade Stickers was founded with a single passion: creating high-durability, vivid visual art that transforms everyday objects into personal canvas expressions. From laptop decals to massive wall posters, we print with ultra-sharp detail."
    )
    about_mission = models.TextField(
        default="To deliver premium quality die-cut stickers and posters across Ethiopia and internationally, empowering artists, music lovers, and aesthetic enthusiasts."
    )
    
    # Live Stats Counters
    stats_stickers_count = models.IntegerField(default=15000, help_text="Stickers printed count")
    stats_customers_count = models.IntegerField(default=3500, help_text="Happy customers count")
    stats_designs_count = models.IntegerField(default=450, help_text="Custom designs catalog count")
    stats_rating = models.CharField(max_length=10, default="4.9 ★", help_text="Satisfaction rating label")

    # Direct Contact & Social Links
    phone_number = models.CharField(max_length=50, default="+251 91 234 5678")
    telegram_username = models.CharField(max_length=100, default="bladestickers", help_text="Telegram username without @")
    whatsapp_number = models.CharField(max_length=50, default="251912345678", help_text="WhatsApp phone number with country code")
    tiktok_handle = models.CharField(max_length=100, default="@bladestickers", help_text="TikTok handle")
    instagram_handle = models.CharField(max_length=100, default="@bladestickers", help_text="Instagram handle")
    facebook_link = models.URLField(blank=True, default="https://facebook.com")
    email = models.EmailField(default="contact@bladestickers.com")
    address = models.CharField(max_length=255, default="Bole, Addis Ababa, Ethiopia")
    map_embed_url = models.TextField(
        blank=True, 
        default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126107.03986877085!2d38.70014264335936!3d9.006001200000003!2m3!1f0!1f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x164b85cef5ab402d%3A0x8467b6b037a24d49!2sAddis%20Ababa!5e0!3m2!1sen!2set!4v1700000000000!5m2!1sen!2set"
    )

    footer_text = models.TextField(
        default="© 2026 Blade Stickers. High precision die-cut stickers, anime decals, Ethiopian musician posters, and custom wall art."
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def clean(self):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("Only one SiteSettings instance is allowed.")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        settings_obj, created = cls.objects.get_or_create(pk=1)
        return settings_obj

    def __str__(self):
        return self.site_name


class Testimonial(models.Model):
    """
    Testimonials from customers showcasing social proof.
    """
    customer_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, help_text="e.g. Graphic Designer, Anime Fan, DJ")
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Star rating from 1 to 5")
    active = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordering', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"
