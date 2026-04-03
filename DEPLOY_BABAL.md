# Babal.host / cPanel Deployment Guide

## Prerequisites
- cPanel hosting with Python support
- SSH access (optional but recommended)
- Domain: msmc.com.np pointing to hosting

## Step 1: Upload Files

1. **ZIP your project** (without venv):
   ```
   git clone https://github.com/prameshchildrawa/women-cooperative-website.git msmc_website
   cd msmc_website
   # Remove unnecessary files
   Remove-Item -Recurse .git
   Remove-Item -Recurse venv
   ```

2. **Upload to cPanel File Manager**:
   - Login to cPanel → File Manager
   - Upload `msmc_website.zip` to `/home/yourusername/`
   - Extract the zip file

## Step 2: Create Python Virtual Environment

In cPanel:
1. Go to **Setup Python App** (or **Select Python Version**)
2. Create new application:
   - **Application Root:** `msmc_website`
   - **Python Version:** 3.11
   - **Application URL:** (leave empty or use subdomain)
3. Click **Create**

Or via SSH:
```bash
cd ~/msmc_website
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables

Create `.env` file in project root:
```
DEBUG=False
SECRET_KEY=your-secret-key-here-generate-a-strong-one
ALLOWED_HOSTS=msmc.com.np,www.msmc.com.np
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

**Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(50))
```

## Step 4: Setup Database

### Option A: SQLite (Easiest)
Already configured by default. Just run:
```bash
cd ~/msmc_website
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@msmc.com.np', 'your-strong-password')
"
```

### Option B: MySQL (Better for production)
1. In cPanel: **MySQL Databases** → Create database and user
2. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=mysql://username:password@localhost/dbname
   ```
3. Install MySQL driver:
   ```
   pip install mysqlclient
   ```

## Step 5: Configure Passenger WSGI

**Important:** Rename or update `passenger_wsgi.py` with your actual paths:

Edit `passenger_wsgi.py`:
```python
import os
import sys

# UPDATE THIS with your cPanel username
project_home = '/home/CPANEL_USERNAME/msmc_website'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual environment
venv_path = '/home/CPANEL_USERNAME/virtualenv/msmc_website/3.11/bin/activate_this.py'
if os.path.exists(venv_path):
    exec(open(venv_path).read(), {'__file__': venv_path})

os.environ['DJANGO_SETTINGS_MODULE'] = 'msmc.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace `CPANEL_USERNAME` with your actual cPanel username.

## Step 6: Configure Static Files

In cPanel File Manager or via SSH:
```bash
cd ~/msmc_website
mkdir -p staticfiles
source venv/bin/activate
python manage.py collectstatic --noinput
```

Create `.htaccess` file in `public_html/`:
```apache
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]

# Serve static files directly
RewriteRule ^static/(.*)$ /home/CPANEL_USERNAME/msmc_website/staticfiles/$1 [L]

# Passenger WSGI
PassengerPython /home/CPANEL_USERNAME/virtualenv/msmc_website/3.11/bin/python
PassengerAppRoot /home/CPANEL_USERNAME/msmc_website
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
```

## Step 7: Update Settings

In `msmc/settings.py`, update:
```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (use Cloudinary in production)
if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME')}/media/"
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
```

## Step 8: Restart Python App

In cPanel:
1. Go to **Setup Python App**
2. Find your application
3. Click **Restart**

Or via SSH:
```bash
touch ~/msmc_website/tmp/restart.txt
```

## Step 9: Verify Installation

Visit your domain:
- **Website:** `https://msmc.com.np`
- **Admin:** `https://msmc.com.np/admin/`

## Troubleshooting

### Error: "Module not found"
```bash
cd ~/msmc_website
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Permission denied"
```bash
chmod -R 755 ~/msmc_website
```

### Error: "Static files not loading"
1. Check `STATIC_ROOT` path
2. Run `python manage.py collectstatic --noinput`
3. Verify `.htaccess` rewrite rules

### Error: "Database locked" (SQLite)
SQLite isn't ideal for production. Switch to MySQL.

## Important Security Notes

1. **Change admin password immediately** after first login
2. **Use strong SECRET_KEY** (50+ random characters)
3. **Enable HTTPS** (cPanel → Let's Encrypt SSL)
4. **Set DEBUG=False** in production
5. **Backup database regularly** (cPanel Backup wizard)

## Support

For babal.host specific issues:
- Contact babal.host support
- Check cPanel documentation
- Verify Python version compatibility
