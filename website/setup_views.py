# Auto-create superuser view - REMOVE AFTER USE!
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_admin(request):
    """One-time view to create admin user. Remove this after first use!"""
    secret = request.GET.get('secret')
    if secret != 'msmc2024setup':
        return JsonResponse({'error': 'Invalid secret'}, status=403)
    
    # Delete existing admin if any (to reset)
    User.objects.filter(username='admin').delete()
    
    # Create fresh superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@msmc.com.np',
        password='admin12345'
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Admin user created/reset successfully',
        'username': 'admin',
        'password': 'admin12345'
    })
