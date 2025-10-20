from django.urls import path
from . import views

urlpatterns = [
    path('', views.InviteView.as_view(), name='invite'),
    path('send-invitation/', views.send_invitation, name='send_invitation'),
    path('enter-sentence/', views.enter_secret_sentence, name='enter_secret_sentence'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('questionnaire-submitted/', views.questionnaire_submitted, name='questionnaire_submitted'),
    path('admin/review-invitations/', views.admin_review_invitations, name='admin_review_invitations'),
    path('signup/<str:token>/', views.signup_with_token, name='signup_with_token'),
]
