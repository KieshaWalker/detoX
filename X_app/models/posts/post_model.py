import json
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import uuid

# Import cloudinary conditionally
try:
    import cloudinary
    from cloudinary import CloudinaryImage
except ImportError:
    cloudinary = None
    CloudinaryImage = None


class Post(models.Model):

    # Unique identifier
    id = models.AutoField(primary_key=True)

    # Author relationship
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )


    # Content fields
    caption = models.TextField(
        max_length=2200,  # Instagram's limit
        blank=True,
        help_text="Post caption/description"
    )
    
    # Legacy content field for database compatibility
    content = models.TextField(
        blank=True,
        help_text="Legacy content field"
    )

    # Media fields
    image = models.ImageField(
        upload_to='posts/images/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        help_text="Main post image"
    )

    video = models.FileField(
        upload_to='posts/videos/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['mp4', 'mov', 'avi', 'webm'])],
        help_text="Post video (for TikTok-style content)"
    )

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Privacy settings
    class PrivacyChoices(models.TextChoices):
        PUBLIC = 'public', 'Public'
        FRIENDS = 'friends', 'Friends Only'
        PRIVATE = 'private', 'Private'

    privacy = models.CharField(
        max_length=10,
        choices=PrivacyChoices.choices,
        default=PrivacyChoices.PUBLIC
    )

    # Location (optional)
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Location tag for the post"
    )

    # Engagement metrics (denormalized for performance)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)  # For TikTok-style view counts

    # Hashtags (stored as comma-separated for simplicity, or use ManyToMany)
    hashtags = models.TextField(
        blank=True,
        help_text="Comma-separated hashtags (e.g., 'travel,photography,nature')"
    )

    # Featured/boosted content
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark as featured content"
    )

    # Archive/soft delete
    is_archived = models.BooleanField(
        default=False,
        help_text="Soft delete - hide from public view but keep data"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['privacy', '-created_at']),
            models.Index(fields=['is_featured', '-created_at']),
            models.Index(fields=['-likes_count']),  # For popular posts
            models.Index(fields=['-views_count']),   # For trending content
        ]

    def __str__(self):
        return f"{self.author.username}: {self.caption[:50]}..."

    def save(self, *args, **kwargs):
        # Ensure only one media type per post (image OR video, not both)
        if self.image and self.video:
            # If both are provided, prioritize video (TikTok style)
            self.image = None
        super().save(*args, **kwargs)

    @property
    def is_video_post(self):
        """Check if this is a video post (TikTok style)"""
        return bool(self.video)

    @property
    def is_image_post(self):
        """Check if this is an image post (Instagram style)"""
        return bool(self.image) and not self.video

    @property
    def media_type(self):
        """Return the type of media in this post"""
        if self.video:
            return 'video'
        elif self.image:
            return 'image'
        else:
            return 'text'

    @property
    def engagement_score(self):
        """Calculate engagement score for algorithmic ranking"""
        # Simple engagement formula: likes + comments*2 + shares*3 + views*0.01
        return (self.likes_count +
                self.comments_count * 2 +
                self.shares_count * 3 +
                self.views_count * 0.01)

    def get_hashtags_list(self):
        """Parse hashtags string into a list"""
        if not self.hashtags:
            return []
        return [tag.strip('#').strip() for tag in self.hashtags.split(',') if tag.strip()]


class PostMedia(models.Model):
    """
    Additional media files for posts (for carousel posts like Instagram)
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='additional_media'
    )

    media_file = models.FileField(
        upload_to='posts/media/%Y/%m/%d/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mov', 'avi', 'webm'])]
    )

    media_type = models.CharField(
        max_length=10,
        choices=[('image', 'Image'), ('video', 'Video')],
        default='image'
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of media in carousel"
    )

    class Meta:
        ordering = ['order']
        unique_together = ['post', 'order']


class Like(models.Model):
    """
    Like model for tracking post likes
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'post']  # One like per user per post


class Comment(models.Model):
    """
    Comment model for post comments
    """
    id = models.AutoField(primary_key=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField(max_length=1000)  # Reasonable comment length

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # For nested comments/replies (optional)
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # Moderation
    is_hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}..."


class Hashtag(models.Model):
    """
    Hashtag model for tracking and searching hashtags
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Hashtag name without # (e.g., 'travel')"
    )

    # Usage statistics
    posts_count = models.PositiveIntegerField(default=0)
    last_used = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posts_count', 'name']

    def __str__(self):
        return f"#{self.name}"

    def save(self, *args, **kwargs):
        # Ensure hashtag name is lowercase and without #
        self.name = self.name.lower().strip('#')
        super().save(*args, **kwargs)


class PostView(models.Model):
    """
    Track post views for analytics (TikTok-style view counts)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_views'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='views'
    )

    viewed_at = models.DateTimeField(default=timezone.now)

    # Track view duration for engagement metrics
    duration_seconds = models.PositiveIntegerField(
        default=0,
        help_text="How long the user viewed the post"
    )

    class Meta:
        unique_together = ['user', 'post']  # One view record per user per post
        ordering = ['-viewed_at']
