from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Invitation, User, Profile, Post, Comment, Like, Follow, Questionaire, Response, ResponseAnswer
from .forms import InvitationForm, SecretSentenceForm, QuestionnaireForm, CustomUserCreationForm


# Create your views here.

class InviteView(CreateView):
   def get(self, request, *args, **kwargs):
       return render(request, 'base.html')
    

@login_required
def send_invitation(request):
    """View for approved users to send invitations with custom messages"""
    # Check if user is approved (you might want to add an is_approved field to User model)
    # For now, allowing all logged-in users to send invites

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.sender = request.user
            invitation.save()

            # Send invitation email
            try:
                send_mail(
                    f'Invitation from {request.user.username}',
                    f'{request.user.username} says: "{invitation.custom_message}"\n\n'
                    f'Click here to join: {request.build_absolute_uri("/enter-sentence/")}\n\n'
                    f'You\'ll need to enter the secret sentence to access the application.',
                    settings.DEFAULT_FROM_EMAIL,
                    [invitation.receiver_email],
                    fail_silently=False,
                )
                messages.success(request, f'Invitation sent to {invitation.receiver_email}!')
                return redirect('send_invitation')
            except Exception as e:
                messages.error(request, f'Failed to send email: {str(e)}')
    else:
        form = InvitationForm()

    return render(request, 'send_invitation.html', {'form': form})


def enter_secret_sentence(request):
    """View for potential users to enter the secret sentence and access questionnaire"""
    if request.method == 'POST':
        form = SecretSentenceForm(request.POST)
        if form.is_valid():
            secret_sentence = form.cleaned_data['secret_sentence']
            try:
                invitation = Invitation.objects.get(secret_sentence=secret_sentence)
                # Store invitation ID in session for questionnaire access
                request.session['invitation_id'] = invitation.id
                return redirect('questionnaire')
            except Invitation.DoesNotExist:
                messages.error(request, 'Invalid secret sentence. Please check your invitation.')
    else:
        form = SecretSentenceForm()

    return render(request, 'enter_secret_sentence.html', {'form': form})


@login_required
def questionnaire(request):
    """Questionnaire view accessible only after entering correct secret sentence"""
    invitation_id = request.session.get('invitation_id')
    if not invitation_id:
        messages.error(request, 'Please enter your secret sentence first.')
        return redirect('enter_secret_sentence')

    try:
        invitation = Invitation.objects.get(id=invitation_id)
    except Invitation.DoesNotExist:
        messages.error(request, 'Invalid invitation.')
        return redirect('enter_secret_sentence')

    if invitation.questionnaire_completed:
        messages.info(request, 'You have already completed the questionnaire. Waiting for admin approval.')
        return redirect('questionnaire_submitted')

    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            # Create questionnaire response
            questionnaire = Questionaire.objects.create(
                user=invitation.sender,  # This might need adjustment
                title=f"Application from {invitation.receiver_email}"
            )

            response = Response.objects.create(
                questionaire=questionnaire,
                user=invitation.sender  # This might need adjustment
            )

            # Save form data (this is simplified - you'd want to map to actual questions)
            # For now, just mark as completed
            invitation.questionnaire_completed = True
            invitation.save()

            messages.success(request, 'Questionnaire submitted! Waiting for admin approval.')
            return redirect('questionnaire_submitted')
    else:
        form = QuestionnaireForm()

    return render(request, 'questionnaire.html', {
        'form': form,
        'invitation': invitation
    })


def questionnaire_submitted(request):
    """Confirmation page after questionnaire submission"""
    return render(request, 'questionnaire_submitted.html')


@login_required
def admin_review_invitations(request):
    """Admin view to review completed questionnaires and approve users"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')

    pending_invitations = Invitation.objects.filter(
        questionnaire_completed=True,
        admin_reviewed=False
    ).select_related('sender')

    if request.method == 'POST':
        invitation_id = request.POST.get('invitation_id')
        action = request.POST.get('action')

        invitation = get_object_or_404(Invitation, id=invitation_id)

        if action == 'approve':
            invitation.approved = True
            invitation.approved_at = timezone.now()
            invitation.admin_reviewed = True
            invitation.generate_token()
            invitation.save()

            # Send approval email with signup link
            signup_url = request.build_absolute_uri(f'/signup/{invitation.token}/')
            try:
                send_mail(
                    'Your application has been approved!',
                    f'Congratulations! Your application has been approved.\n\n'
                    f'Click here to complete your registration: {signup_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [invitation.receiver_email],
                    fail_silently=False,
                )
                messages.success(request, f'Approved {invitation.receiver_email} and sent signup link.')
            except Exception as e:
                messages.error(request, f'Approved but failed to send email: {str(e)}')

        elif action == 'reject':
            invitation.admin_reviewed = True
            invitation.save()
            messages.success(request, f'Rejected application from {invitation.receiver_email}.')

        return redirect('admin_review_invitations')

    return render(request, 'admin_review_invitations.html', {
        'pending_invitations': pending_invitations
    })


def signup_with_token(request, token):
    """Final signup view for approved users"""
    try:
        invitation = Invitation.objects.get(token=token, approved=True)
    except Invitation.DoesNotExist:
        messages.error(request, 'Invalid or expired invitation token.')
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Mark invitation as used (you might want to add a used field)
            messages.success(request, 'Account created successfully! Welcome to detoX.')
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form, 'invitation': invitation})
