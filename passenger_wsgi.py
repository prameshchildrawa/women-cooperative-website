"""
Passenger WSGI Application Entry Point for cPanel Hosting (babal.host)
This file tells the server how to run your Django application
"""

import os
import sys

# Add project to path
project_home = '/home/msmccomn/msmc'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add virtual environment packages
site_packages = '/home/msmccomn/virtualenv/msmc/3.11/lib/python3.11/site-packages'
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'msmc.settings'

# Import Django WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
