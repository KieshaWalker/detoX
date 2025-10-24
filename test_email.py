#!/usr/bin/env python
"""
Email Configuration Test Script for detoX
Run this to verify your email settings are working correctly.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detoX.settings')

# Setup Django
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_config():
    """Test the email configuration."""
    print("🔧 Testing detoX Email Configuration")
    print("=" * 40)

    # Debug environment detection
    on_heroku = bool(os.getenv('ON_HEROKU'))
    print(f"🌐 Environment: {'Heroku Production' if on_heroku else 'Local Development'}")
    print(f"📊 ON_HEROKU: {os.getenv('ON_HEROKU')}")
    print(f"🏭 DYNO: {os.getenv('DYNO')}")
    print()

    # Check configuration
    print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
    if hasattr(settings, 'MAILGUN_ACCESS_KEY'):
        print(f"🔑 Mailgun API Key: {'Set' if settings.MAILGUN_ACCESS_KEY else 'Not Set'}")
    if hasattr(settings, 'MAILGUN_SERVER_NAME'):
        print(f"� Mailgun Domain: {settings.MAILGUN_SERVER_NAME}")
    print(f"�🏠 Email Host: {getattr(settings, 'EMAIL_HOST', 'N/A')}")
    print(f"🔌 Email Port: {getattr(settings, 'EMAIL_PORT', 'N/A')}")
    print(f"🔒 Use TLS: {getattr(settings, 'EMAIL_USE_TLS', 'N/A')}")
    print(f"👤 Email User: {getattr(settings, 'EMAIL_HOST_USER', 'N/A')}")
    print(f"📤 From Email: {settings.DEFAULT_FROM_EMAIL}")
    print()

    # Test email sending based on backend
    can_send = False
    if settings.EMAIL_BACKEND == 'django_mailgun.MailgunBackend':
        can_send = hasattr(settings, 'MAILGUN_ACCESS_KEY') and settings.MAILGUN_ACCESS_KEY
        print(f"🔍 Mailgun API Key present: {hasattr(settings, 'MAILGUN_ACCESS_KEY')}")
        print(f"🔍 Mailgun API Key value: {'Set' if hasattr(settings, 'MAILGUN_ACCESS_KEY') and settings.MAILGUN_ACCESS_KEY else 'Not Set'}")
        if not can_send:
            print("⚠️  Mailgun API key not configured!")
            print("Please check your MAILGUN_ACCESS_KEY environment variable")
    else:
        can_send = settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD
        if not can_send:
            print("⚠️  Email credentials not configured!")
            print("Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your .env file")
            print("For Gmail setup instructions, see the README.md file")

    print(f"📊 Can send email: {can_send}")
    print()

    if can_send:
        print("📤 Attempting to send test email...")

        try:
            send_mail(
                subject='detoX Email Configuration Test',
                message='Congratulations! Your detoX email configuration is working correctly.\n\nThis email confirms that invitation emails will be sent successfully.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Send to yourself
                fail_silently=False,
            )
            print("✅ Email sent successfully!")
            print("📬 Check your inbox for the test email.")

        except Exception as e:
            print(f"❌ Email test failed: {e}")
            print("\n🔧 Troubleshooting tips:")
            print("1. Verify your EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env")
            print("2. For Gmail: Make sure you're using an App Password, not your regular password")
            print("3. Check that 2-Factor Authentication is enabled on your Google account")
            print("4. Verify EMAIL_HOST settings match your email provider")

    else:
        print("⚠️  Email credentials not configured!")
        print("Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your .env file")
        print("For Gmail setup instructions, see the README.md file")

    print("\n" + "=" * 40)
    print("✨ detoX Email Configuration Test Complete")

if __name__ == '__main__':
    test_email_config()