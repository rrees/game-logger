log_insert = """
INSERT INTO game_logs (
    log_id,
    user_id,
    game_name,
    system,
    played_on,
    tags,
    notes
)
VALUES (
    %(log_id)s,
    %(user_id)s,
    %(game_name)s,
    %(system)s,
    %(played_on)s,
    %(tags)s,
    %(notes)s
)
"""

update_log = """
UPDATE game_logs SET 
    game_name = %(game_name)s,
    played_on = %(played_on)s,
    tags = %(tags)s,
    notes = %(notes)s,
    system = %(system)s
WHERE log_id = %(log_id)s
"""

list_user_logs = """
SELECT
    log_id,
    game_name,
    played_on,
    tags,
    notes,
    system
FROM game_logs
ORDER BY played_on DESC
"""

recent_user_logs = list_user_logs + " LIMIT %(limit)s"

delete_user_log = """
DELETE FROM game_logs
WHERE log_id = %(log_id)s
AND user_id = %(user_id)s
"""

delete_log = """
DELETE FROM game_logs
WHERE log_id = %(log_id)s
"""

list_user_logs_by_year = """
SELECT
    log_id,
    game_name,
    played_on,
    tags,
    notes,
    system
FROM game_logs
WHERE EXTRACT(year from "played_on") = %(year)s
ORDER BY played_on DESC
"""

list_user_logs_by_tag = """
SELECT
    log_id,
    game_name,
    played_on,
    tags,
    notes,
    system
FROM game_logs
WHERE %(tag)s = ANY (tags)
ORDER BY played_on DESC
"""
