# AWS EC2 Deployment Guide for MSMC Website

## Prerequisites
- AWS Account (free tier eligible)
- Domain name (msmc.com.np)
- SSH key pair generated

## Step 1: Launch EC2 Instance

1. Login to AWS Console → EC2 → Launch Instance
2. **Name:** msmc-website
3. **AMI:** Ubuntu Server 22.04 LTS (HVM)
4. **Instance Type:** t2.micro (free tier)
5. **Key Pair:** Create new or select existing
6. **Network Settings:**
   - Create security group
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
7. **Storage:** 20 GB (free tier)
8. Click **Launch Instance**

## Step 2: Connect to Instance

```bash
# On Windows (PowerShell)
ssh -i "your-key.pem" ubuntu@YOUR_EC2_IP

# On Mac/Linux
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@YOUR_EC2_IP
```

## Step 3: Run Deployment Script

```bash
# Update system first
sudo apt update && sudo apt upgrade -y

# Install git
sudo apt install git -y

# Clone repository
cd ~
git clone https://github.com/prameshchildrawa/women-cooperative-website.git msmc
cd msmc

# Run deployment script
chmod +x deploy/deploy_aws.sh
sudo ./deploy/deploy_aws.sh
```

## Step 4: Configure Nginx

```bash
# Copy nginx config
sudo cp deploy/nginx.conf /etc/nginx/sites-available/msmc

# Enable site
sudo ln -s /etc/nginx/sites-available/msmc /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

## Step 5: Start Gunicorn Service

```bash
# Copy systemd service
sudo cp deploy/msmc.service /etc/systemd/system/

# Reload daemon
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable msmc
sudo systemctl start msmc

# Check status
sudo systemctl status msmc
```

## Step 6: Configure Domain (Optional)

In your DNS provider, add A record:
- **Type:** A
- **Name:** @ (or www)
- **Value:** Your EC2 Public IP

Then update ALLOWED_HOSTS:
```bash
cd /var/www/msmc
sudo -u www-data nano .env
# Add your domain to ALLOWED_HOSTS
# ALLOWED_HOSTS=localhost,127.0.0.1,34.123.45.67,msmc.com.np,www.msmc.com.np

# Restart
sudo systemctl restart msmc
```

## Step 7: Setup HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d msmc.com.np -d www.msmc.com.np

# Auto-renewal is set up automatically
```

## Useful Commands

```bash
# Check logs
sudo journalctl -u msmc -f
sudo tail -f /var/log/nginx/error.log

# Restart services
sudo systemctl restart msmc
sudo systemctl restart nginx

# Update code
cd /var/www/msmc
sudo -u www-data git pull
sudo -u www-data bash -c "source venv/bin/activate && pip install -r requirements.txt"
sudo -u www-data bash -c "source venv/bin/activate && python manage.py migrate"
sudo -u www-data bash -c "source venv/bin/activate && python manage.py collectstatic --noinput"
sudo systemctl restart msmc
```

## Access Your Site

- **Website:** http://YOUR_EC2_IP/
- **Admin:** http://YOUR_EC2_IP/admin/
- **Username:** admin
- **Password:** admin12345

## Free Tier Limits

- **Instance:** 750 hours/month (t2.micro)
- **Storage:** 30GB EBS
- **Data Transfer:** 15GB out/month
- **Duration:** 12 months from signup

After 12 months: ~$8-10/month for t2.micro + storage
