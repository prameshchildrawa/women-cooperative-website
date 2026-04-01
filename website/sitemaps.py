"""Sitemap configuration for SEO."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import News, Publication, Service, Page


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return [
            'website:home',
            'website:about',
            'website:organization_overview',
            'website:vmgo',
            'website:board',
            'website:management',
            'website:committees',
            'website:services',
            'website:news_list',
            'website:publications',
            'website:notices',
            'website:branches',
            'website:contact',
            'website:membership',
            'website:faq',
        ]
    
    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    """Sitemap for news articles."""
    changefreq = 'daily'
    priority = 0.7
    
    def items(self):
        return News.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class PublicationSitemap(Sitemap):
    """Sitemap for publications."""
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Publication.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class ServiceSitemap(Sitemap):
    """Sitemap for services."""
    changefreq = 'monthly'
    priority = 0.8
    
    def items(self):
        return Service.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class PageSitemap(Sitemap):
    """Sitemap for static pages."""
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self):
        return Page.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()
