#!/usr/bin/env python
"""
Test script for the detoX personality scoring and compatibility system.
This demonstrates how the questionnaire responses are analyzed and matched.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detoX.settings')
django.setup()

from X_app.models import QuestionnaireResponse, UserProfile
from django.contrib.auth.models import User


def create_sample_responses():
    """Create sample questionnaire responses for testing."""

    # Sample response 1: Empathic Grower
    response1 = QuestionnaireResponse.objects.create(
        full_name="Alice Johnson",
        email="alice@example.com",
        invitation_code_id=1,  # Assuming invitation code exists

        # High empathy responses
        response_personal_struggle='emotional_support',
        struggling_thoughts='want_to_help',
        empathy_definition='Understanding and sharing another person\'s feelings',

        # High growth responses
        long_term_goals='positive_impact',
        success_definition='personal_growth',
        personal_growth_definition='continuous_improvement',
        self_reflection_frequency='daily',

        # Other balanced responses
        human_nature_view='inherently_good',
        fairness_belief='equal_opportunities',
        forgiveness_role='forgive_easily',
        coping_failure='analyze_learn',
        learning_cultures='actively_curios',
        home_concept='belonging_security',
        uncertainty_response='embrace_growth',
        gratitude_role='regularly_express',
        feedback_approach='give_constructive',
        life_balance='harmony',
        trust_definition='emotional_safety',
        difficult_conversations='prepare_carefully',
        life_meaning='personal_growth',
        change_response='embrace_opportunity',
        emotion_processing='talk_trusted',
        boundaries_approach='clearly_communicate',
        vulnerability_strength='sign_true_strength',
        change_mind_frequency='frequently',
        admit_fault_frequency='always',
        active_listening_definition='all_above',
        human_being_definition='all_above_human',
        self_love_level='completely_unconditionally',
        true_happiness_knowledge='all_above_happy',
        emotional_intelligence_definition='all_above_ei',
        most_authentic_feeling='when_alone',
        stranger_interaction_motivation='all_above_stranger'
    )

    # Sample response 2: Relational Empath
    response2 = QuestionnaireResponse.objects.create(
        full_name="Bob Smith",
        email="bob@example.com",
        invitation_code_id=1,

        # High empathy responses
        response_personal_struggle='emotional_support',
        struggling_thoughts='want_to_help',
        empathy_definition='Feeling compassion and wanting to help',

        # High relationship focus
        success_definition='relationships',
        life_meaning='relationships',
        trust_definition='shared_values',
        boundaries_approach='clearly_communicate',

        # Other responses
        human_nature_view='environment',
        fairness_belief='subjective',
        long_term_goals='security',
        forgiveness_role='takes_time',
        coping_failure='seek_support',
        learning_cultures='opportunities',
        home_concept='loved_ones',
        uncertainty_response='seek_advice',
        gratitude_role='notice_positive',
        feedback_approach='receive_openly',
        life_balance='equal_time',
        difficult_conversations='speak_from_heart',
        change_response='adapt_gradually',
        emotion_processing='write_journal',
        vulnerability_strength='can_coexist',
        self_reflection_frequency='weekly',
        change_mind_frequency='sometimes',
        admit_fault_frequency='often',
        active_listening_definition='understand_words_emotions',
        human_being_definition='connect_emotionally',
        self_love_level='working_on_it',
        true_happiness_knowledge='joy_everyday',
        emotional_intelligence_definition='manage_effectively',
        personal_growth_definition='better_relationships',
        most_authentic_feeling='with_close_ones',
        stranger_interaction_motivation='right_thing'
    )

    return response1, response2


def demonstrate_scoring():
    """Demonstrate the personality scoring system."""

    print("🔍 detoX Personality Scoring & Compatibility Demo")
    print("=" * 50)

    # Get or create sample responses
    responses = QuestionnaireResponse.objects.all()
    if not responses.exists():
        print("Creating sample questionnaire responses...")
        response1, response2 = create_sample_responses()
        responses = [response1, response2]

    for i, response in enumerate(responses[:2], 1):  # Show first 2 responses
        print(f"\n👤 User {i}: {response.full_name}")
        print("-" * 30)

        # Calculate personality scores
        scores = response.calculate_personality_scores()
        print("Personality Scores (0-10 scale):")
        for dimension, score in scores.items():
            print(f"  {dimension.replace('_', ' ').title()}: {score}")

        # Get personality profile
        profile = response.get_personality_profile()
        print(f"\nPersonality Profile: {profile}")

    # Calculate compatibility between users
    if len(responses) >= 2:
        response1, response2 = responses[:2]
        compatibility_score = response1.calculate_compatibility_score(response2)

        print(f"\n🤝 Compatibility between {response1.full_name} and {response2.full_name}:")
        print(f"   Score: {compatibility_score}%")

        # Show shared values
        print("   Shared Values Analysis:")
        shared_values = UserProfile.objects.filter(questionnaire=response1).first()
        if shared_values:
            other_profile = UserProfile.objects.filter(questionnaire=response2).first()
            if other_profile:
                shared = shared_values.get_shared_values_summary(other_profile)
                for dimension, match_level in shared.items():
                    print(f"     {dimension}: {match_level}")

    print("\n" + "=" * 50)
    print("✨ Scoring Rubric Summary:")
    print("• Empathy Level: Understanding others' feelings")
    print("• Growth Orientation: Personal development focus")
    print("• Relationship Focus: Importance of connections")
    print("• Openness to Change: Adaptability to new experiences")
    print("• Help Motivation: Desire to assist others")
    print("• Fairness Orientation: Commitment to justice")
    print("• Resilience Level: Bouncing back from challenges")
    print("• Cultural Curiosity: Interest in diverse perspectives")
    print("• Authenticity Level: Genuine self-expression")
    print("\nCompatibility ranges from 0-100% (higher = better match)")


if __name__ == '__main__':
    demonstrate_scoring()