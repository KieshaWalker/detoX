from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/login/', LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
    path('invite/', views.inviteView, name='invite'),
    path('register/', views.register, name='register'),
    path('questionaire/', views.questionaireView, name='questionaire'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),

]
