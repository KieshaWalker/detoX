from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q, Count, Prefetch
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
import json
import uuid

from .post_model import Post, PostMedia, Like, Comment, Hashtag, PostView


class PostListView(LoginRequiredMixin, ListView):
    """Main post feed view showing posts from followed users and public posts"""
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        # Get posts from users the current user follows, plus their own posts
        # For now, show all public posts (expand this when following system is implemented)
        if self.request.user.is_authenticated:
            queryset = Post.objects.filter(
                Q(privacy='public') | Q(author=self.request.user)
            )
        else:
            queryset = Post.objects.filter(privacy='public')

        queryset = queryset.select_related('author', 'author__userprofile').prefetch_related(
            'additional_media',
            'likes'
        ).annotate(
            like_count=Count('likes'),
            comment_count=Count('comments')
        ).order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Post Feed'
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    """Detailed view of a single post with all comments and media"""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related(
            'additional_media',
            'likes',
            'comments__author',
            'hashtags'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Record view if user hasn't viewed this post recently
        PostView.objects.get_or_create(
            post=post,
            user=self.request.user,
            defaults={'viewed_at': timezone.now()}
        )

        # Update view count
        post.views_count = PostView.objects.filter(post=post).count()
        post.save(update_fields=['views_count'])

        context['comments'] = post.comments.select_related('author').order_by('created_at')
        context['is_liked'] = post.likes.filter(user=self.request.user).exists()
        context['like_count'] = post.likes.count()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post with media upload"""
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['caption', 'privacy', 'location', 'hashtags']
    success_url = reverse_lazy('posts:post_list')
    isArchive = False

    def form_valid(self, form):
        form.instance.author = self.request.user
        
        # Set content field to match caption (for database compatibility)
        form.instance.content = form.cleaned_data.get('caption', '')

        # Handle hashtags
        hashtags_text = form.cleaned_data.get('hashtags', '')
        if hashtags_text:
            # Process hashtags and create/update Hashtag objects
            hashtag_names = [tag.strip().strip('#').lower() for tag in hashtags_text.split(',') if tag.strip()]
            for name in hashtag_names:
                hashtag, created = Hashtag.objects.get_or_create(
                    name=name,
                    defaults={'posts_count': 0}
                )
                if not created:
                    hashtag.posts_count += 1
                    hashtag.save()

        response = super().form_valid(form)

        # Handle file uploads
        self._handle_media_upload(form.instance)

        messages.success(self.request, 'Post created successfully!')
        return response

    def _handle_media_upload(self, post):
        """Handle media file uploads for the post"""
        # Handle main image
        if 'image' in self.request.FILES:
            post.image = self.request.FILES['image']
            post.save()

        # Handle main video
        if 'video' in self.request.FILES:
            post.video = self.request.FILES['video']
            post.save()

        # Handle additional media files
        media_files = self.request.FILES.getlist('media_files[]')
        for media_file in media_files:
            PostMedia.objects.create(
                post=post,
                media_file=media_file,
                media_type=self._get_media_type(media_file)
            )

    def _get_media_type(self, file):
        """Determine media type based on file extension"""
        if file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return 'image'
        elif file.name.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
            return 'video'
        return 'other'


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing post"""
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['caption', 'privacy', 'location', 'hashtags']
    externaml_fields = ['like_count', 'comment_count', 'views_count']

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        # Get old hashtags from database BEFORE any updates
        old_post = Post.objects.get(pk=self.object.pk)
        old_hashtags_text = old_post.hashtags or ''
        
        # Get new hashtags from form
        new_hashtags_text = form.cleaned_data.get('hashtags', '')
        
        # Call parent form_valid to save the object
        response = super().form_valid(form)
        
        # Handle media updates
        self._handle_media_upload(form.instance)
        
        # Now handle hashtag updates
        old_hashtags = set()
        if old_hashtags_text:
            old_hashtags = set(tag.strip().strip('#').lower() for tag in old_hashtags_text.split(',') if tag.strip())

        new_hashtags = set()
        if new_hashtags_text:
            new_hashtags = set(tag.strip().strip('#').lower() for tag in new_hashtags_text.split(',') if tag.strip())

        # Update hashtag counts
        for old_tag in old_hashtags - new_hashtags:
            try:
                hashtag = Hashtag.objects.get(name=old_tag)
                hashtag.posts_count = max(0, hashtag.posts_count - 1)
                hashtag.save()
            except Hashtag.DoesNotExist:
                pass

        for new_tag in new_hashtags - old_hashtags:
            hashtag, created = Hashtag.objects.get_or_create(
                name=new_tag,
                defaults={'posts_count': 0}
            )
            hashtag.posts_count += 1
            hashtag.save()

        messages.success(self.request, 'Post updated successfully!')
        return response

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.object.pk})

    def _handle_media_upload(self, post):
        """Handle media file uploads for the post"""
        # Handle main image
        if 'image' in self.request.FILES:
            post.image = self.request.FILES['image']
            post.save()

        # Handle main video
        if 'video' in self.request.FILES:
            post.video = self.request.FILES['video']
            post.save()

        # Handle additional media files
        media_files = self.request.FILES.getlist('media_files[]')
        for media_file in media_files:
            PostMedia.objects.create(
                post=post,
                media_file=media_file,
                media_type=self._get_media_type(media_file)
            )

    def _get_media_type(self, file):
        """Determine media type based on file extension"""
        if file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return 'image'
        elif file.name.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
            return 'video'
        return 'other'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a post"""
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post_list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()

        # Update hashtag counts
        if post.hashtags:
            hashtag_names = [tag.strip().strip('#').lower() for tag in post.hashtags.split(',') if tag.strip()]
            for name in hashtag_names:
                try:
                    hashtag = Hashtag.objects.get(name=name)
                    hashtag.posts_count = max(0, hashtag.posts_count - 1)
                    hashtag.save()
                except Hashtag.DoesNotExist:
                    pass

        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
@require_POST
def like_post(request, post_id):
    """AJAX view to like/unlike a post"""
    try:
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'liked_at': timezone.now()}
        )

        if not created:
            # Unlike the post
            like.delete()
            liked = False
        else:
            liked = True

        # Update like count
        like_count = post.likes.count()
        post.likes_count = like_count
        post.save(update_fields=['likes_count'])

        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': like_count
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def add_comment(request, post_id):
    """AJAX view to add a comment to a post"""
    try:
        post = get_object_or_404(Post, id=post_id)
        data = json.loads(request.body)
        content = data.get('content', '').strip()

        if not content:
            return JsonResponse({'success': False, 'error': 'Comment cannot be empty'}, status=400)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )

        # Update comment count
        comment_count = post.comments.count()
        post.comments_count = comment_count
        post.save(update_fields=['comments_count'])

        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'author': comment.author.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'author_avatar': comment.author.userprofile.avatar.url if hasattr(comment.author, 'userprofile') and comment.author.userprofile.avatar else None
            },
            'comment_count': comment_count
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def user_posts(request, username):
    """View all posts by a specific user"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)

    # Check privacy settings
    if request.user != user:
        posts = Post.objects.filter(
            author=user,
            privacy='public'
        )
    else:
        posts = Post.objects.filter(author=user)

    posts = posts.select_related('author').prefetch_related(
        'post_media', 'likes', 'comments'
    ).annotate(
        like_count=Count('likes'),
        comment_count=Count('comments')
    ).order_by('-created_at')

    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'profile_user': user,
        'is_own_profile': request.user == user,
        'posts_count': posts.count(),
    }

    return render(request, 'posts/user_posts.html', context)


