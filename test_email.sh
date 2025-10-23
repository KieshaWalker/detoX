#!/bin/bash
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detoX.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print('Heroku Email Configuration:')
print(f'EMAIL_HOST: {settings.EMAIL_HOST}')
print(f'EMAIL_PORT: {settings.EMAIL_PORT}')
print(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
print(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
print(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')

print('Testing email send...')
try:
    result = send_mail(
        'Test Email from detoX',
        'This is a test email to verify Mailgun configuration is working on Heroku.',
        settings.DEFAULT_FROM_EMAIL,
        ['deto.connect@gmail.com'],
        fail_silently=False,
    )
    print(f'Email sent successfully! Result: {result}')
except Exception as e:
    print(f'Email failed: {e}')
"