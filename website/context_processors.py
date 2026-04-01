"""Context processors for website app."""
from .models import SiteSettings, Service, Branch, Notice


def website_context(request):
    """Add common website context to all templates."""
    context = {}
    
    # Site settings
    try:
        site_settings = SiteSettings.objects.first()
        context['site_settings'] = site_settings
    except:
        pass
    
    # Navigation services (for dropdown menu)
    try:
        context['nav_services'] = Service.objects.filter(
            is_active=True
        ).values('title_en', 'title_np', 'slug')[:6]
    except:
        context['nav_services'] = []
    
    # Branches for footer/contact
    try:
        context['footer_branches'] = Branch.objects.filter(
            is_active=True
        )[:3]
    except:
        context['footer_branches'] = []
    
    # Urgent notices for ticker
    try:
        context['header_notices'] = Notice.objects.filter(
            is_active=True, is_urgent=True
        )[:3]
    except:
        context['header_notices'] = []
    
    # Language
    context['current_language'] = getattr(request, 'LANGUAGE_CODE', 'ne')
    
    return context
