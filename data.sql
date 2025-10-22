SELECT * FROM "X_app_questionaire";  

SELECT * FROM "X_app_questionnaireresponse";  

SELECT * FROM "X_app_question";

SELECT * FROM "X_app_response";

SELECT * FROM "X_app_invitationcode";

-- Find UNUSED invitation codes (where used = false)
SELECT 
    id,
    code,
    invited_by_id,
    used,
    used_by_id,
    created_at
FROM "X_app_invitationcode" 
WHERE used = false 
ORDER BY created_at DESC;

-- Alternative: Find invitation codes that have NOT been used
SELECT * FROM "X_app_invitationcode" WHERE used = 'f' OR used = 0;

-- Count of used vs unused invitation codes
SELECT 
    used,
    COUNT(*) as count
FROM "X_app_invitationcode" 
GROUP BY used;

-- Detailed view of unused codes with inviter information
SELECT 
    ic.id,
    ic.code,
    ic.created_at,
    au.username as invited_by_username,
    au.email as invited_by_email
FROM "X_app_invitationcode" ic
LEFT JOIN auth_user au ON ic.invited_by_id = au.id
WHERE ic.used = false
ORDER BY ic.created_at DESC;

---                List of relations
-- \i data.sql 
--- \dt 

-- Schema |            Name             | Type  | Owner 
--------+-----------------------------+-------+-------
 --public | X_app_answer                | table | k
 --public | X_app_comment               | table | k
 --public | X_app_follow                | table | k
 --public | X_app_invitation            | table | k
 --public | X_app_invitationcode        | table | k
 --public | X_app_like                  | table | k
 --public | X_app_message               | table | k
 --public | X_app_notification          | table | k
 --public | X_app_post                  | table | k
 --public | X_app_profile               | table | k
 --public | X_app_question              | table | k
 --public | X_app_questionaire          | table | k
 --public | X_app_questionnaireresponse | table | k
 --public | X_app_response              | table | k
 --public | X_app_responseanswer        | table | k
 --public | X_app_usercompatibility     | table | k
 --public | X_app_userprofile           | table | k
 --public | auth_group                  | table | k
 --public | auth_group_permissions      | table | k
 --public | auth_permission             | table | k
 --public | auth_user                   | table | k
 --public | auth_user_groups            | table | k
 --public | auth_user_user_permissions  | table | k
 --public | django_admin_log            | table | k
 --public | django_content_type         | table | k
 --public | django_migrations           | table | k
 --public | django_session              | table | k
 --public | main_app_caloricintake      | table | k
 --public | main_app_dailycheckin       | table | k
 --public | main_app_habit              | table | k
 --public | main_app_journalentry       | table | k
 --public | main_app_userprofile       | table | k


 -- to run this database file, use the command:
 -- \i data.sql

