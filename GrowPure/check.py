import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GrowPure.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'This is a test email from Django.',
    settings.DEFAULT_FROM_EMAIL,
    ['kalskars127@gmail.com'],  # Replace with your actual email
    fail_silently=False,
)
print("Email sent successfully!")
