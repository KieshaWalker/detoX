from django import forms
from .models import QuestionnaireResponse, InvitationCode

class RegistrationForm(forms.ModelForm):
    invitation_code = forms.CharField(
        max_length=100,
        label="Invitation Code",
        help_text="Enter the invitation code you received via email"
    )

    class Meta:
        model = QuestionnaireResponse
        fields = [
            'full_name', 'email', 'invitation_code',
            'motivation_help_others', 'human_nature_view', 'fairness_belief',
            'long_term_goals', 'response_personal_struggle', 'response_unfair_treatment',
            'success_definition', 'forgiveness_role', 'coping_failure',
            'learning_cultures', 'empathy_definition', 'values_conflict', 'help_motivation'
        ]
        widgets = {
            'motivation_help_others': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Please describe your motivation...'}),
            'empathy_definition': forms.Textarea(attrs={'rows': 2, 'placeholder': 'How do you define empathy?'}),
            'values_conflict': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describe how you handle conflicting values...'}),
            'help_motivation': forms.Textarea(attrs={'rows': 2, 'placeholder': 'What motivates you to help others?'}),
        }

    def clean_invitation_code(self):
        code = self.cleaned_data.get('invitation_code').upper().strip()
        try:
            invitation = InvitationCode.objects.get(code=code, used=False)
        except InvitationCode.DoesNotExist:
            raise forms.ValidationError("Invalid or already used invitation code.")
        return code

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if QuestionnaireResponse.objects.filter(email=email).exists():
            raise forms.ValidationError("This email has already been registered.")
        return email

# Keep the existing login form
login_form = forms.Form()
login_form.fields['username'] = forms.CharField(max_length=150)
login_form.fields['password'] = forms.CharField(widget=forms.PasswordInput())