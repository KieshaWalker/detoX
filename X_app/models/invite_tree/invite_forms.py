from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .invite_model import InviteList
import uuid


class InviteForm(forms.ModelForm):
    """
    Form for sending invitations to new users
    """
    receiver_email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address to invite',
            'required': True
        }),
        help_text="Enter the email address of the person you want to invite"
    )

    secret_message = forms.CharField(
        label="Secret Message",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Something only they would know...',
            'required': True,
            'maxlength': 200
        }),
        help_text="Include a secret word or sentence they'll recognize",
        max_length=200
    )

    class Meta:
        model = InviteList
        fields = ['email', 'secret_message']  # Include secret_message
        widgets = {
            'email': forms.HiddenInput(),  # Hidden since we use receiver_email
            'secret_message': forms.HiddenInput(),  # Hidden since we use the form field
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the current user
        super().__init__(*args, **kwargs)

    def clean_receiver_email(self):
        """Validate the receiver email"""
        email = self.cleaned_data.get('receiver_email')

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")

        # Check if invitation already sent to this email
        if InviteList.objects.filter(email=email).exists():
            raise forms.ValidationError("An invitation has already been sent to this email.")

        return email

    def save(self, commit=True):
        """Save the invitation and send email"""
        instance = super().save(commit=False)

        # Set the email from the form field
        instance.email = self.cleaned_data['receiver_email']
        instance.secret_message = self.cleaned_data['secret_message']

        # Set the inviter
        if self.user:
            instance.inviter = self.user

            # Create or get an invitation code for this user
            from ..models import InvitationCode
            invite_code, created = InvitationCode.objects.get_or_create(
                invited_by=self.user,
                used=False,
                defaults={'code': str(uuid.uuid4())[:8].upper()}
            )
            instance.invite_code = invite_code

        if commit:
            instance.save()
            # Send the invitation email
            self.send_invitation_email(instance)

        return instance

    def send_invitation_email(self, invite_list):
        """Send invitation email using Mailgun"""
        try:
            # Prepare email content
            subject = f"You're invited to join detoX by {invite_list.inviter.get_full_name() or invite_list.inviter.username}"

            # Create plain text message
            message = f"""Hello!

You've been invited to join detoX by {invite_list.inviter.first_name or invite_list.inviter.username},

They included the following message for you:
{invite_list.secret_message}

Here is your invitation code: {invite_list.invite_code.code}

Please use this code to complete your registration, you will then complete a questionnaire before gaining access to the community.

Lets detoX!,
{invite_list.inviter.get_full_name() or invite_list.inviter.username}
"""

            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[invite_list.email],
                fail_silently=False,
            )

            print(f"✅ Invitation email sent successfully to {invite_list.email}")

        except Exception as e:
            print(f"❌ Error sending invitation email: {e}")
            # Don't raise exception to avoid form errors, but log it
            import logging
            logging.error(f"Failed to send invitation email to {invite_list.email}: {e}")