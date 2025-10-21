from django.db import models
from django.contrib.auth.models import User

from .questionnaire_model import QuestionnaireResponse
from .models import InvitationCode

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    questionnaire = models.OneToOneField(QuestionnaireResponse, on_delete=models.SET_NULL, null=True, blank=True)
    invitation_code = models.ForeignKey(InvitationCode, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.OneToOneField(QuestionnaireResponse, on_delete=models.SET_NULL, null=True, blank=True, related_name='first_name_profile')
    last_name = models.OneToOneField(QuestionnaireResponse, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_name_profile')
    email = models.OneToOneField(QuestionnaireResponse, on_delete=models.SET_NULL, null=True, blank=True, related_name='email_profile')

    
    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_compatibility_matches(self, limit=10):
        """
        Find most compatible users based on questionnaire responses.
        Returns list of (user, compatibility_score) tuples.
        """
        if not self.questionnaire:
            return []

        matches = []
        for profile in UserProfile.objects.exclude(user=self.user).select_related('questionnaire'):
            if profile.questionnaire:
                score = self.questionnaire.calculate_compatibility_score(profile.questionnaire)
                matches.append((profile.user, score))

        # Sort by compatibility score (highest first)
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:limit]

    def get_shared_values_summary(self, other_profile):
        """
        Returns a summary of shared values with another user.
        """
        if not self.questionnaire or not other_profile.questionnaire:
            return {}

        self_scores = self.questionnaire.calculate_personality_scores()
        other_scores = other_profile.questionnaire.calculate_personality_scores()

        shared_values = {}
        dimension_names = {
            'empathy_level': 'Empathy & Understanding',
            'growth_orientation': 'Personal Growth',
            'relationship_focus': 'Relationships',
            'openness_change': 'Openness to Change',
            'help_motivation': 'Helping Others',
            'fairness_orientation': 'Fairness & Justice',
            'success_definition': 'Success',
            'resilience_level': 'Resilience',
            'cultural_curiosity': 'Cultural Curiosity',
            'authenticity_level': 'Authenticity'
        }

        for dim, name in dimension_names.items():
            self_val = self_scores[dim]
            other_val = other_scores[dim]
            diff = abs(self_val - other_val)

            if diff <= 2:  # Close match
                shared_values[name] = 'Strong Match'
            elif diff <= 4:  # Moderate match
                shared_values[name] = 'Moderate Match'
            else:  # Different
                shared_values[name] = 'Different'

        return shared_values


class UserCompatibility(models.Model):
    """
    Stores calculated compatibility scores between users.
    """
    user1 = models.ForeignKey(User, related_name='compatibility_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='compatibility_user2', on_delete=models.CASCADE)
    compatibility_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Compatibility score 0-100")
    calculated_at = models.DateTimeField(auto_now=True)

    # Store key shared dimensions
    shared_empathy = models.BooleanField(default=False)
    shared_growth = models.BooleanField(default=False)
    shared_relationships = models.BooleanField(default=False)
    shared_values = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user1', 'user2']
        indexes = [
            models.Index(fields=['compatibility_score']),
            models.Index(fields=['calculated_at']),
        ]

    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username}: {self.compatibility_score}%"

    @classmethod
    def update_user_compatibilities(cls, user):
        """
        Calculate and update compatibility scores for a user with all other users.
        """
        try:
            user_profile = UserProfile.objects.get(user=user)
            if not user_profile.questionnaire:
                return

            for other_profile in UserProfile.objects.exclude(user=user).select_related('questionnaire'):
                if other_profile.questionnaire:
                    score = user_profile.questionnaire.calculate_compatibility_score(other_profile.questionnaire)

                    # Determine shared key values
                    shared_values = user_profile.get_shared_values_summary(other_profile)
                    shared_empathy = shared_values.get('Empathy & Understanding') in ['Strong Match', 'Moderate Match']
                    shared_growth = shared_values.get('Personal Growth') in ['Strong Match', 'Moderate Match']
                    shared_relationships = shared_values.get('Relationships') in ['Strong Match', 'Moderate Match']
                    shared_values_flag = any(val in ['Strong Match', 'Moderate Match']
                                           for val in shared_values.values())

                    # Create or update compatibility record
                    cls.objects.update_or_create(
                        user1=min(user, other_profile.user, key=lambda u: u.id),
                        user2=max(user, other_profile.user, key=lambda u: u.id),
                        defaults={
                            'compatibility_score': score,
                            'shared_empathy': shared_empathy,
                            'shared_growth': shared_growth,
                            'shared_relationships': shared_relationships,
                            'shared_values': shared_values_flag,
                        }
                    )
        except UserProfile.DoesNotExist:
            pass

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
            

