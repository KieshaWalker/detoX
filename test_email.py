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

    # Check configuration
    print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
    print(f"🏠 Email Host: {settings.EMAIL_HOST}")
    print(f"🔌 Email Port: {settings.EMAIL_PORT}")
    print(f"🔒 Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"👤 Email User: {settings.EMAIL_HOST_USER}")
    print(f"📤 From Email: {settings.DEFAULT_FROM_EMAIL}")
    print()

    # Test email sending
    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
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