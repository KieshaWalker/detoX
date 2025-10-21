-- =========================================
-- detoX Database Schema and Documentation
-- PostgreSQL Database: habits
-- Generated: October 20, 2025
-- =========================================

-- =========================================
-- DATABASE CONNECTION
-- =========================================

-- Connect to the database:
-- psql -h localhost -p 5432 -U k -d habits

-- Note: PostgreSQL table names are case-sensitive. Use quotes for exact case:
-- SELECT * FROM "X_app_invitationcode";
-- SELECT * FROM "X_app_invitation";

-- =========================================
-- INVITATION SYSTEMS OVERVIEW
-- =========================================

-- Your database contains TWO invitation systems:

-- 1. CURRENT SYSTEM (X_app_invitationcode)
--    - Simple token-based system
--    - Used by current Django application
--    - Fields: code, created_at, invited_by, used, used_by
--    - No admin approval required

-- 2. LEGACY SYSTEM (X_app_invitation)
--    - Complex admin-reviewed system
--    - From previous version of the application
--    - Fields: receiver_email, token, sent_at, admin_reviewed, sender, approved, approved_at, questionnaire_completed, secret_sentence
--    - Requires admin approval before user can register

-- The current Django models.py only defines the simple system (InvitationCode).
-- The legacy system tables remain in the database but are not actively used.

-- =========================================
-- TABLE STRUCTURES
-- =========================================

-- 1. Django Auth Tables (automatically created by Django)
-- auth_user - User accounts
-- auth_group - User groups
-- auth_permission - Permissions
-- auth_user_groups - User-group relationships
-- auth_user_user_permissions - User permissions
-- django_session - User sessions
-- django_admin_log - Admin action logs

-- 2. Application Tables
-- X_app_invitationcode - Current invitation codes for registration (simple system)
-- X_app_invitation - Legacy invitation system (complex admin-reviewed system)
-- X_app_questionnaireresponse - User questionnaire responses
-- X_app_userprofile - Extended user profile information
-- Additional legacy tables: X_app_answer, X_app_comment, X_app_follow, X_app_like,
-- X_app_message, X_app_notification, X_app_post, X_app_profile, X_app_question,
-- X_app_questionaire, X_app_response, X_app_responseanswer

-- =========================================
-- DETAILED TABLE SCHEMAS
-- =========================================

-- Current Invitation Codes Table (simple system)
CREATE TABLE IF NOT EXISTS "X_app_invitationcode" (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    invited_by_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    used BOOLEAN DEFAULT FALSE,
    used_by_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL
);

-- Legacy Invitation Table (complex admin-reviewed system)
CREATE TABLE IF NOT EXISTS "X_app_invitation" (
    id SERIAL PRIMARY KEY,
    receiver_email VARCHAR(254) NOT NULL,
    token VARCHAR(100) NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE NOT NULL,
    admin_reviewed BOOLEAN DEFAULT FALSE,
    sender_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    approved BOOLEAN DEFAULT FALSE,
    approved_at TIMESTAMP WITH TIME ZONE,
    questionnaire_completed BOOLEAN DEFAULT FALSE,
    secret_sentence VARCHAR(500) NOT NULL
);

-- Questionnaire Responses Table
CREATE TABLE IF NOT EXISTS X_app_questionnaireresponse (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    invitation_code_id INTEGER NOT NULL REFERENCES X_app_invitationcode(id) ON DELETE CASCADE,

    -- Question responses
    motivation_help_others TEXT NOT NULL,
    human_nature_view VARCHAR(100) NOT NULL,
    fairness_belief VARCHAR(100) NOT NULL,
    long_term_goals VARCHAR(100) NOT NULL,
    response_personal_struggle VARCHAR(100) NOT NULL,
    response_unfair_treatment VARCHAR(100) NOT NULL,
    success_definition VARCHAR(100) NOT NULL,
    forgiveness_role VARCHAR(100) NOT NULL,
    coping_failure VARCHAR(100) NOT NULL,
    learning_cultures VARCHAR(100) NOT NULL,

    -- Additional questions
    empathy_definition VARCHAR(200) DEFAULT '',
    values_conflict VARCHAR(200) DEFAULT '',
    help_motivation VARCHAR(200) DEFAULT '',

    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User Profile Table
CREATE TABLE IF NOT EXISTS X_app_userprofile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    questionnaire_id INTEGER REFERENCES X_app_questionnaireresponse(id) ON DELETE SET NULL,
    invitation_code_id INTEGER REFERENCES X_app_invitationcode(id) ON DELETE SET NULL
);

