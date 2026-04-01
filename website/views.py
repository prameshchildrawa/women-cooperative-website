from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView,
    FormView, View
)
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    SiteSettings, VMGO, OrganizationOverview, BoardMember,
    ManagementTeam, Committee, Branch, NewsCategory, News,
    Publication, Notice, Service, ContactMessage,
    MembershipApplication, FAQ, Testimonial, HeroSlide, Page,
    NewsletterSubscriber
)
from .forms import (
    ContactForm, MembershipForm, NewsletterForm, SearchForm
)


class LanguageContextMixin:
    """Mixin to add language context to views."""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_language'] = self.request.LANGUAGE_CODE
        return context


class HomeView(LanguageContextMixin, TemplateView):
    """Homepage view with all dynamic content."""
    template_name = 'website/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Hero slider
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True)
        
        # Services preview (limit to 6)
        context['services'] = Service.objects.filter(is_active=True)[:6]
        
        # Latest news
        context['latest_news'] = News.objects.filter(
            is_active=True
        ).select_related('category')[:4]
        
        # Featured news
        context['featured_news'] = News.objects.filter(
            is_active=True, is_featured=True
        ).select_related('category').first()
        
        # Urgent notices for ticker
        context['urgent_notices'] = Notice.objects.filter(
            is_active=True, is_urgent=True
        )[:5]
        
        # Latest notices
        context['latest_notices'] = Notice.objects.filter(
            is_active=True
        )[:10]
        
        # Testimonials
        context['testimonials'] = Testimonial.objects.filter(
            is_active=True
        )[:3]
        
        # Popup notice
        popup_notice = Notice.objects.filter(
            is_active=True, is_popup=True
        ).first()
        context['popup_notice'] = popup_notice
        
        # Branches
        context['branches'] = Branch.objects.filter(is_active=True)
        context['main_branch'] = Branch.objects.filter(
            is_active=True, is_main_branch=True
        ).first()
        
        return context


class AboutUsView(LanguageContextMixin, TemplateView):
    """About Us main page."""
    template_name = 'website/about.html'


class OrganizationOverviewView(LanguageContextMixin, DetailView):
    """Organization Overview page."""
    template_name = 'website/organization_overview.html'
    context_object_name = 'overview'
    
    def get_object(self):
        return OrganizationOverview.objects.filter(is_active=True).first()


class VMGOView(LanguageContextMixin, TemplateView):
    """Vision, Mission, Goals, Objectives page."""
    template_name = 'website/vmgo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vmgo'] = VMGO.objects.first()
        return context


class BoardOfDirectorsView(LanguageContextMixin, ListView):
    """Board of Directors page."""
    template_name = 'website/board.html'
    context_object_name = 'board_members'
    
    def get_queryset(self):
        return BoardMember.objects.filter(is_active=True)


class ManagementTeamView(LanguageContextMixin, ListView):
    """Management Team page."""
    template_name = 'website/management.html'
    context_object_name = 'team_members'
    
    def get_queryset(self):
        return ManagementTeam.objects.filter(is_active=True)


class CommitteesView(LanguageContextMixin, ListView):
    """Other Committees page."""
    template_name = 'website/committees.html'
    context_object_name = 'committees'
    
    def get_queryset(self):
        return Committee.objects.filter(is_active=True).prefetch_related('members')


