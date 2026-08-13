from .models import SiteSettings

def site_settings(request):
    """
    Context processor to make site_settings globally available in all templates.
    """
    return {
        'site_settings': SiteSettings.get_settings()
    }