-- =========================================
-- USEFUL QUERIES
-- =========================================

-- View all tables in the database
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Count records in each main table
SELECT
    'auth_user' as table_name, COUNT(*) as record_count FROM auth_user
UNION ALL
SELECT 'X_app_invitationcode (current)', COUNT(*) FROM "X_app_invitationcode"
UNION ALL
SELECT 'X_app_invitation (legacy)', COUNT(*) FROM "X_app_invitation"
UNION ALL
SELECT 'X_app_questionnaireresponse', COUNT(*) FROM "X_app_questionnaireresponse"
UNION ALL
SELECT 'X_app_userprofile', COUNT(*) FROM "X_app_userprofile";

-- View recent invitation codes (current system)
SELECT
    ic.code,
    ic.created_at,
    au.username as invited_by,
    ic.used,
    au2.username as used_by
FROM "X_app_invitationcode" ic
LEFT JOIN auth_user au ON ic.invited_by_id = au.id
LEFT JOIN auth_user au2 ON ic.used_by_id = au2.id
ORDER BY ic.created_at DESC
LIMIT 10;

-- View recent legacy invitations
SELECT
    i.receiver_email,
    i.sent_at,
    au.username as sender,
    i.admin_reviewed,
    i.approved,
    i.approved_at,
    i.questionnaire_completed,
    LEFT(i.secret_sentence, 50) || '...' as secret_preview
FROM "X_app_invitation" i
JOIN auth_user au ON i.sender_id = au.id
ORDER BY i.sent_at DESC
LIMIT 10;

-- View questionnaire responses with user info
SELECT
    qr.full_name,
    qr.email,
    qr.submitted_at,
    au.username,
    ic.code as invitation_code
FROM "X_app_questionnaireresponse" qr
JOIN "X_app_userprofile" up ON qr.id = up.questionnaire_id
JOIN auth_user au ON up.user_id = au.id
LEFT JOIN "X_app_invitationcode" ic ON qr.invitation_code_id = ic.id
ORDER BY qr.submitted_at DESC;

-- View invitation statistics (both systems)
SELECT
    'Current System (invitationcode)' as system,
    COUNT(*) as total_invitations,
    COUNT(CASE WHEN used = true THEN 1 END) as used_invitations,
    COUNT(CASE WHEN used = false THEN 1 END) as unused_invitations,
    COUNT(DISTINCT invited_by_id) as unique_senders
FROM "X_app_invitationcode"
UNION ALL
SELECT
    'Legacy System (invitation)' as system,
    COUNT(*) as total_invitations,
    COUNT(CASE WHEN approved = true THEN 1 END) as approved_invitations,
    COUNT(CASE WHEN approved = false THEN 1 END) as pending_invitations,
    COUNT(DISTINCT sender_id) as unique_senders
FROM "X_app_invitation";

-- View questionnaire response statistics
SELECT
    COUNT(*) as total_responses,
    AVG(EXTRACT(EPOCH FROM (submitted_at - (
        SELECT MIN(submitted_at) FROM "X_app_questionnaireresponse"
    ))) / 86400) as avg_days_since_first
FROM "X_app_questionnaireresponse";

-- =========================================
-- CURRENT SYSTEM DATA MANAGEMENT
-- =========================================

-- Create a new invitation code (example)
-- INSERT INTO "X_app_invitationcode" (code, invited_by_id)
-- VALUES ('ABC123XYZ', (SELECT id FROM auth_user WHERE username = 'admin'));

-- Mark invitation code as used
-- UPDATE "X_app_invitationcode"
-- SET used = true, used_by_id = (SELECT id FROM auth_user WHERE username = 'newuser')
-- WHERE code = 'ABC123XYZ';

-- Delete old unused invitation codes (older than 30 days)
-- DELETE FROM "X_app_invitationcode"
-- WHERE used = false
-- AND created_at < CURRENT_TIMESTAMP - INTERVAL '30 days';

-- View pending legacy invitations (not yet approved)
-- SELECT * FROM "X_app_invitation" WHERE approved = false AND admin_reviewed = false;

-- Approve a legacy invitation
-- UPDATE "X_app_invitation" SET approved = true, approved_at = CURRENT_TIMESTAMP WHERE id = ?;

-- Mark questionnaire as completed for legacy invitation
-- UPDATE "X_app_invitation" SET questionnaire_completed = true WHERE id = ?;

-- Delete old legacy invitations (older than 90 days, not approved)
-- DELETE FROM "X_app_invitation"
-- WHERE approved = false
-- AND sent_at < CURRENT_TIMESTAMP - INTERVAL '90 days';

