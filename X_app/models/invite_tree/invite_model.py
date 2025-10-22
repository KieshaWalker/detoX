from django.db import models

from django.contrib.auth.models import User 
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
from ..models import InvitationCode

# create a model that retrieves the list of invites sent by a user
class InviteList(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invite_lists')
    invite_code = models.ForeignKey(InvitationCode, on_delete=models.CASCADE, related_name='invite_lists')
    email = models.EmailField()
    invited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite by {self.inviter.username} with code {self.invite_code.code}"