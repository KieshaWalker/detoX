from django.db import models
from django.contrib.auth.models import User
from .models import InvitationCode
## Questionnaire Response Model
class QuestionnaireResponse(models.Model):
    # Basic info
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    invitation_code = models.ForeignKey(InvitationCode, on_delete=models.CASCADE)

    # Question 1: Motivation in helping others
    motivation_help_others = models.CharField(max_length=100, choices=[
        ('personal_growth', 'Personal growth and self-actualization'),
        ('helping_others', 'Helping others and making a difference'),
        ('financial_security', 'Achieving financial security'),
        ('social_status', 'Gaining social status and recognition'),
    ])

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
## Question 11-30: Additional personality and reflection questions
    empathy_definition = models.CharField(max_length=100, choices=[
        ('understanding', 'Understanding and sharing the feelings of others'),
        ('compassion', 'Feeling compassion and wanting to help'),
        ('perspective_taking', 'Seeing things from another\'s perspective'),
        ('emotional_resonance', 'Feeling a deep emotional connection with others'),
    ])
    values_conflict = models.CharField(max_length=200, choices=[
        ('open_dialogue', 'I engage in open dialogue to understand different perspectives'),
        ('avoid_conflict', 'I avoid conflict and try to keep the peace'),
        ('assertive', 'I assert my values while respecting others'),
        ('flexible', 'I adapt my values based on the situation'),
    ])
    help_motivation = models.CharField(max_length=200, choices=[
        ('intrinsic', 'I help others because it feels intrinsically rewarding'),
        ('extrinsic', 'I help others to gain recognition or rewards'),
        ('social', 'I help others to strengthen social bonds'),
        ('obligation', 'I help others out of a sense of duty'),
    ])
    home_concept = models.CharField(max_length=100, choices=[
        ('physical_place', 'A physical place where I live'),
        ('belonging_security', 'A feeling of belonging and security'),
        ('loved_ones', 'Where my loved ones are located'),
        ('state_of_mind', 'A state of mind rather than a location'),
    ], blank=True)

    uncertainty_response = models.CharField(max_length=100, choices=[
        ('gather_info', 'I gather information and make a plan'),
        ('seek_advice', 'I seek advice from trusted people'),
        ('feel_anxious', 'I feel anxious and prefer to avoid it'),
        ('embrace_growth', 'I embrace it as an opportunity for growth'),
    ], blank=True)

    gratitude_role = models.CharField(max_length=100, choices=[
        ('regularly_express', 'I regularly express thanks for what I have'),
        ('notice_positive', 'I notice positive aspects but don\'t always express it'),
        ('focus_lacking', 'I focus more on what\'s lacking than what\'s present'),
        ('maintain_perspective', 'Gratitude helps me maintain perspective during challenges'),
    ], blank=True)

    feedback_approach = models.CharField(max_length=100, choices=[
        ('give_constructive', 'I give constructive feedback thoughtfully'),
        ('receive_openly', 'I receive feedback openly and use it for growth'),
        ('giving_difficult', 'I find giving feedback difficult'),
        ('receiving_challenging', 'I find receiving feedback challenging'),
    ], blank=True)

    life_balance = models.CharField(max_length=100, choices=[
        ('equal_time', 'Equal time spent on work, relationships, and self-care'),
        ('harmony', 'Harmony between different aspects of life'),
        ('juggle_responsibilities', 'The ability to juggle multiple responsibilities'),
        ('know_priorities', 'Knowing when to prioritize different areas'),
    ], blank=True)

    trust_definition = models.CharField(max_length=100, choices=[
        ('reliability', 'Reliability and keeping promises'),
        ('emotional_safety', 'Emotional safety and vulnerability'),
        ('shared_values', 'Shared values and mutual respect'),
        ('time_consistency', 'Time and consistency in actions'),
    ], blank=True)

    struggling_thoughts = models.CharField(max_length=100, choices=[
        ('want_to_help', '"I want to help them through this"'),
        ('learn_experience', '"I wonder what I can learn from their experience"'),
        ('feel_grateful', '"I feel grateful that I\'m not in their situation"'),
        ('feel_overwhelmed', '"I feel overwhelmed and unsure how to help"'),
    ], blank=True)

    difficult_conversations = models.CharField(max_length=100, choices=[
        ('prepare_carefully', 'I prepare thoroughly and choose words carefully'),
        ('speak_from_heart', 'I speak from the heart and express emotions'),
        ('avoid_when_possible', 'I avoid them when possible'),
        ('address_directly', 'I address issues directly and honestly'),
    ], blank=True)

    life_meaning = models.CharField(max_length=100, choices=[
        ('career_success', 'Career achievements and professional success'),
        ('relationships', 'Relationships and connections with others'),
        ('personal_growth', 'Personal growth and self-discovery'),
        ('contribute_larger', 'Contributing to something larger than myself'),
    ], blank=True)

    change_response = models.CharField(max_length=100, choices=[
        ('embrace_opportunity', 'I embrace it as an opportunity for new experiences'),
        ('adapt_gradually', 'I adapt gradually and give myself time'),
        ('resist_stability', 'I resist it and prefer stability'),
        ('reinvent_myself', 'I see it as a chance to reinvent myself'),
    ], blank=True)

    emotion_processing = models.CharField(max_length=100, choices=[
        ('talk_trusted', 'I talk about them with trusted people'),
        ('write_journal', 'I write or journal about my feelings'),
        ('physical_activity', 'I engage in physical activity or hobbies'),
        ('suppress_later', 'I suppress them until I can deal with them later'),
    ], blank=True)

    boundaries_approach = models.CharField(max_length=100, choices=[
        ('clearly_communicate', 'I clearly communicate my limits and needs'),
        ('difficult_important', 'I find it difficult but know it\'s important'),
        ('prioritize_others', 'I tend to prioritize others\' needs over mine'),
        ('set_feel_guilty', 'I set boundaries but feel guilty about it'),
    ], blank=True)

    vulnerability_strength = models.CharField(max_length=100, choices=[
        ('sign_true_strength', 'Vulnerability is a sign of true strength'),
        ('never_show', 'Strength means never showing vulnerability'),
        ('can_coexist', 'They can coexist - being strong includes being vulnerable'),
        ('makes_weak', 'Vulnerability makes you weak in others\' eyes'),
    ], blank=True)

    self_reflection_frequency = models.CharField(max_length=100, choices=[
        ('daily', 'Daily - it\'s a regular practice for me'),
        ('weekly', 'Weekly - when I have time to think deeply'),
        ('occasionally', 'Occasionally - during significant life events'),
        ('rarely', 'Rarely - I prefer to stay busy and active'),
        ('never', 'Never - I don\'t see the value in it'),
    ], blank=True)

    change_mind_frequency = models.CharField(max_length=100, choices=[
        ('frequently', 'Frequently - I\'m open to new information'),
        ('sometimes', 'Sometimes - when presented with compelling evidence'),
        ('rarely', 'Rarely - I tend to stick to my initial decisions'),
        ('never', 'Never - once I decide, that\'s it'),
    ], blank=True)

    admit_fault_frequency = models.CharField(max_length=100, choices=[
        ('always', 'Always - accountability is important to me'),
        ('often', 'Often - when I\'m clearly in the wrong'),
        ('sometimes', 'Sometimes - depends on the situation'),
        ('rarely', 'Rarely - I find it difficult to admit mistakes'),
        ('never', 'Never - I prefer to avoid confrontation'),
    ], blank=True)

    active_listening_definition = models.CharField(max_length=100, choices=[
        ('focus_speaker', 'Fully focusing on the speaker without distractions'),
        ('understand_words_emotions', 'Understanding both words and emotions being conveyed'),
        ('ask_questions', 'Asking clarifying questions to ensure comprehension'),
        ('remember_details', 'Remembering details for future reference'),
        ('all_above', 'All of the above'),
    ], blank=True)

    human_being_definition = models.CharField(max_length=100, choices=[
        ('imperfect_learning', 'Being imperfect and learning from mistakes'),
        ('connect_emotionally', 'Connecting with others on an emotional level'),
        ('experience_emotions', 'Experiencing the full range of emotions'),
        ('seek_meaning', 'Seeking meaning and purpose in life'),
        ('all_above_human', 'All of the above'),
    ], blank=True)

    self_love_level = models.CharField(max_length=100, choices=[
        ('completely_unconditionally', 'Yes, completely and unconditionally'),
        ('working_on_it', 'Yes, but I\'m still working on it'),
        ('sometimes', 'Sometimes, it depends on the day'),
        ('struggle', 'No, I struggle with self-acceptance'),
        ('not_sure', 'I\'m not sure what that means'),
    ], blank=True)

    # Self-Reflection Questions
    true_happiness_knowledge = models.CharField(max_length=100, choices=[
        ('content_peace', 'I feel content and at peace with my life'),
        ('joy_everyday', 'I experience joy in everyday moments'),
        ('purpose_fulfillment', 'I have a sense of purpose and fulfillment'),
        ('express_gratitude', 'I can express gratitude for what I have'),
        ('all_above_happy', 'All of the above'),
    ], blank=True)

    emotional_intelligence_definition = models.CharField(max_length=100, choices=[
        ('aware_emotions', 'Being aware of your own emotions and others\''),
        ('manage_effectively', 'Managing emotions effectively in difficult situations'),
        ('understand_dynamics', 'Understanding social dynamics and relationships'),
        ('guide_decisions', 'Using emotions to guide decision-making'),
        ('all_above_ei', 'All of the above'),
    ], blank=True)

    personal_growth_definition = models.CharField(max_length=100, choices=[
        ('learn_skills', 'Learning new skills and knowledge'),
        ('emotional_maturity', 'Developing emotional maturity'),
        ('better_relationships', 'Building better relationships'),
        ('overcome_challenges', 'Overcoming personal challenges'),
        ('continuous_improvement', 'Continuous self-improvement in all areas'),
    ], blank=True)

    most_authentic_feeling = models.CharField(max_length=100, choices=[
        ('when_alone', 'When I\'m alone and can be myself'),
        ('with_close_ones', 'When I\'m with close friends or family'),
        ('pursuing_passions', 'When I\'m pursuing my passions'),
        ('helping_others', 'When I\'m helping others'),
        ('being_creative', 'When I\'m being creative or expressive'),
    ], blank=True)

    stranger_interaction_motivation = models.CharField(max_length=100, choices=[
        ('right_thing', 'It\'s the right thing to do'),
        ('inherent_worth', 'I believe in the inherent worth of all people'),
        ('positive_effects', 'Kindness creates positive ripple effects'),
        ('feel_good', 'It makes me feel good about myself'),
        ('all_above_stranger', 'All of the above'),
    ], blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    def calculate_personality_scores(self):
        """
        Calculate personality dimension scores based on questionnaire responses.
        Returns a dictionary with scores for different personality dimensions.
        """
        scores = {
            'empathy_level': 0,
            'growth_orientation': 0,
            'relationship_focus': 0,
            'openness_change': 0,
            'help_motivation': 0,
            'fairness_orientation': 0,
            'success_definition': 0,
            'resilience_level': 0,
            'cultural_curiosity': 0,
            'authenticity_level': 0
        }

        # Empathy Level (Questions about understanding others)
        if self.response_personal_struggle == 'emotional_support':
            scores['empathy_level'] += 3
        elif self.response_personal_struggle == 'share_experiences':
            scores['empathy_level'] += 2

        if self.empathy_definition and 'sharing' in self.empathy_definition.lower():
            scores['empathy_level'] += 2
        if self.empathy_definition and 'compassion' in self.empathy_definition.lower():
            scores['empathy_level'] += 2

        if self.struggling_thoughts == 'want_to_help':
            scores['empathy_level'] += 3
        elif self.struggling_thoughts == 'learn_experience':
            scores['empathy_level'] += 2

        # Growth Orientation (Questions about personal development)
        if self.long_term_goals == 'positive_impact':
            scores['growth_orientation'] += 3
        elif self.long_term_goals == 'personal_growth':
            scores['growth_orientation'] += 3

        if self.success_definition == 'personal_growth':
            scores['growth_orientation'] += 3
        elif self.success_definition == 'positive_impact':
            scores['growth_orientation'] += 2

        if self.personal_growth_definition == 'continuous_improvement':
            scores['growth_orientation'] += 3
        elif self.personal_growth_definition in ['overcome_challenges', 'emotional_maturity']:
            scores['growth_orientation'] += 2

        if self.self_reflection_frequency == 'daily':
            scores['growth_orientation'] += 3
        elif self.self_reflection_frequency == 'weekly':
            scores['growth_orientation'] += 2

        # Relationship Focus (Questions about connections with others)
        if self.success_definition == 'relationships':
            scores['relationship_focus'] += 3

        if self.life_meaning == 'relationships':
            scores['relationship_focus'] += 3

        if self.trust_definition == 'shared_values':
            scores['relationship_focus'] += 2
        elif self.trust_definition == 'emotional_safety':
            scores['relationship_focus'] += 2

        if self.boundaries_approach == 'clearly_communicate':
            scores['relationship_focus'] += 2

        # Openness to Change (Questions about adaptability)
        if self.change_response == 'embrace_opportunity':
            scores['openness_change'] += 3
        elif self.change_response == 'reinvent_myself':
            scores['openness_change'] += 3

        if self.uncertainty_response == 'embrace_growth':
            scores['openness_change'] += 3

        if self.change_mind_frequency == 'frequently':
            scores['openness_change'] += 3
        elif self.change_mind_frequency == 'sometimes':
            scores['openness_change'] += 2

        # Help Motivation (Questions about why people help others)
        if self.help_motivation and 'difference' in self.help_motivation.lower():
            scores['help_motivation'] += 2
        if self.help_motivation and 'duty' in self.help_motivation.lower():
            scores['help_motivation'] += 2

        if self.stranger_interaction_motivation == 'all_above_stranger':
            scores['help_motivation'] += 3
        elif self.stranger_interaction_motivation in ['inherent_worth', 'positive_effects']:
            scores['help_motivation'] += 2

        # Fairness Orientation (Questions about justice and equality)
        if self.fairness_belief == 'equal_opportunities':
            scores['fairness_orientation'] += 3
        elif self.fairness_belief == 'effort_merit':
            scores['fairness_orientation'] += 2

        if self.response_unfair_treatment == 'speak_up':
            scores['fairness_orientation'] += 3
        elif self.response_unfair_treatment == 'assess_situation':
            scores['fairness_orientation'] += 2

        # Resilience Level (Questions about coping with challenges)
        if self.coping_failure == 'analyze_learn':
            scores['resilience_level'] += 3
        elif self.coping_failure == 'seek_support':
            scores['resilience_level'] += 2

        if self.forgiveness_role == 'forgive_easily':
            scores['resilience_level'] += 2
        elif self.forgiveness_role == 'takes_time':
            scores['resilience_level'] += 1

        if self.emotion_processing == 'talk_trusted':
            scores['resilience_level'] += 2
        elif self.emotion_processing == 'write_journal':
            scores['resilience_level'] += 2

        # Cultural Curiosity (Questions about learning about others)
        if self.learning_cultures == 'actively_curios':
            scores['cultural_curiosity'] += 3

        if self.most_authentic_feeling == 'being_creative':
            scores['cultural_curiosity'] += 1

        # Authenticity Level (Questions about being genuine)
        if self.most_authentic_feeling == 'when_alone':
            scores['authenticity_level'] += 2

        if self.vulnerability_strength == 'sign_true_strength':
            scores['authenticity_level'] += 3
        elif self.vulnerability_strength == 'can_coexist':
            scores['authenticity_level'] += 2

        if self.admit_fault_frequency == 'always':
            scores['authenticity_level'] += 3
        elif self.admit_fault_frequency == 'often':
            scores['authenticity_level'] += 2

        # Normalize scores to 0-10 scale
        for key in scores:
            scores[key] = min(10, max(0, scores[key]))

        return scores

    def get_personality_profile(self):
        """
        Returns a personality profile category based on scores.
        """
        scores = self.calculate_personality_scores()

        # Define personality archetypes based on score combinations
        if scores['empathy_level'] >= 7 and scores['growth_orientation'] >= 7:
            return 'Empathic_Grower'
        elif scores['relationship_focus'] >= 7 and scores['empathy_level'] >= 6:
            return 'Relational_Empath'
        elif scores['openness_change'] >= 7 and scores['cultural_curiosity'] >= 6:
            return 'Open_Explorer'
        elif scores['resilience_level'] >= 7 and scores['authenticity_level'] >= 6:
            return 'Resilient_Authentic'
        elif scores['help_motivation'] >= 7 and scores['fairness_orientation'] >= 6:
            return 'Altruistic_Advocate'
        elif scores['growth_orientation'] >= 6 and scores['authenticity_level'] >= 6:
            return 'Mindful_Grower'
        else:
            return 'Balanced_Individual'

    def calculate_compatibility_score(self, other_response):
        """
        Calculate compatibility score with another questionnaire response.
        Returns a score from 0-100 indicating how well personalities match.
        """
        if not isinstance(other_response, QuestionnaireResponse):
            return 0

        self_scores = self.calculate_personality_scores()
        other_scores = other_response.calculate_personality_scores()

        # Calculate weighted compatibility
        compatibility = 0
        total_weight = 0

        # High weight dimensions (core values)
        high_weight_dims = ['empathy_level', 'growth_orientation', 'authenticity_level']
        for dim in high_weight_dims:
            diff = abs(self_scores[dim] - other_scores[dim])
            compatibility += (10 - diff) * 3  # Max 30 per dimension
            total_weight += 30

        # Medium weight dimensions (social behavior)
        med_weight_dims = ['relationship_focus', 'help_motivation', 'fairness_orientation']
        for dim in med_weight_dims:
            diff = abs(self_scores[dim] - other_scores[dim])
            compatibility += (10 - diff) * 2  # Max 20 per dimension
            total_weight += 20

        # Low weight dimensions (adaptability)
        low_weight_dims = ['openness_change', 'resilience_level', 'cultural_curiosity']
        for dim in low_weight_dims:
            diff = abs(self_scores[dim] - other_scores[dim])
            compatibility += (10 - diff) * 1  # Max 10 per dimension
            total_weight += 10

        # Convert to percentage
        return round((compatibility / total_weight) * 100, 1)
