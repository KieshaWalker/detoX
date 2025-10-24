#!/usr/bin/env python
"""
Test script to verify post creation works correctly
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detoX.settings')

# Setup Django
django.setup()

from django.test import Client, TestCase
from django.contrib.auth.models import User
from X_app.models import Post

def test_post_creation():
    """Test post creation functionality"""
    print("🧪 Testing Post Creation Backend")
    print("=" * 40)

    # Create test client
    client = Client()

    # Create a test user if it doesn't exist
    try:
        user = User.objects.get(username='testuser')
        print("✅ Test user already exists")
        # Reset password just in case
        user.set_password('testpass123')
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print("✅ Created test user")

    # Login the user
    login_success = client.login(username='testuser', password='testpass123')
    if login_success:
        print("✅ User logged in successfully")
    else:
        print("❌ Login failed")
        return

    # Test data
    post_data = {
        'caption': 'Test post from backend! 🚀',
        'location': 'Test City',
        'hashtags': 'test, backend, django',
        'privacy': 'public'
    }

    print(f"📝 Submitting post data: {post_data}")

    # Submit POST request to create post
    response = client.post('/posts/create/', data=post_data)

    print(f"📡 Response status: {response.status_code}")

    if response.status_code == 302:  # Redirect after successful creation
        print("✅ Post creation successful (redirected)")

        # Check if post was actually created in database
        posts = Post.objects.filter(author=user, caption=post_data['caption'])
        if posts.exists():
            post = posts.first()
            print("✅ Post found in database:")
            print(f"   - ID: {post.id}")
            print(f"   - Caption: {post.caption}")
            print(f"   - Content: {post.content}")
            print(f"   - Location: {post.location}")
            print(f"   - Hashtags: {post.hashtags}")
            print(f"   - Privacy: {post.privacy}")
            print(f"   - Author: {post.author.username}")

            # Verify content field matches caption
            if post.content == post.caption:
                print("✅ Content field correctly matches caption")
            else:
                print(f"❌ Content mismatch: content='{post.content}' vs caption='{post.caption}'")

        else:
            print("❌ Post not found in database")

    elif response.status_code == 200:
        print("⚠️  Form returned with validation errors")
        print("Response content preview:")
        print(response.content.decode()[:500])

    else:
        print(f"❌ Unexpected response status: {response.status_code}")
        print("Response content preview:")
        print(response.content.decode()[:500])

    # Test posts list page
    print("\n🧪 Testing Posts List Page")
    print("-" * 30)
    
    response = client.get('/posts/')
    print(f"📡 Posts page response status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Posts page loaded successfully")
        # Check if the template rendered without errors
        if 'post-card' in response.content.decode():
            print("✅ Post cards found in response")
        else:
            print("⚠️  No post cards found (might be empty)")
    else:
        print(f"❌ Posts page failed with status: {response.status_code}")
        print("Response preview:")
        print(response.content.decode()[:300])

if __name__ == '__main__':
    test_post_creation()