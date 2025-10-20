from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Invitation, Questionaire, Response, ResponseAnswer

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['receiver_email', 'custom_message', 'secret_sentence']
        widgets = {
            'custom_message': forms.TextInput(attrs={
                'placeholder': 'Enter your invitation message (e.g., "Join me!")',
                'class': 'form-control'
            }),
            'secret_sentence': forms.TextInput(attrs={
                'placeholder': 'Enter a secret sentence the recipient must type',
                'class': 'form-control'
            }),
            'receiver_email': forms.EmailInput(attrs={
                'placeholder': 'recipient@example.com',
                'class': 'form-control'
            })
        }

class SecretSentenceForm(forms.Form):
    secret_sentence = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the secret sentence from your invitation',
            'class': 'form-control'
        })
    )

class QuestionnaireForm(forms.Form):
    # These would be dynamically generated based on your questionnaire
    # For now, using basic fields as examples
    full_name = forms.CharField(max_length=100)
    experience_years = forms.IntegerField(min_value=0, max_value=50)
    motivation = forms.CharField(widget=forms.Textarea)
    skills = forms.CharField(widget=forms.Textarea)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

