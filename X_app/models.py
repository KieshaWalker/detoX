from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class InvitationCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(User, related_name='sent_invitations', on_delete=models.CASCADE, null=True, blank=True)
    used = models.BooleanField(default=False)
    used_by = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.code

class QuestionnaireResponse(models.Model):
    # Basic info
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    invitation_code = models.ForeignKey(InvitationCode, on_delete=models.CASCADE)

    # Question 1: Motivation in helping others
    motivation_help_others = models.TextField()

    # Question 2: View of human nature
    human_nature_view = models.CharField(max_length=100, choices=[
        ('unpredictable', 'People are unpredictable and complex'),
        ('environment', 'People are shaped by their environment'),
        ('inherently_good', 'People are inherently good'),
        ('self_interested', 'People are self-interested by nature'),
    ])

    # Question 3: Belief about fairness
    fairness_belief = models.CharField(max_length=100, choices=[
        ('equal_outcomes', 'Fairness means equal outcomes for everyone'),
        ('equal_opportunities', 'Fairness means equal opportunities for everyone'),
        ('subjective', 'Fairness is subjective and context-dependent'),
        ('effort_merit', 'Fairness depends on effort and merit'),
    ])

    # Question 4: Long-term goals driver
    long_term_goals = models.CharField(max_length=100, choices=[
        ('security', 'Security and stability'),
        ('recognition', 'Recognition and status'),
        ('achievement', 'Need for personal achievement'),
        ('positive_impact', 'Desire to make a positive impact'),
    ])

    # Question 5: Response to personal struggle
    response_personal_struggle = models.CharField(max_length=100, choices=[
        ('emotional_support', 'I listen actively and offer emotional support'),
        ('practical_solutions', 'I try to provide practical solutions or advice'),
        ('share_experiences', 'I share similar experiences I\'ve had'),
        ('uncomfortable', 'I feel uncomfortable and change the subject'),
    ])

    # Question 6: Response to unfair treatment
    response_unfair_treatment = models.CharField(max_length=100, choices=[
        ('speak_up', 'Speak up immediately, even if it\'s uncomfortable'),
        ('assess_situation', 'Assess the situation and choose the right moment to intervene'),
        ('private_support', 'Support the person privately after the incident'),
        ('own_responsibilities', 'Focus on my own responsibilities and avoid involvement'),
    ])

    # Question 7: Definition of success
    success_definition = models.CharField(max_length=100, choices=[
        ('financial_security', 'Achieving financial security and material comfort'),
        ('relationships', 'Building meaningful relationships and connections'),
        ('positive_impact', 'Making a positive impact on others and society'),
        ('personal_growth', 'Personal growth and self-actualization'),
    ])

    # Question 8: Role of forgiveness
    forgiveness_role = models.CharField(max_length=100, choices=[
        ('forgive_easily', 'I forgive easily and don\'t hold grudges'),
        ('takes_time', 'I forgive but it takes time and effort'),
        ('difficult', 'I find it difficult to forgive serious betrayals'),
        ('situational', 'Forgiveness depends on the situation and the person\'s remorse'),
    ])

    # Question 9: Coping with failure
    coping_failure = models.CharField(max_length=100, choices=[
        ('analyze_learn', 'I analyze what went wrong and learn from it'),
        ('seek_support', 'I seek support from friends or family'),
        ('process_emotions', 'I give myself time to process emotions'),
        ('dwell', 'I tend to dwell on it and find it hard to move forward'),
    ])

    # Question 10: Approach to learning cultures
    learning_cultures = models.CharField(max_length=100, choices=[
        ('actively_curios', 'I\'m actively curious and seek out diverse experiences'),
        ('opportunities', 'I learn when opportunities present themselves'),
        ('stick_known', 'I prefer to stick to what I know and understand'),
        ('challenging', 'I find it challenging but recognize its importance'),
    ])

    # Additional questions (I'll add more fields as needed)
    empathy_definition = models.CharField(max_length=200, blank=True)
    values_conflict = models.CharField(max_length=200, blank=True)
    help_motivation = models.CharField(max_length=200, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    questionnaire = models.OneToOneField(QuestionnaireResponse, on_delete=models.SET_NULL, null=True, blank=True)
    invitation_code = models.ForeignKey(InvitationCode, on_delete=models.SET_NULL, null=True, blank=True)
 
    def __str__(self):
        return f"{self.user.username}'s profile"
