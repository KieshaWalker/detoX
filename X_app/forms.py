from django import forms
from .models import QuestionnaireResponse, InvitationCode

class RegistrationForm(forms.ModelForm):
    invitation_code = forms.CharField(
        max_length=100,
        label="Invitation Code",
        help_text="Enter the invitation code you received via email"
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
            'first_name', 'last_name', 'email', 'invitation_code',
            'motivation_help_others', 'human_nature_view', 'fairness_belief',
            'long_term_goals', 'response_personal_struggle', 'response_unfair_treatment',
            'success_definition', 'forgiveness_role', 'coping_failure',
            'learning_cultures', 'empathy_definition', 'values_conflict', 'help_motivation'
        ]
       

    def clean_invitation_code(self):
        code = self.cleaned_data.get('invitation_code').upper().strip()
        try:
            invitation = InvitationCode.objects.get(code=code, used=False)
        except InvitationCode.DoesNotExist:
            raise forms.ValidationError("Invalid or already used invitation code.")
        return invitation

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if QuestionnaireResponse.objects.filter(email=email).exists():
            raise forms.ValidationError("This email has already been registered.")
        return email
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.save()
        return user


login_form = forms.Form()
login_form.fields['username'] = forms.CharField(max_length=150)
login_form.fields['password'] = forms.CharField(widget=forms.PasswordInput())