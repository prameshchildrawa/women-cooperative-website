# Passenger WSGI entry point for cPanel hosting (babal.host)
# This file tells the server how to run your Django app

import os
import sys

# Add project to path
project_home = '/home/yourusername/public_html'  # Update with your cPanel username
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual environment path
venv_path = '/home/yourusername/virtualenv/public_html/3.11/bin/activate_this.py'
if os.path.exists(venv_path):
    exec(open(venv_path).read(), {'__file__': venv_path})

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'msmc.settings'

# Import application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
