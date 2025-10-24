from django import forms
from django.contrib.auth.models import User
from .models import QuestionnaireResponse, InvitationCode, Post, PostMedia


class MultipleFileInput(forms.ClearableFileInput):
    """Custom widget for multiple file uploads"""
    allow_multiple_selected = True


class RegistrationForm(forms.ModelForm):
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


class PostForm(forms.ModelForm):
    """Form for creating and editing posts with Cloudinary media upload support"""

    # Additional media files (for carousel posts)
    additional_media = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': 'image/*,video/*',
            'class': 'form-control'
        }),
        help_text="Upload additional images or videos for a carousel post",
        label="Additional Media"
    )

    class Meta:
        model = Post
        fields = ['caption', 'image', 'video', 'location', 'hashtags', 'privacy']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share what\'s on your mind...',
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control'
            }),
            'video': forms.ClearableFileInput(attrs={
                'accept': 'video/*',
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Where was this taken?',
                'class': 'form-control'
            }),
            'hashtags': forms.TextInput(attrs={
                'placeholder': 'travel, photography, nature',
                'class': 'form-control'
            }),
            'privacy': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'caption': 'Share what\'s on your mind...',
            'image': 'Upload a main image for your post',
            'video': 'Upload a video for your post (alternative to image)',
            'location': 'Where was this taken?',
            'hashtags': 'Separate multiple hashtags with commas',
            'privacy': 'Who can see this post?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image and video optional in form validation since we handle this in view
        self.fields['image'].required = False
        self.fields['video'].required = False

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        # Ensure only one media type is selected
        if image and video:
            raise forms.ValidationError(
                "You can only upload either an image OR a video, not both."
            )

        return cleaned_data

    def clean_hashtags(self):
        """Clean and validate hashtags"""
        hashtags = self.cleaned_data.get('hashtags', '')
        if hashtags:
            # Process hashtags: remove extra spaces, ensure # prefix
            hashtag_list = []
            for tag in hashtags.split(','):
                tag = tag.strip()
                if tag:
                    # Remove # if present and add it back
                    tag = tag.lstrip('#')
                    if tag:  # Only add non-empty tags
                        hashtag_list.append(f"#{tag}")
            return ', '.join(hashtag_list)
        return hashtags

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set content field to match caption for backward compatibility
        instance.content = instance.caption or ''

        if commit:
            instance.save()

        # Handle additional media files
        additional_files = self.files.getlist('additional_media')
        for file in additional_files:
            if file:
                # Determine media type
                media_type = 'image' if file.content_type.startswith('image/') else 'video'

                PostMedia.objects.create(
                    post=instance,
                    media_file=file,
                    media_type=media_type
                )

        return instance