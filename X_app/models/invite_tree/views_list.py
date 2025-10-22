from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
import uuid

from .invite_model import InviteList
from ..models import InvitationCode
from ..User_model import UserProfile
from ...forms import RegistrationForm


def list_invites(request):
    invites = InviteList.objects.filter(inviter=request.user)
    return render(request, 'app_/invite_list/treeList.html', {
        'title': 'Your Invitations',
        'invites': invites
    })
print(f"list_invites view loaded successfully.")