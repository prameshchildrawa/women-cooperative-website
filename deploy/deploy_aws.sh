#!/bin/bash
# AWS EC2 Deployment Script for MSMC Website
# Run this on a fresh Ubuntu 22.04 EC2 instance

set -e

echo "=========================================="
echo "MSMC Website AWS EC2 Deployment Script"
echo "=========================================="

# Update system
echo "[1/10] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "[2/10] Installing dependencies..."
sudo apt install -y python3-pip python3-venv python3-dev nginx postgresql postgresql-contrib git curl

# Install Node.js (for static files handling)
echo "[3/10] Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Setup PostgreSQL
echo "[4/10] Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE msmc;" 2>/dev/null || true
sudo -u postgres psql -c "CREATE USER msmc WITH PASSWORD 'msmc_password_2024';" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE msmc TO msmc;" 2>/dev/null || true
sudo -u postgres psql -c "ALTER DATABASE msmc OWNER TO msmc;" 2>/dev/null || true

# Create app directory
echo "[5/10] Creating application directory..."
sudo mkdir -p /var/www/msmc
cd /var/www/msmc

# Clone repository (replace with your repo)
echo "[6/10] Cloning repository..."
if [ ! -d ".git" ]; then
    sudo git clone https://github.com/prameshchildrawa/women-cooperative-website.git .
fi

# Set permissions
echo "[7/10] Setting permissions..."
sudo chown -R www-data:www-data /var/www/msmc
sudo chmod -R 755 /var/www/msmc

# Create virtual environment
echo "[8/10] Creating Python virtual environment..."
sudo -u www-data python3 -m venv venv
sudo -u www-data bash -c "source venv/bin/activate && pip install --upgrade pip"
sudo -u www-data bash -c "source venv/bin/activate && pip install -r requirements.txt"
sudo -u www-data bash -c "source venv/bin/activate && pip install gunicorn psycopg2-binary"

# Setup environment file
echo "[9/10] Creating environment file..."
sudo -u www-data tee .env > /dev/null <<EOF
DEBUG=False
SECRET_KEY=$(openssl rand -base64 50 | tr -d '\n')
ALLOWED_HOSTS=localhost,127.0.0.1,$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
DATABASE_URL=postgres://msmc:msmc_password_2024@localhost:5432/msmc
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=info@msmc.com.np
EOF

# Collect static files and run migrations
echo "[10/10] Running Django setup..."
sudo -u www-data bash -c "source venv/bin/activate && python manage.py collectstatic --noinput"
sudo -u www-data bash -c "source venv/bin/activate && python manage.py migrate"

# Create superuser
echo "Creating Django superuser..."
sudo -u www-data bash -c "source venv/bin/activate && python manage.py shell -c \"
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@msmc.com.np', 'admin12345')
    print('Superuser created: admin / admin12345')
else:
    print('Admin user already exists')
\""

echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy nginx config: sudo cp deploy/nginx.conf /etc/nginx/sites-available/msmc"
echo "2. Enable site: sudo ln -s /etc/nginx/sites-available/msmc /etc/nginx/sites-enabled/"
echo "3. Remove default: sudo rm /etc/nginx/sites-enabled/default"
echo "4. Copy systemd service: sudo cp deploy/msmc.service /etc/systemd/system/"
echo "5. Start services:"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable msmc"
echo "   sudo systemctl start msmc"
echo "   sudo systemctl restart nginx"
echo ""
echo "Admin URL: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/admin/"
echo "Username: admin"
echo "Password: admin12345"
echo "=========================================="
