#!/usr/bin/env python
"""
Email Configuration Test Script for detoX
Test Django email backend with Mailgun SMTP
"""

import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detoX.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Test the email configuration"""
    print("🔧 Testing Django Email Configuration...")
    print(f"EMAIL_BACKEND: {settings.SENDER_DOMAIN}")
    print(f"EMAIL_HOST: {settings.MAILGUN_SMTP_SERVER}")
    print(f"EMAIL_PORT: {settings.MAILGUN_SMTP_PORT}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
    print(f"EMAIL_HOST_USER: {settings.SENDER_DOMAIN}")
    print()

    # Test sending an email
    try:
        subject = "detoX Email Test"
        message = """Hello!

This is a test email from your detoX application.

If you received this, your Mailgun SMTP configuration is working correctly!

Lets detoX!
The detoX Team
"""
        recipient = input("Enter your email address to test: ").strip()

        if not recipient:
            print("❌ No email address provided. Test cancelled.")
            return

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

        print(f"✅ Test email sent successfully to {recipient}")
        print("📧 Check your inbox (and spam folder) for the test email.")

    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        print("🔍 Check your Mailgun configuration and environment variables.")

if __name__ == '__main__':
    test_email_configuration()