class ServicesView(LanguageContextMixin, ListView):
    """All services page."""
    template_name = 'website/services.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ServiceDetailView(LanguageContextMixin, DetailView):
    """Individual service detail page."""
    model = Service
    template_name = 'website/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class NewsListView(LanguageContextMixin, ListView):
    """News listing page with pagination and search."""
    model = News
    template_name = 'website/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = News.objects.filter(is_active=True).select_related('category')
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title_en__icontains=search_query) |
                Q(title_np__icontains=search_query) |
                Q(content_en__icontains=search_query) |
                Q(content_np__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        context['featured_news'] = News.objects.filter(
            is_active=True, is_featured=True
        ).select_related('category').first()
        context['search_query'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        return context


class NewsDetailView(LanguageContextMixin, DetailView):
    """News detail page."""
    model = News
    template_name = 'website/news_detail.html'
    context_object_name = 'news'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return News.objects.filter(is_active=True).select_related('category')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related news
        context['related_news'] = News.objects.filter(
            is_active=True,
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context


class PublicationsView(LanguageContextMixin, ListView):
    """Publications listing page."""
    model = Publication
    template_name = 'website/publications.html'
    context_object_name = 'publications'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Publication.objects.filter(is_active=True)
        
        # Type filter
        pub_type = self.request.GET.get('type')
        if pub_type:
            queryset = queryset.filter(publication_type=pub_type)
        
        # Year filter
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(year=year)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication_types'] = Publication.PUBLICATION_TYPES
        context['years'] = Publication.objects.filter(
            is_active=True
        ).values_list('year', flat=True).distinct().order_by('-year')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_year'] = self.request.GET.get('year', '')
        return context


class NoticesView(LanguageContextMixin, ListView):
    """Notices page."""
    model = Notice
    template_name = 'website/notices.html'
    context_object_name = 'notices'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Notice.objects.filter(is_active=True)
        
        # Type filter
        notice_type = self.request.GET.get('type')
        if notice_type:
            queryset = queryset.filter(notice_type=notice_type)
        
        return queryset.exclude(expiry_date__lt=__import__('django.utils.timezone').utils.timezone.now())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notice_types'] = Notice.NOTICE_TYPES
        context['current_type'] = self.request.GET.get('type', '')
        context['urgent_notices'] = Notice.objects.filter(
            is_active=True, is_urgent=True
        )[:5]
        return context


class ContactView(LanguageContextMixin, FormView):
    """Contact page with form."""
    template_name = 'website/contact.html'
    form_class = ContactForm
    success_url = '/contact/?sent=1'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings_obj = SiteSettings.objects.first()
        context['site_settings'] = settings_obj
        context['branches'] = Branch.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        # Save message to database
        message = ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data.get('phone', ''),
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message']
        )
        
        # Send email notification (if configured)
        try:
            if settings.EMAIL_HOST:
                send_mail(
                    subject=f'Contact Form: {form.cleaned_data["subject"]}',
                    message=f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                            f"Phone: {form.cleaned_data.get('phone', 'N/A')}\n\n"
                            f"Message:\n{form.cleaned_data['message']}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.SiteSettings.objects.first().email],
                    fail_silently=True
                )
        except:
            pass
        
        messages.success(
            self.request, 
            'Thank you for your message. We will get back to you soon.'
        )
        return super().form_valid(form)


class MembershipView(LanguageContextMixin, CreateView):
    """Membership/Join form page."""
    model = MembershipApplication
    form_class = MembershipForm
    template_name = 'website/membership.html'
    success_url = '/membership/?success=1'
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Thank you for your membership application. We will review and contact you soon.'
        )
        return super().form_valid(form)


class FAQView(LanguageContextMixin, ListView):
    """FAQ page."""
    model = FAQ
    template_name = 'website/faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group FAQs by category
        categories = FAQ.objects.filter(
            is_active=True
        ).values_list('category', flat=True).distinct()
        context['categories'] = categories
        return context


class BranchesView(LanguageContextMixin, ListView):
    """All branches/locations page."""
    model = Branch
    template_name = 'website/branches.html'
    context_object_name = 'branches'
    
    def get_queryset(self):
        return Branch.objects.filter(is_active=True)


class PageDetailView(LanguageContextMixin, DetailView):
    """Static pages (Privacy Policy, Terms, etc.)."""
    model = Page
    template_name = 'website/page_detail.html'
    context_object_name = 'page'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True)


class NewsletterSubscribeView(View):
    """AJAX newsletter subscription."""
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required.'})
        
        try:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            
            if not created and not subscriber.is_active:
                subscriber.is_active = True
                subscriber.save()
                return JsonResponse({
                    'success': True, 
                    'message': 'Your subscription has been reactivated.'
                })
            
            if created:
                return JsonResponse({
                    'success': True, 
                    'message': 'Thank you for subscribing to our newsletter!'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'You are already subscribed.'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': 'An error occurred. Please try again.'
            })


class SearchView(LanguageContextMixin, ListView):
    """Site-wide search results."""
    template_name = 'website/search_results.html'
    context_object_name = 'results'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return []
        
        # Search in News
        news_results = News.objects.filter(
            Q(title_en__icontains=query) |
            Q(title_np__icontains=query) |
            Q(content_en__icontains=query) |
            Q(content_np__icontains=query),
            is_active=True
        )
        
        # Search in Services
        service_results = Service.objects.filter(
            Q(title_en__icontains=query) |
            Q(title_np__icontains=query) |
            Q(full_description_en__icontains=query) |
            Q(full_description_np__icontains=query),
            is_active=True
        )
        
        # Search in Notices
        notice_results = Notice.objects.filter(
            Q(title_en__icontains=query) |
            Q(title_np__icontains=query) |
            Q(content_en__icontains=query) |
            Q(content_np__icontains=query),
            is_active=True
        )
        
        # Combine results with type annotation
        results = []
        for item in news_results:
            item.result_type = 'news'
            results.append(item)
        for item in service_results:
            item.result_type = 'service'
            results.append(item)
        for item in notice_results:
            item.result_type = 'notice'
            results.append(item)
        
        return results
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


def set_language(request):
    """Set language preference."""
    from django.utils import translation
    from django.http import HttpResponseRedirect
    
    language = request.GET.get('lang', 'ne')
    next_url = request.GET.get('next', '/')
    
    if language in ['ne', 'en']:
        translation.activate(language)
        request.session['django_language'] = language
    
    response = HttpResponseRedirect(next_url)
    response.set_cookie('django_language', language)
    return response
