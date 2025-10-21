from django.db import models
from django.contrib.auth.models import User

# Remove the circular import - InvitationCode is defined in this file
# from X_app.models import QuestionnaireResponse, InvitationCode, UserProfile

## Invitation Code Model
class InvitationCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(User, related_name='sent_invitations', on_delete=models.CASCADE, null=True, blank=True)
    used = models.BooleanField(default=False)
    used_by = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.code

