from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .models.invite_tree.views_list import list_invites

urlpatterns = [
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/login/', LoginView.as_view(template_name='first_contact/login.html', redirect_authenticated_user=True), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
    path('invite/', views.inviteView, name='invite'),
    path('register/', views.register, name='register'),
    path('questionnaire/', views.questionnaireView, name='questionnaire'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('invite/list/', list_invites, name='invite_list'),

    # Posts URLs
    path('posts/', include('X_app.models.posts.urls')),
]
