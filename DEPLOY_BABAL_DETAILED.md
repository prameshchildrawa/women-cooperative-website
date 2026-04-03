# Complete Babal.Host Deployment Guide for MSMC Website

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Step 1: Prepare Your Files](#step-1-prepare-your-files)
3. [Step 2: Purchase Hosting & Domain](#step-2-purchase-hosting--domain)
4. [Step 3: Upload Files to cPanel](#step-3-upload-files-to-cpanel)
5. [Step 4: Create Python Environment](#step-4-create-python-environment)
6. [Step 5: Configure Database](#step-5-configure-database)
7. [Step 6: Update Configuration Files](#step-6-update-configuration-files)
8. [Step 7: Install Dependencies](#step-7-install-dependencies)
9. [Step 8: Setup Django](#step-8-setup-django)
10. [Step 9: Configure Domain & SSL](#step-9-configure-domain--ssl)
11. [Step 10: Test & Troubleshoot](#step-10-test--troubleshoot)
12. [Maintenance & Updates](#maintenance--updates)

---

## Pre-Deployment Checklist

Before starting, you need:
- [ ] babal.host hosting account (with cPanel access)
- [ ] Domain name: msmc.com.np (already registered)
- [ ] Cloudinary account (for image storage)
- [ ] Generated SECRET_KEY
- [ ] SSH access (optional but recommended)

---

## Step 1: Prepare Your Files

### 1.1 Download Your Repository
```bash
# On your local machine
cd Desktop
git clone https://github.com/prameshchildrawa/women-cooperative-website.git msmc_website
cd msmc_website
```

### 1.2 Generate SECRET_KEY
Create a file `generate_secret.py`:
```python
import secrets
key = secrets.token_urlsafe(50)
print(f"Your SECRET_KEY: {key}")
```

Run it:
```bash
python generate_secret.py
```

**SAVE THIS KEY!** You'll need it later.

### 1.3 Prepare for Upload
Remove unnecessary files:
```bash
# Remove git history (not needed on server)
Remove-Item -Recurse -Force .git

# Remove local virtual environment
Remove-Item -Recurse -Force venv

# Remove local database
Remove-Item db.sqlite3

# Remove __pycache__ folders
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Directory -Filter "*.pyc" | Remove-Item -Recurse -Force
```

### 1.4 Update Configuration Files

Edit `.htaccess`:
```apache
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]

# Serve static files directly
RewriteRule ^static/(.*)$ /home/YOUR_CPANEL_USERNAME/public_html/staticfiles/$1 [L]
RewriteRule ^media/(.*)$ /home/YOUR_CPANEL_USERNAME/public_html/media/$1 [L]

# Prevent access to sensitive files
<FilesMatch "\.(env|ini|log|sh|sql|json|lock|py)$">
    Order allow,deny
    Deny from all
</FilesMatch>

# Disable directory browsing
Options -Indexes

# Passenger WSGI Configuration
PassengerPython /home/YOUR_CPANEL_USERNAME/virtualenv/public_html/3.11/bin/python
PassengerAppRoot /home/YOUR_CPANEL_USERNAME/public_html
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
```

Replace `YOUR_CPANEL_USERNAME` with your actual cPanel username (e.g., `msmcuser`).

Edit `passenger_wsgi.py`:
```python
import os
import sys

# IMPORTANT: Update with your cPanel username
CPANEL_USERNAME = 'YOUR_CPANEL_USERNAME'  # <-- CHANGE THIS

project_home = f'/home/{CPANEL_USERNAME}/public_html'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual environment
venv_path = f'/home/{CPANEL_USERNAME}/virtualenv/public_html/3.11/bin/activate_this.py'
if os.path.exists(venv_path):
    exec(open(venv_path).read(), {'__file__': venv_path})

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'msmc.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 1.5 Create Environment File
Create `.env` file:
```
DEBUG=False
SECRET_KEY=paste-your-generated-secret-key-here
ALLOWED_HOSTS=msmc.com.np,www.msmc.com.np,localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=info@msmc.com.np
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

### 1.6 Zip Your Files
```powershell
# Create zip archive
Compress-Archive -Path "*" -DestinationPath "msmc_website.zip" -Force
```

Your zip file should contain:
- msmc/ (Django project settings)
- website/ (your app)
- static/ (static files)
- templates/ (HTML templates)
- manage.py
- requirements.txt
- .htaccess
- passenger_wsgi.py
- .env
- DEPLOY_BABAL.md

---

## Step 2: Purchase Hosting & Domain

### 2.1 Purchase babal.host Hosting
1. Go to https://babal.host
2. Select a Python hosting plan
3. Recommended:至少 1GB storage, Python 3.11 support
4. Complete purchase and get cPanel login credentials

### 2.2 Point Your Domain
Login to register.com.np (your domain registrar):

**Option A: Using Cloudflare (Recommended)**
1. Sign up at https://dash.cloudflare.com
2. Add site: msmc.com.np
3. Cloudflare will scan for DNS records
4. Update nameservers at register.com.np to Cloudflare nameservers
5. In Cloudflare DNS:
   - Add A record: `@` → Your babal.host server IP
   - Add CNAME: `www` → msmc.com.np

**Option B: Direct DNS**
1. Login to register.com.np
2. Go to DNS Management
3. Add A record:
   - Name: @
   - Value: (babal.host server IP address)
4. Add CNAME record:
   - Name: www
   - Value: msmc.com.np

---

## Step 3: Upload Files to cPanel

### 3.1 Login to cPanel
1. Go to https://yourdomain.com:2083 (or https://cpanel.babal.host)
2. Enter username and password

### 3.2 Upload Files
**Method A: File Manager (Easier)**
1. In cPanel, click **File Manager**
2. Navigate to `/public_html/`
3. Delete any existing files (like index.html)
4. Click **Upload** → Select your `msmc_website.zip`
5. After upload, right-click zip → **Extract**
6. Move files from extracted folder to `/public_html/`

**Method B: FTP (Faster for large files)**
1. Download FileZilla (https://filezilla-project.org)
2. Connect using FTP credentials from cPanel
3. Upload files to `/public_html/`

### 3.3 Verify Upload
In File Manager, check that `/public_html/` contains:
- msmc/
- website/
- static/
- templates/
- manage.py
- requirements.txt
- .htaccess
- passenger_wsgi.py
- .env

---

## Step 4: Create Python Environment

### 4.1 Setup Python Application
1. In cPanel, find **Setup Python App** (or **Select Python Version**)
2. Click **Create Application**
3. Configure:
   - **Python Version:** 3.11
   - **Application Root:** `public_html`
   - **Application URL:** (leave empty for root domain)
   - **Application Entry Point:** `passenger_wsgi.py`
4. Click **Create**

### 4.2 Note Virtual Environment Path
The system will create a virtual environment. Note the path:
```
/home/YOURUSERNAME/virtualenv/public_html/3.11/bin/python
```

You'll need this for configuration.

---

## Step 5: Configure Database

### 5.1 Option A: SQLite (Easiest, Good for Small Sites)
SQLite is already configured. No additional setup needed.

### 5.2 Option B: MySQL (Better for Production)
**Create Database:**
1. In cPanel, click **MySQL Database Wizard**
2. Step 1 - Create Database:
   - Database Name: `msmc_db`
   - Full name will be: `username_msms_db`
3. Step 2 - Create User:
   - Username: `msmc_user`
   - Password: Generate strong password (save it!)
4. Step 3 - Add User to Database:
   - Select user and database
   - Check **ALL PRIVILEGES**
5. Click **Next Step**

**Update .env:**
```
DATABASE_URL=mysql://username_msmc_user:PASSWORD@localhost/username_msmc_db
```

Replace:
- `username` with your cPanel username
- `PASSWORD` with the database password you generated

---

## Step 6: Update Configuration Files

### 6.1 Update .htaccess
Edit `/public_html/.htaccess` in File Manager:

```apache
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]

# Serve static files directly
RewriteRule ^static/(.*)$ /home/YOURUSERNAME/public_html/staticfiles/$1 [L]
RewriteRule ^media/(.*)$ /home/YOURUSERNAME/public_html/media/$1 [L]

# Prevent access to sensitive files
<FilesMatch "\.(env|ini|log|sh|sql|json|lock|py)$">
    Order allow,deny
    Deny from all
</FilesMatch>

# Disable directory browsing
Options -Indexes

# Passenger WSGI Configuration
PassengerPython /home/YOURUSERNAME/virtualenv/public_html/3.11/bin/python
PassengerAppRoot /home/YOURUSERNAME/public_html
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
```

### 6.2 Update passenger_wsgi.py
Edit `/public_html/passenger_wsgi.py`:

```python
import os
import sys

# UPDATE THIS LINE ONLY:
CPANEL_USERNAME = 'your_actual_cpanel_username'  # <-- CHANGE THIS

project_home = f'/home/{CPANEL_USERNAME}/public_html'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual environment
venv_path = f'/home/{CPANEL_USERNAME}/virtualenv/public_html/3.11/bin/activate_this.py'
if os.path.exists(venv_path):
    exec(open(venv_path).read(), {'__file__': venv_path})

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'msmc.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## Step 7: Install Dependencies

### 7.1 Via SSH (Recommended)
If you have SSH access:

```bash
# Connect via SSH
ssh yourusername@yourserver.com

# Navigate to project
cd ~/public_html

# Activate virtual environment
source /home/yourusername/virtualenv/public_html/3.11/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install additional packages
pip install mysqlclient  # If using MySQL
```

### 7.2 Via cPanel Terminal
1. In cPanel, open **Terminal**
2. Run the same commands as above

### 7.3 Via Python App Interface
Some cPanel providers have a "Install dependencies" button in the Python App section.

---

## Step 8: Setup Django

### 8.1 Run Migrations
```bash
cd ~/public_html
source /home/yourusername/virtualenv/public_html/3.11/bin/activate

# Create database tables
python manage.py migrate
```

### 8.2 Create Superuser
```bash
# Create admin user
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@msmc.com.np', 'your-strong-password')
    print('Admin user created successfully')
else:
    print('Admin user already exists')
"
```

**Change 'your-strong-password' to a real secure password!**

### 8.3 Collect Static Files
```bash
# Create staticfiles directory
mkdir -p staticfiles

# Collect all static files
python manage.py collectstatic --noinput
```

### 8.4 Create Media Directory
```bash
mkdir -p media
chmod 755 media
```

---

## Step 9: Configure Domain & SSL

### 9.1 Point Domain to Hosting
Ensure your domain DNS points to babal.host server IP:
1. Login to register.com.np or Cloudflare
2. Update A record to your server IP
3. Wait 10-30 minutes for propagation

### 9.2 Install SSL Certificate
In cPanel:
1. Go to **SSL/TLS** or **Let's Encrypt**
2. Click **Install SSL Certificate**
3. Select your domain: msmc.com.np
4. Click **Install**

Or use AutoSSL which is often enabled by default.

### 9.3 Force HTTPS
Update `.htaccess` to redirect HTTP to HTTPS:

```apache
# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# www to non-www redirect
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]

# Rest of your configuration...
```

---

## Step 10: Test & Troubleshoot

### 10.1 Restart Python App
In cPanel:
1. Go to **Setup Python App**
2. Find your application
3. Click **Restart**

### 10.2 Test Website
Visit:
- https://msmc.com.np (should show your website)
- https://msmc.com.np/admin/ (Django admin login)

### 10.3 Common Errors & Fixes

**Error: "Module not found"**
```bash
pip install -r requirements.txt
```

**Error: "Permission denied"**
```bash
chmod -R 755 /home/yourusername/public_html
```

**Error: "Database locked" (SQLite)**
Switch to MySQL or ensure proper file permissions:
```bash
chmod 666 /home/yourusername/public_html/db.sqlite3
```

**Error: "Static files not loading"**
1. Check `STATIC_ROOT` in settings
2. Run `collectstatic` again
3. Verify `.htaccess` rewrite rules

**Error: "400 Bad Request"**
Add your domain to ALLOWED_HOSTS in `.env`:
```
ALLOWED_HOSTS=msmc.com.np,www.msmc.com.np,localhost,127.0.0.1,YOUR_SERVER_IP
```

**Error: "500 Internal Server Error"**
Check error logs in cPanel → **Error Logs**

### 10.4 Check Application Status
```bash
# Check if Django can start
source /home/yourusername/virtualenv/public_html/3.11/bin/activate
cd /home/yourusername/public_html
python manage.py check --deploy
```

---

## Maintenance & Updates

### Update Website Code
```bash
cd ~/public_html
git pull origin master  # If using git

# Or upload new files via File Manager

# Then restart
source /home/yourusername/virtualenv/public_html/3.11/bin/activate
pip install -r requirements.txt  # If requirements changed
python manage.py migrate
python manage.py collectstatic --noinput

# Restart app in cPanel
```

### Backup Database
**SQLite:**
```bash
cp /home/yourusername/public_html/db.sqlite3 /home/yourusername/backup_$(date +%Y%m%d).sqlite3
```

**MySQL:**
In cPanel: **Backup Wizard** → MySQL Database Backup

### Monitor Logs
In cPanel:
- **Error Logs** - Check for errors
- **Latest Visitors** - See traffic
- **Awstats** - Website statistics

---

## Quick Reference

### Important Paths
```
Project Root: /home/USERNAME/public_html/
Virtual Env:  /home/USERNAME/virtualenv/public_html/3.11/
Static Files: /home/USERNAME/public_html/staticfiles/
Media Files:  /home/USERNAME/public_html/media/
Database:     /home/USERNAME/public_html/db.sqlite3
```

### Essential Commands
```bash
# Activate virtual environment
source /home/USERNAME/virtualenv/public_html/3.11/bin/activate

# Run Django commands
cd /home/USERNAME/public_html
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py shell

# Restart app (in cPanel: Setup Python App → Restart)
touch /home/USERNAME/public_html/tmp/restart.txt
```

### File Permissions
```bash
# Set correct permissions
chmod -R 755 /home/USERNAME/public_html
chmod 644 /home/USERNAME/public_html/.env
chmod 666 /home/USERNAME/public_html/db.sqlite3  # If using SQLite
```

---

## Support & Help

### babal.host Support
- Contact via their support portal
- WhatsApp/Email support

### Django Documentation
- https://docs.djangoproject.com

### Common Issues
1. **500 Error**: Check .env file exists and is readable
2. **Static files 404**: Check .htaccess rewrite rules
3. **Database errors**: Verify DATABASE_URL format
4. **Permission denied**: Fix file ownership (www-data or your user)

---

**Congratulations! Your MSMC Website is now live on babal.host!** 🎉

Remember to:
- ✅ Change admin password immediately
- ✅ Enable Cloudinary for image storage
- ✅ Set up regular backups
- ✅ Monitor error logs weekly
