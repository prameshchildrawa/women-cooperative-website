# Women Community Multipurpose Cooperative Ltd. Website

A production-ready full-stack Django web application for Women Community Multipurpose Cooperative Ltd., featuring a modern, responsive design with multi-language support (English/Nepali), dark mode, and a comprehensive CMS admin panel.

## 🏢 Organization Details

- **Name:** Women Community Multipurpose Cooperative Ltd.
- **Domain:** msmc.com.np
- **Head Office:** Ghorahi-15, Dang, Nepal
- **Service Outlets:** Bangalachuli-8, Hansipur; Tulsipur-14, Karanga
- **Sector:** Cooperative / Finance / Women Empowerment / Community Development

## 🎯 Features

### Frontend Features
- **Responsive Design:** Mobile, tablet, and desktop optimized
- **Multi-Language Support:** English and Nepali (UTF-8)
- **Dark Mode Toggle:** With localStorage persistence
- **SEO Optimized:** Meta tags, sitemap.xml, robots.txt
- **Hero Slider:** Dynamic homepage slider (CMS-managed)
- **Notice Ticker:** Real-time announcements
- **News & Publications:** Organized content management
- **Contact Form:** With database storage and email notifications
- **Membership Application:** Online join form with document upload
- **Newsletter Subscription:** Email subscription system

### Backend Features
- **Django Admin Dashboard:** Custom CMS interface
- **VMGO Management:** Vision, Mission, Goals, Objectives
- **News & Publications CRUD:** Full content management
- **Board & Staff Management:** Team member profiles
- **Services Management:** Service details and categorization
- **Branch Management:** Multiple location support
- **Notice Management:** With popup and urgency settings
- **File Uploads:** Secure media storage
- **Contact Message Management:** Message tracking and replies

## 🛠️ Tech Stack

- **Backend:** Django 4.2+
- **Database:** PostgreSQL (Production) / SQLite (Development)
- **Frontend:** Django Templates + Bootstrap 5
- **WYSIWYG Editor:** CKEditor 5
- **Authentication:** Django Auth System
- **Media Storage:** Django FileField / Local Storage
- **Additional:** whitenoise, django-compressor, python-dotenv

## 📁 Project Structure

```
msmc_website/
├── msmc/                      # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── website/                   # Main Django app
│   ├── models.py             # All database models
│   ├── views.py              # Class-based views
│   ├── urls.py               # URL routing
│   ├── admin.py              # Admin configuration
│   ├── forms.py              # Form classes
│   ├── context_processors.py # Global template context
│   └── sitemaps.py           # SEO sitemaps
├── templates/                 # HTML templates
│   ├── base.html             # Base layout
│   └── website/              # Page templates
├── static/                    # Static files
│   ├── css/style.css         # Custom styles
│   └── js/main.js            # Custom JavaScript
├── media/                     # User-uploaded files
├── locale/                    # Translation files
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── manage.py                 # Django management script
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (or SQLite for development)
- pip
- virtualenv (recommended)

### Step 1: Clone and Setup Environment

```bash
# Navigate to project directory
cd msmc_website

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# Generate a new SECRET_KEY:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 4: Load Initial Data (Optional)