@login_required
def explore_posts(request):
    """Explore page showing trending posts and hashtags"""
    # Get trending posts (most liked in last 7 days)
    from django.utils import timezone
    from datetime import timedelta

    seven_days_ago = timezone.now() - timedelta(days=7)

    trending_posts = Post.objects.filter(
        created_at__gte=seven_days_ago,
        privacy='public'
    ).annotate(
        recent_likes=Count('likes')
    ).order_by('-recent_likes', '-created_at')[:20]

    # Get popular hashtags
    popular_hashtags = Hashtag.objects.order_by('-posts_count')[:10]

    context = {
        'trending_posts': trending_posts,
        'popular_hashtags': popular_hashtags,
        'page_title': 'Explore'
    }

    return render(request, 'posts/explore.html', context)


@login_required
def hashtag_posts(request, hashtag_name):
    """View all posts with a specific hashtag"""
    hashtag = get_object_or_404(Hashtag, name=hashtag_name.lower())

    # For now, we'll filter posts by hashtag text
    # In a more advanced implementation, you'd use a many-to-many relationship
    posts = Post.objects.filter(
        Q(privacy='public') | Q(author=request.user),
        hashtags__icontains=hashtag.name
    ).select_related('author').prefetch_related(
        'post_media', 'likes', 'comments'
    ).annotate(
        like_count=Count('likes'),
        comment_count=Count('comments')
    ).order_by('-created_at')

    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'hashtag': hashtag,
        'page_obj': page_obj,
        'posts_count': posts.count(),
        'page_title': f'#{hashtag.name}'
    }

    return render(request, 'posts/hashtag_posts.html', context)


# API-style views for AJAX requests
@login_required
def get_post_comments(request, post_id):
    """Get comments for a post (AJAX)"""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author').order_by('created_at')

    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'author_avatar': comment.author.userprofile.avatar.url if hasattr(comment.author, 'userprofile') and comment.author.userprofile.avatar else None,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return JsonResponse({'comments': comments_data})


@login_required
def get_post_likes(request, post_id):
    """Get users who liked a post (AJAX)"""
    post = get_object_or_404(Post, id=post_id)
    likes = post.likes.select_related('user').order_by('-liked_at')

    likes_data = []
    for like in likes:
        likes_data.append({
            'username': like.user.username,
            'display_name': like.user.get_full_name() or like.user.username,
            'avatar': like.user.userprofile.avatar.url if hasattr(like.user, 'userprofile') and like.user.userprofile.avatar else None,
            'liked_at': like.liked_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return JsonResponse({'likes': likes_data})
