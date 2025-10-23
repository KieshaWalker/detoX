---INSERT INTO "X_app_invitationcode" (id, code, created_at, used, invited_by_id, used_by_id) VALUES (0, 12344, NOW(), false, NULL, NULL);
-- above line used for inserting a first value for production testing


-- Select all records from the invitation code table
SELECT * FROM "X_app_invitationcode";
-- Select all records from questionnaire response table
SELECT * FROM "X_app_questionnaireresponse";

-- Select all records from invitation code table
SELECT * FROM "X_app_invitationcode";   
-- Find UNUSED invitation codes (where used = false)
SELECT 
    id,
    code,
    invited_by_id,
    used,
    used_by_id FROM "X_app_invitationcode" 
WHERE used = false 
ORDER BY created_at DESC;

-- Count of used vs unused invitation codes
SELECT 
    COUNT(*) FILTER (WHERE used = true) AS used_count,
    COUNT(*) FILTER (WHERE used = false) AS unused_count
FROM "X_app_invitationcode";

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
