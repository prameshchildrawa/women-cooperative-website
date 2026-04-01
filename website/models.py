from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class BaseModel(models.Model):
    """Base model with common fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SiteSettings(BaseModel):
    """Site-wide settings and configuration."""
    site_name_en = models.CharField(max_length=200, default='Women Community Multipurpose Cooperative Ltd.')
    site_name_np = models.CharField(max_length=200, default='महिला सामुदायिक बहुउद्देश्यीय सहकारी लि.')
    tagline_en = models.CharField(max_length=300, blank=True)
    tagline_np = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    apple_touch_icon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Established Year & Stats
    established_year = models.CharField(max_length=10, default='2079', help_text='Year of establishment (e.g., 2079 BS)')
    member_count = models.CharField(max_length=20, default='5000+', help_text='Number of members (e.g., 5000+)')
    service_center_count = models.PositiveIntegerField(default=3, help_text='Number of service centers/branch offices')
    
    # Homepage Images (upload via CRM to replace placeholders)
    about_cooperative_image = models.ImageField(upload_to='home/', blank=True, null=True, help_text='About section image (replaces about-cooperative.svg)')
    empowerment_1_image = models.ImageField(upload_to='home/', blank=True, null=True, help_text='Women empowerment image 1 (replaces empowerment-1.svg)')
    empowerment_2_image = models.ImageField(upload_to='home/', blank=True, null=True, help_text='Women empowerment image 2 (replaces empowerment-2.svg)')
    
    # Contact Information
    email = models.EmailField(default='info@msmc.com.np')
    phone = models.CharField(max_length=50, default='+977-082-XXXXXX')
    phone_secondary = models.CharField(max_length=50, blank=True)
    address_en = models.TextField(default='Ghorahi-15, Dang, Nepal')
    address_np = models.TextField(default='घोराही-१५, दाङ, नेपाल')
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # SEO
    meta_description_en = models.TextField(blank=True)
    meta_description_np = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    # Map
    google_map_embed = models.TextField(blank=True, help_text='Paste Google Maps embed iframe HTML')
    
    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name_en

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            return
        super().save(*args, **kwargs)


class VMGO(BaseModel):
    """Vision, Mission, Goals, Objectives model."""
    # Content fields
    vision_en = RichTextUploadingField(verbose_name='Vision (English)')
    vision_np = RichTextUploadingField(verbose_name='Vision (Nepali)')
    mission_en = RichTextUploadingField(verbose_name='Mission (English)')
    mission_np = RichTextUploadingField(verbose_name='Mission (Nepali)')
    goals_en = RichTextUploadingField(verbose_name='Goals (English)')
    goals_np = RichTextUploadingField(verbose_name='Goals (Nepali)')
    objectives_en = RichTextUploadingField(verbose_name='Objectives (English)')
    objectives_np = RichTextUploadingField(verbose_name='Objectives (Nepali)')
    
    # Image fields (upload via CRM to replace placeholder SVGs)
    vision_image = models.ImageField(upload_to='vmgo/', blank=True, null=True, verbose_name='Vision Image', help_text='Replaces vision.svg')
    mission_image = models.ImageField(upload_to='vmgo/', blank=True, null=True, verbose_name='Mission Image', help_text='Replaces mission.svg')
    goals_image = models.ImageField(upload_to='vmgo/', blank=True, null=True, verbose_name='Goals Image', help_text='Replaces goals.svg')
    objectives_image = models.ImageField(upload_to='vmgo/', blank=True, null=True, verbose_name='Objectives Image', help_text='Replaces objectives.svg')
    
    class Meta:
        verbose_name = 'VMGO'
        verbose_name_plural = 'VMGO'

    def __str__(self):
        return 'VMGO Configuration'

    def save(self, *args, **kwargs):
        if not self.pk and VMGO.objects.exists():
            return
        super().save(*args, **kwargs)


class OrganizationOverview(BaseModel):
    """Organization overview content."""
    title_en = models.CharField(max_length=200)
    title_np = models.CharField(max_length=200)
    content_en = RichTextUploadingField()
    content_np = RichTextUploadingField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Organization Overview'
        verbose_name_plural = 'Organization Overview'

    def __str__(self):
        return self.title_en


class BoardMember(BaseModel):
    """Board of Directors member."""
    DESIGNATION_CHOICES = [
        ('chairperson', 'Chairperson'),
        ('vice_chairperson', 'Vice Chairperson'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('member', 'Member'),
    ]
    
    name_en = models.CharField(max_length=200)
    name_np = models.CharField(max_length=200)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    photo = models.ImageField(upload_to='board/', blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    bio_en = models.TextField(blank=True)
    bio_np = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name_en']
        verbose_name = 'Board Member'
        verbose_name_plural = 'Board Members'

    def __str__(self):
        return self.name_en


class ManagementTeam(BaseModel):
    """Management team member."""
    POSITION_CHOICES = [
        ('ceo', 'Chief Executive Officer'),
        ('manager', 'Manager'),
        ('accountant', 'Accountant'),
        ('loan_officer', 'Loan Officer'),
        ('field_supervisor', 'Field Supervisor'),
        ('assistant', 'Assistant'),
        ('other', 'Other'),
    ]
    
    name_en = models.CharField(max_length=200)
    name_np = models.CharField(max_length=200)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    photo = models.ImageField(upload_to='management/', blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    bio_en = models.TextField(blank=True)
    bio_np = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name_en']
        verbose_name = 'Management Team Member'
        verbose_name_plural = 'Management Team'

    def __str__(self):
        return f"{self.name_en} - {self.get_position_display()}"


class Committee(BaseModel):
    """Other committees."""
    name_en = models.CharField(max_length=200)
    name_np = models.CharField(max_length=200)
    description_en = RichTextUploadingField(blank=True)
    description_np = RichTextUploadingField(blank=True)
    
    class Meta:
        verbose_name = 'Committee'
        verbose_name_plural = 'Committees'

    def __str__(self):
        return self.name_en


class CommitteeMember(BaseModel):
    """Committee member."""
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='members')
    name_en = models.CharField(max_length=200)
    name_np = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='committees/', blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name_en']
        verbose_name = 'Committee Member'
        verbose_name_plural = 'Committee Members'

    def __str__(self):
        return f"{self.name_en} - {self.committee.name_en}"


class Branch(BaseModel):
    """Service outlet/branch location."""
    name_en = models.CharField(max_length=200)
    name_np = models.CharField(max_length=200)
    address_en = models.TextField()
    address_np = models.TextField()
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    map_embed = models.TextField(blank=True, help_text='Google Maps embed iframe HTML')
    manager_name = models.CharField(max_length=200, blank=True)
    opening_hours_en = models.CharField(max_length=200, blank=True)
    opening_hours_np = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_main_branch = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order', 'name_en']
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name_en


class NewsCategory(BaseModel):
    """News/Activity category."""
    name_en = models.CharField(max_length=100)
    name_np = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ['name_en']
        verbose_name = 'News Category'
        verbose_name_plural = 'News Categories'

    def __str__(self):
        return self.name_en

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


class News(BaseModel):
    """News/Activities model."""
    title_en = models.CharField(max_length=300)
    title_np = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name='news')
    content_en = RichTextUploadingField()
    content_np = RichTextUploadingField()
    excerpt_en = models.TextField(blank=True, help_text='Short summary for listings')
    excerpt_np = models.TextField(blank=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    meta_description_en = models.TextField(blank=True)
    meta_description_np = models.TextField(blank=True)
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_en)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        if not self.excerpt_en and self.content_en:
            self.excerpt_en = self.content_en[:200] + '...'
        if not self.excerpt_np and self.content_np:
            self.excerpt_np = self.content_np[:200] + '...'
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


class Publication(BaseModel):
    """Publications (Annual Report, Audit Report, etc.)"""
    PUBLICATION_TYPES = [
        ('annual_report', 'Annual Report'),
        ('audit_report', 'Audit Report'),
        ('financial_report', 'Financial Report'),
        ('policy', 'Policy Document'),
        ('brochure', 'Brochure'),
        ('other', 'Other'),
    ]
    
    title_en = models.CharField(max_length=300)
    title_np = models.CharField(max_length=300)
    publication_type = models.CharField(max_length=50, choices=PUBLICATION_TYPES)
    file = models.FileField(upload_to='publications/')
    year = models.PositiveIntegerField()
    description_en = models.TextField(blank=True)
    description_np = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='publications/covers/', blank=True, null=True)
    
    class Meta:
        ordering = ['-year', '-created_at']
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'

    def __str__(self):
        return f"{self.title_en} ({self.year})"

    def get_absolute_url(self):
        return reverse('publication_detail', kwargs={'pk': self.pk})


class Notice(BaseModel):
    """Notices and announcements."""
    NOTICE_TYPES = [
        ('general', 'General Notice'),
        ('tender', 'Tender'),
        ('vacancy', 'Job Vacancy'),
        ('meeting', 'Meeting Notice'),
        ('urgent', 'Urgent Notice'),
    ]
    
    title_en = models.CharField(max_length=300)
    title_np = models.CharField(max_length=300)
    content_en = RichTextUploadingField()
    content_np = RichTextUploadingField()
    notice_type = models.CharField(max_length=50, choices=NOTICE_TYPES, default='general')
    published_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_urgent = models.BooleanField(default=False)
    is_popup = models.BooleanField(default=False, help_text='Show as popup on homepage')
    popup_delay_days = models.PositiveIntegerField(default=7, help_text='Days before showing popup again')
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    
    class Meta:
        ordering = ['-is_urgent', '-published_date']
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

    def __str__(self):
        return self.title_en

    def is_expired(self):
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False


class Service(BaseModel):
    """Services offered by the cooperative."""
    SERVICE_TYPES = [
        ('savings', 'Savings'),
        ('loans', 'Loans'),
        ('agriculture', 'Agriculture'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('insurance', 'Insurance'),
        ('remittance', 'Remittance'),
        ('other', 'Other'),
    ]
    
    title_en = models.CharField(max_length=200)
    title_np = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    short_description_en = models.TextField()
    short_description_np = models.TextField()
    full_description_en = RichTextUploadingField()
    full_description_np = RichTextUploadingField()
    icon = models.CharField(max_length=100, blank=True, help_text='Font Awesome icon class (e.g., fa-piggy-bank)')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    features_en = RichTextUploadingField(blank=True, help_text='List of features/benefits')
    features_np = RichTextUploadingField(blank=True)
    eligibility_en = RichTextUploadingField(blank=True)
    eligibility_np = RichTextUploadingField(blank=True)
    documents_required_en = RichTextUploadingField(blank=True)
    documents_required_np = RichTextUploadingField(blank=True)
    interest_rate_info_en = models.TextField(blank=True)
    interest_rate_info_np = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'title_en']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_en)
            slug = base_slug
            counter = 1
            while Service.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class ContactMessage(BaseModel):
    """Contact form messages."""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    reply_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"


class MembershipApplication(BaseModel):
    """Membership/Join form applications."""
    MEMBERSHIP_TYPES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
        ('institutional', 'Institutional'),
    ]
    
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    ]
    
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    citizenship_number = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    address = models.TextField()
    ward_number = models.CharField(max_length=10, blank=True)
    municipality = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPES)
    occupation = models.CharField(max_length=100, blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    nominee_name = models.CharField(max_length=200, blank=True)
    nominee_relationship = models.CharField(max_length=100, blank=True)
    nominee_phone = models.CharField(max_length=50, blank=True)
    
    photo = models.ImageField(upload_to='membership/photos/', blank=True, null=True)
    citizenship_document = models.FileField(upload_to='membership/documents/', blank=True, null=True)
    
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    remarks = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Membership Application'
        verbose_name_plural = 'Membership Applications'

    def __str__(self):
        return f"{self.full_name} - {self.get_membership_type_display()}"


class FAQ(BaseModel):
    """Frequently Asked Questions."""
    question_en = models.CharField(max_length=500)
    question_np = models.CharField(max_length=500)
    answer_en = RichTextUploadingField()
    answer_np = RichTextUploadingField()
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'question_en']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question_en


class Testimonial(BaseModel):
    """Member testimonials."""
    name_en = models.CharField(max_length=200)
    name_np = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    testimonial_en = models.TextField()
    testimonial_np = models.TextField()
    designation_en = models.CharField(max_length=200, blank=True, help_text='Member designation/role')
    designation_np = models.CharField(max_length=200, blank=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return self.name_en


class HeroSlide(BaseModel):
    """Homepage hero slider images."""
    title_en = models.CharField(max_length=200, blank=True)
    title_np = models.CharField(max_length=200, blank=True)
    subtitle_en = models.TextField(blank=True)
    subtitle_np = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero/')
    button_text_en = models.CharField(max_length=100, blank=True)
    button_text_np = models.CharField(max_length=100, blank=True)
    button_url = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return self.title_en or f'Slide {self.order}'


class Page(BaseModel):
    """Static pages (Privacy Policy, Terms, etc.)"""
    title_en = models.CharField(max_length=200)
    title_np = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content_en = RichTextUploadingField()
    content_np = RichTextUploadingField()
    meta_description_en = models.TextField(blank=True)
    meta_description_np = models.TextField(blank=True)
    
    class Meta:
        ordering = ['title_en']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})


class NewsletterSubscriber(BaseModel):
    """Newsletter email subscribers."""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return self.email
