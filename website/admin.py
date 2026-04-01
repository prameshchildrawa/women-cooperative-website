from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, VMGO, OrganizationOverview, BoardMember,
    ManagementTeam, Committee, CommitteeMember, Branch,
    NewsCategory, News, Publication, Notice, Service,
    ContactMessage, MembershipApplication, FAQ, Testimonial,
    HeroSlide, Page, NewsletterSubscriber
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name_en', 'email', 'phone', 'established_year', 'member_count', 'service_center_count']
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name_en', 'site_name_np', 'tagline_en', 'tagline_np', 
                      'established_year', 'member_count', 'service_center_count',
                      'logo', 'favicon', 'apple_touch_icon')
        }),
        ('Homepage Images', {
            'fields': ('about_cooperative_image', 'empowerment_1_image', 'empowerment_2_image'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'phone_secondary', 'address_en', 'address_np')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 
                      'youtube_url', 'instagram_url')
        }),
        ('SEO & Analytics', {
            'fields': ('meta_description_en', 'meta_description_np', 
                      'meta_keywords', 'google_analytics_id')
        }),
        ('Map', {
            'fields': ('google_map_embed',)
        }),
    )


@admin.register(VMGO)
class VMGOAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Vision', {
            'fields': ('vision_en', 'vision_np', 'vision_image')
        }),
        ('Mission', {
            'fields': ('mission_en', 'mission_np', 'mission_image')
        }),
        ('Goals', {
            'fields': ('goals_en', 'goals_np', 'goals_image')
        }),
        ('Objectives', {
            'fields': ('objectives_en', 'objectives_np', 'objectives_image')
        }),
    )


@admin.register(OrganizationOverview)
class OrganizationOverviewAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'is_active', 'updated_at']
    list_filter = ['is_active']


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'designation', 'order', 'is_active']
    list_filter = ['designation', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name_en', 'name_np', 'email']


@admin.register(ManagementTeam)
class ManagementTeamAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'position', 'order', 'is_active']
    list_filter = ['position', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name_en', 'name_np', 'email']


class CommitteeMemberInline(admin.TabularInline):
    model = CommitteeMember
    extra = 1


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'member_count', 'is_active']
    inlines = [CommitteeMemberInline]
    
    def member_count(self, obj):
        return obj.members.filter(is_active=True).count()
    member_count.short_description = 'Active Members'


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'is_main_branch', 'phone', 'order', 'is_active']
    list_filter = ['is_main_branch', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name_en', 'name_np', 'address_en', 'address_np']


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'category', 'published_date', 'is_featured', 
                   'is_active', 'views_count']
    list_filter = ['category', 'is_featured', 'is_active', 'published_date']
    list_editable = ['is_active']
    search_fields = ['title_en', 'title_np', 'content_en', 'content_np']
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'published_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title_en', 'title_np', 'slug', 'category', 'image')
        }),
        ('Content', {
            'fields': ('content_en', 'content_np', 'excerpt_en', 'excerpt_np')
        }),
        ('Publishing', {
            'fields': ('published_date', 'is_featured', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_description_en', 'meta_description_np')
        }),
    )


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'publication_type', 'year', 'is_active']
    list_filter = ['publication_type', 'year', 'is_active']
    list_editable = ['is_active']
    search_fields = ['title_en', 'title_np', 'description_en', 'description_np']
    date_hierarchy = 'created_at'


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'notice_type', 'is_urgent', 'is_popup', 
                   'published_date', 'is_active']
    list_filter = ['notice_type', 'is_urgent', 'is_popup', 'is_active']
    list_editable = ['is_active']
    search_fields = ['title_en', 'title_np', 'content_en', 'content_np']
    date_hierarchy = 'published_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title_en', 'title_np', 'notice_type', 'attachment')
        }),
        ('Content', {
            'fields': ('content_en', 'content_np')
        }),
        ('Publishing', {
            'fields': ('published_date', 'expiry_date', 'is_urgent', 'is_active')
        }),
        ('Popup Settings', {
            'fields': ('is_popup', 'popup_delay_days'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'service_type', 'order', 'is_active']
    list_filter = ['service_type', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title_en', 'title_np']
    prepopulated_fields = {'slug': ('title_en',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title_en', 'title_np', 'slug', 'service_type', 
                      'icon', 'image', 'order')
        }),
        ('Description', {
            'fields': ('short_description_en', 'short_description_np',
                      'full_description_en', 'full_description_np')
        }),
        ('Details', {
            'fields': ('features_en', 'features_np', 'eligibility_en', 
                      'eligibility_np', 'documents_required_en', 
                      'documents_required_np', 'interest_rate_info_en',
                      'interest_rate_info_np')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'replied', 'created_at']
    list_filter = ['is_read', 'replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read', 'replied', 'reply_message')
        }),
    )


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'membership_type', 'phone', 'district', 'status', 'created_at']
    list_filter = ['membership_type', 'status', 'gender', 'created_at']
    list_editable = ['status']
    search_fields = ['full_name', 'phone', 'email', 'citizenship_number']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'date_of_birth', 'gender', 'citizenship_number',
                      'phone', 'email')
        }),
        ('Address', {
            'fields': ('address', 'ward_number', 'municipality', 'district', 'province')
        }),
        ('Membership Details', {
            'fields': ('membership_type', 'occupation', 'monthly_income')
        }),
        ('Nominee', {
            'fields': ('nominee_name', 'nominee_relationship', 'nominee_phone'),
            'classes': ('collapse',)
        }),
        ('Documents', {
            'fields': ('photo', 'citizenship_document')
        }),
        ('Status', {
            'fields': ('status', 'remarks')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_en', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['question_en', 'question_np', 'answer_en', 'answer_np']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'designation_en', 'rating', 'order', 'is_active']
    list_filter = ['rating', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'order', 'is_active', 'preview_image']
    list_editable = ['order', 'is_active']
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', 
                               obj.image.url)
        return '-'
    preview_image.short_description = 'Preview'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'slug', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title_en', 'title_np', 'content_en', 'content_np']
    prepopulated_fields = {'slug': ('title_en',)}


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    date_hierarchy = 'subscribed_at'
