from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
import uuid
from .models import InvitationCode, UserProfile
from .forms import RegistrationForm


# Create your views here.

def home(request):
    return render(request, 'home.html')

def inviteView(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        email = request.POST.get('email')
        secret_message = request.POST.get('secret_message')

        if not email or not secret_message:
            messages.error(request, 'Please provide both email and secret message.')
            return redirect('invite')

        # Generate unique invitation code
        invitation_code = str(uuid.uuid4())[:8].upper()

        # Save to database
        InvitationCode.objects.create(code=invitation_code, invited_by=request.user)

        # Send email with secret message
        try:
            subject = 'Your detoX Invitation'
            message = f'''
Hello!

You've been invited to join detoX!

Secret Message: {secret_message}

Your invitation code: {invitation_code}

Please use this code to complete your registration.

Best regards,
{request.user.get_full_name() or request.user.username}
'''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, f'Invitation sent to {email} with your secret message!')
        except Exception as e:
            messages.error(request, 'Failed to send email. Please try again later.')
            # Clean up the invitation code if email failed
            InvitationCode.objects.filter(code=invitation_code).delete()

        return redirect('invite')

    return render(request, 'invite.html')

def register(request):
    if request.method == 'POST':
        invitation_code = request.POST.get('invitation_code', '').upper().strip()

        if not invitation_code:
            messages.error(request, 'Please enter an invitation code.')
            return redirect('register')

        # Validate invitation code
        try:
            invitation = InvitationCode.objects.get(code=invitation_code, used=False)
        except InvitationCode.DoesNotExist:
            messages.error(request, 'Invalid or already used invitation code.')
            return redirect('register')

        # Store the valid invitation code in session and redirect to questionnaire
        request.session['invitation_code'] = invitation_code
        return redirect('questionaire')

    return render(request, 'register.html')

def profile(request):
    return render(request, 'profile.html')

def questionaireView(request):
    # Check if user has a valid invitation code in session
    invitation_code = request.session.get('invitation_code')
    if not invitation_code:
        messages.error(request, 'Please enter a valid invitation code first.')
        return redirect('register')

    try:
        invitation = InvitationCode.objects.get(code=invitation_code, used=False)
    except InvitationCode.DoesNotExist:
        messages.error(request, 'Invalid invitation code.')
        return redirect('register')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create questionnaire response
            questionnaire = form.save(commit=False)
            questionnaire.invitation_code = invitation
            questionnaire.save()

            # Create user account
            username = questionnaire.email.split('@')[0] + str(uuid.uuid4())[:4]
            user = User.objects.create_user(
                username=username,
                email=questionnaire.email,
                first_name=questionnaire.full_name.split()[0] if questionnaire.full_name.split() else '',
                last_name=' '.join(questionnaire.full_name.split()[1:]) if len(questionnaire.full_name.split()) > 1 else ''
            )

            # Create user profile
            UserProfile.objects.create(
                user=user,
                questionnaire=questionnaire,
                invitation_code=invitation
            )

            # Mark invitation code as used
            invitation.used = True
            invitation.used_by = user
            invitation.save()

            # Clear session and log the user in
            del request.session['invitation_code']
            login(request, user)

            messages.success(request, 'Registration successful! Welcome to detoX.')
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'questionaire.html', {'form': form})