```bash
# Create default site settings
python manage.py shell -c "
from website.models import SiteSettings, VMGO
SiteSettings.objects.create(
    site_name_en='Women Community Multipurpose Cooperative Ltd.',
    site_name_np='महिला सामुदायिक बहुउद्देश्यीय सहकारी लि.',
    email='info@msmc.com.np',
    phone='+977-082-XXXXXX',
    address_en='Ghorahi-15, Dang, Nepal',
    address_np='घोराही-१५, दाङ, नेपाल'
)
VMGO.objects.create(
    vision_en='To be a leading cooperative empowering women for sustainable development.',
    vision_np='दिगो विकासको लागि महिलाहरूलाई सशक्तिकरण गर्ने अग्रणी सहकारी बन्ने।',
    mission_en='Providing accessible financial services to empower women entrepreneurs.',
    mission_np='महिला उद्यमीहरूलाई सशक्तिकरण गर्न सुलभ वित्तीय सेवाहरू प्रदान गर्ने।',
    goals_en='Economic empowerment, social inclusion, and community welfare.',
    goals_np='आर्थिक सशक्तिकरण, सामाजिक समावेशीकरण, र समुदाय कल्याण।',
    objectives_en='Expand member base, provide quality services, ensure sustainable growth.',
    objectives_np='सदस्य आधार विस्तार गर्ने, गुणस्तरीय सेवाहरू प्रदान गर्ने, दिगो वृद्धि सुनिश्चित गर्ने।'
)
"
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Access the site at: http://127.0.0.1:8000

Admin panel at: http://127.0.0.1:8000/admin/

## 📝 Usage Guide

### Admin Dashboard

1. **Login:** `/admin/`
2. **Site Settings:** Configure logo, contact info, social links
3. **VMGO:** Manage Vision, Mission, Goals, Objectives
4. **News:** Add news articles with categories
5. **Publications:** Upload PDFs (Annual Reports, etc.)
6. **Services:** Add/modify service offerings
7. **Board Members:** Manage BOD profiles
8. **Branches:** Add service outlet locations
9. **Notices:** Publish announcements
10. **Contact Messages:** View and reply to inquiries

### Multi-Language Content

All translatable models have dual fields:
- `*_en` - English content
- `*_np` - Nepali content (Unicode)

The language switcher in the navbar toggles between languages.

### Dark Mode

Users can toggle dark mode using the moon/sun icon in the top bar. The preference is saved to localStorage.

## 🔐 Security Features

- CSRF protection on all forms
- Secure file upload handling
- XSS protection (CKEditor content sanitized)
- Authentication required for admin routes
- Environment variables for sensitive data
- HTTPS redirect in production (when DEBUG=False)

## 🔍 SEO Configuration

- **Meta Tags:** Auto-generated from model content
- **Sitemap:** Auto-generated at `/sitemap.xml`
- **Robots.txt:** Configured at `/robots.txt`
- **Slugs:** SEO-friendly URLs for all content
- **Open Graph:** Social media sharing tags

## 📊 Database Models

### Core Models
- `SiteSettings` - Website configuration
- `VMGO` - Vision, Mission, Goals, Objectives
- `OrganizationOverview` - About page content
- `BoardMember` - BOD profiles
- `ManagementTeam` - Staff profiles
- `Committee` & `CommitteeMember` - Other committees
- `Branch` - Service outlet locations

### Content Models
- `NewsCategory` & `News` - News articles
- `Publication` - PDF documents
- `Notice` - Announcements
- `Service` - Service offerings
- `Page` - Static pages (Privacy Policy, Terms, etc.)
- `HeroSlide` - Homepage slider
- `Testimonial` - Member testimonials
- `FAQ` - Frequently asked questions

### Interaction Models
- `ContactMessage` - Form submissions
- `MembershipApplication` - Join requests
- `NewsletterSubscriber` - Email subscriptions

## 🚀 Deployment

### Production Checklist

1. **Environment Variables:**
   - Set `DEBUG=False`
   - Generate new `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`
   - Setup PostgreSQL database

2. **Static & Media Files:**
   - Run `collectstatic`
   - Configure media file serving (nginx/Apache)

3. **Database:**
   - Use PostgreSQL in production
   - Run migrations
   - Backup strategy

4. **Security:**
   - Enable HTTPS
   - Configure secure cookies
   - Set up firewall rules

### Gunicorn Setup

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn msmc.wsgi:application --bind 0.0.0.0:8000
```

### Nginx Configuration (Example)

```nginx
server {
    listen 80;
    server_name msmc.com.np www.msmc.com.np;
    
    location /static/ {
        alias /var/www/msmc/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/msmc/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛠️ Development

### Adding New Languages

1. Create translation files:
```bash
django-admin makemessages -l ne
django-admin compilemessages
```

2. Edit `locale/ne/LC_MESSAGES/django.po`

3. Compile:
```bash
django-admin compilemessages
```

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 📞 Support

For technical support or inquiries:
- Email: info@msmc.com.np
- Website: https://msmc.com.np

## 📄 License

Copyright © Women Community Multipurpose Cooperative Ltd. All rights reserved.

## 🙏 Acknowledgments

- Bootstrap 5 - Frontend framework
- Django - Backend framework
- Font Awesome - Icons
- CKEditor - Rich text editor
- Nepali Unicode Font Support
