import os
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def reset_admin(request):
    """Secure admin reset endpoint. Only accessible with correct secret."""
    # Use environment variable or strong fallback secret
    valid_secret = os.environ.get('ADMIN_RESET_SECRET', 'msmc_secure_reset_2024!@#')
    provided_secret = request.GET.get('secret')
    
    if provided_secret != valid_secret:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Delete existing admin
    User.objects.filter(username='admin').delete()
    
    # Create fresh superuser
    user = User(
        username='admin',
        email='admin@msmc.com.np',
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )
    user.set_password('admin12345')
    user.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Admin user reset successfully',
        'username': 'admin',
        'password': 'admin12345'
    })
