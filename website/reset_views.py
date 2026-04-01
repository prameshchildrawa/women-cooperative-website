# Auto-create superuser view - REMOVE AFTER USE!
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def reset_admin(request):
    """Reset admin user. Remove this after first use!"""
    secret = request.GET.get('secret')
    if secret != 'msmc2024reset':
        return JsonResponse({'error': 'Invalid secret'}, status=403)
    
    # Delete existing admin
    User.objects.filter(username='admin').delete()
    
    # Create fresh superuser with explicit password
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
        'password': 'admin12345',
        'note': 'Password is set to: admin12345'
    })
