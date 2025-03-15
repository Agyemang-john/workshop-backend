import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Create a superuser with custom fields"

    def handle(self, *args, **kwargs):
        first_name = os.getenv("DJANGO_SUPERUSER_FIRST_NAME")
        last_name = os.getenv("DJANGO_SUPERUSER_LAST_NAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        phone = os.getenv("DJANGO_SUPERUSER_PHONE")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not all([first_name, last_name, email, phone, password]):
            self.stderr.write(self.style.ERROR("Missing environment variables for superuser."))
            return

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully."))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser {email} already exists."))
