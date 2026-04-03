import os
import sys

# Add your project directory to the sys.path
project_home = '/home/yourusername/msmc_website'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'msmc.settings'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'your-secret-key-here-change-this'
os.environ['ALLOWED_HOSTS'] = 'msmc.com.np,www.msmc.com.np'

# Activate virtual environment
activate_this = '/home/yourusername/msmc_website/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
