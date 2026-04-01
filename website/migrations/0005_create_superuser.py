# Generated manually to create default superuser
from django.db import migrations
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    """Create default superuser for admin access."""
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create(
            username='admin',
            email='admin@msmc.com.np',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password('admin12345')
        user.save()
        print("="*50)
        print("SUPERUSER CREATED: admin / admin12345")
        print("="*50)


def delete_superuser(apps, schema_editor):
    """Remove default superuser if needed."""
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('website', '0004_sitesettings_about_cooperative_image_and_more'),
    ]

    operations = [
        migrations.RunPython(create_superuser, delete_superuser),
    ]
