"""URL configuration for website app."""
from django.urls import path
from . import views
from .setup_views import create_admin


app_name = 'website'

urlpatterns = [
    # Setup - REMOVE AFTER CREATING ADMIN!
    path('setup/create-admin/', create_admin, name='create_admin'),
    
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # About Us
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('about/organization-overview/', views.OrganizationOverviewView.as_view(), 
         name='organization_overview'),
    path('about/vmgo/', views.VMGOView.as_view(), name='vmgo'),
    path('about/board/', views.BoardOfDirectorsView.as_view(), name='board'),
    path('about/management/', views.ManagementTeamView.as_view(), name='management'),
    path('about/committees/', views.CommitteesView.as_view(), name='committees'),
    
    # Services
    path('services/', views.ServicesView.as_view(), name='services'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    # News
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    
    # Publications
    path('publications/', views.PublicationsView.as_view(), name='publications'),
    
    # Notices
    path('notices/', views.NoticesView.as_view(), name='notices'),
    
    # Branches
    path('branches/', views.BranchesView.as_view(), name='branches'),
    
    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Membership
    path('membership/', views.MembershipView.as_view(), name='membership'),
    
    # FAQ
    path('faq/', views.FAQView.as_view(), name='faq'),
    
    # Pages
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Newsletter
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), 
         name='newsletter_subscribe'),
    
    # Language switch
    path('set-language/', views.set_language, name='set_language'),
]
