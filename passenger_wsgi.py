"""
Passenger WSGI Application Entry Point for cPanel Hosting (babal.host)
This file tells the server how to run your Django application

IMPORTANT: This configuration assumes your app is in /home/USERNAME/msmc
NOT in public_html (cPanel doesn't allow public_html as Python app root)
"""

import os
import sys

# ============================================
# IMPORTANT: UPDATE THIS VALUE
# ============================================
CPANEL_USERNAME = 'your_cpanel_username'  # <-- CHANGE THIS to your cPanel username

# ============================================
# PATH CONFIGURATION
# ============================================
# Project directory - use 'msmc' subdirectory (NOT public_html)
PROJECT_ROOT = f'/home/{CPANEL_USERNAME}/msmc'

# Add project to Python path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ============================================
# VIRTUAL ENVIRONMENT
# ============================================
# cPanel Python App virtual environment path (for 'msmc' app)
VENV_PATH = f'/home/{CPANEL_USERNAME}/virtualenv/msmc/3.11/bin/activate_this.py'

# Alternative paths (depending on cPanel configuration)
VENV_PATH_ALT1 = f'/home/{CPANEL_USERNAME}/virtualenv/msmc/3.11/bin/activate'
VENV_PATH_ALT2 = f'/home/{CPANEL_USERNAME}/virtualenv/msmc/bin/activate_this.py'

# Activate virtual environment
def activate_virtualenv():
    """Activate the Python virtual environment"""
    paths_to_try = [VENV_PATH, VENV_PATH_ALT1, VENV_PATH_ALT2]
    
    for venv_path in paths_to_try:
        if os.path.exists(venv_path):
            try:
                with open(venv_path, 'r') as f:
                    exec(f.read(), {'__file__': venv_path})
                return True
            except Exception:
                continue
    
    # If no activation file found, at least try to add site-packages
    site_packages = f'/home/{CPANEL_USERNAME}/virtualenv/msmc/3.11/lib/python3.11/site-packages'
    if os.path.exists(site_packages) and site_packages not in sys.path:
        sys.path.insert(0, site_packages)
    
    return False

# Activate the virtual environment
activate_virtualenv()

# ============================================
# DJANGO CONFIGURATION
# ============================================
# Tell Django where to find settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msmc.settings')

# Import and create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