-- Migrate legacy invitations to current system (if needed)
-- INSERT INTO "X_app_invitationcode" (code, invited_by_id, used)
-- SELECT token, sender_id, questionnaire_completed
-- FROM "X_app_invitation"
-- WHERE approved = true;

-- =========================================
-- INDEXES FOR PERFORMANCE
-- =========================================

-- =========================================
-- SCORING RUBRIC AND COMPATIBILITY SYSTEM
-- =========================================

-- The detoX platform uses a comprehensive personality scoring system
-- to match users with similar values and worldviews.

-- =========================================
-- PERSONALITY DIMENSIONS
-- =========================================

-- 1. Empathy Level (0-10)
--    Measures ability to understand and share others' feelings
--    High scorers: emotional_support, compassion, want_to_help
--    Used for: Finding emotionally supportive connections

-- 2. Growth Orientation (0-10)
--    Measures focus on personal development and self-improvement
--    High scorers: positive_impact, personal_growth, continuous_improvement
--    Used for: Connecting with ambitious, self-improving individuals

-- 3. Relationship Focus (0-10)
--    Measures importance of interpersonal connections
--    High scorers: relationships, shared_values, emotional_safety
--    Used for: Building meaningful social networks

-- 4. Openness to Change (0-10)
--    Measures adaptability and willingness to embrace new experiences
--    High scorers: embrace_opportunity, frequently change mind, embrace_growth
--    Used for: Finding flexible, adventurous companions

-- 5. Help Motivation (0-10)
--    Measures intrinsic desire to assist others
--    High scorers: personal satisfaction, positive effects, inherent worth
--    Used for: Community building and mutual support

-- 6. Fairness Orientation (0-10)
--    Measures commitment to justice and equality
--    High scorers: equal_opportunities, speak_up, effort_merit
--    Used for: Finding like-minded advocates for social causes

-- 7. Resilience Level (0-10)
--    Measures ability to bounce back from challenges
--    High scorers: analyze_learn, seek_support, forgive_easily
--    Used for: Finding reliable, stable relationships

-- 8. Cultural Curiosity (0-10)
--    Measures interest in diverse perspectives and experiences
--    High scorers: actively_curios, being_creative
--    Used for: Cultural exchange and learning opportunities

-- 9. Authenticity Level (0-10)
--    Measures commitment to genuine self-expression
--    High scorers: sign_true_strength, always admit fault, when_alone authentic
--    Used for: Finding honest, transparent connections

-- =========================================
-- PERSONALITY PROFILES
-- =========================================

-- Empathic_Grower: High empathy + high growth (nurturing mentors)
-- Relational_Empath: High relationships + high empathy (supportive friends)
-- Open_Explorer: High openness + high curiosity (adventurous learners)
-- Resilient_Authentic: High resilience + high authenticity (reliable truth-seekers)
-- Altruistic_Advocate: High help motivation + high fairness (community activists)
-- Mindful_Grower: High growth + high authenticity (conscious developers)
-- Balanced_Individual: Moderate scores across dimensions (well-rounded)

-- =========================================
-- COMPATIBILITY SCORING
-- =========================================

-- Compatibility is calculated using weighted dimensions:
-- Core Values (empathy, growth, authenticity): 30% weight each
-- Social Behavior (relationships, help, fairness): 20% weight each
-- Adaptability (openness, resilience, curiosity): 10% weight each

-- Final Score: 0-100, where higher scores indicate better matches

-- =========================================
-- COMPATIBILITY QUERIES
-- =========================================

-- Find top 5 most compatible users for a given user
-- SELECT u2.username, uc.compatibility_score,
--        uc.shared_empathy, uc.shared_growth, uc.shared_relationships
-- FROM "X_app_usercompatibility" uc
-- JOIN auth_user u1 ON uc.user1_id = u1.id
-- JOIN auth_user u2 ON uc.user2_id = u2.id
-- WHERE u1.username = 'your_username'
-- ORDER BY uc.compatibility_score DESC
-- LIMIT 5;

-- Find users with shared empathy values
-- SELECT u2.username, uc.compatibility_score
-- FROM "X_app_usercompatibility" uc
-- JOIN auth_user u1 ON uc.user1_id = u1.id
-- JOIN auth_user u2 ON uc.user2_id = u2.id
-- WHERE u1.username = 'your_username'
-- AND uc.shared_empathy = true
-- ORDER BY uc.compatibility_score DESC;

-- =========================================
-- END OF DOCUMENT
-- =========================================
