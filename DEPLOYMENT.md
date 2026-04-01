# Django Deployment Guide for MSMC Website

## Overview
This guide provides multiple deployment options for the Women Community Multipurpose Cooperative Ltd. website.

## Prerequisites
- Python 3.10+
- Git
- Domain name (e.g., msmc.com.np)
- Server/VPS or hosting platform account

---

## Option 1: PythonAnywhere (Easiest - Free Tier Available)

### Steps:
1. **Create account** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Open Bash console** and clone your repo:
```bash
git clone https://github.com/yourusername/msmc_website.git
cd msmc_website
```

3. **Create virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
# Create .env file
nano .env
```
Add:
```
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=yourusername.pythonanywhere.com,msmc.com.np
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

5. **Generate new secret key**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

6. **Run migrations**:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

7. **Configure Web App**:
   - Go to Web tab
   - Click "Add a new web app"
   - Select "Manual configuration (including virtualenvs)"
   - Select Python 3.10
   
8. **Configure WSGI file**:
Replace the contents of `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import os
import sys

path = '/home/yourusername/msmc_website'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'msmc.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

9. **Set virtualenv path**: `/home/yourusername/msmc_website/venv`

10. **Set static files**:
- URL: `/static/`
- Directory: `/home/yourusername/msmc_website/staticfiles`

- URL: `/media/`
- Directory: `/home/yourusername/msmc_website/media`

11. **Reload** the web app

---

## Option 2: Render.com (Free Tier)

### Steps:
1. **Push code to GitHub**

2. **Create `render.yaml`** in project root:
```yaml
services:
  - type: web
    name: msmc-website
    runtime: python
    buildCommand: |
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py migrate
    startCommand: gunicorn msmc.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: false
      - key: ALLOWED_HOSTS
        value: msmc-website.onrender.com,msmc.com.np
      - key: DATABASE_URL
        fromDatabase:
          name: msmc-db
          property: connectionString

databases:
  - name: msmc-db
    databaseName: msmc
    user: msmc
```

3. **Create `build.sh`**:
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

4. **Sign up** at [render.com](https://render.com) and connect GitHub repo

5. **Deploy** - Render will auto-deploy on git push

---

## Option 3: DigitalOcean / VPS (Full Control)

### Server Setup (Ubuntu 22.04)

1. **Update system**:
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install dependencies**:
```bash
sudo apt install python3-pip python3-venv python3-dev nginx postgresql postgresql-contrib supervisor git -y
```

3. **Create database**:
```bash
sudo -u postgres psql
CREATE DATABASE msmc_db;
CREATE USER msmc_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE msmc_db TO msmc_user;
\q
```

4. **Create app directory**:
```bash
sudo mkdir -p /var/www/msmc
cd /var/www/msmc
sudo git clone https://github.com/yourusername/msmc_website.git .
sudo chown -R $USER:$USER /var/www/msmc
```

5. **Setup virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

6. **Create production `.env`**:
```bash
nano .env
```
```
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=msmc.com.np,www.msmc.com.np,localhost
DB_ENGINE=django.db.backends.postgresql
DB_NAME=msmc_db
DB_USER=msmc_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=info@msmc.com.np
```

7. **Run migrations and collect static**:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

8. **Test Gunicorn**:
```bash
gunicorn --bind 0.0.0.0:8000 msmc.wsgi:application
```

9. **Create Gunicorn systemd service**:
```bash
sudo nano /etc/systemd/system/msmc.service
```
```ini
[Unit]
Description=MSMC Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/msmc
EnvironmentFile=/var/www/msmc/.env
ExecStart=/var/www/msmc/venv/bin/gunicorn --workers 3 --bind unix:/var/www/msmc/msmc.sock msmc.wsgi:application

[Install]
WantedBy=multi-user.target
```

10. **Start the service**:
```bash
sudo systemctl start msmc
sudo systemctl enable msmc
```

11. **Configure Nginx**:
```bash
sudo nano /etc/nginx/sites-available/msmc
```
```nginx
server {
    listen 80;
    server_name msmc.com.np www.msmc.com.np;

    location /static/ {
        alias /var/www/msmc/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/msmc/media/;
        expires 1M;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/msmc/msmc.sock;
    }
}
```

12. **Enable site and restart**:
```bash
sudo ln -s /etc/nginx/sites-available/msmc /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
```

13. **Setup SSL with Certbot**:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d msmc.com.np -d www.msmc.com.np
```

---

## Option 4: Heroku (Platform as a Service)

1. **Install Heroku CLI** and login

2. **Create files**:

`Procfile`:
```
web: gunicorn msmc.wsgi:application --log-file -
```

`runtime.txt`:
```
python-3.11.6
```

3. **Install whitenoise** (already in requirements.txt)

4. **Update settings.py**:
Add at the top:
```python
import django_heroku
django_heroku.settings(locals())
```

5. **Deploy**:
```bash
git init
git add .
git commit -m "Initial commit"
heroku create msmc-website
heroku config:set SECRET_KEY=your-secret-key DEBUG=False ALLOWED_HOSTS=msmc-website.herokuapp.com
heroku config:set DISABLE_COLLECTSTATIC=1
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## Production Checklist

### Security
- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set strong admin password
- [ ] Remove `admindocs` from INSTALLED_APPS if present

### Database
- [ ] Switch from SQLite to PostgreSQL (recommended for production)
- [ ] Run all migrations
- [ ] Create superuser
- [ ] Backup strategy configured

### Static/Media Files
- [ ] Run `collectstatic`
- [ ] Configure static file serving (nginx/whitenoise)
- [ ] Set up media file storage
- [ ] Configure CDN for static files (optional)

### Performance
- [ ] Enable gzip compression (nginx/whitenoise)
- [ ] Set browser caching headers
- [ ] Use database connection pooling
- [ ] Configure multiple Gunicorn workers

### Monitoring
- [ ] Set up error logging (Sentry recommended)
- [ ] Configure server monitoring
- [ ] Set up backup alerts

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | `django-insecure-...` |
| DEBUG | Debug mode | `False` |
| ALLOWED_HOSTS | Allowed domains | `msmc.com.np,www.msmc.com.np` |
| DB_ENGINE | Database engine | `django.db.backends.postgresql` |
| DB_NAME | Database name | `msmc_db` |
| DB_USER | Database user | `msmc_user` |
| DB_PASSWORD | Database password | `secure_password` |
| DB_HOST | Database host | `localhost` |
| EMAIL_HOST_USER | SMTP email | `info@msmc.com.np` |
| EMAIL_HOST_PASSWORD | SMTP password | `app_password` |

---

## Troubleshooting

### Static files not loading
- Check `STATIC_ROOT` is set correctly
- Run `collectstatic` again
- Verify nginx/whitenoise configuration

### Database connection errors
- Verify database credentials in `.env`
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Test connection: `psql -U msmc_user -d msmc_db`

### 502 Bad Gateway
- Check gunicorn is running: `sudo systemctl status msmc`
- Check socket file permissions
- Review gunicorn logs: `sudo journalctl -u msmc`

### SSL/HTTPS issues
- Verify certbot installed certificate
- Check nginx config includes SSL settings
- Test with `curl -I https://yourdomain.com`

---

## Recommended: DigitalOcean + Domain Setup

For the best performance and control for msmc.com.np:

1. **Buy VPS** from DigitalOcean, AWS Lightsail, or local Nepali host
2. **Point domain DNS** to server IP
3. **Follow Option 3** (VPS deployment)
4. **Setup SSL** with Let's Encrypt
5. **Configure backups** with pg_dump and rsync

Estimated cost: $5-10/month for VPS + domain registration
