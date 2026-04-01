# Auto-create superuser view - REMOVE AFTER USE!
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_admin(request):
    """One-time view to create admin user. Remove this after first use!"""
    # Secret key to prevent abuse - change this!
    secret = request.GET.get('secret')
    if secret != 'msmc2024setup':
        return JsonResponse({'error': 'Invalid secret'}, status=403)
    
    # Check if admin already exists
    if User.objects.filter(username='admin').exists():
        return JsonResponse({
            'message': 'Admin user already exists',
            'username': 'admin'
        })
    
    # Create superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@msmc.com.np',
        password='admin12345'
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Admin user created successfully',
        'username': 'admin',
        'password': 'admin12345',
        'warning': 'Please change password immediately after logging in!'
    })
