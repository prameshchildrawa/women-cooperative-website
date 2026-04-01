"""URL Configuration for msmc project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from website.sitemaps import (
    StaticViewSitemap, NewsSitemap, PublicationSitemap,
    PageSitemap, ServiceSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'news': NewsSitemap,
    'publications': PublicationSitemap,
    'pages': PageSitemap,
    'services': ServiceSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('website.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
