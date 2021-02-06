from django.db import migrations
from django.conf import settings
from django.contrib.auth import get_user_model


def create_default_admin(*args) -> None:
    User = get_user_model()
    User.objects.create_superuser(
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD
    )


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_admin),
    ]
