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

You've been invited to join detoX by {request.user.get_full_name() or request.user.username},

They included the following message for you:
{secret_message}

Here is your invitation code: {invitation_code}

Please use this code to complete your registration, you will then complete a questionnaire before gaining access to the community.

Lets detoX!,
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


def terms_of_service(request):
    """
    Display the Terms of Service document.
    Required for legal compliance during registration.
    """
    try:
        with open('X_app/documents/terms_of_service.txt', 'r') as f:
            terms_content = f.read()
    except FileNotFoundError:
        terms_content = """
        Terms of Service

        Welcome to detoX. By using our service, you agree to these terms.

        1. Acceptance of Terms
        By accessing and using detoX, you accept and agree to be bound by the terms and provision of this agreement.

        2. Use License
        Permission is granted to temporarily access the materials (information or software) on detoX's website for personal, non-commercial transitory viewing only.

        3. Disclaimer
        The materials on detoX's website are provided on an 'as is' basis. detoX makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.

        4. Limitations
        In no event shall detoX or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on detoX's website.

        5. Accuracy of Materials
        The materials appearing on detoX's website could include technical, typographical, or photographic errors. detoX does not warrant that any of the materials on its website are accurate, complete, or current.

        6. Links
        detoX has not reviewed all of the sites linked to its website and is not responsible for the contents of any such linked site.

        7. Modifications
        detoX may revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these terms of service.

        8. Governing Law
        These terms and conditions are governed by and construed in accordance with the laws of the applicable jurisdiction, and you irrevocably submit to the exclusive jurisdiction of the courts in that state or location.
        """

    return render(request, 'legalsites/terms_of_service.html', {
        'terms_content': terms_content,
        'title': 'Terms of Service'
    })


def privacy_policy(request):
    """
    Display the Privacy Policy document.
    Required for legal compliance during registration.
    """
    try:
        with open('X_app/documents/privacy_policy.txt', 'r') as f:
            privacy_content = f.read()
    except FileNotFoundError:
        privacy_content = """
        Privacy Policy

        Welcome to detoX. This Privacy Policy explains how we collect, use, disclose, and safeguard your information.

        1. Information We Collect
        We collect information you provide directly to us, such as when you create an account, use our services, or contact us for support.

        2. How We Use Your Information
        We use the information we collect to provide, maintain, and improve our services, process transactions, and communicate with you.

        3. Information Sharing
        We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this policy.

        4. Data Security
        We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.

        5. Your Rights
        You have the right to access, update, or delete your personal information. You may also opt out of certain data collection and use.

        6. Changes to This Policy
        We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page.

        7. Contact Us
        If you have any questions about this Privacy Policy, please contact us.
        """

    return render(request, 'legalsites/privacy_policy.html', {
        'privacy_content': privacy_content,
        'title': 'Privacy Policy'
    })

