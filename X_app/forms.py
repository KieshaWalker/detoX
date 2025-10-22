from django import forms
from django.contrib.auth.models import User
from .models import QuestionnaireResponse, InvitationCode

class RegistrationForm(forms.ModelForm):
    # Username field - allow users to choose their own username
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Choose a username",
        help_text="Choose a unique username for your account",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your desired username'})
    )
    # Terms of Service Agreement - Required for legal compliance
    terms_agreement = forms.BooleanField(
        required=True,
        label="I agree to the Terms of Service",
        help_text="You must read and agree to our Terms of Service to continue",
        error_messages={
            'required': 'You must agree to the Terms of Service to register.'
        }
    )

    # Privacy Policy Agreement - Required for legal compliance
    privacy_agreement = forms.BooleanField(
        required=True,
        label="I agree to the Privacy Policy",
        help_text="You must read and agree to our Privacy Policy to continue",
        error_messages={
            'required': 'You must agree to the Privacy Policy to register.'
        }
    )

    # Waiver of Results - Required for data usage consent
    results_waiver = forms.BooleanField(
        required=True,
        label="I consent to the use of my questionnaire responses for compatibility matching and research",
        help_text="Your responses will be used to find compatible matches and may be analyzed for research purposes",
        error_messages={
            'required': 'You must consent to the use of your questionnaire responses to continue.'
        }
    )

    class Meta:
        model = QuestionnaireResponse
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'motivation_help_others', 'human_nature_view', 'fairness_belief',
            'long_term_goals', 'response_personal_struggle', 'response_unfair_treatment',
            'success_definition', 'forgiveness_role', 'coping_failure',
            'learning_cultures', 'empathy_definition', 'values_conflict', 'help_motivation'
        ]
       

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if QuestionnaireResponse.objects.filter(email=email).exists():
            raise forms.ValidationError("This email has already been registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        # Additional validation for username format
        if not username.replace('_', '').replace('-', '').isalnum():
            raise forms.ValidationError("Username can only contain letters, numbers, underscores, and hyphens.")
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")
        return username


login_form = forms.Form()
login_form.fields['username'] = forms.CharField(max_length=150)
login_form.fields['password'] = forms.CharField(widget=forms.PasswordInput())