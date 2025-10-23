from django.urls import path
from .post_views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    user_posts, explore_posts, hashtag_posts,
    like_post, add_comment, get_post_comments, get_post_likes
)

app_name = 'posts'

urlpatterns = [
    # Post listing and detail
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Post CRUD operations
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # User posts
    path('user/<str:username>/', user_posts, name='user_posts'),

    # Explore and discovery
    path('explore/', explore_posts, name='explore_posts'),
    path('hashtag/<str:hashtag_name>/', hashtag_posts, name='hashtag_posts'),

    # AJAX endpoints
    path('<int:post_id>/like/', like_post, name='like_post'),
    path('<int:post_id>/comment/', add_comment, name='add_comment'),
    path('<int:post_id>/comments/', get_post_comments, name='get_post_comments'),
    path('<int:post_id>/likes/', get_post_likes, name='get_post_likes'),
]